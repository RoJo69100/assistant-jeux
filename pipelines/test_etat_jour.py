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


CAS = [cas_config, cas_etats_ligue, cas_etats_amical, cas_ligne, cas_hors_match, cas_horizon_et_completude, cas_exports]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
