"""Tests de pipelines/etat_jour.py (P2 du plan v4 du 13/11) : entrées synthétiques, sans réseau ni base.
Lancer : python -I pipelines/test_etat_jour.py   (code 1 si un cas se trompe)"""
import datetime as dt
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import etat_jour as ej  # noqa: E402

J = dt.date(2026, 11, 18)
MAINT = dt.datetime(2026, 11, 17, 10, 0)
CFG = ej.charger_config()


def match(**kw):
    ev = {"type": "match", "genre": "ligue", "id": "m1", "adversaire": "Adv A", "jour": J,
          "coup_envoi": dt.datetime(2026, 11, 18, 20, 0), "verrou": dt.datetime(2026, 11, 18, 19, 45),
          "joue": False, "resultat": None, "apercu_at": None, "fiche": None, "ecran": None, "page_at": None,
          "analyse": False, "juge": False, "juge_requis": False, "maj_at": None}
    ev.update(kw)
    return ev


FICHE = {"ok": True, "adversaire": "Adv A", "fichier": "briefs/x.md"}
ECRAN = {"sauvegarde": True}
T_APERCU = dt.datetime(2026, 11, 17, 9, 0)


def prochain(ev, maintenant=MAINT, cfg=CFG):
    return ej.etat_evenement(ev, cfg, maintenant)["prochain"]


def cas_config():
    yield "config : lue dans docs/attentes/jeux/basketvibe.yaml", CFG["horizon_h"] == 48 and CFG["donnee_perimee_h"] == 24 \
        and CFG["minutes_max"] == 36
    yield "config : états de la ligue et de la coupe, dans l'ordre", \
        CFG["matchs"]["ligue"]["etats"] == ["calendrier", "apercu", "fiche", "ecran", "verrou", "joue", "analyse", "juge"] \
        and CFG["matchs"]["coupe"]["etats"] == CFG["matchs"]["ligue"]["etats"]
    yield "config : l'amical n'a ni aperçu ni analyse", "apercu" not in CFG["matchs"]["amical"]["etats"] \
        and "analyse" not in CFG["matchs"]["amical"]["etats"]
    yield "config : événements hors match", set(CFG["evenements"]) == {"academie", "entrainement", "enchere"}


def cas_etats_ligue():
    yield "ligue : calendrier inconnu → calendrier", prochain(match(jour=None, coup_envoi=None, verrou=None)) == "calendrier"
    yield "ligue : calendrier connu, aperçu absent → apercu", prochain(match()) == "apercu"
    yield "ligue : aperçu exporté, pas de fiche → fiche", prochain(match(apercu_at=T_APERCU)) == "fiche"
    yield "ligue : fiche non valide (ok faux) → fiche", prochain(match(apercu_at=T_APERCU, fiche=dict(FICHE, ok=False))) == "fiche"
    yield "ligue : fiche valide, écran non sauvegardé → ecran", prochain(match(apercu_at=T_APERCU, fiche=FICHE, ecran={"sauvegarde": False})) == "ecran"
    yield "ligue : fiche valide, écran absent → ecran", prochain(match(apercu_at=T_APERCU, fiche=FICHE)) == "ecran"
    pret = match(apercu_at=T_APERCU, fiche=FICHE, ecran=ECRAN)
    yield "ligue : écran sauvegardé, verrou à venir → verrou", prochain(pret) == "verrou"
    yield "ligue : verrou passé, match pas joué → joue", prochain(pret, dt.datetime(2026, 11, 18, 19, 50)) == "joue"
    yield "ligue : verrou passé sans écran : l'état raté ne bloque pas, → joue", \
        prochain(match(apercu_at=T_APERCU, fiche=FICHE), dt.datetime(2026, 11, 18, 19, 50)) == "joue"
    joue = dict(pret, joue=True)
    yield "ligue : joué, page non exportée → joue", prochain(joue, dt.datetime(2026, 11, 18, 21, 0)) == "joue"
    exporte = dict(joue, page_at=dt.datetime(2026, 11, 18, 20, 55), resultat="L")
    yield "ligue : défaite exportée, pas analysée → analyse", prochain(exporte, dt.datetime(2026, 11, 18, 21, 0)) == "analyse"
    yield "ligue : victoire exportée : aucune analyse requise → plus rien", \
        prochain(dict(exporte, resultat="W"), dt.datetime(2026, 11, 18, 21, 0)) is None
    yield "ligue : défaite analysée, aucun jugement requis → plus rien", \
        prochain(dict(exporte, analyse=True), dt.datetime(2026, 11, 18, 21, 0)) is None
    yield "ligue : défaite analysée, jugement requis → juge", \
        prochain(dict(exporte, analyse=True, juge_requis=True), dt.datetime(2026, 11, 18, 21, 0)) == "juge"
    yield "ligue : jugement fait → plus rien", \
        prochain(dict(exporte, analyse=True, juge_requis=True, juge=True), dt.datetime(2026, 11, 18, 21, 0)) is None
    l = ej.etat_evenement(pret, CFG, MAINT)
    yield "ligue : le dernier état atteint est nommé", l["etat"] == "ecran"
    c = match(genre="coupe")
    yield "coupe : mêmes états que la ligue", prochain(c) == "apercu" and prochain(dict(c, apercu_at=T_APERCU)) == "fiche"


def cas_etats_amical():
    am = match(genre="amical", adversaire="Adv B", coup_envoi=dt.datetime(2026, 11, 18, 8, 0), verrou=dt.datetime(2026, 11, 18, 7, 45))
    yield "amical : jamais d'aperçu, → fiche", prochain(am) == "fiche"
    yield "amical : fiche valide → ecran", prochain(dict(am, fiche=FICHE)) == "ecran"
    yield "amical : écran sauvegardé → verrou", prochain(dict(am, fiche=FICHE, ecran=ECRAN)) == "verrou"
    for etat in ({}, {"fiche": FICHE}, {"fiche": FICHE, "ecran": ECRAN}):
        t = ej.etat_evenement(dict(am, **etat), CFG, MAINT)["consigne"].lower()
        yield f"amical avant le match ({sorted(etat)}) : ni aperçu ni export dans la consigne", "aperçu" not in t and "export" not in t
    jo = dict(am, fiche=FICHE, ecran=ECRAN, joue=True)
    apres = ej.etat_evenement(jo, CFG, dt.datetime(2026, 11, 18, 9, 0))
    yield "amical joué : la page du match est à exporter", apres["prochain"] == "joue" and "export" in apres["consigne"].lower()
    yield "amical joué et exporté, même perdu : plus rien (jamais d'analyse)", \
        prochain(dict(jo, page_at=dt.datetime(2026, 11, 18, 9, 5), resultat="L"), dt.datetime(2026, 11, 18, 9, 10)) is None


def cas_ligne():
    ev = match(apercu_at=T_APERCU)
    l = ej.etat_evenement(ev, CFG, MAINT)
    yield "ligne : consigne exacte, adversaire et date nommés", l["prochain"] == "fiche" and "Adv A" in l["consigne"] and "18/11" in l["consigne"]
    yield "ligne : échéance = verrou du match", l["echeance"] == dt.datetime(2026, 11, 18, 19, 45)
    yield "ligne : une action à faire", l["action"] is True
    yield "ligne : événement nommé (genre, adversaire, date)", l["evenement"] == "ligue contre Adv A, 18/11"
    fin = ej.etat_evenement(match(apercu_at=T_APERCU, fiche=FICHE, ecran=ECRAN, joue=True, page_at=dt.datetime(2026, 11, 18, 21, 0),
                                  resultat="W"), CFG, dt.datetime(2026, 11, 18, 22, 0))
    yield "ligne : complet → une ligne sans action", fin["prochain"] is None and fin["action"] is False
    frais = ej.etat_evenement(match(maj_at=dt.datetime(2026, 11, 17, 8, 0)), CFG, MAINT)
    yield "ligne : âge des données en heures", frais["age_h"] == 2.0
    vieux = ej.etat_evenement(match(maj_at=dt.datetime(2026, 11, 16, 8, 0)), CFG, MAINT)
    yield "ligne : donnée de plus de 24 h = priorité dégradée d'un cran", vieux["age_h"] == 26.0 and vieux["priorite"] == frais["priorite"] + 1
    yield "ligne : priorité jamais au-delà de 3", ej.etat_evenement(match(maj_at=dt.datetime(2026, 11, 10, 8, 0), jour=dt.date(2026, 11, 19),
                                                                           coup_envoi=dt.datetime(2026, 11, 19, 20, 0), verrou=dt.datetime(2026, 11, 19, 19, 45)),
                                                                     CFG, MAINT)["priorite"] <= 3
    proche = ej.etat_evenement(match(), CFG, dt.datetime(2026, 11, 18, 12, 0))
    yield "ligne : échéance dans moins de 24 h = priorité 1", proche["priorite"] == 1


def cas_hors_match():
    jeu = dt.datetime(2026, 11, 19, 9, 0)
    ac = {"type": "academie", "quand": jeu, "rapport_at": None, "decide": False, "maj_at": None}
    yield "académie : avant jeudi 09:00 → rapport_attendu", ej.etat_evenement(ac, CFG, MAINT)["prochain"] == "rapport_attendu"
    yield "académie : après 09:00, rapport absent → rapport_exporte", ej.etat_evenement(ac, CFG, dt.datetime(2026, 11, 19, 10, 0))["prochain"] == "rapport_exporte"
    ok = dict(ac, rapport_at=dt.datetime(2026, 11, 19, 9, 0, 1))
    l = ej.etat_evenement(ok, CFG, dt.datetime(2026, 11, 19, 10, 0))
    yield "académie : rapport en base, non décidé → decide", l["prochain"] == "decide" and "tester, signer ou ignorer" in l["consigne"]
    yield "académie : décidé → plus rien", ej.etat_evenement(dict(ok, decide=True), CFG, dt.datetime(2026, 11, 19, 10, 0))["prochain"] is None
    en = {"type": "entrainement", "quand": dt.datetime(2026, 11, 22, 4, 0), "page_at": None, "saisi": False, "maj_at": None}
    yield "entraînement : avant dimanche 04:00 → traitement_attendu", ej.etat_evenement(en, CFG, dt.datetime(2026, 11, 21, 12, 0))["prochain"] == "traitement_attendu"
    yield "entraînement : traité, page non exportée → page_exportee", ej.etat_evenement(en, CFG, dt.datetime(2026, 11, 22, 9, 0))["prochain"] == "page_exportee"
    yield "entraînement : page exportée, non saisi → saisi", \
        ej.etat_evenement(dict(en, page_at=dt.datetime(2026, 11, 22, 8, 0)), CFG, dt.datetime(2026, 11, 22, 9, 0))["prochain"] == "saisi"
    ench = {"type": "enchere", "nom": "Cible A", "fin": dt.datetime(2026, 11, 18, 4, 0), "gros": True, "police": False, "resultat": False, "maj_at": None}
    l = ej.etat_evenement(ench, CFG, MAINT)
    yield "enchère de gros montant sans police → police", l["prochain"] == "police" and "police" in l["consigne"] and "Cible A" in l["consigne"]
    yield "enchère de petit montant : la police n'est pas requise → fin", \
        ej.etat_evenement(dict(ench, gros=False), CFG, MAINT)["prochain"] == "fin"
    yield "enchère finie, résultat non lu → resultat", \
        ej.etat_evenement(dict(ench, police=True), CFG, dt.datetime(2026, 11, 18, 5, 0))["prochain"] == "resultat"
    yield "enchère : résultat lu → plus rien", \
        ej.etat_evenement(dict(ench, police=True, resultat=True), CFG, dt.datetime(2026, 11, 18, 5, 0))["prochain"] is None


def cas_horizon_et_completude():
    dans = match(id="a")
    loin = match(id="b", jour=dt.date(2026, 11, 21), coup_envoi=dt.datetime(2026, 11, 21, 20, 0), verrou=dt.datetime(2026, 11, 21, 19, 45))
    jouee = match(id="c", jour=dt.date(2026, 11, 14), coup_envoi=dt.datetime(2026, 11, 14, 20, 0), verrou=dt.datetime(2026, 11, 14, 19, 45),
                  joue=True, page_at=dt.datetime(2026, 11, 14, 21, 0), resultat="L")
    vieille = match(id="d", jour=dt.date(2026, 11, 2), coup_envoi=dt.datetime(2026, 11, 2, 20, 0), verrou=dt.datetime(2026, 11, 2, 19, 45),
                    joue=True, page_at=dt.datetime(2026, 11, 2, 21, 0), resultat="L")
    gagnee = match(id="e", jour=dt.date(2026, 11, 14), coup_envoi=dt.datetime(2026, 11, 14, 20, 0), verrou=dt.datetime(2026, 11, 14, 19, 45), joue=True, page_at=dt.datetime(2026, 11, 14, 21, 0), resultat="W")
    ac = {"type": "academie", "id": "ac", "quand": dt.datetime(2026, 11, 19, 9, 0), "rapport_at": None, "decide": False, "maj_at": None}
    en = {"type": "entrainement", "id": "en", "quand": dt.datetime(2026, 11, 22, 4, 0), "page_at": None, "saisi": False, "maj_at": None}
    ench = {"type": "enchere", "id": "ench", "nom": "Cible A", "fin": dt.datetime(2026, 11, 18, 4, 0), "gros": False, "police": True,
            "resultat": False, "maj_at": None}
    tous = [dans, loin, jouee, vieille, gagnee, ac, en, ench]
    ls = ej.lignes(tous, CFG, MAINT)
    ids = [l["id"] for l in ls]
    yield "horizon : le match à 34 h, l'académie à 47 h, l'enchère à 18 h sont dans les 48 h", {"a", "ac", "ench"} <= set(ids)
    yield "horizon : l'entraînement (dimanche) et le match à 4 jours sont hors des 48 h", "en" not in ids and "b" not in ids
    yield "horizon : un match joué non analysé a sa ligne, à toute date de la fenêtre de 7 jours", "c" in ids
    yield "horizon : un match joué il y a plus de 7 jours n'a plus de ligne", "d" not in ids
    yield "horizon : un match joué gagné (rien à analyser) a une ligne sans action ou aucune", \
        all(not l["action"] for l in ls if l["id"] == "e")
    yield "complétude : une seule ligne par événement", len(ids) == len(set(ids))
    yield "complétude : aucun événement des 48 h sans ligne", ej.sans_ligne(tous, ls, CFG, MAINT) == []
    yield "complétude : détecte un événement oublié", ej.sans_ligne(tous, [l for l in ls if l["id"] != "a"], CFG, MAINT) == [dans]


def cas_exports():
    """P2.2 : un export n'est demandé que s'il débloque une transition, nomme l'événement et disparaît dès que la base voit la capture."""
    ex = lambda evs, m=MAINT: ej.exports(ej.lignes(evs, CFG, m))
    e = ex([match(id="a")])
    yield "export : l'aperçu manquant est demandé, avec adversaire et date", len(e) == 1 and "aperçu" in e[0]["consigne"] \
        and "Adv A" in e[0]["consigne"] and "18/11" in e[0]["consigne"]
    yield "export : l'aperçu capturé disparaît", ex([match(id="a", apercu_at=T_APERCU)]) == []
    yield "export : ni fiche ni écran ne sont des exports", ex([match(id="a", apercu_at=T_APERCU, fiche=FICHE)]) == []
    pret = match(id="a", apercu_at=T_APERCU, fiche=FICHE, ecran=ECRAN)
    yield "export : avant la fin du match, aucune page à exporter", ex([pret], dt.datetime(2026, 11, 18, 19, 50)) == []
    joue = dict(pret, joue=True)
    e = ex([joue], dt.datetime(2026, 11, 18, 21, 0))
    yield "export : match joué, page demandée", len(e) == 1 and "page du match" in e[0]["consigne"] and "Adv A" in e[0]["consigne"]
    yield "export : page capturée, disparaît", ex([dict(joue, page_at=dt.datetime(2026, 11, 18, 20, 55))], dt.datetime(2026, 11, 18, 21, 0)) == []
    am = match(id="b", genre="amical", coup_envoi=dt.datetime(2026, 11, 18, 8, 0), verrou=dt.datetime(2026, 11, 18, 7, 45))
    yield "export : amical avant le match, jamais d'export", all(ex([dict(am, **k)]) == [] for k in ({}, {"fiche": FICHE}, {"fiche": FICHE, "ecran": ECRAN}))
    ac = {"type": "academie", "id": "ac", "quand": dt.datetime(2026, 11, 19, 9, 0), "rapport_at": None, "decide": False, "maj_at": None}
    yield "export : académie avant 09:00, rien", ex([ac]) == []
    e = ex([ac], dt.datetime(2026, 11, 19, 10, 0))
    yield "export : académie après 09:00, page Académie demandée avec la date du rapport", len(e) == 1 and "Académie" in e[0]["consigne"] and "19/11" in e[0]["consigne"]
    yield "export : rapport capturé, disparaît", ex([dict(ac, rapport_at=dt.datetime(2026, 11, 19, 9, 1))], dt.datetime(2026, 11, 19, 10, 0)) == []
    yield "export : chaque export porte l'état qu'il débloque", all(x["prochain"] in ej.ETATS_EXPORT for x in ex([match(id="a"), ac], dt.datetime(2026, 11, 19, 10, 0)))


def joueur(nom, minutes, agress=3, off=3, role=3, tir=3):
    return {"nom": nom, "minutes": minutes, "agress": agress, "off": off, "role": role, "tir": tir}


def cas_controles():
    """P2.3 : contrôles fiche contre réalité ; un défaut = ❌ + correction exacte."""
    fj = [joueur("Alpha", 30), joueur("Beta", 24), joueur("Gamma", 0)]
    d = ej.controle_blessures(fj, {"Joueur Alpha": dt.date(2026, 11, 19)}, J)
    yield "blessure : joueur de la fiche blessé jusqu'après le match → ❌ + correction", len(d) == 1 and d[0]["texte"].startswith("❌") \
        and "Alpha" in d[0]["texte"] and "19/11" in d[0]["texte"] and "Alpha à 0 min" in d[0]["correction"]
    yield "blessure : retour le jour du match = disponible", ej.controle_blessures(fj, {"Joueur Alpha": J}, J) == []
    yield "blessure : joueur à 0 min dans la fiche, blessé : pas de défaut", ej.controle_blessures(fj, {"Joueur Gamma": dt.date(2026, 11, 30)}, J) == []
    yield "blessure : homonyme de prénom seul non confondu", ej.controle_blessures(fj, {"Alphabet Zed": dt.date(2026, 11, 30)}, J) == []
    d = ej.controle_minutes([joueur("Alpha", 40), joueur("Beta", 36)], 36)
    yield "minutes : plus de 36 → ❌, 36 accepté", len(d) == 1 and "Alpha" in d[0]["texte"] and "40" in d[0]["texte"] and "36 min" in d[0]["correction"]
    d = ej.controle_fatigue(fj, {"Joueur Beta": 23.5, "Joueur Gamma": 40.0}, 20)
    yield "fatigue : joueur qui joue au-dessus du seuil → ❌ ; au repos : rien", len(d) == 1 and "Beta" in d[0]["texte"] and "23,5" in d[0]["texte"] \
        and "20" in d[0]["texte"]
    ecran = [joueur("Alpha", 24), joueur("Beta", 24, agress=4), joueur("Gamma", 0)]
    d = ej.controle_ecran(fj, ecran)
    yield "écran contre fiche : chaque écart nommé, avec la valeur de la fiche", len(d) == 2 \
        and any("Alpha" in x["texte"] and "minutes 24" in x["texte"] and "30" in x["correction"] for x in d) \
        and any("Beta" in x["texte"] and "agressivité 4" in x["texte"] for x in d)
    yield "écran contre fiche : identique → aucun défaut", ej.controle_ecran(fj, [dict(j) for j in fj]) == []
    yield "écran contre fiche : joueur de la fiche absent de l'écran → ❌", \
        any("Beta" in x["texte"] and "absent" in x["texte"] for x in ej.controle_ecran(fj, [joueur("Alpha", 30), joueur("Gamma", 0)])) \
        and not any("Gamma" in x["texte"] for x in ej.controle_ecran(fj, [joueur("Alpha", 30), joueur("Beta", 24)]))
    d = ej.controle_e1([joueur("Alpha", 20, agress=3), joueur("Beta", 20, agress=4), joueur("Gamma", 0, agress=1)], 3)
    yield "E1 amical : agressivité non uniforme → ❌, correction à la valeur du test", len(d) == 1 and "agressivité 3" in d[0]["correction"] \
        and "Beta" in d[0]["texte"]
    yield "E1 amical : uniforme (les joueurs à 0 min ne comptent pas) → rien", \
        ej.controle_e1([joueur("Alpha", 20, agress=3), joueur("Gamma", 0, agress=1)], 3) == []
    d = ej.controle_adversaire("Adv A", "Adv C")
    yield "adversaire changé depuis la fiche → ❌ + relance de la fiche", len(d) == 1 and "Adv A" in d[0]["texte"] and "Adv C" in d[0]["texte"] \
        and "agent tactique" in d[0]["correction"]
    yield "adversaire identique → rien", ej.controle_adversaire("Adv A", "Adv A") == []
    # branchement : un défaut de fiche empêche l'état « fiche valide », un écart d'écran l'état « écran conforme »
    reel = {"blessures": {"Joueur Alpha": dt.date(2026, 11, 20)}, "fatigue": {}, "seuil_fatigue": 20}
    ev = ej.appliquer_controles(match(apercu_at=T_APERCU, fiche=dict(FICHE, joueurs=fj), ecran={"sauvegarde": True, "joueurs": fj}), reel, CFG)
    l = ej.etat_evenement(ev, CFG, MAINT)
    yield "branchement : fiche avec un blessé → prochaine transition « fiche », consigne = la correction", \
        l["prochain"] == "fiche" and "Alpha à 0 min" in l["consigne"] and any(x["texte"].startswith("❌") for x in l["defauts"])
    ev = ej.appliquer_controles(match(apercu_at=T_APERCU, fiche=dict(FICHE, joueurs=fj), ecran={"sauvegarde": True, "joueurs": ecran}),
                                {"blessures": {}, "fatigue": {}, "seuil_fatigue": 20}, CFG)
    l = ej.etat_evenement(ev, CFG, MAINT)
    yield "branchement : écran différent de la fiche → « ecran », consigne = corrections", l["prochain"] == "ecran" and "30" in l["consigne"]
    am = match(genre="amical", coup_envoi=dt.datetime(2026, 11, 18, 8, 0), verrou=dt.datetime(2026, 11, 18, 7, 45),
               fiche=dict(FICHE, joueurs=fj, agress_test=3), ecran={"sauvegarde": True, "joueurs": [joueur("Alpha", 30, agress=2), joueur("Beta", 24)]})
    l = ej.etat_evenement(ej.appliquer_controles(am, {"blessures": {}, "fatigue": {}, "seuil_fatigue": 20}, CFG), CFG, MAINT)
    yield "branchement amical : E1 non uniforme à l'écran → « ecran », pas de contrôle écran contre fiche", \
        l["prochain"] == "ecran" and "agressivité 3" in l["consigne"] and not any("minutes" in x["texte"] for x in l["defauts"])
    ok = ej.appliquer_controles(match(apercu_at=T_APERCU, fiche=dict(FICHE, joueurs=fj), ecran={"sauvegarde": True, "joueurs": fj}),
                                {"blessures": {}, "fatigue": {}, "seuil_fatigue": 20}, CFG)
    yield "branchement : aucun défaut → l'écran est conforme (« verrou »)", ej.etat_evenement(ok, CFG, MAINT)["prochain"] == "verrou"
    yield "branchement : adversaire du match différent de celui de la fiche → « fiche »", ej.etat_evenement(
        ej.appliquer_controles(dict(ok, adversaire="Adv C"), {"blessures": {}, "fatigue": {}, "seuil_fatigue": 20}, CFG), CFG, MAINT)["prochain"] == "fiche"


COLS_EM = ["fixture_id", "competition_kind", "day", "opponent", "home", "played", "my_result", "coup_envoi_paris", "verrou_paris",
           "apercu_paris", "page_paris", "sauvegarde", "saisie_export_paris", "joueurs_saisis"]
BRIEF = """# Tactique — Ligue J8 contre Adv A (mer. 18/11 20:00, verrou 19:45)

| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Minutes | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Alpha | PG | PG | — | PG | PG | — | 36 | 3 | 3 | 3 | 3 |
| Beta | SG | SG | SG | — | — | — | 24 (+2) | 2 | 2 | 3 | 3 |
| Gamma | C | — | — | — | — | — | 0 | 1 | 1 | 1 | 1 |

| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Opp Un | PG | 3 | Rim |
"""


def donnees(**plus):
    d = {"etat_match": (COLS_EM, [
            ("f1", "ligue", "2026-11-18", "Adv A", True, False, None, None, None, None, None, None, None, None),
            ("f2", "amical", "2026-11-18", "Adv B", True, False, None, "2026-11-18T08:00:00", "2026-11-18T07:45:00", None, None, None, None, None),
            ("f3", "ligue", "2026-11-16", "Adv C", False, False, None, "2026-11-16T20:00:00", "2026-11-16T19:45:00",
             "2026-11-16T11:02:02", None, False, "2026-11-16T11:02:03", 9),
            ("f4", "ligue", "2026-11-14", "Adv D", False, True, "L", "2026-11-14T20:00:00", "2026-11-14T19:45:00",
             "2026-11-13T10:00:00", "2026-11-16T11:01:38", False, "2026-11-13T10:27:06", 10)]),
         "ecran_joueurs": (["fixture_id", "joueur", "minutes", "off_focus", "role", "tir", "agress"], []),
         "blessures_match": (["player_id", "name", "injury_return_on", "fixture_id", "competition_kind", "day", "indisponible"], []),
         "fatigue_roster": (["name", "fatigue"], []), "seuil_fatigue": (["seuil_bas"], [(20,)]),
         "prospects": (["rapport_paris"], [("2026-11-12T09:00:01",)]),
         "gold.bv_exports_state": (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
                                   [(11, "Entraînement", "x", "2026-11-15T10:00:00", 48, "🟩 à jour")]),
         "a_evaluer": (["n"], [(2,)]), "transferts_recents": (["name"], [])}
    d.update(plus)
    return d


def cas_construire():
    """P2.4 : événements construits depuis la base (gold.bv_etat_match, gold.bv_blessures_match, saisie, fatigue) et les fichiers."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "briefs").mkdir()
        (Path(tmp) / "briefs" / "2026-11-17-tactique.md").write_text(BRIEF, encoding="utf-8")
        S = {"analyste": dt.date(2026, 11, 10), "cles": [], "cibles": [], "police": ""}
        evs = ej.construire(donnees(), S, tmp, dt.date(2026, 11, 17), MAINT, CFG)
        m = {e["id"]: e for e in evs if e["type"] == "match"}
        yield "construire : un événement par match de la vue", set(m) == {"f1", "f2", "f3", "f4"}
        yield "construire : ligue sans heure en base → coup d'envoi et verrou de la config (20:00, 19:45)", \
            m["f1"]["coup_envoi"] == dt.datetime(2026, 11, 18, 20, 0) and m["f1"]["verrou"] == dt.datetime(2026, 11, 18, 19, 45)
        yield "construire : la fiche du match est lue (adversaire, joueurs, minutes)", m["f1"]["fiche"] is not None \
            and m["f1"]["fiche"]["adversaire"] == "Adv A" and [j["minutes"] for j in m["f1"]["fiche"]["joueurs"]] == [36, 24, 0]
        yield "construire : pas de fiche pour un autre adversaire", m["f2"]["fiche"] is None
        yield "construire : page capturée avant le coup d'envoi = pas la page du match", m["f3"]["page_at"] is None
        yield "construire : défaite jouée, analyse du 10/11 antérieure → non analysée", m["f4"]["joue"] and not m["f4"]["analyse"]
        yield "construire : juger seulement le dernier match officiel joué, décisions à mesurer > 0", \
            m["f4"]["juge_requis"] and not m["f4"]["juge"] and not m["f3"]["juge_requis"]
        yield "construire : âge des données = dernière capture du match", m["f3"]["maj_at"] == dt.datetime(2026, 11, 16, 11, 2, 3)
        ls = {l["id"]: l for l in ej.lignes(evs, CFG, MAINT)}
        yield "construire : match passé non marqué joué → exporte sa page", ls["f3"]["prochain"] == "joue" and ls["f3"]["action"] \
            and "exporte la page du match de ligue contre Adv C (16/11)" == ls["f3"]["consigne"]
        yield "construire : défaite non analysée → l'agent analyste", ls["f4"]["prochain"] == "analyse"
        yield "construire : ligue de demain, aperçu absent → aperçu", ls["f1"]["prochain"] == "apercu"
        yield "construire : amical de demain sans fiche → fiche, jamais d'aperçu", ls["f2"]["prochain"] == "fiche"
        ac = [e for e in evs if e["type"] == "academie"]
        yield "construire : académie, le rapport du jeudi 19/11 09:00", any(e["quand"] == dt.datetime(2026, 11, 19, 9, 0) for e in ac)
        en = [e for e in evs if e["type"] == "entrainement"]
        yield "construire : entraînement, traitement du dimanche 04:00 et page lue dans l'état des exports", \
            any(e["quand"] == dt.datetime(2026, 11, 22, 4, 0) for e in en) and all(e["page_at"] == dt.datetime(2026, 11, 15, 10, 0) for e in en)
        blesse = donnees(blessures_match=(["player_id", "name", "injury_return_on", "fixture_id", "competition_kind", "day", "indisponible"],
                                          [("p1", "Prénom Alpha", "2026-11-20", "f1", "ligue", "2026-11-18", True)]))
        l1 = {l["id"]: l for l in ej.lignes(ej.construire(blesse, S, tmp, dt.date(2026, 11, 17), MAINT, CFG), CFG, MAINT)}["f1"]
        yield "construire : blessé à la date du match (par la vue) → ❌ et correction dans la ligne", \
            any("Alpha" in d["texte"] and d["texte"].startswith("❌") for d in l1["defauts"])
        cible = {"nom": "Cible A", "fin": dt.datetime(2026, 11, 18, 4, 0), "max": 300000, "police": False}
        e = [x for x in ej.construire(donnees(), dict(S, cibles=[cible]), tmp, dt.date(2026, 11, 17), MAINT, CFG) if x["type"] == "enchere"]
        yield "construire : enchère décidée au-dessus du seuil → police requise", len(e) == 1 and e[0]["gros"] and not e[0]["police"]
        e = [x for x in ej.construire(donnees(), dict(S, cibles=[cible], police="- décision : acheter cible a"), tmp, dt.date(2026, 11, 17),
                                      MAINT, CFG) if x["type"] == "enchere"]
        yield "construire : police du jour qui nomme la cible → police faite", e[0]["police"]
    yield "requêtes : lecture seule, vues de P2", all(q.lstrip().lower().startswith("select") for q in ej.REQUETES.values()) \
        and "gold.bv_etat_match" in ej.REQUETES["etat_match"] and "gold.bv_blessures_match" in ej.REQUETES["blessures_match"]


CAS = [cas_config, cas_etats_ligue, cas_etats_amical, cas_ligne, cas_hors_match, cas_horizon_et_completude, cas_exports, cas_controles,
       cas_construire]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
