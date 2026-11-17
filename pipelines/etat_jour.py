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
        return bool(ev.get("fiche")) and ev["fiche"].get("ok", True) and not ev["fiche"].get("defauts")
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
        defauts = (ev.get("fiche") or {}).get("defauts")
        if defauts:
            return ev.get("verrou"), f"corrige la fiche du {quoi} : " + " ; ".join(d["correction"] for d in defauts), True
        return ev.get("verrou"), f"lance l'agent tactique : fiche du {quoi}", True
    if etat == "ecran":
        defauts = (ev.get("ecran") or {}).get("defauts")
        if defauts:
            return ev.get("verrou"), f"corrige l'écran du {quoi} puis sauvegarde : " + " ; ".join(d["correction"] for d in defauts), True
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
    defauts = [] if ev["type"] != "match" else (ev.get("fiche") or {}).get("defauts", []) + (ev.get("ecran") or {}).get("defauts", [])
    return {"id": ev.get("id"), "type": ev["type"], "evenement": _nom(ev), "etat": atteint, "prochain": prochain, "rates": rates,
            "echeance": echeance, "consigne": consigne, "age_h": age, "priorite": prio, "action": action, "defauts": defauts}


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


# ---- P2.3 : contrôles fiche contre réalité (fonctions pures) ; un défaut = {"texte": "❌ …", "correction": "…"} ---------

CHAMPS_ECRAN = (("minutes", "minutes"), ("off", "focus offensif"), ("role", "rôle"), ("tir", "tir"), ("agress", "agressivité"))


def _meme(court: str, complet: str) -> bool:
    """Nom de la fiche (souvent le nom de famille) contre nom complet en base : égal, ou fin du nom complet après une espace."""
    c, n = str(court).strip().lower(), str(complet).strip().lower()
    return c == n or n.endswith(" " + c)


def _virg(x) -> str:
    return (f"{float(x):g}").replace(".", ",")


def _joue(j) -> bool:
    return int(j.get("minutes") or 0) > 0


def controle_blessures(joueurs, blessures, jour_match) -> list:
    """Joueur de la fiche qui joue alors qu'il est blessé à la date du match (date de retour postérieure au jour du match)."""
    res = []
    for j in joueurs:
        for nom, retour in blessures.items():
            if _joue(j) and _meme(j["nom"], nom) and retour is not None and retour > jour_match:
                res.append({"texte": f"❌ {j['nom']} blessé jusqu'au {_jj(retour)}, indisponible le {_jj(jour_match)}",
                            "correction": f"mets {j['nom']} à 0 min et redistribue ses {j['minutes']} min"})
    return res


def controle_minutes(joueurs, maximum) -> list:
    return [{"texte": f"❌ {j['nom']} à {j['minutes']} min (maximum {maximum})", "correction": f"ramène {j['nom']} à {maximum} min"}
            for j in joueurs if int(j.get("minutes") or 0) > maximum]


def controle_fatigue(joueurs, fatigue, seuil) -> list:
    """Joueur qui joue dont la fatigue actuelle dépasse le seuil (zone verte de core.alert_rule)."""
    res = []
    for j in joueurs:
        for nom, f in fatigue.items():
            if _joue(j) and _meme(j["nom"], nom) and f is not None and float(f) > float(seuil):
                res.append({"texte": f"❌ {j['nom']} fatigue {_virg(f)} au-dessus de {_virg(seuil)}",
                            "correction": f"réduis les minutes de {j['nom']} (fatigue {_virg(f)})"})
    return res


def controle_ecran(fiche, ecran) -> list:
    """Ligue et coupe : chaque réglage de l'écran sauvegardé contre la fiche, joueur par joueur."""
    res = []
    for j in fiche:
        e = next((x for x in ecran if _meme(j["nom"], x["nom"]) or _meme(x["nom"], j["nom"])), None)
        if e is None:
            if _joue(j):
                res.append({"texte": f"❌ {j['nom']} absent de l'écran", "correction": f"ajoute {j['nom']} à {j['minutes']} min"})
            continue
        for cle, libelle in CHAMPS_ECRAN:
            if j.get(cle) is not None and e.get(cle) is not None and str(e[cle]) != str(j[cle]):
                res.append({"texte": f"❌ écran : {j['nom']} {libelle} {e[cle]} (fiche {j[cle]})",
                            "correction": f"mets {libelle} de {j['nom']} à {j[cle]}"})
    return res


def controle_e1(joueurs, valeur) -> list:
    """Amical, test E1 : même agressivité pour tous les joueurs qui jouent ; `valeur` = celle du test (None : la plus fréquente)."""
    jouent = [j for j in joueurs if _joue(j)]
    vals = [j["agress"] for j in jouent]
    if not vals or len(set(vals)) == 1 and (valeur is None or vals[0] == valeur):
        return []
    cible = valeur if valeur is not None else max(set(vals), key=vals.count)
    ecarts = [j["nom"] for j in jouent if j["agress"] != cible]
    return [{"texte": f"❌ E1 non uniforme : {', '.join(ecarts)} hors de l'agressivité {cible}",
             "correction": f"mets l'agressivité {cible} à tous les joueurs qui jouent"}]


def controle_adversaire(fiche_adversaire, adversaire) -> list:
    if not fiche_adversaire or _meme(fiche_adversaire, adversaire) or _meme(adversaire, fiche_adversaire):
        return []
    return [{"texte": f"❌ adversaire changé : fiche contre {fiche_adversaire}, match contre {adversaire}",
             "correction": f"relance l'agent tactique pour le match contre {adversaire}"}]


def appliquer_controles(ev, reel, cfg) -> dict:
    """Copie du match avec fiche["defauts"] (blessure, minutes, fatigue, adversaire) et ecran["defauts"] (écran contre fiche en
    ligue et coupe, E1 uniforme en amical) ; `reel` = {"blessures": {nom: retour}, "fatigue": {nom: valeur}, "seuil_fatigue": x}."""
    if ev["type"] != "match":
        return ev
    ev = dict(ev)
    regle = cfg["matchs"][ev["genre"]]
    fiche = dict(ev["fiche"]) if ev.get("fiche") else None
    if fiche:
        fj = fiche.get("joueurs", [])
        fiche["defauts"] = controle_adversaire(fiche.get("adversaire"), ev["adversaire"]) \
            + (controle_blessures(fj, reel.get("blessures", {}), ev["jour"]) if ev.get("jour") else []) \
            + controle_minutes(fj, cfg["minutes_max"]) \
            + (controle_fatigue(fj, reel.get("fatigue", {}), reel["seuil_fatigue"]) if reel.get("seuil_fatigue") is not None else [])
        ev["fiche"] = fiche
    if ev.get("ecran") and ev["ecran"].get("joueurs"):
        ecran = dict(ev["ecran"])
        if regle.get("e1_uniforme"):
            ecran["defauts"] = controle_e1(ecran["joueurs"], (fiche or {}).get("agress_test"))
        elif regle.get("ecran_contre_fiche") and fiche and fiche.get("joueurs"):
            ecran["defauts"] = controle_ecran(fiche["joueurs"], ecran["joueurs"])
        ev["ecran"] = ecran
    return ev


# P2.2 : états dont la transition est un export (la capture passive de la page fait passer l'état)
ETATS_EXPORT = ("apercu", "joue", "rapport_exporte", "page_exportee")


def exports(ls) -> list:
    """Exports à demander : seulement les lignes dont la prochaine transition est un export (action, état d'ETATS_EXPORT).
    La consigne nomme l'événement ; dès que la base voit la capture, l'état est atteint et la ligne n'est plus un export.
    Un match pas encore joué n'en demande aucun (« joue » sans action) ; un amical n'a pas d'aperçu."""
    return [l for l in ls if l["action"] and l["prochain"] in ETATS_EXPORT]


def sans_ligne(evenements, ls, cfg, maintenant) -> list:
    """Complétude : événements retenus qui n'ont pas de ligne dans `ls` (doit être vide)."""
    ids = {l["id"] for l in ls}
    return [ev for ev in evenements if dans_horizon(ev, cfg, maintenant) and ev.get("id") not in ids]
