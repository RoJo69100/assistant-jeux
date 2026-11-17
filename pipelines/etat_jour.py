"""État calculé par événement (P2 du plan v4 du 13/11) : le « que faire » sort de l'état de CHAQUE événement, chaque jour.

Événements : matchs (ligue, coupe, amical), rapport d'académie, traitement d'entraînement, fins d'enchères. Leurs types et
leurs états viennent de la config du jeu (docs/attentes/jeux/<jeu>.yaml, section `etat_jour`) ; ce module n'écrit aucun nom
de joueur, de match ou d'adversaire : chaque consigne est un gabarit par état, rempli avec les champs de l'événement.

Chaque événement des 48 h, et chaque match joué non analysé, reçoit exactement UNE ligne : la prochaine transition manquante
(échéance, consigne exacte, âge des données). Fonctions pures ; la lecture de la base est isolée dans `lire_evenements`.
"""
import datetime as dt
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))  # python -I n'ajoute pas le dossier du script
RACINE = ICI.parent
CONFIG = RACINE / "docs" / "attentes" / "jeux"


def charger_config(jeu: str = "basketvibe", chemin=None) -> dict:
    """Section `etat_jour` de docs/attentes/jeux/<jeu>.yaml."""
    import yaml
    texte = Path(chemin or CONFIG / f"{jeu}.yaml").read_text(encoding="utf-8")
    return yaml.safe_load(texte)["etat_jour"]


def _jj(d) -> str:
    return f"{d:%d/%m}" if d else "date inconnue"


def _hh(t) -> str:
    return f"{t:%H:%M}" if t else "heure inconnue"


# ---- Matchs : un prédicat « état atteint » et un gabarit « prochaine transition » par état ------------------------------
# Gabarit : (échéance, consigne, action). Une ligne sans action est une attente (rien à faire avant l'échéance).

def _match_ok(ev, etat, maintenant, cfg) -> bool:
    if etat == "calendrier":
        return ev.get("jour") is not None
    if etat == "apercu":
        return ev.get("apercu_at") is not None
    if etat == "fiche":
        return bool(ev.get("fiche")) and ev["fiche"].get("ok", True)
    if etat == "ecran":
        return bool(ev.get("ecran")) and ev["ecran"].get("sauvegarde") is True and not ev["ecran"].get("defauts")
    if etat == "verrou":
        return ev.get("verrou") is not None and maintenant >= ev["verrou"]
    if etat == "joue":
        return bool(ev.get("joue")) and ev.get("page_at") is not None
    if etat == "analyse":
        return ev.get("resultat") not in cfg["matchs"][ev["genre"]].get("analyse_si", []) or bool(ev.get("analyse"))
    if etat == "juge":
        return not ev.get("juge_requis") or bool(ev.get("juge"))
    raise ValueError(f"état de match inconnu : {etat}")


def _match_gabarit(ev, etat, maintenant):
    quoi = f"match de {ev['genre']} contre {ev['adversaire']} ({_jj(ev.get('jour'))})"
    if etat == "calendrier":
        return None, f"ouvre la page des matchs : le {quoi} n'a pas de date en base", True
    if etat == "apercu":
        return ev.get("verrou"), f"exporte l'aperçu du {quoi}", True
    if etat == "fiche":
        return ev.get("verrou"), f"lance l'agent tactique : fiche du {quoi}", True
    if etat == "ecran":
        return ev.get("verrou"), f"saisis et sauvegarde l'écran du {quoi} selon la fiche", True
    if etat == "verrou":
        return ev.get("verrou"), f"rien avant le verrou {_hh(ev.get('verrou'))} : écran du {quoi} sauvegardé", False
    if etat == "joue":
        if not ev.get("joue"):
            return ev.get("coup_envoi"), f"rien avant la fin du {quoi} (coup d'envoi {_hh(ev.get('coup_envoi'))})", False
        return None, f"exporte la page du {quoi}", True
    if etat == "analyse":
        return None, f"lance l'agent analyste : défaite, {quoi}", True
    if etat == "juge":
        return None, f"juge les décisions à mesurer après le {quoi} : python -I pipelines/evaluer_decisions.py", True
    raise ValueError(f"état de match inconnu : {etat}")


# ---- Événements hors match ----------------------------------------------------------------------------------------------

def _autre_ok(ev, etat, maintenant, cfg) -> bool:
    t = ev["type"]
    if t in ("academie", "entrainement") and etat in ("rapport_attendu", "traitement_attendu"):
        return maintenant >= ev["quand"]
    if t == "academie" and etat == "rapport_exporte":
        return ev.get("rapport_at") is not None and ev["rapport_at"] >= ev["quand"]
    if t == "academie" and etat == "decide":
        return bool(ev.get("decide"))
    if t == "entrainement" and etat == "page_exportee":
        return ev.get("page_at") is not None and ev["page_at"] >= ev["quand"]
    if t == "entrainement" and etat == "saisi":
        return bool(ev.get("saisi"))
    if t == "enchere" and etat == "police":
        return not ev.get("gros") or bool(ev.get("police"))
    if t == "enchere" and etat == "fin":
        return ev.get("fin") is not None and maintenant >= ev["fin"]
    if t == "enchere" and etat == "resultat":
        return bool(ev.get("resultat"))
    raise ValueError(f"état inconnu : {t} / {etat}")


def _autre_gabarit(ev, etat, maintenant):
    t = ev["type"]
    if etat == "rapport_attendu":
        return ev["quand"], f"rien avant le rapport du scout ({_jj(ev['quand'])} {_hh(ev['quand'])})", False
    if etat == "rapport_exporte":
        return None, f"exporte la page Académie (rapport du {_jj(ev['quand'])})", True
    if etat == "decide":
        return None, f"décide pour chaque prospect du rapport du {_jj(ev['quand'])} : tester, signer ou ignorer", True
    if etat == "traitement_attendu":
        return ev["quand"], f"rien avant le traitement de l'entraînement ({_jj(ev['quand'])} {_hh(ev['quand'])})", False
    if etat == "page_exportee":
        return None, f"exporte la page Entraînement (traitement du {_jj(ev['quand'])})", True
    if etat == "saisi":
        return None, "saisis et sauvegarde l'entraînement de la semaine selon la fiche", True
    if t == "enchere" and etat == "police":
        return ev.get("fin"), f"police d'abord pour l'enchère sur {ev['nom']} : python pipelines/dossier.py basketvibe achat", True
    if t == "enchere" and etat == "fin":
        return ev.get("fin"), f"rien avant la fin de l'enchère sur {ev['nom']} ({_jj(ev.get('fin'))} {_hh(ev.get('fin'))})", False
    if t == "enchere" and etat == "resultat":
        return None, f"lis le résultat de l'enchère sur {ev['nom']} : ouvre Mes enchères", True
    raise ValueError(f"état inconnu : {t} / {etat}")


def _nom(ev) -> str:
    t = ev["type"]
    if t == "match":
        return f"{ev['genre']} contre {ev['adversaire']}, {_jj(ev.get('jour'))}"
    if t == "academie":
        return f"rapport d'académie du {_jj(ev['quand'])}"
    if t == "entrainement":
        return f"traitement de l'entraînement du {_jj(ev['quand'])}"
    return f"enchère sur {ev['nom']}"


def etats_de(ev, cfg) -> list:
    return cfg["matchs"][ev["genre"]]["etats"] if ev["type"] == "match" else cfg["evenements"][ev["type"]]["etats"]


def etat_evenement(ev, cfg, maintenant) -> dict:
    """UNE ligne : dernier état atteint, prochaine transition manquante (None = tout est fait), échéance, consigne, âge des
    données (h), priorité (1-3, dégradée d'un cran si la donnée a plus de `donnee_perimee_h`), action (faux = attente).
    Match dont le verrou est passé : les états d'avant le verrou non atteints sont « ratés » et ne bloquent plus la suite."""
    etats = etats_de(ev, cfg)
    ok = _match_ok if ev["type"] == "match" else _autre_ok
    gabarit = _match_gabarit if ev["type"] == "match" else _autre_gabarit
    verrou_passe = ev["type"] == "match" and "verrou" in etats and ok(ev, "verrou", maintenant, cfg)
    atteint, prochain, rates = None, None, []
    for e in etats:
        if ok(ev, e, maintenant, cfg):
            atteint = e
            continue
        if verrou_passe and etats.index(e) < etats.index("verrou"):
            rates.append(e)
            continue
        prochain = e
        break
    echeance, consigne, action = gabarit(ev, prochain, maintenant) if prochain else (None, "rien à faire", False)
    age = round((maintenant - ev["maj_at"]).total_seconds() / 3600, 1) if ev.get("maj_at") else None
    prio = 3 if not action else 1 if echeance is not None and echeance - maintenant <= dt.timedelta(hours=cfg["urgent_h"]) else 2
    if age is not None and age > cfg["donnee_perimee_h"]:
        prio = min(3, prio + 1)
    return {"id": ev.get("id"), "type": ev["type"], "evenement": _nom(ev), "etat": atteint, "prochain": prochain, "rates": rates,
            "echeance": echeance, "consigne": consigne, "age_h": age, "priorite": prio, "action": action}


def _repere(ev):
    """Date et heure qui situent l'événement : coup d'envoi (ou jour) d'un match, heure prévue ou fin d'enchère sinon."""
    if ev["type"] == "match":
        return ev.get("coup_envoi") or (dt.datetime.combine(ev["jour"], dt.time()) if ev.get("jour") else None)
    return ev.get("quand") or ev.get("fin")


def dans_horizon(ev, cfg, maintenant) -> bool:
    """À venir dans `horizon_h`, ou passé de moins de `jours_non_analyses` jours avec une transition encore manquante
    (match joué non analysé, rapport non décidé, enchère au résultat non lu). Sans repère (calendrier inconnu) : oui."""
    r = _repere(ev)
    if r is None:
        return True
    if r > maintenant + dt.timedelta(hours=cfg["horizon_h"]):
        return False
    if r >= maintenant:
        return True
    return r >= maintenant - dt.timedelta(days=cfg["jours_non_analyses"]) and etat_evenement(ev, cfg, maintenant)["prochain"] is not None


def lignes(evenements, cfg, maintenant) -> list:
    """Une ligne par événement retenu (`dans_horizon`), dans l'ordre : action d'abord, puis priorité, puis échéance."""
    res = [etat_evenement(ev, cfg, maintenant) for ev in evenements if dans_horizon(ev, cfg, maintenant)]
    return sorted(res, key=lambda l: (not l["action"], l["priorite"], l["echeance"] or dt.datetime.max))


def sans_ligne(evenements, ls, cfg, maintenant) -> list:
    """Complétude : événements retenus qui n'ont pas de ligne dans `ls` (doit être vide)."""
    ids = {l["id"] for l in ls}
    return [ev for ev in evenements if dans_horizon(ev, cfg, maintenant) and ev.get("id") not in ids]
