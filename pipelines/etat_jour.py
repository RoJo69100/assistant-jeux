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
    if etat == "decide":
        n = ev.get("tests")
        if n:  # 17/11 : décision attendue chiffrée (verdict « tester » de aujourdhui.verdict_prospect, coût de la config)
            cout = f"{n * cfg['evenements']['academie']['cout_test']:,}".replace(",", " ")
            return None, f"décision attendue : tester {n} prospect{'s' if n > 1 else ''} ({cout}), rapport du {_jj(ev['quand'])}", True
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
    defauts = [] if ev["type"] != "match" else (ev.get("fiche") or {}).get("defauts", []) + (ev.get("ecran") or {}).get("defauts", [])
    return {"id": ev.get("id"), "type": ev["type"], "evenement": _nom(ev), "etat": atteint, "prochain": prochain, "rates": rates,
            "echeance": echeance, "consigne": consigne, "age_h": age, "priorite": prio, "action": action, "defauts": defauts,
            "genre": ev.get("genre"), "cle": _cle_fichier(ev), "titre": _titre(ev)}


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


def exports_periodiques(donnees, cfg, maintenant) -> list:
    """Exports périodiques de la config (`exports_periodiques`, décision de l'utilisateur du 17/11) : une ligne par écran dont l'export a
    plus de `perime_h` heures, avec l'âge de l'export ; dès que la base voit la capture, la ligne disparaît. Âge lu dans
    gold.bv_exports_state (règles core.export_rule) ou, sans écran dédié, dans la dernière page de `page_type` (bronze.raw_pages)."""
    etat = {r["ecran"]: r for r in _rows(donnees, "gold.bv_exports_state")}
    page = next((_dt(r["derniere_paris"]) for r in _rows(donnees, "historique_global")), None)
    res = []
    for p in cfg.get("exports_periodiques", []):
        if p["source"] == "exports_state":
            age = (etat.get(p["ecran"]) or {}).get("age_h")
            age = None if age in (None, "") else float(age)
        else:
            age = None if page is None else (maintenant - page).total_seconds() / 3600
        if age is not None and age <= p["perime_h"]:
            continue
        quoi = "jamais exporté" if age is None else f"export de {int(age)} h"
        res.append({"id": f"export-{p['ecran']}", "type": "export_periodique", "evenement": p["ecran"], "ecran": p["ecran"], "etat": None,
                    "prochain": "export_periodique", "rates": [], "echeance": None, "consigne": f"exporte {p['libelle']} — {quoi}", "age_h": None,
                    "priorite": 2, "action": True, "defauts": []})
    return res


# ---- Phase A (17/11) : offres et ventes du jour, seuils lus dans la section `offres` du yaml -------------------------------

MARCHE = "Marché (enchères)"


def charger_offres(jeu: str = "basketvibe", chemin=None) -> dict:
    """Section `offres` de docs/attentes/jeux/<jeu>.yaml (seuils de l'utilisateur) et `domaines.transferts.minimum_effectif`."""
    import yaml
    y = yaml.safe_load(Path(chemin or CONFIG / f"{jeu}.yaml").read_text(encoding="utf-8"))
    return dict(y["offres"], minimum_effectif=y["domaines"]["transferts"]["minimum_effectif"])


def charger_personnel(jeu: str = "basketvibe", chemin=None) -> dict:
    """Section `personnel_propose` du yaml (règle proposée, à valider) ; {} si absente."""
    import yaml
    return yaml.safe_load(Path(chemin or CONFIG / f"{jeu}.yaml").read_text(encoding="utf-8")).get("personnel_propose") or {}


def texte_personnel(p: dict, actuel=()) -> str:
    """« proposition de règle Personnel : … à valider » (jamais une action) ; `actuel` = lignes de gold.bv_personnel_status."""
    if not p.get("roles"):
        return "règle de personnel non tranchée, à valider"
    emb = {forme_role(r["role"]): r for r in actuel}
    parts = []
    for r in p["roles"]:
        a = emb.get(forme_role(r["role"]))
        parts.append(f"{r['role']} {r['garder']}" + (f" (aujourd'hui {a['hired']}/{a['slots']})" if a else "") + f" : {r['raison']}")
    cout = sum(int(r["garder"]) * int(r["cout_unitaire"]) for r in p["roles"])
    return (f"proposition de règle Personnel : {' ; '.join(parts)} ; coût {_m(cout)} par semaine (plafond {_m(p['plafond_semaine'])}) "
            f"— à valider")


def forme_role(x) -> str:
    import unicodedata
    return unicodedata.normalize("NFKD", str(x)).encode("ascii", "ignore").decode().lower().strip()


def requete_rotation(n: int) -> str:
    """Minutes de chaque joueur de l'effectif sur les `n` derniers matchs de ligue (0 s'il n'a pas joué) : moyenne et matchs joués."""
    n = int(n)
    return ("select r.player_id, r.name, r.position, r.ps, round(coalesce(sum(l.min), 0)::numeric / " + str(n) + ", 1) as min_moy, "
            "count(l.fixture_id) filter (where l.min > 0) as matchs_joues from gold.bv_roster_now r "
            "left join gold.bv_match_player_lines l on l.player_id = r.player_id and l.fixture_id in ("
            "select fixture_id from (select distinct fixture_id, match_day from gold.bv_match_player_lines where competition = 'league') x "
            "order by match_day desc limit " + str(n) + ") group by r.player_id, r.name, r.position, r.ps")


def _f(v):
    return None if v in (None, "") else float(v)


def offres_du_jour(donnees, o, capacite, maintenant=None) -> dict:
    """{"inconnu": texte ou None, "offres": [...]} : annonces actives du Marché de type « amélioration » (note au poste > celle de
    notre joueur utilisé le plus faible à ce poste, prix ≤ médiane de la case, prix ≤ capacité) ou « revente » (case ≥ case_min_ventes
    ventes, prix ≤ p25, médiane ≥ revente_marge × prix), triées par gain attendu (médiane − prix). Marché périmé : « inconnu »."""
    import aujourdhui as auj
    import que_faire_blocs as qfb
    perime = auj.inconnu_si_perime(donnees, MARCHE, maintenant)
    if perime is not None:
        return {"inconnu": perime, "offres": []}
    cases = qfb._cases(donnees)
    faibles = {}
    for r in _rows(donnees, "rotation"):
        if int(float(r["matchs_joues"] or 0)) > 0 and r.get("ps") is not None:
            if r["position"] not in faibles or float(r["ps"]) < float(faibles[r["position"]]["ps"]):
                faibles[r["position"]] = r
    vues, res = set(), []
    for r in _rows(donnees, "annonces_actives"):
        if r["auction_id"] in vues or None in (_f(r.get("price_now")), _f(r.get("ps")), _f(r.get("age"))):
            continue
        vues.add(r["auction_id"])
        case = cases.get((qfb.palier_note(r["ps"]), auj.tranche_age(r["age"])))
        if case is None or int(float(case["n"])) < int(o["case_min_ventes"]):
            continue
        prix, med, p25 = float(r["price_now"]), float(case["median"]), float(case["p25"])
        f = faibles.get(r["position"])
        base = {"nom": r["name"], "poste": r["position"], "age": int(float(r["age"])), "note": float(r["ps"]), "prix": prix, "mediane": med,
                "p25": p25, "n_case": int(float(case["n"])), "fin": _dt(r.get("ends_paris")), "gain": med - prix}
        if f is not None and float(r["ps"]) > float(f["ps"]) and prix <= med and capacite is not None and prix <= float(capacite):
            res.append(dict(base, type="amélioration", faible=f["name"], faible_note=float(f["ps"]), capacite=float(capacite)))
        elif prix <= p25 and med >= float(o["revente_marge"]) * prix:
            res.append(dict(base, type="revente"))
    return {"inconnu": None, "offres": sorted(res, key=lambda x: -x["gain"])}


def ventes_du_jour(donnees, o, tolerance, police="") -> list:
    """Joueurs à vendre pour profit : hors rotation (moyenne ≤ minutes_hors_rotation sur les matchs_rotation derniers matchs de
    ligue), écart de force avec son remplaçant ≤ tolérance du bloc 4, prix attendu = médiane de sa case (case ≥ case_min_ventes
    ventes) ; prix payé connu (gold.bv_transfer_history, bought_by_me) : profit ≥ vente_marge_profit, sinon « prix d'achat
    inconnu, profit non calculé » et la vente reste proposée ; jamais « ne pas vendre <nom> » de la police du jour, jamais déjà en vente ; l'effectif reste
    ≥ minimum_effectif. Triés par prix attendu décroissant."""
    import aujourdhui as auj
    import que_faire_blocs as qfb
    if tolerance is None:
        return []
    cases = qfb._cases(donnees)
    rot = {str(r["player_id"]): r for r in _rows(donnees, "rotation")}
    rempl = {str(r["player_id"]): r for r in _rows(donnees, "gold.bv_sell_replacement")}
    joueurs = _rows(donnees, "vendre")
    achats = {str(r["player_id"]): float(r["fee"]) for r in _rows(donnees, "prix_achat") if _f(r.get("fee")) and float(r["fee"]) > 0}
    res = []
    for j in joueurs:
        r, m = rempl.get(str(j["player_id"]), {}), rot.get(str(j["player_id"]))
        if auj.vrai(j.get("on_transfer_list")) or m is None or float(m["min_moy"]) > float(o["minutes_hors_rotation"]):
            continue
        if r.get("gap") is None or float(r["gap"]) > float(tolerance):
            continue
        if f"ne pas vendre {str(j['name']).lower()}" in str(police).lower():
            continue
        case = cases.get((qfb.palier_note(j["ps"]), auj.tranche_age(j["age"])))
        if case is None or int(float(case["n"])) < int(o["case_min_ventes"]):
            continue
        prix = float(case["median"])  # prix attendu = médiane de la case
        paye = achats.get(str(j["player_id"]))
        profit = None if paye is None else (prix - paye) / paye
        if profit is not None and profit < float(o["vente_marge_profit"]):
            continue
        res.append({"type": "vente", "nom": j["name"], "poste": j["position"], "age": int(float(j["age"])), "note": float(j["ps"]),
                    "prix": prix, "mediane": prix, "n_case": int(float(case["n"])), "min_moy": float(m["min_moy"]),
                    "remplacant": r.get("replacement_name"), "ecart": float(r["gap"]), "tolerance": float(tolerance), "gain": prix,
                    "prix_achat": paye, "profit": profit})
    places = max(0, len(joueurs) - int(o["minimum_effectif"]))
    return sorted(res, key=lambda x: -x["gain"])[:places]


def _m(x) -> str:
    return f"{x:,.0f}".replace(",", " ")


def texte_transfert(x, o) -> str:
    """Ligne d'une offre ou d'une vente : nom, poste, âge, note, prix, médiane de la case, type, fin, seuils du yaml, règle 2, police."""
    from police import SEUIL_GROS_MONTANT
    qui = f"{x['nom']} ({x['poste']}, {x['age']} ans, note {_virg(x['note'])})"
    if x["type"] == "vente":
        t = (f"vente : {qui}, prix attendu {_m(x['prix'])}, médiane de la case {_m(x['mediane'])} ({x['n_case']} ventes ≥ {o['case_min_ventes']}) ; "
             f"{_virg(x['min_moy'])} min en moyenne sur {o['matchs_rotation']} matchs de ligue (≤ {_virg(o['minutes_hors_rotation'])}), "
             f"écart avec {x['remplacant']} {_virg(x['ecart'])} (tolérance {_virg(x['tolerance'])}) ; "
             + ("prix d'achat inconnu, profit non calculé" if x.get("prix_achat") is None else
                f"profit {x['profit'] * 100:.0f} % sur le prix payé {_m(x['prix_achat'])} (≥ {o['vente_marge_profit'] * 100:.0f} %)")
             + " ; fin : annonce à créer")
    else:
        if x["type"] == "amélioration":
            seuil = (f"note > {_virg(x['faible_note'])} de {x['faible']} (notre plus faible utilisé au poste sur {o['matchs_rotation']} matchs "
                     f"de ligue), prix ≤ médiane, budget {_m(x['capacite'])}")
        else:
            seuil = f"case de {x['n_case']} ventes (≥ {o['case_min_ventes']}), prix ≤ p25 {_m(x['p25'])}, médiane ≥ {_virg(o['revente_marge'])} × prix"
        fin = f"{x['fin']:%d/%m %H:%M}" if x.get("fin") else "inconnue"
        t = f"{x['type']} : {qui} à {_m(x['prix'])}, médiane de la case {_m(x['mediane'])} ; {seuil} ; fin {fin}"
    t += " — proposition seulement (règle 2)"
    if x["prix"] > SEUIL_GROS_MONTANT["basketvibe"]:
        t += " — police d'abord : dossier.py puis agent police"
    return t


def lignes_transferts(donnees, capacite, tolerance, police="", maintenant=None, o=None) -> list:
    """Lignes « Transferts » de l'état par événement : `max_offres` offres et `max_ventes` ventes au plus, triées par gain attendu ;
    Marché périmé : une ligne « inconnu » à la place des offres. Le bloc 4 lit ces mêmes lignes."""
    o = o or charger_offres()
    of = offres_du_jour(donnees, o, capacite, maintenant)
    choix = of["offres"][:int(o["max_offres"])] + ventes_du_jour(donnees, o, tolerance, police)[:int(o["max_ventes"])]
    ligne = lambda i, prochain, consigne: {"id": i, "type": "transfert", "evenement": "transferts", "etat": None, "prochain": prochain,
                                           "rates": [], "echeance": None, "consigne": consigne, "age_h": None, "priorite": 2,
                                           "action": True, "defauts": []}
    res = [ligne("offres-inconnu", "offre", f"offres du Marché : {of['inconnu']}")] if of["inconnu"] else []
    return res + [ligne(f"{x['type']}-{x['nom']}", x["type"] if x["type"] == "vente" else "offre", texte_transfert(x, o))
                  for x in sorted(choix, key=lambda x: -x["gain"])]


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
             "consigne": " ; ".join(x for x in (l.get("consigne"), r.get("consigne", "").format_map(champs)) if x),
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
REQUETES["rotation"] = requete_rotation(charger_offres()["matchs_rotation"])  # phase A : N lu dans le yaml
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


def _tests_academie(donnees):
    """Nombre de prospects du rapport au verdict « tester » (gold.bv_academy_prospects) ; None si une taille ou un poste manque."""
    import aujourdhui as auj
    pros = _rows(donnees, "prospects")
    if not pros or any(p.get("position") not in auj.PLAGE_TAILLE or p.get("height_cm") in (None, "") for p in pros):
        return None
    return sum(auj.verdict_prospect(p)[0] == "tester" for p in pros)


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
        evs.append(appliquer_controles(ev, {"blessures": blessures.get(r["fixture_id"], {}), "fatigue": fatigue, "seuil_fatigue": seuil}, cfg))
    rapport = max((_dt(r["rapport_paris"]) for r in _rows(donnees, "prospects")), default=None)
    page_entr = next((_dt(r["dernier_paris"]) for r in _rows(donnees, "gold.bv_exports_state") if r["ecran"] == "Entraînement"), None)
    for t, c in cfg["evenements"].items():
        if t == "enchere":
            continue
        for q in occurrences(c["quand"], maintenant):
            ev = {"type": t, "id": f"{t}-{q:%Y-%m-%d}", "quand": q, "maj_at": None}
            if t == "academie":
                ev.update(rapport_at=rapport, decide=_cle(S, "academie", q.date()), tests=_tests_academie(donnees))
            else:
                ev.update(page_at=page_entr, saisi=_cle(S, "entrainement", q.date()), fiche=fiche_entrainement(base, jour, q.date()))
            evs.append(ev)
    vendus = {str(r["name"]).lower() for r in _rows(donnees, "transferts_recents")}
    for c in S.get("cibles", []):
        evs.append({"type": "enchere", "id": f"enchere-{c['nom']}", "nom": c["nom"], "fin": c.get("fin"),
                    "gros": c.get("max") is not None and float(c["max"]) > SEUIL_GROS_MONTANT["basketvibe"],
                    "police": c["nom"].lower() in str(S.get("police", "")).lower(), "resultat": c["nom"].lower() in vendus, "maj_at": None})
    return evs
