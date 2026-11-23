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


LIEN_FICHE = "https://github.com/RoJo69100/assistant-jeux/blob/claude/passage-quotidien/"  # la branche du passage contient tout main


def lien_fiche(fichier) -> str:
    """« chemin — lien » d'une fiche (`briefs/<nom>` relatif à outputs/basketvibe, ou nom seul) : toute action « selon la fiche » ou
    « corrige la fiche » le cite (17/11)."""
    chemin = f"outputs/basketvibe/briefs/{Path(str(fichier)).name}"
    return f"{chemin} — {LIEN_FICHE}{chemin}"


def _avec_fiche(texte, fiche) -> str:
    return f"{texte} ({lien_fiche(fiche['fichier'])})" if fiche and fiche.get("fichier") else texte


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
        return ev.get("apercu_at") is not None and ev.get("adv_connus") is not False  # phase A : joueurs adverses vus (preset fait)
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


def _match_gabarit(ev, etat, maintenant, cfg):
    libelle = cfg["matchs"][ev["genre"]].get("libelle", f"match de {ev['genre']}")
    quoi = f"{libelle} contre {ev['adversaire']} ({_jj(ev.get('jour'))})"
    if etat == "calendrier":
        return None, f"ouvre la page des matchs : le {quoi} n'a pas de date en base", True
    if etat == "apercu":
        etape = f"fais le preset de l'adversaire (pour voir ses joueurs) puis exporte l'aperçu du {quoi}"  # aucun nom de preset en dur
        if ev.get("apercu_at") is not None and ev.get("adv_connus") is False:
            return ev.get("verrou"), f"preset de l'adversaire à faire : ses joueurs ne sont pas connus ; {etape}", True
        return ev.get("verrou"), etape, True
    if etat == "fiche":
        defauts = (ev.get("fiche") or {}).get("defauts")
        if defauts:
            return ev.get("verrou"), _avec_fiche(f"corrige la fiche du {quoi} : " + " ; ".join(d["correction"] for d in defauts), ev.get("fiche")), True
        return ev.get("verrou"), f"lance l'agent tactique : fiche du {quoi}", True
    if etat == "ecran":
        defauts = (ev.get("ecran") or {}).get("defauts")
        if defauts:
            return ev.get("verrou"), f"corrige l'écran du {quoi} puis sauvegarde : " + " ; ".join(d["correction"] for d in defauts), True
        if not (ev.get("fiche") or {}).get("fichier"):
            return ev.get("verrou"), f"saisis et sauvegarde l'écran du {quoi} : fiche introuvable dans briefs/ (agent tactique)", True
        return ev.get("verrou"), _avec_fiche(f"saisis et sauvegarde l'écran du {quoi} selon la fiche", ev["fiche"]), True
    if etat == "verrou":
        return ev.get("verrou"), f"rien avant le verrou {_hh(ev.get('verrou'))} : écran du {quoi} sauvegardé", False
    if etat == "joue":
        fini = ev.get("coup_envoi") is not None and maintenant >= ev["coup_envoi"] + dt.timedelta(hours=cfg.get("duree_match_h", 2))
        if not ev.get("joue") and not fini:
            return ev.get("coup_envoi"),f"rien avant la fin du {quoi} (coup d'envoi {_hh(ev.get('coup_envoi'))})", False
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
    if t == "academie" and etat == "teste":  # 18/11 : plus aucun prospect au verdict « tester » (tests lus sur la dernière capture)
        return ev.get("tests") == 0
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


def _autre_gabarit(ev, etat, maintenant, cfg):
    t = ev["type"]
    if etat == "rapport_attendu":
        return ev["quand"], f"rien avant le rapport du scout ({_jj(ev['quand'])} {_hh(ev['quand'])})", False
    if etat == "rapport_exporte":
        return None, f"exporte la page Académie (rapport du {_jj(ev['quand'])})", True
    if etat == "teste":
        n = ev.get("tests")
        if n:  # 17/11 : tests attendus chiffrés (verdict « tester » de aujourdhui.verdict_prospect, coût de la config)
            cout = f"{n * cfg['evenements']['academie']['cout_test']:,}".replace(",", " ")
            return None, f"décision attendue : tester {n} prospect{'s' if n > 1 else ''} ({cout}), rapport du {_jj(ev['quand'])}", True
        return None, f"décide pour chaque prospect du rapport du {_jj(ev['quand'])} : tester, signer ou ignorer", True
    if etat == "decide":
        v = ev.get("verdicts") or []
        if v:  # 18/11 : tests lus, verdict de la règle de signature de l'utilisateur (17/11)
            signer = [x["nom"] for x in v if x["verdict"] == "signer"]
            quoi = f"signe {', '.join(signer)}" if signer else "aucun prospect à signer"
            return None, (f"testé (capture du {_jj(ev.get('capture'))}), rapport du {_jj(ev['quand'])} : "
                          + " ; ".join(f"{x['nom']} ({x['poste']}, {x['potentiel']}) : {x['verdict']}" for x in v) + f" — {quoi}"), True
        return None, f"décide pour chaque prospect du rapport du {_jj(ev['quand'])} : tester, signer ou ignorer", True
    if etat == "traitement_attendu":
        return ev["quand"], f"rien avant le traitement de l'entraînement ({_jj(ev['quand'])} {_hh(ev['quand'])})", False
    if etat == "page_exportee":
        return None, f"exporte la page Entraînement (traitement du {_jj(ev['quand'])})", True
    if etat == "saisi":
        if not (ev.get("fiche") or {}).get("fichier"):
            return None, "saisis et sauvegarde l'entraînement de la semaine : aucune fiche d'entraînement de la semaine dans briefs/ (agent entrainement)", True
        return None, _avec_fiche("saisis et sauvegarde l'entraînement de la semaine selon la fiche", ev["fiche"]), True
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
    echeance, consigne, action = gabarit(ev, prochain, maintenant, cfg) if prochain else (None, "rien à faire", False)
    age = round((maintenant - ev["maj_at"]).total_seconds() / 3600, 1) if ev.get("maj_at") else None
    prio = 3 if not action else 1 if echeance is not None and echeance - maintenant <= dt.timedelta(hours=cfg["urgent_h"]) else 2
    if age is not None and age > cfg["donnee_perimee_h"]:
        prio = min(3, prio + 1)
    if ev["type"] == "match" and prochain == "joue" and action:  # 19/11 : export de la page d'un match joué
        if ev["genre"] == "ligue":  # 🟧 au minimum, 🟥 plus de 24 h après le match
            ce = ev.get("coup_envoi")
            prio = 1 if ce is not None and maintenant - ce > dt.timedelta(hours=24 + cfg.get("duree_match_h", 2)) else min(prio, 2)
        elif ev["genre"] == "amical":  # sous l'export d'un match de ligue
            prio = 3
    defauts = [] if ev["type"] != "match" else (ev.get("fiche") or {}).get("defauts", []) + (ev.get("ecran") or {}).get("defauts", [])
    return {"id": ev.get("id"), "type": ev["type"], "evenement": _nom(ev), "etat": atteint, "prochain": prochain, "rates": rates,
            "echeance": echeance, "consigne": consigne, "age_h": age, "priorite": prio, "action": action, "defauts": defauts,
            "genre": ev.get("genre"), "cle": _cle_fichier(ev), "titre": _titre(ev), "test": ev.get("test")}


def texte_test_fiche(experiences, r, joues=()) -> str:
    """18/11 : test de la file d'expériences pour la fiche de cet amical (niveau alterné, aujourdhui.test_en_cours), à porter
    tel quel dans la fiche ; « » si aucune expérience en cours."""
    import aujourdhui as auj
    t = auj.test_en_cours(experiences, {"match": r["opponent"], "date": _date(r["day"])}, joues) if experiences else None
    if not t:
        return ""
    return (f"réglage de test à écrire dans la fiche : {auj.texte_test(t[0], t[1])} ; tout le reste au réglage neutre de "
            "docs/attentes/experiences-amicales-basketvibe.yaml (un seul test)")


def _slug(s) -> str:
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _cle_fichier(ev) -> str:
    """Morceau de nom de fichier propre à l'événement (P3) : adversaire ou objet, puis date (jj-mm)."""
    d = ev.get("jour") or ev.get("quand") or ev.get("fin")
    return "-".join(x for x in (_slug(ev.get("adversaire") or ev.get("nom") or ev["type"]), f"{d:%d-%m}" if d else "") if x)


def _titre(ev) -> str:
    """Première ligne attendue d'une fiche de match (contrat de que_faire_blocs.contrat_brief) ; nom de l'événement sinon."""
    if ev["type"] == "match":
        return f"{ev['genre'].capitalize()} contre {ev['adversaire']} ({_jj(ev.get('jour'))})"
    return _nom(ev)


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
    # passé : un match garde sa ligne `jours_non_analyses` jours, un autre événement `horizon_h` heures, tant qu'il reste une transition
    jours = cfg["jours_non_analyses"] if ev["type"] == "match" else cfg["evenements"].get(ev["type"], {}).get("jours_decision")
    recul = dt.timedelta(days=jours) if jours else dt.timedelta(hours=cfg["horizon_h"])  # 17/11 : un rapport d'académie non décidé reste 7 jours
    return r >= maintenant - recul and etat_evenement(ev, cfg, maintenant)["prochain"] is not None


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


def exports_periodiques(donnees, cfg, maintenant, enchere_proposee=False) -> list:
    """Paramètre enchere_proposee (19/11) : une de nos enchères est ouverte ou une ligne d'enchère est proposée (condition « si: enchere »).
    Exports périodiques de la config (`exports_periodiques`, décision de l'utilisateur du 17/11) : une ligne par écran dont l'export a
    plus de `perime_h` heures, avec l'âge de l'export ; dès que la base voit la capture, la ligne disparaît. Âge lu dans
    gold.bv_exports_state (règles core.export_rule) ou, sans écran dédié, dans la dernière page de `page_type` (bronze.raw_pages)."""
    etat = {r["ecran"]: r for r in _rows(donnees, "gold.bv_exports_state")}
    pages = {r["page_type"]: _dt(r["derniere_paris"]) for r in _rows(donnees, "pages_periodiques")}
    pages["transfers_global-history"] = next((_dt(r["derniere_paris"]) for r in _rows(donnees, "historique_global")), None)
    classements = {str(r["league_id"]): _dt(r["derniere_paris"]) for r in _rows(donnees, "classements")}
    journee = derniere_journee(donnees, maintenant)
    res = []
    for p in cfg.get("exports_periodiques", []):
        if p.get("si") == "enchere" and not enchere_proposee:
            continue  # 19/11 : Mes enchères seulement avec une enchère ouverte ou proposée
        if p["source"] == "exports_state":
            age = (etat.get(p["ecran"]) or {}).get("age_h")
            age = None if age in (None, "") else float(age)
        else:
            vu = classements.get(str(p["league_id"])) if p["source"] == "classement" else pages.get(p["page_type"])
            age = None if vu is None else (maintenant - vu).total_seconds() / 3600
        if p["source"] == "classement":  # 19/11 : à refaire après chaque journée (capture antérieure au dernier coup d'envoi de ligue)
            if age is not None and (journee is None or vu >= journee):
                continue
        elif age is not None and age <= p["perime_h"]:
            continue
        quoi = "jamais exporté" if age is None else f"export de {int(age)} h"
        res.append({"id": f"export-{p['ecran']}", "type": "export_periodique", "evenement": p["ecran"], "ecran": p["ecran"], "etat": None,
                    "prochain": "export_periodique", "rates": [], "echeance": None, "consigne": f"exporte {p['libelle']} — {quoi}", "age_h": None,
                    "priorite": 2, "action": True, "defauts": []})
    return res


def age_calendrier(donnees):
    """Âge en heures (entier) de la dernière capture de la page Amicaux (gold.bv_exports_state) ; None si jamais exportée."""
    age = next((r.get("age_h") for r in _rows(donnees, "gold.bv_exports_state") if r.get("ecran") == "Amicaux (liste)"), None)
    return None if age in (None, "") else int(float(age))


def amical_connu(donnees, jour) -> bool:
    """Un amical est-il au calendrier en base à cette date ?"""
    return any(r.get("competition_kind") == "amical" and _date(r.get("day")) == jour for r in _rows(donnees, "calendrier"))


def texte_calendrier_inconnu(donnees) -> str:
    h = age_calendrier(donnees)
    return "inconnu : calendrier jamais exporté, à refaire" if h is None else f"inconnu : calendrier de {h} h, à refaire"


def calendrier_a_refaire(donnees, maintenant) -> list:
    """22/11 : aucun amical connu pour demain -> une ligne d'export « exporte le calendrier » (jamais « aucun amical programmé »)."""
    if amical_connu(donnees, maintenant.date() + dt.timedelta(days=1)):
        return []
    h = age_calendrier(donnees)
    quoi = "jamais exporté" if h is None else f"export de {h} h"
    return [{"id": "export-calendrier", "type": "export_periodique", "evenement": "Calendrier", "ecran": "Amicaux (liste)", "etat": None,
             "prochain": "export_periodique", "rates": [], "echeance": None, "age_h": None, "priorite": 2, "action": True, "defauts": [],
             "consigne": f"exporte le calendrier (page Amicaux) : aucun amical connu pour demain — {quoi}"}]


def derniere_journee(donnees, maintenant):
    """Coup d'envoi (heure de Paris) du dernier match de ligue déjà commencé, lu dans gold.bv_etat_match ; None sans match."""
    envois = [_dt(r["coup_envoi_paris"]) for r in _rows(donnees, "etat_match") if r.get("competition_kind") == "ligue"]
    passes = [e for e in envois if e is not None and e <= maintenant]
    return max(passes) if passes else None


ETUDES = RACINE / "docs" / "etudes"


def etude_b1(dossier=None):
    """19/11 : (date, n 5×48, n rotation) de la ligne « B1 » (colonne « 29 / 95 ») de la dernière étude Match Engine de docs/etudes/
    qui l'a ; None si aucune."""
    import re
    for f in sorted(Path(dossier or ETUDES).glob("20*.md"), reverse=True):
        for ligne in f.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("| B1"):
                m = re.search(r"\|\s*(\d+)\s*/\s*(\d+)\s*\|", ligne)
                if m:
                    return f.name[:10], int(m.group(1)), int(m.group(2))
    return None


def texte_b1(b1, objectif) -> str:
    """« B1 (étude du JJ/MM) : 5×48 : 29 sur 150 ; rotation : 95 sur 150 » ; effectifs illisibles sinon."""
    if b1 is None:
        return f"effectifs B1 de l'étude illisibles (docs/etudes/), objectif ~{objectif} par sous-ensemble"
    d, a, r = b1
    return f"B1 (étude du {d[8:10]}/{d[5:7]}) : 5×48 : {a} sur {objectif} ; rotation : {r} sur {objectif}"


def matchs_ligue(donnees, cfg, maintenant, base=None, etudes=None) -> list:
    """19/11 (consigne de l'utilisateur) : une ligne 🟩 « exporte les N matchs de la ligue joués hier et pas encore en base » (N plafonné,
    du plus ancien au plus récent) ; la liste des liens est écrite dans <base>/<dossier>/ligue-<date des matchs>.md. Un match est en base
    si ses onglets Details (preview « finished ») et Stats par quart (period-box) sont capturés. [] si tout est en base."""
    reg = cfg.get("matchs_ligue")
    if not reg:
        return []
    hier = maintenant.date() - dt.timedelta(days=1)
    manque = sorted((r for r in _rows(donnees, "matchs_ligue") if _date(r["match_day"]) == hier and not r["is_mine"] and not r["en_base"]),
                    key=lambda r: (str(r.get("kickoff") or ""), str(r["fixture_id"])))[:int(reg["plafond_jour"])]
    if not manque:
        return []
    jour = maintenant.date()  # 19/11 : fichier nommé par le jour du passage
    rel = f"outputs/basketvibe/{reg['dossier']}/ligue-{jour:%Y-%m-%d}.md"
    if base is not None:
        f = Path(base) / reg["dossier"] / f"ligue-{jour:%Y-%m-%d}.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"# Matchs de ma ligue du {hier:%d/%m/%Y} à exporter (onglets Details et Stats par quart)\n\n"
                     + "".join(f"{i}. {r['home_team']} – {r['away_team']} : https://www.basketvibe.com/match/{r['fixture_id']}\n"
                               for i, r in enumerate(manque, 1)), encoding="utf-8")
    consigne = (f"exporte les {len(manque)} matchs de la ligue joués hier et pas encore en base (onglets Details et Stats par quart ; "
                f"liste : {rel}) — sert à l'étude du Match Engine : {texte_b1(etude_b1(etudes), reg['objectif_etude'])}")
    return [{"id": f"export-ligue-{hier}", "type": "export_periodique", "evenement": "Matchs de la ligue", "ecran": "Matchs de la ligue",
             "etat": None, "prochain": "export_periodique", "rates": [], "echeance": None, "consigne": consigne, "age_h": None,
             "priorite": 3, "action": True, "defauts": []}]


# ---- Phase A (17/11) : offres et ventes du jour, seuils lus dans la section `offres` du yaml -------------------------------

MARCHE = "Marché (enchères)"


def charger_offres(jeu: str = "basketvibe", chemin=None) -> dict:
    """Section `offres` de docs/attentes/jeux/<jeu>.yaml (seuils de l'utilisateur) et `domaines.transferts.minimum_effectif`."""
    import yaml
    y = yaml.safe_load(Path(chemin or CONFIG / f"{jeu}.yaml").read_text(encoding="utf-8"))
    return dict(y["offres"], minimum_effectif=y["domaines"]["transferts"]["minimum_effectif"],
                cout_test=y["etat_jour"]["evenements"]["academie"]["cout_test"])


def charger_personnel(jeu: str = "basketvibe", chemin=None) -> dict:
    """Section `personnel_propose` du yaml (règle proposée, à valider) ; {} si absente."""
    import yaml
    return yaml.safe_load(Path(chemin or CONFIG / f"{jeu}.yaml").read_text(encoding="utf-8")).get("personnel_propose") or {}


def texte_personnel(p: dict, actuel=()) -> str:
    """Règle `personnel_propose` décidée le 17/11 : « personnel : <action> (<±coût> par semaine) : <raison chiffrée> » si
    gold.bv_personnel_status (`actuel`) s'en écarte ; "" si conforme ou sans règle (un rôle absent du relevé n'est pas un écart)."""
    emb = {forme_role(r["role"]): r for r in actuel}
    actions, raisons, delta = [], [], 0
    for r in p.get("roles") or []:
        a = emb.get(forme_role(r["role"]))
        if a is None or a.get("hired") is None:
            continue
        ecart = int(r["garder"]) - int(float(a["hired"]))
        if ecart == 0:
            continue
        actions.append(f"{'embauche' if ecart > 0 else 'licencie'} {abs(ecart)} {r['role']} ({int(float(a['hired']))} → {r['garder']})")
        raisons.append(f"{r['role']} : {r['raison']}")
        delta += ecart * int(r["cout_unitaire"])
    if not actions:
        return ""
    signe = "+" if delta > 0 else ("−" if delta < 0 else "±")
    return f"personnel : {', '.join(actions)} ({signe}{_m(abs(delta))} par semaine) : {' ; '.join(raisons)}"


def forme_role(x) -> str:
    import unicodedata
    return unicodedata.normalize("NFKD", str(x)).encode("ascii", "ignore").decode().lower().strip()


def requete_rotation(n: int) -> str:
    """Minutes de chaque joueur de l'effectif sur les 4 derniers matchs de ligue, lues dans gold.bv_sell_candidates (18/11 : la
    jointure sur gold.bv_match_player_lines dépasse le délai, la rotation revenait vide et toute offre tombait en « revente »).
    min_moy = league_min_last4 (moyenne sur ses lignes de match), matchs_joues = 1 s'il a joué. La vue fixe N = 4 : `n` doit valoir 4."""
    assert int(n) == 4, "gold.bv_sell_candidates porte les 4 derniers matchs de ligue : matchs_rotation doit valoir 4"
    return ("select player_id, name, position, ps, league_min_last4 as min_moy, "
            "case when league_min_last4 > 0 then 1 else 0 end as matchs_joues from gold.bv_sell_candidates")


def _f(v):
    return None if v in (None, "") else float(v)


def enchere_max(case, capacite, salaire, revente_marge=None):
    """Enchère maximale d'une offre (18/11, règle de l'utilisateur) : min(p75 de la case, capacité − salaire hebdo de la recrue) ;
    revente : min(médiane / revente_marge, capacité − salaire), au-delà la marge de revente disparaît. Capacité = capacite_invest
    (gold.finance_health) moins les enchères déjà décidées, jamais le solde. Capacité ou salaire inconnus : None (pas d'offre)."""
    if capacite is None or salaire is None:
        return None
    haut = float(case["p75"]) if revente_marge is None else float(case["median"]) / float(revente_marge)
    return min(haut, float(capacite) - float(salaire))


def cases_poste(donnees) -> dict:
    """19/11 (règle de la police du 17/11) : case de prix = (poste, palier de note de 5, tranche d'âge), ventes à au moins une enchère
    (requête prix_cases_poste) ; {(poste, palier, tranche): ligne}."""
    return {(r["position"], int(float(r["ps_band"])), r["age_band"]): r for r in _rows(donnees, "prix_cases_poste")}


def case_du_poste(cases, poste, ps, age):
    import que_faire_blocs as qfb
    return cases.get((poste, qfb.palier_note(ps), qfb.tranche_age(age)))


def fits_au_poste(donnees) -> dict:
    """{(player_id, poste): (nom, ajustement, poste du joueur)} de gold.bv_slot_fit (requête slot_fit)."""
    return {(str(r["player_id"]), r["slot"]): (r["name"], float(r["fit"]), r.get("position")) for r in _rows(donnees, "slot_fit") if _f(r.get("fit")) is not None}


def offres_du_jour(donnees, o, capacite, maintenant=None, exclus=(), refus="") -> dict:
    """{"inconnu": texte ou None, "offres": [...], "tests": [...]} ; règle de l'utilisateur du 18/11 (titulaires de tout âge,
    remplaçants de 16 à 18 ans à fort potentiel) :
    - « amélioration » : note > celle de notre titulaire au poste (le joueur du poste qui a le plus de minutes sur les 4 derniers
      matchs de ligue), quel que soit l'âge ;
    - pas titulaire : jamais d'enchère, sauf « jeune » (jeune_age_min–jeune_age_max ans, test de potentiel connu = High) ;
    - pas titulaire, 16-18 ans, aucun test connu, taille dans la plage du poste (règle de signature d'académie) : « tester le
      potentiel » (cout_test), tests_par_jour au plus et tests_budget au total, meilleure note d'abord. Test connu : jamais retesté.
    Enchère max X (enchere_max) ; ligne supprimée si le prix relu (dernier export, gold.bv_market_candidates) dépasse X. Triées par
    gain attendu (médiane − prix). Marché périmé ou capacité illisible : « inconnu ». La revente (prix ≤ p25) ne donne plus de ligne
    d'enchère (18/11). `exclus` : noms déjà décidés (leur plafond est déjà retiré de la capacité)."""
    import aujourdhui as auj
    import que_faire_blocs as qfb
    perime = auj.inconnu_si_perime(donnees, MARCHE, maintenant)
    if perime is not None:
        return {"inconnu": perime, "offres": [], "tests": []}
    if capacite is None:
        return {"inconnu": "inconnu : capacité d'investissement illisible (capacite_invest de gold.finance_health)", "offres": [], "tests": []}
    if donnees.get("rotation") is None:  # 18/11 : sans rotation, aucun titulaire connu
        return {"inconnu": "inconnu : rotation illisible (minutes de ligue), offres non classées", "offres": [], "tests": []}
    exclus = {str(x).lower() for x in exclus}
    age_export = auj.age_export_h(donnees, MARCHE, maintenant)
    cases = cases_poste(donnees)
    fits = fits_au_poste(donnees)
    gain_min = float(o.get("gain_ajustement_min", 1.0))
    titulaires = {}  # 18/11 : titulaire du poste = le plus de minutes de ligue (min_moy) parmi ceux qui ont joué
    for r in _rows(donnees, "rotation"):
        if int(float(r["matchs_joues"] or 0)) > 0 and r.get("ps") is not None:
            t = titulaires.get(r["position"])
            if t is None or float(r["min_moy"] or 0) > float(t["min_moy"] or 0):
                titulaires[r["position"]] = r
    testes = {str(r["player_id"]): str(r["potentiel"]).strip().lower() for r in _rows(donnees, "tests_marche")
              if r.get("player_id") and r.get("potentiel")}
    jeune = lambda a: int(o["jeune_age_min"]) <= a <= int(o["jeune_age_max"])  # noqa: E731
    vues, res, a_tester = set(), [], []
    for r in _rows(donnees, "annonces_actives"):
        if r["auction_id"] in vues or None in (_f(r.get("price_now")), _f(r.get("ps")), _f(r.get("age"))) \
                or str(r["name"]).lower() in exclus or f"ne pas acheter {str(r['name']).lower()}" in str(refus).lower():
            continue  # 19/11 : « ne pas acheter » d'une police des 14 derniers jours
        vues.add(r["auction_id"])
        age, prix, sal = int(float(r["age"])), float(r["price_now"]), _f(r.get("est_weekly_salary"))
        # 19/11 : amélioration = ajustement au poste (gold.bv_slot_fit), jamais la note brute ; gain ≥ gain_ajustement_min sur notre titulaire
        poste = r.get("best_slot") or r["position"]
        f = titulaires.get(poste)
        fit_t = fits.get((str(f["player_id"]), poste)) if f is not None else None
        fit_c = _f(r.get("best_fit"))
        gain_fit = None if fit_t is None or fit_c is None else fit_c - fit_t[1]
        titulaire = gain_fit is not None and gain_fit >= gain_min
        if "slot_fit" not in donnees:  # appelant sans la requête slot_fit (anciens rejeux) : note brute, comme avant le 19/11
            f = titulaires.get(r["position"])
            titulaire, gain_fit = f is not None and float(r["ps"]) > float(f["ps"]), None
        pot = testes.get(str(r.get("player_id") or ""))
        if not titulaire and not jeune(age):
            continue  # remplaçant adulte : jamais d'enchère (règle du 18/11)
        if not titulaire and pot is None:
            if prix <= float(capacite) - (sal or 0) and r.get("height_cm") is not None and r["position"] in auj.PLAGE_TAILLE and auj.verdict_prospect(
                    {"position": r["position"], "age": age, "height_cm": r["height_cm"]})[0] == "tester":
                a_tester.append({"type": "tester", "nom": r["name"], "poste": r["position"], "age": age, "note": float(r["ps"]),
                                 "taille": int(float(r["height_cm"])), "prix": prix, "fin": _dt(r.get("ends_paris")),
                                 "cout": float(o["cout_test"]), "age_export_h": age_export})
            continue
        if not titulaire and pot != "high":
            continue  # test connu Low / Decent : ni enchère ni nouveau test
        case = case_du_poste(cases, r["position"], r["ps"], r["age"])
        if case is None or int(float(case["n"])) < int(o["case_min_ventes"]):
            continue  # 19/11 : moins de case_min_ventes ventes au poste = prix inconnu, aucune ligne
        med = float(case["median"])
        base = {"nom": r["name"], "poste": r["position"], "age": age, "note": float(r["ps"]), "prix": prix, "mediane": med,
                "p25": float(case["p25"]), "p75": float(case["p75"]), "n_case": int(float(case["n"])), "fin": _dt(r.get("ends_paris")),
                "mini": _f(case.get("mini")), "maxi": _f(case.get("maxi")),
                "gain": med - prix, "capacite": float(capacite), "salaire": sal, "age_export_h": age_export}
        x = enchere_max(case, capacite, sal)
        if x is None or prix > x:  # prix relu au-dessus de l'enchère max : ligne supprimée
            continue
        if titulaire:
            res.append(dict(base, type="amélioration", faible=f["name"], faible_note=float(f["ps"]), max=x, slot=poste, fit=fit_c,
                            faible_fit=fit_t and fit_t[1], gain_fit=gain_fit,
                            cout_point=x / gain_fit if gain_fit else None))
        else:
            res.append(dict(base, type="jeune", potentiel=pot, max=x))
    tests, total = [], 0.0
    for t in sorted(a_tester, key=lambda t: (-t["note"], t["prix"])):
        if len(tests) >= int(o["tests_par_jour"]) or total + t["cout"] > float(o["tests_budget"]) or total + t["cout"] > float(capacite):
            break
        total += t["cout"]
        tests.append(t)
    return {"inconnu": None, "offres": sorted(res, key=lambda x: -x["gain"]), "tests": tests}


def ventes_du_jour(donnees, o, tolerance, police="", bilan=None) -> list:
    """Joueurs à vendre pour profit : hors rotation (moyenne ≤ minutes_hors_rotation sur les matchs_rotation derniers matchs de
    ligue), écart de force avec son remplaçant ≤ tolérance du bloc 4, prix attendu = médiane de sa case (case ≥ case_min_ventes
    ventes) ; prix payé connu (gold.bv_transfer_history, bought_by_me) : profit ≥ vente_marge_profit, sinon « prix d'achat
    inconnu, profit non calculé » et la vente reste proposée ; jamais « ne pas vendre <nom> » de la police du jour, jamais déjà en vente ; l'effectif reste
    ≥ minimum_effectif. Triés par prix attendu décroissant."""
    import aujourdhui as auj
    import que_faire_blocs as qfb
    bilan = {} if bilan is None else bilan
    compte = lambda r: bilan.__setitem__(r, bilan.get(r, 0) + 1)  # noqa: E731
    if tolerance is None:
        bilan["tolérance du bloc 4 non lue"] = 0
        return []
    cases = cases_poste(donnees)
    fits = fits_au_poste(donnees)
    rot = {str(r["player_id"]): r for r in _rows(donnees, "rotation")}
    titulaires = {}  # même règle que les offres : le plus de minutes de ligue au poste
    for r in rot.values():
        if int(float(r.get("matchs_joues") or 0)) > 0:
            t = titulaires.get(r["position"])
            if t is None or float(r["min_moy"] or 0) > float(t["min_moy"] or 0):
                titulaires[r["position"]] = r
    testes = {str(r["player_id"]): str(r["potentiel"]).strip().lower() for r in _rows(donnees, "tests_marche")
              if r.get("player_id") and r.get("potentiel")}
    joueurs = _rows(donnees, "vendre")
    achats = {str(r["player_id"]): float(r["fee"]) for r in _rows(donnees, "prix_achat") if _f(r.get("fee")) and float(r["fee"]) > 0}
    res = []
    bilan["_n"] = len(joueurs)
    for j in joueurs:
        pid, poste, m = str(j["player_id"]), j["position"], rot.get(str(j["player_id"]))
        # 19/11 : remplaçant pris au même poste, par l'ajustement au poste (gold.bv_slot_fit), jamais la note brute
        autres = [(nf[1], nf[0]) for (p, s), nf in fits.items() if s == poste and p != pid and nf[2] == poste]
        moi = fits.get((pid, poste))
        r = {} if moi is None or not autres else {"replacement_name": max(autres)[1], "gap": moi[1] - max(autres)[0]}
        if "slot_fit" not in donnees:  # appelant sans la requête slot_fit (anciens rejeux) : gold.bv_sell_replacement
            r = next((x for x in _rows(donnees, "gold.bv_sell_replacement") if str(x["player_id"]) == pid), {})
        if auj.vrai(j.get("on_transfer_list")):
            compte("déjà en vente")
            continue
        if m is None:
            compte("minutes de ligue absentes")
            continue
        if float(m["min_moy"]) > float(o["minutes_hors_rotation"]):
            compte("en rotation")
            continue
        if r.get("gap") is None or float(r["gap"]) > float(tolerance):
            compte("remplaçant trop faible ou absent")
            continue
        if f"ne pas vendre {str(j['name']).lower()}" in str(police).lower():
            compte("« ne pas vendre » de la police")
            continue
        age = int(float(j["age"]))  # règle 14 (19/11) : 16-18 ans non titulaire vendu seulement si test connu Low ou Decent
        if int(o["jeune_age_min"]) <= age <= int(o["jeune_age_max"]) and (titulaires.get(poste) or {}).get("player_id") != j["player_id"] \
                and testes.get(pid) not in ("low", "decent"):
            compte("jeune de 16 à 18 ans sans test Low ou Decent")
            continue
        case = case_du_poste(cases, poste, j["ps"], j["age"])
        if case is None or int(float(case["n"])) < int(o["case_min_ventes"]):
            compte(f"prix inconnu (moins de {o['case_min_ventes']} ventes à au moins une enchère au poste)")
            continue
        prix = float(case["median"])  # prix attendu = médiane de la case
        paye = achats.get(str(j["player_id"]))
        profit = None if paye is None else (prix - paye) / paye
        if profit is not None and profit < float(o["vente_marge_profit"]):
            compte("profit insuffisant")
            continue
        res.append({"type": "vente", "nom": j["name"], "poste": j["position"], "age": int(float(j["age"])), "note": float(j["ps"]),
                    "prix": prix, "mediane": prix, "n_case": int(float(case["n"])), "min_moy": float(m["min_moy"]),
                    "mini": _f(case.get("mini")), "maxi": _f(case.get("maxi")),
                    "remplacant": r.get("replacement_name"), "ecart": float(r["gap"]), "tolerance": float(tolerance), "gain": prix,
                    "prix_achat": paye, "profit": profit})
    places = max(0, len(joueurs) - int(o["minimum_effectif"]))
    if res and not places:
        bilan["minimum d'effectif atteint"] = len(res)
    return sorted(res, key=lambda x: -x["gain"])[:places]


def _m(x) -> str:
    return f"{x:,.0f}".replace(",", " ")


def _virg1(v) -> str:
    return f"{float(v):.1f}".replace(".", ",")


def _fourchette(x) -> str:
    """19/11 : « , fourchette min à max » des ventes comparables du poste ; vide si inconnue."""
    return "" if x.get("mini") is None or x.get("maxi") is None else f", fourchette {_m(x['mini'])} à {_m(x['maxi'])}"


def texte_transfert(x, o) -> str:
    """Ligne d'une offre ou d'une vente : nom, poste, âge, note, prix, médiane de la case, type, fin, seuils du yaml, règle 2, police."""
    from police import SEUIL_GROS_MONTANT
    qui = f"{x['nom']} ({x['poste']}, {x['age']} ans, note {_virg(x['note'])})"
    if x["type"] == "vente":
        t = (f"vente : {qui}, prix attendu {_m(x['prix'])}, médiane du poste {_m(x['mediane'])}{_fourchette(x)} "
             f"({x['n_case']} ventes à au moins une enchère ≥ {o['case_min_ventes']}) ; "
             f"{_virg(x['min_moy'])} min en moyenne sur {o['matchs_rotation']} matchs de ligue (≤ {_virg(o['minutes_hors_rotation'])}), "
             f"écart avec {x['remplacant']} {_virg(x['ecart'])} (tolérance {_virg(x['tolerance'])}) ; "
             + ("prix d'achat inconnu, profit non calculé" if x.get("prix_achat") is None else
                f"profit {x['profit'] * 100:.0f} % sur le prix payé {_m(x['prix_achat'])} (≥ {o['vente_marge_profit'] * 100:.0f} %)")
             + " ; fin : annonce à créer")
    else:
        if x["type"] == "amélioration" and x.get("gain_fit") is None:
            seuil = (f"note > {_virg(x['faible_note'])} de {x['faible']} (notre titulaire au poste, le plus de minutes sur {o['matchs_rotation']} matchs de ligue ; ajustement au poste non lu) ; "
                     f"max = min(p75 {_m(x['p75'])}, capacité {_m(x['capacite'])} − salaire {_m(x['salaire'])})")
        elif x["type"] == "amélioration":
            seuil = (f"ajustement {x['slot']} {_virg(x['fit'])} contre {_virg(x['faible_fit'])} pour {x['faible']} (notre titulaire au poste, le plus "
                     f"de minutes sur {o['matchs_rotation']} matchs de ligue), gain {_virg1(x['gain_fit'])} (≥ {_virg1(o.get('gain_ajustement_min', 1.0))}), "
                     f"coût par point gagné {_m(x['cout_point'])} (enchère max / gain) ; max = min(p75 {_m(x['p75'])}, capacité {_m(x['capacite'])} − salaire {_m(x['salaire'])})")
        elif x["type"] == "jeune":
            seuil = (f"remplaçant {o['jeune_age_min']}-{o['jeune_age_max']} ans, test de potentiel connu High ; "
                     f"max = min(p75 {_m(x['p75'])}, capacité {_m(x['capacite'])} − salaire {_m(x['salaire'])})")
        else:
            seuil = (f"case de {x['n_case']} ventes (≥ {o['case_min_ventes']}), prix ≤ p25 {_m(x['p25'])}, médiane ≥ {_virg(o['revente_marge'])} × prix ; "
                     f"max = min(médiane / {_virg(o['revente_marge'])}, capacité {_m(x['capacite'])} − salaire {_m(x['salaire'])})")
        fin = f"{x['fin']:%d/%m %H:%M}" if x.get("fin") else "inconnue"
        import aujourdhui as auj
        age = x.get("age_export_h")
        age = f"export du Marché de {age:.0f} h" if age is not None else "âge de l'export du Marché illisible"
        prix = (f"prix inconnu (aucune enchère, {age})" if x["prix"] <= auj.PRIX_NON_SIGNIFICATIF  # 18/11 : « à 0 » = inconnu
                else f"à {_m(x['prix'])} ({age})")
        t = f"{x['type']} : {qui}, enchère max {_m(x['max'])}, {prix} ; médiane du poste {_m(x['mediane'])}{_fourchette(x)} ; {seuil} ; fin {fin}"
    t += " — proposition seulement (règle 2)"
    if max(x["prix"], x.get("max") or 0) > SEUIL_GROS_MONTANT["basketvibe"]:
        t += " — police d'abord : dossier.py puis agent police"
    return t


def texte_test_marche(x, o) -> str:
    """18/11 : « tester le potentiel (25 000) » d'un 16-18 ans du Marché sans test connu ; seul High justifie une enchère."""
    fin = f"{x['fin']:%d/%m %H:%M}" if x.get("fin") else "inconnue"
    return (f"pas d'enchère avant le test ; Police : ne pas acheter — tester le potentiel ({_m(x['cout'])}) : {x['nom']} ({x['poste']}, {x['age']} ans, {x['taille']} cm, note {_virg(x['note'])}), "
            f"fin {fin} ; taille dans la plage du poste (règle de signature d'académie) ; seul « High » justifie une enchère "
            f"(au plus {o['tests_par_jour']} test{'s' if int(o['tests_par_jour']) > 1 else ''} et {_m(float(o['tests_budget']))} par jour) — proposition seulement (règle 2)")


def texte_aucune_vente(bilan) -> str:
    """« Ventes : aucune à proposer (N joueurs évalués, raison) » ; raisons triées par nombre de joueurs écartés."""
    n = bilan.get("_n", 0)
    raisons = sorted(((k, v) for k, v in bilan.items() if k != "_n"), key=lambda x: -x[1])
    r = " ; ".join(k if not v else f"{k} : {v}" for k, v in raisons) or "aucun joueur dans l'effectif lu"
    return f"Ventes : aucune à proposer ({n} joueur{'s' if n > 1 else ''} évalué{'s' if n > 1 else ''}, {r})"


def lignes_transferts(donnees, capacite, tolerance, police="", maintenant=None, o=None, exclus=(), refus="") -> list:
    """Lignes « Transferts » de l'état par événement : `max_offres` offres et `max_ventes` ventes au plus, triées par gain attendu ;
    Marché périmé : une ligne « inconnu » à la place des offres. Le bloc 4 lit ces mêmes lignes. `refus` : verdicts « ne pas vendre /
    ne pas acheter » des polices des 14 derniers jours (aujourdhui_sources.lire_refus_police)."""
    o = o or charger_offres()
    of = offres_du_jour(donnees, o, capacite, maintenant, exclus, refus)
    bilan = {}
    ventes = ventes_du_jour(donnees, o, tolerance, f"{police}\n{refus}", bilan)[:int(o["max_ventes"])]
    choix = of["offres"][:int(o["max_offres"])] + ventes
    ligne = lambda i, prochain, consigne: {"id": i, "type": "transfert", "evenement": "transferts", "etat": None, "prochain": prochain,
                                           "rates": [], "echeance": None, "consigne": consigne, "age_h": None, "priorite": 2,
                                           "action": True, "defauts": []}
    res = [ligne("offres-inconnu", "offre", f"offres du Marché : {of['inconnu']}")] if of["inconnu"] else []
    offres = sorted(of["offres"][:int(o["max_offres"])], key=lambda x: -x["gain"])
    somme = sum(x["max"] for x in offres)
    if capacite is not None and len(offres) > 1 and somme > float(capacite):  # 18/11 : plafonds additionnés > capacité
        cumul, tient = 0.0, []
        for x in offres:
            if cumul + x["max"] <= float(capacite):
                cumul += x["max"]
                tient.append(x["nom"])
        ordre = ", ".join(f"{i}. {x['nom']} (max {_m(x['max'])})" for i, x in enumerate(offres, 1))
        res.append(dict(ligne("offres-priorite", "offre",
                              f"priorité : plafonds additionnés {_m(somme)} > capacité {_m(float(capacite))} ; enchéris dans cet ordre "
                              f"(gain attendu) : {ordre} ; tiennent ensemble à leur plafond : {', '.join(tient) or 'aucune'} ; "
                              "chaque enchère gagnée retire son prix de la capacité et baisse les plafonds suivants"), priorite=1))
    if not ventes:  # 18/11 : jamais de silence sur les ventes
        res.append(dict(ligne("ventes-aucune", "vente", texte_aucune_vente(bilan)), action=False, priorite=3))
    return res + [ligne(f"{x['type']}-{x['nom']}", x["type"] if x["type"] == "vente" else "offre", texte_transfert(x, o))
                  for x in sorted(choix, key=lambda x: -x["gain"])] \
        + [ligne(f"tester-{x['nom']}", "offre", texte_test_marche(x, o)) for x in of.get("tests", [])]


class _Champs(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def agents_a_lancer(etats, cfg=None, base=None, jour=None, dossier_agents=None) -> list:
    """P3 (17/11) : agents à lancer pour les états du jour, lus dans la table `agents` de la config (état → agent → sortie).
    Une ligne d'état (action vraie) prend la première ligne de table dont chaque clé type / genre / prochain lui est égale.
    Agent null : rien. Résultat, une entrée par lancement prévu : {agent, id, evenement, sortie (relative à `base`), consigne,
    avant, statut, raison} ; statut « a_lancer », « deja_fait » (sortie présente et non vide : pas de relance) ou « refus »
    (agent absent de .claude/agents, plafond d'agents d'analyse du passage atteint), avec sa raison."""
    cfg = cfg or charger_config()
    base = Path(base) if base else RACINE / "outputs" / "basketvibe"
    if jour is None:
        from heure_paris import paris
        jour = paris().date()
    dossier_agents = Path(dossier_agents) if dossier_agents else RACINE / ".claude" / "agents"
    hors = set(cfg.get("agents_hors_plafond", []))
    plafond, n, res = cfg.get("agents_plafond"), 0, []
    for l in etats:
        if not l.get("action"):
            continue
        r = next((r for r in cfg.get("agents", []) if all(l.get(k) == r[k] for k in ("type", "genre", "prochain") if k in r)), None)
        if not r or not r.get("agent"):
            continue
        champs = _Champs(l, jour=jour.isoformat())
        sortie = r["sortie"].format_map(champs)
        e = {"agent": r["agent"], "id": l.get("id"), "evenement": l.get("evenement"), "sortie": sortie,
             "consigne": " ; ".join(x for x in (l.get("consigne"), l.get("test"), r.get("consigne", "").format_map(champs)) if x),
             "avant": r.get("avant"), "statut": "a_lancer", "raison": None}
        f = base / sortie
        if f.is_file() and f.stat().st_size > 0:
            e.update(statut="deja_fait", raison=f"sortie déjà présente ({sortie})")
        elif not (dossier_agents / f"{r['agent']}.md").is_file():
            e.update(statut="refus", raison=f"agent {r['agent']} absent de .claude/agents")
        elif r["agent"] not in hors and plafond is not None and n >= plafond:
            e.update(statut="refus", raison=f"plafond de {plafond} agents d'analyse par passage atteint")
        elif r["agent"] not in hors:
            n += 1
        res.append(e)
    return res


def sans_ligne(evenements, ls, cfg, maintenant) -> list:
    """Complétude : événements retenus qui n'ont pas de ligne dans `ls` (doit être vide)."""
    ids = {l["id"] for l in ls}
    return [ev for ev in evenements if dans_horizon(ev, cfg, maintenant) and ev.get("id") not in ids]


# ---- P2.4 : la lecture (vues gold de sql/gold/085_bv_etat_jour.sql) et la construction des événements ------------------
# Lues avec les autres requêtes de aujourdhui.py (même lecteur, mêmes erreurs « vue illisible ») ; les clés « prospects »,
# « gold.bv_exports_state », « a_evaluer » et « transferts_recents » viennent de aujourdhui.REQUETES.
REQUETES = {
    "etat_match": "select fixture_id, competition_kind, day, opponent, home, played, my_result, coup_envoi_paris, verrou_paris, "
                  "apercu_paris, page_paris, sauvegarde, saisie_export_paris, joueurs_saisis from gold.bv_etat_match "
                  "order by day, coup_envoi_paris",
    "blessures_match": "select player_id, name, injury_return_on, fixture_id, competition_kind, day, indisponible from gold.bv_blessures_match",
    "ecran_joueurs": "select fixture_id, joueur, minutes, off_focus, role, tir, agress from gold.bv_saisie_joueurs "
                     "where match_day >= (now() at time zone 'Europe/Paris')::date - 1",
    "adversaires_connus": "select fixture_id, count(*) as n from gold.bv_saisie_adversaires "
                          "where match_day >= (now() at time zone 'Europe/Paris')::date - 1 and fixture_id is not null group by fixture_id",
    "fatigue_roster": "select name, fatigue from gold.bv_roster_now",
    "seuil_fatigue": "select seuil_bas from core.alert_rule where game = 'basketvibe' and rule_id = 'fatigue' and actif",
    "historique_global": "select max(captured_at at time zone 'Europe/Paris') as derniere_paris from bronze.raw_pages "
                         "where page_type = 'transfers_global-history'",
}
REQUETES["prix_achat"] = ("select distinct on (player_id) player_id, fee from gold.bv_transfer_history "
                          "where bought_by_me and fee is not null order by player_id, sold_on desc")  # prix payé pour nos joueurs achetés
# 19/11 : âge des exports périodiques par page_type (onglets de la ligue), du classement par ligue, et matchs de ma ligue des 3 derniers
# jours avec l'état de leurs onglets Details (preview « finished ») et Stats par quart (period-box).
_FIX_LIGUE = "source_url ~ '/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/fixtures$'"
_MOI = ("(select payload->'body'->>'club_id' from bronze.raw_pages where game = 'basketvibe' and source = 'api' "
        "and source_url ~ '/api/v1/auth/me$' order by captured_at desc limit 1)")
_EN_BASE = ("(select substring(source_url from '/fixtures/([0-9a-f-]{36})/') as fid from bronze.raw_pages "
            "where game = 'basketvibe' and source = 'api' and source_url ~ '/fixtures/[0-9a-f-]{36}/(preview|period-box)' group by 1 "
            "having bool_or(source_url ~ '/preview' and payload->'body'->>'kind' = 'finished') and bool_or(source_url ~ '/period-box'))")
# 19/11 (règle de la police du 17/11) : case de prix par poste, ventes à au moins une enchère (prix > prix de départ ou bids > 0 vu
# au Marché), avec la fourchette min–max ; ajustement de chaque joueur à chaque poste.
REQUETES["prix_cases_poste"] = (
    "select t.position, t.ps_band, t.age_band, count(*) as n, percentile_cont(0.25) within group (order by t.fee) as p25, "
    "percentile_cont(0.5) within group (order by t.fee) as median, percentile_cont(0.75) within group (order by t.fee) as p75, "
    "min(t.fee) as mini, max(t.fee) as maxi from gold.bv_transfer_history t where t.fee > 0 and t.position is not null "
    "and t.ps_band is not null and (t.fee > t.starting_price or exists (select 1 from core.market_listing l where l.game = 'basketvibe' "
    "and l.listing_id = t.auction_id::text and l.bids > 0)) group by 1, 2, 3")
REQUETES["slot_fit"] = "select player_id, name, position, slot, fit from gold.bv_slot_fit"
REQUETES["pages_periodiques"] = (
    "select page_type, max(captured_at at time zone 'Europe/Paris') as derniere_paris from bronze.raw_pages "
    "where game = 'basketvibe' and page_type in ('standings_teams', 'standings_players', 'standings_injuries') group by page_type")
REQUETES["classements"] = (
    "select substring(source_url from '/leagues/([0-9a-f-]{36})/') as league_id, max(captured_at at time zone 'Europe/Paris') as derniere_paris "
    "from bronze.raw_pages where game = 'basketvibe' and source = 'api' "
    "and source_url ~ '/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/standings$' group by 1")
REQUETES["matchs_ligue"] = (
    "select distinct on (f->>'id') f->>'id' as fixture_id, (f->>'match_day')::date as match_day, f->>'kickoff_time' as kickoff, "
    "jsonb_path_query_first(p.payload->'body'->'team_labels', '$[*] ? (@.team_id == $t).team_name', jsonb_build_object('t', f->>'home_team_id')) #>> '{}' as home_team, "
    "jsonb_path_query_first(p.payload->'body'->'team_labels', '$[*] ? (@.team_id == $t).team_name', jsonb_build_object('t', f->>'away_team_id')) #>> '{}' as away_team, "
    f"{_MOI} in (f->>'home_team_id', f->>'away_team_id') as is_mine, b.fid is not null as en_base "
    f"from bronze.raw_pages p cross join lateral jsonb_array_elements(p.payload->'body'->'fixtures') f left join {_EN_BASE} b on b.fid = f->>'id' "
    f"where p.game = 'basketvibe' and p.source = 'api' and p.{_FIX_LIGUE} "
    "and exists (select 1 from jsonb_array_elements(p.payload->'body'->'fixtures') g "
    f"where {_MOI} in (g->>'home_team_id', g->>'away_team_id')) "
    "and (f->>'match_day')::date >= (now() at time zone 'Europe/Paris')::date - 3 "
    "and (f->>'match_day')::date < (now() at time zone 'Europe/Paris')::date order by f->>'id', p.captured_at desc")
REQUETES["matchs_en_base"] = (
    f"select count(*) as n from {_EN_BASE} b where b.fid in (select f->>'id' from bronze.raw_pages p "
    f"cross join lateral jsonb_array_elements(p.payload->'body'->'fixtures') f where p.game = 'basketvibe' and p.source = 'api' and p.{_FIX_LIGUE})")
REQUETES["rotation"] = requete_rotation(charger_offres()["matchs_rotation"])  # phase A : N lu dans le yaml
# 18/11 : test de potentiel connu d'un joueur (Low / Decent / High), lu sur sa page profil (season-profile ou transfer-auction de
# l'API), dernière capture ; aucune vue silver ne le porte. 12 ms mesuré le 18/11.
REQUETES["tests_marche"] = (
    "select distinct on (right(p.page_url, 36)) right(p.page_url, 36) as player_id, "
    "jsonb_path_query_first(p.payload, 'lax $.body.**.potential_bucket') #>> '{}' as potentiel "
    "from bronze.raw_pages p where p.game = 'basketvibe' and p.page_type = 'player' "
    "and p.source_url ~ '/players/[0-9a-f-]{36}/(season-profile|transfer-auction)' "
    "and jsonb_path_exists(p.payload, 'lax $.body.**.potential_bucket ? (@ != null)') "
    "order by right(p.page_url, 36), p.captured_at desc")
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def _rows(donnees, nom) -> list:
    d = donnees.get(nom)
    if not d or d == "rejeu":
        return []
    cols, lignes = d
    return [dict(zip(cols, l)) for l in lignes]


def _dt(v):
    if v in (None, ""):
        return None
    return v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v)[:19])


def _date(v):
    if v in (None, ""):
        return None
    return v if isinstance(v, dt.date) and not isinstance(v, dt.datetime) else dt.date.fromisoformat(str(v)[:10])


def _entier(v):
    import re
    m = re.match(r"\s*(\d+)", str(v or ""))
    return int(m.group(1)) if m else None


def occurrences(quand: str, maintenant) -> list:
    """« jeudi 09:00 » → [dernière occurrence passée, suivante] (heure de Paris)."""
    jour, heure = quand.split()
    h = dt.time.fromisoformat(heure)
    d = maintenant.date() - dt.timedelta(days=(maintenant.weekday() - JOURS.index(jour)) % 7)
    prec = dt.datetime.combine(d, h)
    if prec > maintenant:
        prec -= dt.timedelta(days=7)
    return [prec, prec + dt.timedelta(days=7)]


def _cle(S, mot, depuis) -> bool:
    """Déclaration au registre (`[clé=<mot>]`, skill deja-fait) datée d'au moins `depuis`."""
    import unicodedata
    n = lambda s: unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return any(n(c["nom"]).startswith(mot) and c["jour"] >= depuis for c in S.get("cles", []))


def lire_fiche(base, jour, ev):
    """Fiche du match : brief tactique le plus récent (≤ `jour`) qui nomme l'adversaire et, s'il porte une date, celle du match."""
    import re
    import composition as comp
    b = comp.brief_pour(base, jour, ev["adversaire"], ev["genre"] == "amical")
    if not b:
        return None
    _, f, texte = b
    titre = texte.splitlines()[0] if texte else ""
    d = re.search(r"\b(\d{2})/(\d{2})\b", titre)
    if d and ev.get("jour") and (int(d.group(1)), int(d.group(2))) != (ev["jour"].day, ev["jour"].month):
        return None  # fiche d'un autre match contre le même adversaire
    lue = comp.lire_fiche(texte)
    fiche = {"ok": lue is not None, "adversaire": comp.adversaire_du_titre(titre), "fichier": f"briefs/{Path(f).name}", "joueurs": []}
    for c in (lue[0] if lue else []):  # joueur, poste, q1, q2, q3, q4, prol, min, off, role, tir, agress
        fiche["joueurs"].append({"nom": c[0], "minutes": _entier(c[7]) or 0, "off": _entier(c[8]), "role": _entier(c[9]),
                                 "tir": _entier(c[10]), "agress": _entier(c[11])})
    agr = {j["agress"] for j in fiche["joueurs"] if j["minutes"] > 0}
    fiche["agress_test"] = agr.pop() if len(agr) == 1 else None
    return fiche


def fiche_entrainement(base, jour, depuis):
    """Fiche d'entraînement la plus récente (`briefs/AAAA-MM-JJ-entrainement*.md`) datée entre `depuis` et `jour` ; None sinon."""
    import re
    trouves = []
    for f in (Path(base) / "briefs").glob("*-entrainement*.md"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-entrainement", f.name)
        if m and depuis <= dt.date.fromisoformat(m.group(1)) <= jour and f.stat().st_size > 0:
            trouves.append((m.group(1), f.name))
    return {"fichier": f"briefs/{max(trouves)[1]}"} if trouves else None


MANQUE_SIGNATURE = ("à juger, il manque la mesure « meilleures caractéristiques du poste » de la règle de signature "
                    "(aucun seuil écrit par l'utilisateur)")


def _tests_academie(donnees):
    """(n, verdicts, capture) : n = prospects du rapport encore au verdict « tester » (None si une taille ou un poste manque) ;
    verdicts des prospects testés, lus sur la dernière capture de la page Académie (requête « tests_academie », max(captured_at)) :
    règle de signature de l'utilisateur du 17/11 (potentiel énorme, meilleures caractéristiques du poste, bonne taille).
    Potentiel autre que high : ignorer. High et taille juste : la mesure des compétences au poste manque, elle est nommée."""
    import aujourdhui as auj
    pros = _rows(donnees, "prospects")
    if not pros or any(p.get("position") not in auj.PLAGE_TAILLE or p.get("height_cm") in (None, "") for p in pros):
        return None, [], None
    tests = {str(r["slot"]): r for r in _rows(donnees, "tests_academie") if r.get("teste") and r.get("potentiel")}
    capture = max((_dt(r["capture_paris"]) for r in _rows(donnees, "tests_academie") if r.get("capture_paris")), default=None)
    n, verdicts = 0, []
    for p in pros:
        t = tests.get(str(p["slot"]))
        verdict = auj.verdict_prospect(dict(p, test_potentiel=t["potentiel"] if t else None))[0]
        if t is None:
            n += verdict == "tester"
            continue
        verdicts.append({"nom": p["name"], "poste": p["position"], "potentiel": str(t["potentiel"]).lower(),
                         "verdict": MANQUE_SIGNATURE if verdict == "à juger" else verdict})
    return n, verdicts, capture


def construire(donnees, S, base, jour, maintenant, cfg) -> list:
    """Événements du jour depuis les lignes lues (`donnees`, format de aujourdhui.lignes_de), les sources (S : analyste, cles,
    cibles, police) et les briefs de `base` ; les contrôles fiche contre réalité sont appliqués à chaque match."""
    from police import SEUIL_GROS_MONTANT
    S = S or {}
    evs = []
    ecran = {}
    for r in _rows(donnees, "ecran_joueurs"):
        ecran.setdefault(r["fixture_id"], []).append({"nom": r["joueur"], "minutes": _entier(r["minutes"]) or 0, "off": _entier(r["off_focus"]),
                                                      "role": _entier(r["role"]), "tir": _entier(r["tir"]), "agress": _entier(r["agress"])})
    blessures = {}
    for r in _rows(donnees, "blessures_match"):
        blessures.setdefault(r["fixture_id"], {})[r["name"]] = _date(r["injury_return_on"])
    seuil = next((r["seuil_bas"] for r in _rows(donnees, "seuil_fatigue")), None)
    fatigue = {r["name"]: r["fatigue"] for r in _rows(donnees, "fatigue_roster")}
    a_evaluer = sum(int(r["n"]) for r in _rows(donnees, "a_evaluer"))
    matchs = _rows(donnees, "etat_match")
    officiels = [r for r in matchs if r["played"] and r["competition_kind"] != "amical"]
    dernier = max(officiels, key=lambda r: (str(r["day"]), str(r["coup_envoi_paris"] or "")))["fixture_id"] if officiels else None
    connus = None if donnees.get("adversaires_connus") in (None, "rejeu") else {str(r["fixture_id"]) for r in _rows(donnees, "adversaires_connus")}
    for r in matchs:
        genre, d = r["competition_kind"], _date(r["day"])
        regle = cfg["matchs"].get(genre)
        if regle is None:
            continue
        defaut = lambda cle: dt.datetime.combine(d, dt.time.fromisoformat(regle[cle])) if d and regle.get(cle) else None
        ce = _dt(r["coup_envoi_paris"]) or defaut("coup_envoi_defaut")
        page = _dt(r["page_paris"])
        dates = [x for x in (_dt(r["apercu_paris"]), _dt(r["saisie_export_paris"]), page) if x]
        ev = {"type": "match", "genre": genre, "id": r["fixture_id"], "adversaire": r["opponent"], "jour": d, "coup_envoi": ce,
              "verrou": _dt(r["verrou_paris"]) or defaut("verrou_defaut"), "joue": bool(r["played"]), "resultat": r["my_result"],
              "apercu_at": _dt(r["apercu_paris"]), "page_at": page if page and (ce is None or page >= ce) else None,
              "ecran": ({"sauvegarde": bool(r["sauvegarde"]), "joueurs": ecran.get(r["fixture_id"], [])} if r["sauvegarde"] is not None else None),
              "analyse": S.get("analyste") is not None and d is not None and S["analyste"] >= d,
              "adv_connus": None if connus is None else str(r["fixture_id"]) in connus,
              "juge_requis": r["fixture_id"] == dernier, "juge": a_evaluer == 0, "maj_at": max(dates) if dates else None}
        ev["fiche"] = lire_fiche(base, jour, ev) if d and d >= jour else None
        if genre == "amical" and d and d >= jour:
            ev["test"] = texte_test_fiche(S.get("experiences"), r, _rows(donnees, "amical_reglage")) or None
        evs.append(appliquer_controles(ev, {"blessures": blessures.get(r["fixture_id"], {}), "fatigue": fatigue, "seuil_fatigue": seuil}, cfg))
    rapport = max((_dt(r["rapport_paris"]) for r in _rows(donnees, "prospects")), default=None)
    page_entr = next((_dt(r["dernier_paris"]) for r in _rows(donnees, "gold.bv_exports_state") if r["ecran"] == "Entraînement"), None)
    for t, c in cfg["evenements"].items():
        if t == "enchere":
            continue
        for q in occurrences(c["quand"], maintenant):
            ev = {"type": t, "id": f"{t}-{q:%Y-%m-%d}", "quand": q, "maj_at": None}
            if t == "academie":
                n, verdicts, capture = _tests_academie(donnees)
                ev.update(rapport_at=rapport, decide=_cle(S, "academie", q.date()), tests=n, verdicts=verdicts, capture=capture)
            else:
                ev.update(page_at=page_entr, saisi=_cle(S, "entrainement", q.date()), fiche=fiche_entrainement(base, jour, q.date()))
            evs.append(ev)
    vendus = {str(r["name"]).lower() for r in _rows(donnees, "transferts_recents")}
    for c in S.get("cibles", []):
        evs.append({"type": "enchere", "id": f"enchere-{c['nom']}", "nom": c["nom"], "fin": c.get("fin"),
                    "gros": c.get("max") is not None and float(c["max"]) > SEUIL_GROS_MONTANT["basketvibe"],
                    "police": c["nom"].lower() in str(S.get("police", "")).lower(), "resultat": c["nom"].lower() in vendus, "maj_at": None})
    return evs
