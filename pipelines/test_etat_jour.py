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
    yield "amical : libellé « match amical » lu dans la config, jamais « match de amical »", \
        "match amical contre Adv B" in ej.etat_evenement(am, CFG, MAINT)["consigne"] and "de amical" not in ej.etat_evenement(am, CFG, MAINT)["consigne"]
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
    yield "académie : rapport en base, tests inconnus → teste (18/11)", l["prochain"] == "teste" and "tester, signer ou ignorer" in l["consigne"]
    yield "académie : décidé → plus rien", ej.etat_evenement(dict(ok, decide=True, tests=0), CFG, dt.datetime(2026, 11, 19, 10, 0))["prochain"] is None
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


INSTANTANE = ICI / "jeu_essai" / "2026-11-17" / "etat_match.json"


def a_la_date(maintenant):
    """gold.bv_etat_match telle que la base la voyait à `maintenant`, reconstruite depuis l'extrait du 17/11 : fenêtre J-7 à J+3,
    captures postérieures effacées, match « joué » seulement si sa fin (coup d'envoi + 2 h) est passée."""
    import json
    snap = json.loads(INSTANTANE.read_text(encoding="utf-8"))
    cols, res = snap["colonnes"], []
    for l in snap["lignes"]:
        r = dict(zip(cols, l))
        d = dt.date.fromisoformat(r["day"])
        if not (maintenant.date() - dt.timedelta(days=7) <= d <= maintenant.date() + dt.timedelta(days=3)):
            continue
        for k in ("apercu_paris", "page_paris", "saisie_export_paris"):
            if r[k] and dt.datetime.fromisoformat(r[k]) > maintenant:
                r[k] = None
        if r["saisie_export_paris"] is None:
            r["sauvegarde"], r["joueurs_saisis"] = None, None
        if r["coup_envoi_paris"] and dt.datetime.fromisoformat(r["coup_envoi_paris"]) + dt.timedelta(hours=2) > maintenant:
            r["played"], r["my_result"] = False, None
        res.append(tuple(r[c] for c in cols))
    return cols, res


def rejeu(maintenant, analyste):
    import tempfile
    d = donnees(etat_match=a_la_date(maintenant), prospects=(["rapport_paris"], []))
    with tempfile.TemporaryDirectory() as tmp:
        S = {"analyste": analyste, "cles": [], "cibles": [], "police": ""}
        evs = ej.construire(d, S, tmp, maintenant.date(), maintenant, CFG)
    return evs, ej.lignes(evs, CFG, maintenant)


def cas_rejeu():
    """P2.6 : rejeu sur les entrées du 12/11 (14:51) et du 17/11 (10:00) ; aucun libellé n'est écrit pour un cas."""
    import json
    snap = json.loads(INSTANTANE.read_text(encoding="utf-8"))
    noms = {l[3] for l in snap["lignes"]}
    code = (ICI / "etat_jour.py").read_text(encoding="utf-8")
    yield "rejeu : aucun adversaire de l'extrait n'est écrit dans etat_jour.py", not any(n in code for n in noms)
    for maint, analyste in ((dt.datetime(2026, 11, 12, 14, 51), dt.date(2026, 11, 10)), (dt.datetime(2026, 11, 17, 10, 0), dt.date(2026, 11, 17))):
        evs, ls = rejeu(maint, analyste)
        tag = f"{maint:%d/%m}"
        yield f"rejeu {tag} : complétude, chaque événement retenu a sa ligne", ej.sans_ligne(evs, ls, CFG, maint) == []
        yield f"rejeu {tag} : une seule ligne par événement", len({l["id"] for l in ls}) == len(ls)
        par = {e["id"]: e for e in evs}
        yield f"rejeu {tag} : chaque consigne de match nomme son adversaire et sa date (gabarit rempli par la base)", \
            all(par[l["id"]]["adversaire"] in l["consigne"] and f"{par[l['id']]['jour']:%d/%m}" in l["consigne"]
                for l in ls if l["type"] == "match" and l["action"])
    _, l12 = rejeu(dt.datetime(2026, 11, 12, 14, 51), dt.date(2026, 11, 10))
    p = {l["id"]: l for l in l12}
    yield "rejeu 12/11 14:51 : coupe du soir, aperçu pas encore en base → aperçu demandé avant le verrou 20:00", \
        p["m05"]["prochain"] == "apercu" and p["m05"]["echeance"] == dt.datetime(2026, 11, 12, 20, 0)
    yield "rejeu 12/11 14:51 : ligue du 11/11 jouée, page capturée seulement à 17:52 → page à exporter", \
        p["m03"]["prochain"] == "joue" and p["m03"]["action"]
    yield "rejeu 12/11 14:51 : amical du 13/11 (08:00) → fiche à faire, jamais d'aperçu", p["m06"]["prochain"] == "fiche"
    _, l17 = rejeu(dt.datetime(2026, 11, 17, 10, 0), dt.date(2026, 11, 17))
    p = {l["id"]: l for l in l17}
    yield "rejeu 17/11 10:00 : ligue du 16/11 non marquée jouée → page du match contre son adversaire", \
        p["m11"]["prochain"] == "joue" and p["m11"]["consigne"].startswith("exporte la page du match de ligue")
    yield "rejeu 17/11 10:00 : amical de 08:00 passé → page du match", p["m12"]["prochain"] == "joue" and p["m12"]["action"]
    yield "rejeu 17/11 10:00 : défaite du 14/11 analysée le 17/11, décisions à mesurer → juger", p["m08"]["prochain"] == "juge"
    yield "rejeu 17/11 10:00 : ligue du 18/11 sans heure en base → aperçu, échéance 19:45 de la config", \
        p["m14"]["prochain"] == "apercu" and p["m14"]["echeance"] == dt.datetime(2026, 11, 18, 19, 45)
    yield "rejeu 17/11 10:00 : amical du 20/11 hors des 48 h", "m16" not in p


def cas_branchement():
    """P2.5 : section « Aujourd'hui — état par événement » en tête du plan, à côté des blocs actuels."""
    import tempfile
    import forme
    import que_faire_blocs as qfb
    maint = dt.datetime(2026, 11, 17, 10, 0)
    d = donnees(etat_match=a_la_date(maint))
    S = {"analyste": dt.date(2026, 11, 17), "cles": [], "cibles": [], "police": ""}
    with tempfile.TemporaryDirectory() as tmp:
        lignes, consignes = qfb.bloc_etat(d, S, tmp, maint.date(), maint)
        texte, cons = qfb.rendre_blocs({"actions": [], "exports": [], "garder": [], "infos": [], "capacite": None}, d, {}, maint.date(), maint,
                                       S, etudes=[], base=tmp)
        attendu = [l for l in ej.lignes(ej.construire(d, S, tmp, maint.date(), maint, CFG), CFG, maint) if l["action"]] + ej.exports_periodiques(d, CFG, maint) + ej.matchs_ligue(d, CFG, maint) \
            + qfb.lignes_transferts_du_jour(d, None, S, maint)
    t = "\n".join(lignes)
    rangs = [l for l in lignes if l.startswith("| ") and not l.startswith("| Priorité")]
    yield "branchement : une rangée par transition à faire, aucune pour une attente", len(rangs) == len(attendu)
    yield "branchement : tableau au format du plan (forme)", t.count("| Priorité | Catégorie | Action |") == 1 and forme.fautes_tableaux(t, "basketvibe") == []
    yield "branchement : aucune commande d'agent affichée, elle part dans les consignes de session", \
        "lance l'agent" not in t and any("lance l'agent tactique" in c for c in consignes)
    yield "branchement : la section est en tête, avant le bloc 2", texte.index("## Aujourd'hui — état par événement") < texte.index("## Bloc 2")
    yield "branchement : les blocs 2 et 4 à 9 restent là, pas de bloc 0, 1, 3 ni 10 (18/11)", all(f"## Bloc {n} — " in texte for n in (2, 4, 5, 6, 7, 8, 9)) and not any(f"## Bloc {n} — " in texte for n in (0, 1, 3, 10))
    yield "branchement : consignes de la section dans les consignes de session", any("lance l'agent tactique" in c for c in cons)


def cas_deux_amicaux_meme_jour():
    """17/11 : deux amicaux préparés le même jour = deux fichiers `AAAA-MM-JJ-tactique-amical[-adversaire].md`, chacun retrouvé par adversaire."""
    import tempfile
    entete = "# Tactique — Ligue J8 contre Adv A (mer. 18/11 20:00, verrou 19:45)"
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "briefs").mkdir()
        (Path(tmp) / "briefs" / "2026-11-17-tactique-amical.md").write_text(BRIEF.replace(entete, "Amical contre Union Heidelberg (18/11)"), encoding="utf-8")
        (Path(tmp) / "briefs" / "2026-11-17-tactique-amical-bg-bangers.md").write_text(BRIEF.replace(entete, "Amical contre BG Bangers (19/11)"), encoding="utf-8")
        a = __import__("composition").brief_pour(tmp, dt.date(2026, 11, 17), "Union Heidelberg", True)
        b = __import__("composition").brief_pour(tmp, dt.date(2026, 11, 17), "BG Bangers", True)
    yield "deux amicaux le même jour : le premier est retrouvé par son adversaire", a is not None and a[1].name == "2026-11-17-tactique-amical.md"
    yield "deux amicaux le même jour : le second (suffixe adversaire) est retrouvé", b is not None and b[1].name == "2026-11-17-tactique-amical-bg-bangers.md"


# 19/11 : classements des trois ligues et onglets hebdo de la ligue tous frais (pour isoler les cas du 17/11)
LIGUES_19 = ["5fdd980c-032b-4ea3-b608-5eadc0c61f44", "45caebc5-824f-4d86-85e5-e8956e8cac6a", "a7250ea5-b8b1-4e1d-87c2-020b4572412e"]
FRAIS_19 = {"classements": (["league_id", "derniere_paris"], [(l, "2026-11-17T09:30:00") for l in LIGUES_19]),
            "pages_periodiques": (["page_type", "derniere_paris"], [(t, "2026-11-16T09:00:00") for t in ("standings_teams", "standings_players", "standings_injuries")])}


def cas_exports_ligue_19():
    """19/11 (consigne de l'utilisateur) : classement des trois ligues après chaque journée, onglets Équipes/Joueurs/Blessés chaque semaine,
    et une ligne 🟩 « exporte les N matchs de la ligue joués hier » (N ≤ 8, liste écrite dans exports-a-faire/ligue-AAAA-MM-JJ.md)."""
    cols = ["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"]
    frais = {"gold.bv_exports_state": (cols, [(8, "Marché (enchères)", "x", "2026-11-17T09:00:00", 1, "🟩"), (1, "Équipe (aperçu, joueurs)", "x", "2026-11-17T09:00:00", 1, "🟩"), (13, "Personnel", "x", "2026-11-14T09:00:00", 73, "🟩")]),
             "historique_global": (["derniere_paris"], [("2026-11-17T08:00:00",)])}
    em = (COLS_EM, [("f1", "ligue", "2026-11-16", "Adv A", True, True, "W", "2026-11-16T20:00:00") + (None,) * 6])
    a = ej.exports_periodiques(donnees(etat_match=em, **frais, **FRAIS_19), CFG, MAINT)
    yield "classement : capture après la dernière journée = aucune ligne", a == []
    em2 = (COLS_EM, [("f1", "ligue", "2026-11-17", "Adv A", True, True, "W", "2026-11-17T09:45:00") + (None,) * 6])
    b = ej.exports_periodiques(donnees(etat_match=em2, **frais, **FRAIS_19), CFG, MAINT)
    yield "classement : capture antérieure au dernier coup d'envoi de ligue = une ligne par ligue, âge inclus", \
        [l["ecran"] for l in b] == ["Classement Tier 3 - League 13", "Classement Tier 2 - League 4", "Classement Premier League"] \
        and all("export de 0 h" in l["consigne"] and l["priorite"] == 2 for l in b)
    vieux = dict(FRAIS_19, pages_periodiques=(["page_type", "derniere_paris"], [("standings_teams", "2026-11-09T09:00:00")]))
    c = ej.exports_periodiques(donnees(etat_match=em, **frais, **vieux), CFG, MAINT)
    yield "onglets de la ligue : Équipes périmé (193 h), Joueurs et Blessés jamais exportés", \
        [(l["ecran"], l["consigne"].split(" — ")[1]) for l in c] == [("Ligue — Équipes", "export de 193 h"), ("Ligue — Joueurs", "jamais exporté"), ("Ligue — Blessés", "jamais exporté")]
    cm = ["fixture_id", "match_day", "kickoff", "home_team", "away_team", "is_mine", "en_base"]
    rows = [(f"m{i:02d}", "2026-11-16", None, f"H{i}", f"A{i}", False, False) for i in range(10, 0, -1)]
    rows += [("moi", "2026-11-16", None, "Moi", "X", True, False), ("ok", "2026-11-16", None, "B", "C", False, True), ("av", "2026-11-15", None, "D", "E", False, False)]
    d = donnees(matchs_ligue=(cm, rows), matchs_en_base=(["n"], [(273,)]))
    with __import__("tempfile").TemporaryDirectory() as tmp:
        m = ej.matchs_ligue(d, CFG, MAINT, tmp)
        f = Path(tmp) / "exports-a-faire" / "ligue-2026-11-17.md"
        liste = f.read_text(encoding="utf-8") if f.is_file() else ""
    yield "matchs de la ligue : 8 au plus, hors les miens, ceux en base et ceux d'avant-hier", len(m) == 1 and m[0]["consigne"].startswith("exporte les 8 matchs de la ligue joués hier")
    yield "matchs de la ligue : catégorie Export, 🟩 SUIVI, pourquoi chiffré", m[0]["prochain"] == "export_periodique" and m[0]["priorite"] == 3 \
        and "sert à l'étude du Match Engine : B1 (étude du 18/11) : 5×48 : 29 sur 150 ; rotation : 95 sur 150" in m[0]["consigne"] \
        and "273" not in m[0]["consigne"] and "exports-a-faire/ligue-2026-11-17.md" in m[0]["consigne"]
    yield "matchs de la ligue : liste des liens écrite, du plus ancien au plus récent", liste.count("https://www.basketvibe.com/match/") == 8 \
        and liste.index("/match/m01") < liste.index("/match/m08") and "/match/m09" not in liste and "/match/moi" not in liste
    yield "matchs de la ligue : tout en base = aucune ligne", ej.matchs_ligue(donnees(matchs_ligue=(cm, rows[-2:-1])), CFG, MAINT) == []


def cas_exports_periodiques():
    """17/11 (décision de l'utilisateur) : Marché et historique global des transferts chaque jour (périmés après 24 h), Personnel chaque semaine ;
    une ligne par écran avec l'âge de l'export, qui disparaît quand la base voit la capture."""
    cols = ["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"]
    vieux = (cols, [(8, "Marché (enchères)", "x", "2026-11-13T10:26:30", 97, "🟧 à refaire"), (1, "Équipe (aperçu, joueurs)", "x", "2026-11-17T09:00:00", 1, "🟩"), (13, "Personnel", "x", "2026-11-08T11:10:48", 216, "🟧 à refaire")])
    frais = (cols, [(8, "Marché (enchères)", "x", "2026-11-17T09:00:00", 1, "🟩 à jour"), (1, "Équipe (aperçu, joueurs)", "x", "2026-11-17T09:00:00", 1, "🟩"), (13, "Personnel", "x", "2026-11-14T09:00:00", 73, "🟩 à jour")])
    h_vieux = (["derniere_paris"], [("2026-11-13T10:24:16",)])
    h_frais = (["derniere_paris"], [("2026-11-17T08:00:00",)])
    a = ej.exports_periodiques(donnees(**{"gold.bv_exports_state": vieux, "historique_global": h_vieux, **FRAIS_19}), CFG, MAINT)
    yield "périodiques : trois lignes quand les trois exports sont périmés", [l["ecran"] for l in a] == ["Marché (enchères)", "Historique global des transferts", "Personnel"]
    yield "périodiques : l'âge de l'export est dans la ligne", "export de 97 h" in a[0]["consigne"] and "export de 216 h" in a[2]["consigne"] and "export de 95 h" in a[1]["consigne"]
    yield "périodiques : action, priorité 2, jamais une attente", all(l["action"] and l["priorite"] == 2 for l in a)
    b = ej.exports_periodiques(donnees(**{"gold.bv_exports_state": frais, "historique_global": h_frais, **FRAIS_19}), CFG, MAINT)
    yield "périodiques : les captures vues en base font disparaître les lignes", b == []
    c = ej.exports_periodiques(donnees(**{"gold.bv_exports_state": (cols, []), "historique_global": (["derniere_paris"], [(None,)]), **FRAIS_19}), CFG, MAINT)
    yield "périodiques : jamais exporté (Marché, historique, Personnel, Équipe)", len(c) == 4 and all("jamais exporté" in l["consigne"] for l in c)
    d = ej.exports_periodiques(donnees(**{"gold.bv_exports_state": (cols, [(8, "Marché (enchères)", "x", "2026-11-16T11:00:00", 23, "🟩 à jour"), (1, "Équipe (aperçu, joueurs)", "x", "2026-11-17T09:00:00", 1, "🟩"), (13, "Personnel", "x", "2026-11-10T10:00:00", 120, "🟩 à jour")]), "historique_global": h_frais, **FRAIS_19}), CFG, MAINT)
    yield "périodiques : Marché 23 h et Personnel 120 h ne sont pas périmés", d == []


def cas_academie_decision():
    """17/11 : rapport du 12/11 non décidé, 5 jours après : une ligne « décision attendue : tester N prospects (N × 25 000) »."""
    cols = ["rapport_paris", "slot", "name", "position", "age", "tsp_min", "tsp_max", "ps_mid", "height_cm"]
    pros = [("2026-11-12T09:00:01", 0, "P1", "PF", 17, 260, 420, 42.8, 197), ("2026-11-12T09:00:01", 1, "P2", "PF", 16, 219, 379, 37.8, 198),
            ("2026-11-12T09:00:01", 2, "P3", "SF", 16, 236, 396, 39.4, 190), ("2026-11-12T09:00:01", 3, "P4", "PF", 16, 200, 300, 30, 150)]
    S = {"analyste": None, "cles": [], "cibles": [], "police": ""}
    d = donnees(prospects=(cols, pros))
    ls = [l for l in ej.lignes(ej.construire(d, S, "/nonexistent", dt.date(2026, 11, 17), MAINT, CFG), CFG, MAINT) if l["type"] == "academie" and l["action"]]
    yield "académie : une seule ligne pour le rapport du 12/11 non testé", len(ls) == 1 and ls[0]["prochain"] == "teste"
    yield "académie : tests attendus chiffrés (3 tests, 75 000 ; le prospect hors taille est ignoré)", \
        ls and "tester 3 prospects (75 000)" in ls[0]["consigne"]
    # 18/11 : les 3 tests faits et exportés le 17/11 (dernière capture de la page Académie) → état « testé », verdict de la règle
    tcols = ["slot", "name", "position", "height_cm", "potentiel", "teste", "capture_paris"]
    tests = [(0, "P1", "PF", 197, "low", True, "2026-11-17T21:50:48"), (1, "P2", "PF", 198, "decent", True, "2026-11-17T21:50:48"),
             (2, "P3", "SF", 190, "decent", True, "2026-11-17T21:50:48"), (3, "P4", "PF", 150, None, False, "2026-11-17T21:50:48")]
    dt_ = donnees(prospects=(cols, pros), tests_academie=(tcols, tests))
    ev = next(e for e in ej.construire(dt_, S, "/nonexistent", dt.date(2026, 11, 17), MAINT, CFG) if e["type"] == "academie")
    lt = [l for l in ej.lignes([ev], CFG, MAINT) if l["action"]]
    yield "académie : tests lus → état « testé », plus de « tester 3 prospects »", ej.etat_evenement(ev, CFG, MAINT)["etat"] == "teste" \
        and lt and lt[0]["prochain"] == "decide" and "tester 3 prospects" not in lt[0]["consigne"]
    yield "académie : verdict par prospect testé (low, decent : pas de très gros potentiel → ignorer)", lt and all(
        x in lt[0]["consigne"] for x in ("P1 (PF, low) : ignorer", "P2 (PF, decent) : ignorer", "P3 (SF, decent) : ignorer", "capture du 17/11"))
    haut = [(0, "P1", "PF", 197, "high", True, "2026-11-17T21:50:48")] + tests[1:]
    lh = [l for l in ej.lignes([e for e in ej.construire(donnees(prospects=(cols, pros), tests_academie=(tcols, haut)), S, "/nonexistent",
                                                          dt.date(2026, 11, 17), MAINT, CFG) if e["type"] == "academie"], CFG, MAINT) if l["action"]]
    yield "académie : potentiel high → la règle ne s'applique pas en entier, ce qui manque est nommé, aucun seuil inventé", lh and \
        "P1 (PF, high) : à juger, il manque" in lh[0]["consigne"]
    ok, err = ej._rows({"tests_academie": (tcols, tests)}, "tests_academie"), None
    yield "académie : requête des tests sur la dernière capture (max(captured_at))", "tests_academie" in __import__("aujourdhui").REQUETES \
        and "max(captured_at)" in __import__("aujourdhui").REQUETES["tests_academie"] and len(ok) == 4
    yield "académie : sans prospects, la consigne générique reste", "décide pour chaque prospect" in [l for l in ej.lignes(ej.construire(donnees(), S, "/nonexistent", dt.date(2026, 11, 17), MAINT, CFG), CFG, MAINT) if l["type"] == "academie" and l["action"]][0]["consigne"]


def ligne_etat(type_, prochain, genre=None, action=True, **kw):
    l = {"id": f"{type_}-{genre}-{prochain}", "type": type_, "genre": genre, "prochain": prochain, "action": action,
         "evenement": f"{type_} test", "consigne": "consigne test", "cle": "adv-a-18-11", "titre": "Ligue contre Adv A (18/11)"}
    l.update(kw)
    return l


def cas_agents():
    """P3 (17/11) : table état → agent → sortie (config `agents`), lue par agents_a_lancer ; aucun cas particulier par événement."""
    import tempfile
    jour = dt.date(2026, 11, 17)
    agents_repo = {f.stem for f in (ICI.parent / ".claude" / "agents").glob("*.md")}
    table = CFG["agents"]
    yield "agents : la table n'utilise que des agents du dépôt (.claude/agents)", all(r["agent"] in agents_repo for r in table if r.get("agent"))
    with tempfile.TemporaryDirectory() as tmp:
        for r in table:
            l = ligne_etat(r["type"], r["prochain"], r.get("genre") or "ligue")
            res = ej.agents_a_lancer([l], CFG, tmp, jour)
            nom = f"{r['type']}/{r.get('genre', '*')}/{r['prochain']}"
            if not r.get("agent"):
                yield f"agents : {nom} sans agent défini → aucun lancement", res == []
                continue
            attendu = r["sortie"].format(jour=jour.isoformat(), cle="adv-a-18-11")
            yield f"agents : {nom} → agent {r['agent']}, sortie {attendu}", \
                len(res) == 1 and res[0]["agent"] == r["agent"] and res[0]["sortie"] == attendu and res[0]["statut"] == "a_lancer"
        yield "agents : état absent de la table (aperçu) → aucun lancement", ej.agents_a_lancer([ligne_etat("match", "apercu", "ligue")], CFG, tmp, jour) == []
        yield "agents : ligne d'attente (action fausse) → aucun lancement", ej.agents_a_lancer([ligne_etat("match", "fiche", "ligue", action=False)], CFG, tmp, jour) == []
        yield "agents : export périodique (sans type de la table) → aucun lancement", \
            ej.agents_a_lancer([{"type": "export_periodique", "prochain": "export_periodique", "action": True}], CFG, tmp, jour) == []
        yield "agents : la consigne de la ligne remplit le titre", "« Ligue contre Adv A (18/11) »" in ej.agents_a_lancer([ligne_etat("match", "fiche", "ligue")], CFG, tmp, jour)[0]["consigne"]
        sortie = Path(tmp) / "briefs" / f"{jour.isoformat()}-tactique-adv-a-18-11.md"
        sortie.parent.mkdir()
        sortie.write_text("Ligue contre Adv A (18/11)\n", encoding="utf-8")
        res = ej.agents_a_lancer([ligne_etat("match", "fiche", "ligue")], CFG, tmp, jour)
        yield "agents : sortie déjà présente → pas de relance", len(res) == 1 and res[0]["statut"] == "deja_fait"
        sortie.write_text("", encoding="utf-8")
        yield "agents : sortie vide → relance", ej.agents_a_lancer([ligne_etat("match", "fiche", "ligue")], CFG, tmp, jour)[0]["statut"] == "a_lancer"
        vide = Path(tmp) / "agents"
        vide.mkdir()
        res = ej.agents_a_lancer([ligne_etat("match", "analyse", "ligue")], CFG, tmp, jour, dossier_agents=vide)
        yield "agents : agent absent du dépôt → refus avec raison", res and res[0]["statut"] == "refus" and "analyste" in res[0]["raison"]
        quatre = [ligne_etat("match", "fiche", "amical", cle=f"adv-{i}") for i in range(4)] + [ligne_etat("match", "analyse", "ligue")]
        res = ej.agents_a_lancer(quatre, CFG, tmp, jour)
        yield "agents : plafond de 3 agents d'analyse par passage, analyste hors plafond", \
            [r["statut"] for r in res] == ["a_lancer"] * 3 + ["refus", "a_lancer"] and "plafond" in res[3]["raison"]
    l = ej.etat_evenement(match(), CFG, MAINT)
    yield "agents : l'état d'un match porte genre, clé de fichier et titre", l["genre"] == "ligue" and l["cle"] == "adv-a-18-11" and l["titre"] == "Ligue contre Adv A (18/11)"


def cas_lien_fiche():
    """17/11 : chaque ligne qui cite une fiche (« … selon la fiche », « corrige la fiche … ») contient son chemin et son lien."""
    import re
    import tempfile
    url = "https://github.com/RoJo69100/assistant-jeux/blob/claude/passage-quotidien/outputs/basketvibe/briefs/"
    fiche = {"ok": True, "adversaire": "Adv A", "fichier": "briefs/2026-11-17-tactique-amical-adv-a-18-11.md"}
    lignes = []
    for genre in ("ligue", "coupe", "amical"):
        lignes.append(ej.etat_evenement(match(genre=genre, fiche=fiche, apercu_at=T_APERCU), CFG, MAINT))
        mauvaise = dict(fiche, defauts=[{"texte": "❌ x", "correction": "ramène X à 36 min"}])
        lignes.append(ej.etat_evenement(match(genre=genre, fiche=mauvaise, apercu_at=T_APERCU), CFG, MAINT))
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "briefs").mkdir()
        (Path(tmp) / "briefs" / "2026-11-22-entrainement-semaine.md").write_text("x", encoding="utf-8")
        f = ej.fiche_entrainement(tmp, dt.date(2026, 11, 22), dt.date(2026, 11, 22))
        yield "lien : fiche d'entraînement trouvée dans briefs/", f == {"fichier": "briefs/2026-11-22-entrainement-semaine.md"}
        yield "lien : fiche d'entraînement d'avant le traitement ignorée", ej.fiche_entrainement(tmp, dt.date(2026, 11, 29), dt.date(2026, 11, 29)) is None
    en = {"type": "entrainement", "quand": dt.datetime(2026, 11, 22, 4, 0), "page_at": dt.datetime(2026, 11, 22, 8, 0), "saisi": False, "maj_at": None}
    lignes.append(ej.etat_evenement(dict(en, fiche=f), CFG, dt.datetime(2026, 11, 22, 9, 0)))
    sans = ej.etat_evenement(en, CFG, dt.datetime(2026, 11, 22, 9, 0))
    citent = [l for l in lignes + [sans] if re.search(r"selon la fiche|corrige la fiche", l["consigne"])]
    yield "lien : 7 lignes citent une fiche (3 écrans, 3 corrections, 1 entraînement)", len(citent) == 7
    yield "lien : chaque ligne qui cite une fiche contient son chemin et son lien", all(
        re.search(r"outputs/basketvibe/briefs/\S+\.md — " + re.escape(url) + r"\S+\.md", l["consigne"]) for l in citent)
    yield "lien : le lien pointe sur le fichier de la fiche", url + "2026-11-17-tactique-amical-adv-a-18-11.md" in citent[0]["consigne"] \
        and url + "2026-11-22-entrainement-semaine.md" in citent[-1]["consigne"]
    yield "lien : sans fiche, la ligne ne dit pas « selon la fiche »", "selon la fiche" not in sans["consigne"] and "aucune fiche" in sans["consigne"]


def cas_preset_adversaire():
    """Phase A, point 1 : ligue et coupe demandent le preset de l'adversaire avant l'aperçu ; l'amical n'en parle jamais."""
    for genre in ("ligue", "coupe"):
        l = ej.etat_evenement(match(genre=genre), CFG, MAINT)
        yield f"preset : {genre}, aperçu à faire → preset puis aperçu", l["prochain"] == "apercu" \
            and l["consigne"].startswith("fais le preset de l'adversaire (pour voir ses joueurs) puis exporte l'aperçu du ")
        l = ej.etat_evenement(match(genre=genre, apercu_at=T_APERCU, adv_connus=False), CFG, MAINT)
        yield f"preset : {genre}, aperçu exporté sans joueurs adverses → « preset de l'adversaire à faire »", l["prochain"] == "apercu" \
            and l["consigne"].startswith("preset de l'adversaire à faire")
        l = ej.etat_evenement(match(genre=genre, apercu_at=T_APERCU, adv_connus=True), CFG, MAINT)
        yield f"preset : {genre}, joueurs adverses connus → fiche", l["prochain"] == "fiche"
    for kw in ({}, {"fiche": FICHE}, {"fiche": FICHE, "ecran": ECRAN}, {"adv_connus": False}):
        l = ej.etat_evenement(match(genre="amical", **kw), CFG, MAINT)
        yield f"preset : amical ({', '.join(kw) or 'rien'}) → aucune mention de preset", "preset" not in l["consigne"].lower()
    rows = ej._rows({"adversaires_connus": (["fixture_id", "n"], [["m1", 12]])}, "adversaires_connus")
    yield "preset : requête des adversaires connus déclarée", "adversaires_connus" in ej.REQUETES and rows[0]["fixture_id"] == "m1"


O = ej.charger_offres()
CASE_COLS = ["ps_band", "age_band", "n", "p25", "median", "p75", "last_sale"]
ANN = ["auction_id", "name", "position", "age", "ps", "price_now", "ends_paris", "est_weekly_salary"]
ROT = ["player_id", "name", "position", "ps", "min_moy", "matchs_joues"]


def marche(age_h=2, annonces=(), cases=None, rotation=None, **plus):
    """Annonce sans salaire (7 colonnes) : salaire hebdo 10 000."""
    d = {"gold.bv_exports_state": (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
                                   [[3, "Marché (enchères)", "x", "2026-11-17T10:00:00", age_h, "s"]]),
         "prix_cases": (CASE_COLS, cases if cases is not None else [[50, "22-25", 4, 40000, 60000, 80000, "2026-11-10"],
                                                                    [55, "22-25", 2, 50000, 90000, 100000, "2026-11-10"]]),
         "annonces_actives": (ANN, [list(a) + [10000] if len(a) == 7 else list(a) for a in annonces]),
         "rotation": (ROT, rotation if rotation is not None else [["p1", "Jean Moyen", "SF", 48, 30, 4], ["p2", "Paul Banc", "SF", 40, 2, 1],
                                                                 ["p3", "Luc Absent", "SF", 30, 0, 0]])}
    d.update(plus)
    return d


_rows_orig = ej._rows


def _rows_compat(donnees, nom):
    """Anciens cas (avant le 19/11) : cases sans poste recopiées pour chaque poste (fourchette = p25 à p75)."""
    if nom == "prix_cases_poste" and nom not in donnees:
        return [dict(r, position=p, mini=r["p25"], maxi=r["p75"]) for r in _rows_orig(donnees, "prix_cases") for p in ("PG", "SG", "SF", "PF", "C")]
    return _rows_orig(donnees, nom)


ej._rows = _rows_compat


def cas_rotation_illisible():
    """Verdict du 18/11 : Szewczyk (SG 56,4) classé « revente » alors que Bonnet (SG 51,9) joue : la requête de rotation était en
    timeout, donc aucun « plus faible » connu et toute annonce tombait en revente."""
    sz = ["a9", "Alan Szewczyk", "SG", 23, 52, 38000, "2026-11-18T23:37:00"]
    d = marche(annonces=[sz])
    d["rotation"] = None
    r = ej.offres_du_jour(d, O, 300000)
    yield "rotation illisible → aucune offre classée, « inconnu » nomme la rotation", r["offres"] == [] and "rotation" in (r["inconnu"] or "")
    r = ej.offres_du_jour(marche(annonces=[sz], rotation=[["p9", "Thibault Bonnet", "SG", 48, 36, 1]]), O, 300000)
    yield "rotation lue (min_moy > 0) → Szewczyk en amélioration face à Bonnet", [(x["type"], x.get("faible")) for x in r["offres"]] == \
        [("amélioration", "Thibault Bonnet")]


def cas_prix_inconnu():
    """Verdict du 18/11 : Pellegrini et Balbuena « à 0 » (aucune enchère = prix inconnu) proposés en revente ; aucun âge d'export."""
    zero_rv = ["b1", "Gino Pellegrini", "PG", 24, 51, 0, "2026-11-18T23:49:00"]   # PG : aucun utilisé → serait revente
    zero_am = ["b2", "Armando Balbuena", "SF", 23, 52, 0, "2026-11-18T17:52:00"]  # 52 > 40 → amélioration
    r = ej.offres_du_jour(marche(annonces=[zero_rv, zero_am]), O, 300000)
    yield "prix 0 : pas de revente (marge non calculable)", [x["nom"] for x in r["offres"]] == ["Armando Balbuena"]
    t = ej.texte_transfert(r["offres"][0], O)
    yield "prix 0 : « prix inconnu », jamais « à 0 »", "prix inconnu" in t and "à 0 " not in t
    am = ["b3", "Tom Gain", "SF", 23, 52, 751, "2026-11-18T09:00:00"]
    t = ej.texte_transfert(ej.offres_du_jour(marche(annonces=[am]), O, 300000)["offres"][0], O)
    yield "prix connu : âge de l'export du Marché donné", "à 751 (export du Marché de 2 h)" in t


def cas_priorite_capacite():
    """Verdict du 18/11 : 3 plafonds additionnés (1 439 392) au-dessus de la capacité (666 868) sans ligne de priorité."""
    a = ["c1", "Tom Gain", "SF", 23, 52, 55000, "2026-11-18T09:00:00"]
    b = ["c2", "Bob Juste", "SF", 23, 51, 58000, "2026-11-18T10:00:00"]
    l = ej.lignes_transferts(marche(annonces=[a, b]), 100000, None, o=O)
    p = [x for x in l if x["id"] == "offres-priorite"]
    yield "plafonds 80 000 + 80 000 > capacité 100 000 → ligne de priorité urgente", len(p) == 1 and p[0]["priorite"] == 1 \
        and "160 000" in p[0]["consigne"] and "100 000" in p[0]["consigne"] \
        and p[0]["consigne"].index("Tom Gain") < p[0]["consigne"].index("Bob Juste")
    l = ej.lignes_transferts(marche(annonces=[a, b]), 300000, None, o=O)
    yield "plafonds dans la capacité → pas de ligne de priorité", not [x for x in l if x["id"] == "offres-priorite"]


def cas_offres():
    yield "offres : seuils lus dans le yaml", O["revente_marge"] == 1.25 and O["case_min_ventes"] == 3 and O["matchs_rotation"] == 4 \
        and O["minimum_effectif"] == 8
    yield "offres : la requête de rotation lit la vue rapide (bv_match_player_lines dépasse le délai, 18/11)", \
        "bv_sell_candidates" in ej.REQUETES["rotation"] and "bv_match_player_lines" not in ej.REQUETES["rotation"]
    am = ["a1", "Tom Gain", "SF", 23, 52, 55000, "2026-11-18T09:00:00"]   # note 52 > 40 (Paul Banc, utilisé le plus faible), 55 000 ≤ médiane 60 000
    rv = ["a2", "Yan Bas", "PG", 24, 51, 38000, "2026-11-18T10:00:00"]   # PG : aucun utilisé ; 38 000 ≤ p25 40 000 et 60 000 ≥ 1,25 × 38 000
    rien = ["a3", "Max Cher", "C", 24, 50, 70000, "2026-11-18T11:00:00"]
    petite = ["a4", "Eli Rare", "SF", 23, 57, 10000, "2026-11-18T11:00:00"]  # case de 2 ventes < 3
    r = ej.offres_du_jour(marche(annonces=[am, rv, rien, petite]), O, 300000)
    yield "offres : amélioration seule, la revente adulte ne donne plus d'enchère (règle du 18/11)", \
        [(x["nom"], x["type"]) for x in r["offres"]] == [("Tom Gain", "amélioration")] and r["inconnu"] is None
    yield "offres : l'amélioration nomme notre titulaire au poste (le plus de minutes)", r["offres"][0]["faible"] == "Jean Moyen"
    yield "offres : hors budget → pas d'amélioration", [x["nom"] for x in ej.offres_du_jour(marche(annonces=[am]), O, 50000)["offres"]] == []
    yield "offres : aucune annonce intéressante → aucune offre", ej.offres_du_jour(marche(annonces=[rien, petite]), O, 300000)["offres"] == []
    p = ej.offres_du_jour(marche(age_h=100, annonces=[am, rv]), O, 300000)
    yield "offres : Marché périmé → inconnu, aucune offre", p["offres"] == [] and p["inconnu"].startswith("inconnu : export de 100 h")
    yield "offres : case_min_ventes du yaml à 2 → la petite case compte", "Eli Rare" in [
        x["nom"] for x in ej.offres_du_jour(marche(annonces=[petite]), dict(O, case_min_ventes=2), 300000)["offres"]]


def cas_regle_jeunes():
    """Règle de l'utilisateur du 18/11 : titulaires de tout âge, remplaçants de 16 à 18 ans à fort potentiel (4 cas)."""
    cols = ANN + ["height_cm", "player_id"]
    cases = [[50, "22-25", 4, 40000, 60000, 80000, "2026-11-10"], [55, "30+", 4, 40000, 60000, 80000, "2026-11-10"],
             [40, "≤21", 4, 40000, 60000, 80000, "2026-11-10"], [55, "26-28", 4, 40000, 60000, 80000, "2026-11-10"]]
    vieux = ["j1", "Vieux Titulaire", "SF", 31, 55, 50000, "2026-11-18T22:00:00", 10000, 198, "v1"]  # 55 > 48 Jean Moyen
    adulte = ["j2", "Alan Szewczyk", "SG", 28, 56, 50000, "2026-11-18T23:37:00", 10000, 196, "v2"]  # 56 < 60 Bonnet titulaire
    high = ["j3", "Jeune High", "C", 17, 40, 30000, "2026-11-19T10:00:00", 10000, 206, "v3"]
    low = ["j4", "Jeune Low", "C", 17, 41, 30000, "2026-11-19T10:00:00", 10000, 206, "v4"]
    inconnus = [["j0", "Jeune Cher", "C", 17, 49, 5000000, "2026-11-19T17:00:00", 10000, 206, "v0"],  # hors capacité : pas de test
                ["j5", "Jeune A", "C", 18, 45, 50000, "2026-11-20T16:31:00", 10000, 207, "v5"],
                ["j6", "Jeune B", "C", 18, 40, 2000, "2026-11-20T15:20:00", 10000, 210, "v6"],
                ["j7", "Jeune C", "PG", 17, 39, 1000, "2026-11-20T15:20:00", 10000, 184, "v7"],
                ["j8", "Jeune Petit", "C", 17, 46, 1000, "2026-11-20T15:20:00", 10000, 190, "v8"]]  # 190 cm : hors plage C
    rot = [["p1", "Jean Moyen", "SF", 48, 30, 4], ["p2", "Paul Banc", "SF", 40, 2, 1], ["p9", "Thibault Bonnet", "SG", 60, 36, 4],
           ["p3", "Armand Fournier", "C", 52, 30, 4]]
    tm = (["player_id", "potentiel"], [["v3", "high"], ["v4", "low"]])
    d = marche(annonces=[], cases=cases, rotation=rot, tests_marche=tm)
    d["annonces_actives"] = (cols, [vieux, adulte, high, low] + inconnus)
    r = ej.offres_du_jour(d, O, 300000)
    types = {x["nom"]: x["type"] for x in r["offres"]}
    yield "règle 18/11 cas 1 : titulaire chez nous de 31 ans → amélioration (tout âge)", types.get("Vieux Titulaire") == "amélioration"
    yield "règle 18/11 cas 2 : adulte pas titulaire (Szewczyk sous Bonnet) → aucune ligne", "Alan Szewczyk" not in types \
        and "Alan Szewczyk" not in [t["nom"] for t in r["tests"]]
    yield "règle 18/11 cas 3 : 17 ans testé High → enchère « jeune » ; testé Low → ni enchère ni test", types.get("Jeune High") == "jeune" \
        and "Jeune Low" not in types and "Jeune Low" not in [t["nom"] for t in r["tests"]] \
        and "Jeune High" not in [t["nom"] for t in r["tests"]]
    yield "règle 19/11 cas 4 : sans test, 1 test au plus (25 000), meilleure note d'abord, taille hors plage et prix hors capacité exclus", \
        [t["nom"] for t in r["tests"]] == ["Jeune A"] and sum(t["cout"] for t in r["tests"]) == 25000 and O["tests_par_jour"] == 1 and O["tests_budget"] == 25000
    l = ej.lignes_transferts(d, 300000, None, o=O)
    t = [x for x in l if x["id"].startswith("tester-")]
    yield "règle 19/11 : ligne « pas d'enchère avant le test ; Police : ne pas acheter » en tête, seul High justifie une enchère, règle 2", len(t) == 1 \
        and t[0]["consigne"].startswith("pas d'enchère avant le test ; Police : ne pas acheter — tester le potentiel (25 000) : Jeune A") and "seul « High » justifie une enchère" in t[0]["consigne"] \
        and "proposition seulement (règle 2)" in t[0]["consigne"]
    yield "règle 18/11 : test de potentiel lu sur la page profil (requête déclarée)", "potential_bucket" in ej.REQUETES["tests_marche"]


VEN = ["player_id", "name", "position", "age", "ps", "salary", "best_slot", "rank_in_slot", "league_min_last4", "on_transfer_list"]
REM = ["player_id", "name", "best_slot", "fit_best", "replacement_name", "replacement_fit", "gap", "weekly_salary", "on_transfer_list",
       "available", "available_players"]


def effectif(n=10, police_nom=None):
    """`n` joueurs ; p2 (Paul Banc, 2 min, écart 0,5) vendable ; p3 (Luc Absent, 0 min) sans remplaçant ; p1 en rotation."""
    v = [["p1", "Jean Moyen", "SF", 24, 48, 20000, "SF", 1, 30, False], ["p2", "Paul Banc", "SF", 23, 51, 15000, "SF", 2, 2, False],
         ["p3", "Luc Absent", "SF", 24, 50, 15000, "SF", 3, 0, False]]
    v += [[f"x{i}", f"Autre {i}", "PG", 30, 45, 10000, "PG", 1, 30, False] for i in range(n - 3)]
    r = [["p1", "Jean Moyen", "SF", 50, "Paul Banc", 49, 1.0, 20000, False, True, n], ["p2", "Paul Banc", "SF", 50, "Jean Moyen", 49.5, 0.5, 15000, False, True, n],
         ["p3", "Luc Absent", "SF", 50, None, None, None, 15000, False, True, n]]
    return {"vendre": (VEN, v), "gold.bv_sell_replacement": (REM, r)}


def cas_ventes():
    rot = [["p1", "Jean Moyen", "SF", 48, 30, 4], ["p2", "Paul Banc", "SF", 51, 2, 1], ["p3", "Luc Absent", "SF", 50, 0, 0]]
    d = marche(rotation=rot, **effectif())
    v = ej.ventes_du_jour(d, O, 1.0)
    yield "ventes : hors rotation, remplaçable, case fiable → vendable", [x["nom"] for x in v] == ["Paul Banc"] and v[0]["prix"] == 60000
    yield "ventes : jamais « ne pas vendre » de la police", ej.ventes_du_jour(d, O, 1.0, "ne pas vendre Paul Banc (police du jour)") == []
    yield "ventes : tolérance dépassée → rien", ej.ventes_du_jour(d, O, 0.4) == []
    yield "ventes : tolérance inconnue → rien", ej.ventes_du_jour(d, O, None) == []
    yield "ventes : minimum d'effectif de 8 respecté", ej.ventes_du_jour(marche(rotation=rot, **effectif(8)), O, 1.0) == []
    yield "ventes : minutes_hors_rotation du yaml à 1 → Paul Banc (2 min) reste", ej.ventes_du_jour(d, dict(O, minutes_hors_rotation=1), 1.0) == []
    yield "ventes : vente_marge_profit lue dans le yaml (25 %)", O["vente_marge_profit"] == 0.25
    yield "ventes : prix d'achat inconnu → proposée, « prix d'achat inconnu, profit non calculé »", v and v[0]["prix_achat"] is None \
        and "prix d'achat inconnu, profit non calculé" in ej.texte_transfert(v[0], O)
    achat = lambda fee: dict(d, prix_achat=(["player_id", "fee"], [["p2", fee]]))
    yield "ventes : prix d'achat connu, profit 20 % < 25 % → pas de vente", ej.ventes_du_jour(achat(50000), O, 1.0) == []
    v2 = ej.ventes_du_jour(achat(40000), O, 1.0)
    yield "ventes : prix d'achat connu, profit 50 % ≥ 25 % → vente avec le profit", [x["nom"] for x in v2] == ["Paul Banc"] \
        and "profit 50 % sur le prix payé 40 000 (≥ 25 %)" in ej.texte_transfert(v2[0], O)
    yield "ventes : marge du yaml à 0,6 → la vente à 50 % disparaît", ej.ventes_du_jour(achat(40000), dict(O, vente_marge_profit=0.6), 1.0) == []
    yield "ventes : requête du prix d'achat déclarée", "bought_by_me" in ej.REQUETES["prix_achat"]
    yield "ventes : case_min_ventes du yaml à 3 → case de 2 ventes refusée", ej.ventes_du_jour(
        marche(rotation=rot, cases=[[50, "22-25", 2, 40000, 60000, 80000, "2026-11-10"]], **effectif()), O, 1.0) == []


def cas_niveau_e1():
    """18/11 : le niveau de E1 alterne A et B ; l'amical FuzzyTeam du 20/11 est en niveau B, et la fiche le reçoit."""
    import yaml
    import aujourdhui as auj
    conf = yaml.safe_load((ej.RACINE / "docs/attentes/experiences-amicales-basketvibe.yaml").read_text(encoding="utf-8"))
    e1 = next(e for e in conf["experiences"] if e["id"] == "E1")
    yield "E1 : ordre du yaml alterné A, B", e1["ordre"] == ["A", "B", "A", "B"]
    j = lambda m, d: dt.date(2026, 11, d)  # noqa: E731
    fait = lambda nom, d, niv: {"id": "E1", "niveau": niv, "jour": j(0, d), "cle": {"nom": nom, "date": j(0, d), "jour": j(0, d), "fichier": "f"}}
    jo = lambda nom, d, cran: {"fixture_id": nom, "match_day": f"2026-11-{d}", "opponent": nom, "agress_uniforme": True, "agress_cran": cran}
    x = {"file": conf["experiences"], "debut": dt.date(2026, 11, 10), "faits": [fait("Artificial Instinct", 14, "A")]}
    fz = {"match": "FuzzyTeam", "date": j(0, 20)}
    t = auj.test_en_cours(x, fz, [jo("Artificial Instinct", 14, 2)])
    yield "E1 : après le 14/11 en A, FuzzyTeam (20/11) en niveau B", t and (t[0]["id"], t[1]) == ("E1", "B")
    x2 = dict(x, faits=x["faits"] + [fait("BG Bangers", 19, "A")])
    t2 = auj.test_en_cours(x2, fz, [jo("Artificial Instinct", 14, 2), jo("BG Bangers", 19, 2)])
    yield "E1 : 14/11 et 19/11 en A → FuzzyTeam (20/11) toujours en B (alternance sur le dernier niveau joué)", t2 and t2[1] == "B"
    x3 = dict(x, faits=x["faits"] + [fait("BG Bangers", 19, "B")])
    yield "E1 : dernier en B → le suivant en A", auj.test_en_cours(x3, fz, [jo("Artificial Instinct", 14, 2), jo("BG Bangers", 19, 4)])[1] == "A"
    texte = ej.texte_test_fiche(x, {"opponent": "FuzzyTeam", "day": "2026-11-20"}, [jo("Artificial Instinct", 14, 2)])
    yield "fiche d'amical : la consigne porte le test E1 niveau B (agressivité 5 à l'écran), le reste neutre", \
        "test E1 niveau B : agressivité 5 à l'écran (cran 4, agressive) sur tous les joueurs" in texte and "neutre" in texte
    yield "fiche : la consigne de l'agent reprend le test", any("test E1 niveau B" in e["consigne"] for e in ej.agents_a_lancer(
        [{"action": True, "type": "match", "genre": "amical", "prochain": "fiche", "consigne": "fiche", "test": texte, "cle": "fuzzyteam-20-11",
          "titre": "Amical contre FuzzyTeam (20/11)", "id": "m"}], base=ej.RACINE / "outputs" / "inexistant", jour=dt.date(2026, 11, 18)))


def cas_affichage_transferts():
    import que_faire_blocs as qfb
    rot = [["p1", "Jean Moyen", "SF", 48, 30, 4], ["p2", "Paul Banc", "SF", 51, 2, 1], ["p3", "Luc Absent", "SF", 50, 0, 0]]
    am = ["a1", "Tom Gain", "SF", 23, 52, 55000, "2026-11-18T09:00:00"]
    rv = ["a2", "Yan Bas", "PG", 24, 51, 38000, "2026-11-18T10:00:00"]
    d = dict(marche(annonces=[am, rv], rotation=rot, **effectif()), tolerance_vente=(["value"], [[1.0]]))
    ls = ej.lignes_transferts(d, 300000, 1.0)
    yield "affichage : offre et vente, triées par gain attendu (revente adulte retirée le 18/11)", \
        [l["id"] for l in ls] == ["vente-Paul Banc", "amélioration-Tom Gain"]
    yield "affichage : catégorie Transferts", all(qfb.AFFICHAGE[qfb.CAT_ETAT[l["prochain"]]] == "Transferts" for l in ls)
    t = ls[1]["consigne"]
    yield "affichage : la ligne porte nom, poste, âge, note, prix, médiane, type, fin, règle 2", all(x in t for x in (
        "amélioration : Tom Gain (SF, 23 ans, note 52)", "à 55 000", "médiane du poste 60 000", "fin 18/11 09:00", "proposition seulement (règle 2)"))
    yield "affichage : les seuils du yaml sont dans la ligne", "notre titulaire au poste" in t and "sur 4 matchs de ligue" in t
    yield "affichage : petite somme sans police", "police d'abord" not in t
    gros = dict(d, annonces_actives=(ANN, [["a9", "Gros Prix", "PG", 24, 51, 260000, "2026-11-18T10:00:00", 10000]]),
                prix_cases=(CASE_COLS, [[50, "22-25", 4, 300000, 400000, 500000, "2026-11-10"]]))
    yield "affichage : somme > 250 000 → police d'abord", any("police d'abord : dossier.py puis agent police" in l["consigne"]
                                                             for l in ej.lignes_transferts(gros, 1000000, 1.0))
    sans = dict(d, annonces_actives=(ANN, []), vendre=(VEN, []))
    ls0 = ej.lignes_transferts(sans, 300000, 1.0)
    yield "affichage : sans offre ni vente → une seule ligne « Ventes : aucune à proposer (0 joueur évalué, …) »", \
        [l["id"] for l in ls0] == ["ventes-aucune"] and ls0[0]["consigne"].startswith("Ventes : aucune à proposer (0 joueur évalué, ")
    rot_tous = [["p1", "Jean Moyen", "SF", 48, 30, 4], ["p2", "Paul Banc", "SF", 51, 30, 4], ["p3", "Luc Absent", "SF", 50, 30, 4]]
    t0 = [l for l in ej.lignes_transferts(dict(d, rotation=(ROT, rot_tous)), 300000, 1.0) if l["id"] == "ventes-aucune"]
    yield "affichage : aucune vente → N joueurs évalués et la raison (en rotation)", len(t0) == 1 \
        and t0[0]["consigne"].startswith("Ventes : aucune à proposer (10 joueurs évalués, ") and "en rotation : 3" in t0[0]["consigne"] and t0[0]["prochain"] == "vente"
    yield "affichage : tolérance inconnue → raison dite", "tolérance du bloc 4 non lue" in \
        [l for l in ej.lignes_transferts(d, 300000, None) if l["id"] == "ventes-aucune"][0]["consigne"]
    yield "affichage : une vente proposée → pas de ligne « aucune »", "ventes-aucune" not in [l["id"] for l in ls]
    p = ej.lignes_transferts(dict(d, **{"gold.bv_exports_state": marche(age_h=100)["gold.bv_exports_state"]}), 300000, 1.0)
    yield "affichage : Marché périmé → ligne « inconnu », pas d'offre", p[0]["consigne"].startswith("offres du Marché : inconnu : export de 100 h") \
        and not any(l["id"].startswith(("revente", "amélioration")) for l in p)
    yield "affichage : max_offres du yaml à 1 → une seule offre", len([l for l in ej.lignes_transferts(d, 300000, 1.0, o=dict(O, max_offres=1))
                                                                     if l["prochain"] == "offre"]) == 1
    yield "affichage : revente_marge du yaml à 1,6 → Yan Bas disparaît", "revente-Yan Bas" not in [
        l["id"] for l in ej.lignes_transferts(d, 300000, 1.0, o=dict(O, revente_marge=1.6))]


def cas_enchere_max():
    """18/11 : budget = capacite_invest (666 868 le 17/11), jamais le solde (1 500 018) ; enchère max X = min(p75 de la case,
    capacité − salaire hebdo de la recrue) ; ligne supprimée si le prix relu dépasse X. Cas réels du 17/11 : Naguib (28 250 périmé
    dans le plan, 510 000 relu à 22:07) et Szewczyk (751)."""
    cases = [[45, "≤21", 51, 535000, 950000, 1645832.5, "2026-11-15"], [55, "26-29", 88, 757500, 1000000, 1357031.25, "2026-11-15"]]
    rot = [["d1", "Jonathan Durand", "SF", 43.7, 20, 4], ["b1", "Thibault Bonnet", "SG", 51.9, 15, 4]]
    nag = lambda prix: ["bd0f", "Fouad Naguib", "SF", 17, 45.9, prix, "2026-11-19T12:31:00", 18130]
    sze = lambda prix: ["3061", "Alan Szewczyk", "SG", 28, 56.4, prix, "2026-11-18T23:37:00", 25500]
    d = lambda *a: marche(annonces=list(a), cases=cases, rotation=rot)
    t = lambda ls, nom: next((l["consigne"] for l in ls if nom in l["consigne"] and l["id"] != "offres-priorite"), None)
    ls = ej.lignes_transferts(d(nag(28250), sze(751)), 666868, None)
    yield "enchère max : Naguib périmé à 28 250 → max 648 738 (capacité 666 868 − salaire 18 130 < p75)", \
        "Fouad Naguib (SF, 17 ans, note 45,9), enchère max 648 738, à 28 250" in (t(ls, "Naguib") or "")
    yield "enchère max : Szewczyk → max 641 368 (666 868 − 25 500), à 751, police d'abord (max > 250 000)", \
        "Alan Szewczyk (SG, 28 ans, note 56,4), enchère max 641 368, à 751" in (t(ls, "Szewczyk") or "") and "police d'abord" in t(ls, "Szewczyk")
    yield "enchère max : la ligne nomme la capacité, pas le solde", "capacité 666 868" in t(ls, "Szewczyk") and "1 500 018" not in t(ls, "Szewczyk")
    ls = ej.lignes_transferts(d(nag(510000)), 666868, None)
    yield "enchère max : Naguib relu à 510 000 ≤ 648 738 → gardé, « à 510 000 »", "enchère max 648 738, à 510 000" in (t(ls, "Naguib") or "")
    ls = ej.lignes_transferts(d(nag(510000), sze(751)), 666868 - 550000, None, exclus=["Alan Szewczyk"])
    yield "enchère max : Szewczyk décidé à 550 000 → capacité 116 868, Naguib relu à 510 000 > 98 738 → ligne supprimée", \
        t(ls, "Naguib") is None and t(ls, "Szewczyk") is None
    yield "enchère max : Szewczyk relu à 700 000 > 641 368 → ligne supprimée", t(ej.lignes_transferts(d(sze(700000)), 666868, None), "Szewczyk") is None
    yield "enchère max : salaire inconnu → aucune offre", t(ej.lignes_transferts(d(sze(751)[:7] + [None]), 666868, None), "Szewczyk") is None
    p = ej.lignes_transferts(d(sze(751)), None, None)
    p = [l for l in p if l["id"] != "ventes-aucune"]
    yield "enchère max : capacité illisible → ligne « inconnu », jamais le solde", len(p) == 1 and "capacité d'investissement illisible" in p[0]["consigne"]


def cas_personnel():
    p = ej.charger_personnel()
    yield "personnel : règle décidée dans le yaml, 4 rôles", p.get("statut", "").startswith("décidée") and len(p["roles"]) == 4
    t = ej.texte_personnel(p, [{"role": "marketing", "hired": 2, "slots": 2}])
    yield "personnel : écart → ligne d'action chiffrée", t.startswith("personnel : licencie 2 marketing (2 → 0) (−") and "par semaine) : marketing : 1 %" in t
    yield "personnel : conforme ou sans règle → aucune ligne", ej.texte_personnel(p, [{"role": "marketing", "hired": 0, "slots": 2}]) == "" and ej.texte_personnel({}) == ""


def _plan_19():
    """Effectif du plan du 19/11 : Baron (PG, 24 ans, hors rotation), Boyer (PG) et Durand (SF), Bonnet titulaire SG, 7 joueurs en rotation."""
    rot = [["baron", "Nolan Baron", "PG", 45, 2, 1], ["boyer", "Naël Boyer", "PG", 47, 25, 4], ["durand", "Léo Durand", "SF", 50, 30, 4],
           ["bonnet", "Thibault Bonnet", "SG", 50, 30, 4], ["jeune", "Tim Jeune", "PG", 44, 1, 1]] \
        + [[f"x{i}", f"Autre {i}", "C", 45, 30, 4] for i in range(6)]
    ven = [[r[0], r[1], r[2], 24, r[3], 10000, r[2], 2, r[4], False] for r in rot]
    ven[4][3] = 17
    fit = [["baron", "Nolan Baron", "PG", "PG", 44.7], ["boyer", "Naël Boyer", "PG", "PG", 48.3], ["durand", "Léo Durand", "SF", "PG", 52.0],
           ["bonnet", "Thibault Bonnet", "SG", "SG", 56.1], ["jeune", "Tim Jeune", "PG", "PG", 44.0]]
    cases = [["PG", 45, "22-25", 4, 300000, 400000, 500000, 290000, 910000], ["PG", 40, "≤21", 4, 30000, 100000, 290000, 26250, 290000]]
    return dict(rotation=rot, vendre=(VEN, ven), slot_fit=(["player_id", "name", "position", "slot", "fit"], fit),
                prix_cases_poste=(["position", "ps_band", "age_band", "n", "p25", "median", "p75", "mini", "maxi"], cases))


def cas_plan_19_11():
    """19/11 : les deux lignes fausses du plan du 19/11 et les règles qui les corrigent (police ancienne, ajustement au poste, n par poste,
    règle 14)."""
    import aujourdhui_sources as src
    d = marche(**_plan_19())
    v = ej.ventes_du_jour(d, O, 1.0)
    yield "vente : remplaçant au même poste (Baron PG → Boyer, pas Durand SF), écart d'ajustement", \
        [(x["nom"], x["remplacant"], round(x["ecart"], 1)) for x in v] == [("Nolan Baron", "Naël Boyer", -3.6)]
    yield "vente : fourchette min à max du poste affichée avec la médiane", "médiane du poste 400 000, fourchette 290 000 à 910 000" in ej.texte_transfert(v[0], O)
    with __import__("tempfile").TemporaryDirectory() as tmp:
        (Path(tmp) / "police-2026-11-17.md").write_text("## vente — Nolan Baron\n- Décision : ne pas vendre Nolan Baron\n", encoding="utf-8")
        refus = src.lire_refus_police(tmp, dt.date(2026, 11, 19))
        trop_vieux = src.lire_refus_police(tmp, dt.date(2026, 12, 2))
        (Path(tmp) / "police-2026-11-18.md").write_text("- Décision : vendre Nolan Baron, minimum 400 000\n", encoding="utf-8")
        leve = src.lire_refus_police(tmp, dt.date(2026, 11, 19))
    yield "police du 17/11 « ne pas vendre Nolan Baron » vaut encore le 19/11", refus == "ne pas vendre nolan baron" \
        and not [l for l in ej.lignes_transferts(d, 300000, 1.0, "", refus=refus) if "Nolan Baron" in l["consigne"] and "vente" in l["consigne"]]
    yield "police : verdict de plus de 14 jours oublié, verdict contraire plus récent le lève", trop_vieux == "" and leve == ""
    fontana = ["f1", "Fontana", "SG", 24, 52, 100000, "2026-11-20T10:00:00", 10000, None, "SG", 51.7]
    gain = ["f2", "Tom Gain", "SG", 24, 50, 100000, "2026-11-20T10:00:00", 10000, None, "SG", 58.1]
    ann = (ANN + ["height_cm", "best_slot", "best_fit"], [fontana, gain])
    cas = (["position", "ps_band", "age_band", "n", "p25", "median", "p75", "mini", "maxi"], [["SG", 50, "22-25", 4, 100000, 200000, 300000, 90000, 400000]])
    r = ej.offres_du_jour(dict(d, annonces_actives=ann, prix_cases_poste=cas), O, 600000)
    yield "amélioration : Fontana (note 52, ajustement SG 51,7 contre 56,1 pour Bonnet) → aucune ligne ; Tom Gain (+2,0) → ligne", \
        [x["nom"] for x in r["offres"]] == ["Tom Gain"]
    t = ej.texte_transfert(r["offres"][0], O)
    yield "amélioration : gain d'ajustement et coût par point gagné écrits", "ajustement SG 58,1 contre 56,1 pour Thibault Bonnet" in t \
        and "gain 2,0 (≥ 1,0)" in t and "coût par point gagné 150 000" in t
    d2 = dict(d, prix_cases_poste=(cas[0], [["PG", 45, "22-25", 2, 300000, 400000, 500000, 290000, 910000]]))
    bilan = {}
    yield "meneur sans n suffisant (2 ventes PG) : prix inconnu, aucune vente", ej.ventes_du_jour(d2, O, 1.0, "", bilan) == [] \
        and any("prix inconnu" in k for k in bilan)
    jeune = lambda tm: [x["nom"] for x in ej.ventes_du_jour(dict(d, tests_marche=(["player_id", "potentiel"], tm)), O, 1.0, "ne pas vendre nolan baron")]
    yield "règle 14 : jeune de 17 ans non titulaire sans test → aucune vente ; test Low → vente possible", jeune([]) == [] and jeune([["jeune", "Low"]]) == ["Tim Jeune"]


def cas_priorite_export_match():
    """19/11 : export de la page d'un de nos matchs de ligue joués = 🟧 au minimum, 🟥 plus de 24 h après le match, au-dessus d'un amical."""
    pret = match(apercu_at=T_APERCU, fiche=FICHE, ecran=ECRAN)
    p = lambda ev, m: ej.etat_evenement(ev, CFG, m)  # noqa: E731
    juste = p(pret, dt.datetime(2026, 11, 18, 22, 30))
    tard = p(pret, dt.datetime(2026, 11, 19, 23, 0))
    perime = p(dict(pret, maj_at=dt.datetime(2026, 11, 16, 9, 0)), dt.datetime(2026, 11, 18, 22, 30))
    amical = p(match(genre="amical", fiche=FICHE, ecran=ECRAN), dt.datetime(2026, 11, 18, 22, 30))
    yield "export de match de ligue joué : 🟧 au minimum, même avec des données périmées", juste["prochain"] == "joue" and juste["priorite"] == 2 \
        and perime["priorite"] == 2
    yield "export de match de ligue joué : 🟥 plus de 24 h après le match", tard["prochain"] == "joue" and tard["priorite"] == 1
    yield "export d'un amical joué : sous celui de la ligue", amical["prochain"] == "joue" and amical["priorite"] > juste["priorite"]


def cas_equipe_encheres():
    """19/11 : Équipe (effectif, salaires, contrats) toutes les 168 h ; Mes enchères seulement avec une enchère ouverte ou proposée."""
    cols = ["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"]
    base = [(8, "Marché (enchères)", "x", "2026-11-17T09:00:00", 1, "🟩"), (13, "Personnel", "x", "2026-11-14T09:00:00", 73, "🟩"),
            (9, "Mes enchères", "x", "2026-11-13T10:25:53", 96, "🟧")]
    h = ("historique_global", (["derniere_paris"], [("2026-11-17T08:00:00",)]))
    d = lambda eq: donnees(**{"gold.bv_exports_state": (cols, base + [(1, "Équipe (aperçu, joueurs)", "x", "2026-11-10T09:00:00", eq, "🟧")]),  # noqa: E731
                             h[0]: h[1], **FRAIS_19})
    ecrans = lambda ls: [l["ecran"] for l in ls]  # noqa: E731
    yield "Équipe : export de 169 h → ligne ; 167 h → rien", "Équipe (aperçu, joueurs)" in ecrans(ej.exports_periodiques(d(169), CFG, MAINT)) \
        and "Équipe (aperçu, joueurs)" not in ecrans(ej.exports_periodiques(d(167), CFG, MAINT))
    yield "Mes enchères : aucune enchère ouverte ni proposée → rien", "Mes enchères" not in ecrans(ej.exports_periodiques(d(1), CFG, MAINT))
    a = ej.exports_periodiques(d(1), CFG, MAINT, enchere_proposee=True)
    yield "Mes enchères : enchère ouverte ou proposée, export de 96 h → ligne avec l'âge", [l["consigne"] for l in a if l["ecran"] == "Mes enchères"] \
        == ["exporte la page Mes enchères — export de 96 h"]


CAS = [cas_config, cas_equipe_encheres, cas_priorite_export_match, cas_plan_19_11, cas_regle_jeunes, cas_niveau_e1, cas_agents, cas_personnel, cas_lien_fiche, cas_preset_adversaire, cas_rotation_illisible, cas_prix_inconnu, cas_priorite_capacite, cas_offres, cas_ventes, cas_affichage_transferts, cas_enchere_max, cas_etats_ligue, cas_etats_amical, cas_ligne, cas_hors_match, cas_horizon_et_completude, cas_exports, cas_controles,
       cas_construire, cas_deux_amicaux_meme_jour, cas_exports_periodiques, cas_exports_ligue_19, cas_academie_decision, cas_rejeu, cas_branchement]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
