import requests
import json
import os
from datetime import datetime

GAMES_TO_RUN = ["DerbyManager","BasketVibe","WorldAces","SixZeroLeague","KickOffBoss","VM","FinalWhistle","BuzzerBeater","RedZoneAction","Hardwood","FromThePavillon","FMP","HockeyNation","Perso"]

# --- CONFIGURATION ---
def _load_token():
    """DISCORD_TOKEN : variable d'environnement ou ligne du .env à la racine du projet (jamais dans le code)."""
    if os.environ.get("DISCORD_TOKEN"):
        return os.environ["DISCORD_TOKEN"]
    env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            if line.startswith("DISCORD_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("DISCORD_TOKEN manquant : l'ajouter au .env (voir .env.example)")


TOKEN = _load_token()

# Chemins de base mis à jour
BASE_DATA_DIR = r"C:\dev\assistant-jeux\data"
DISCORD_DATA_DIR = os.path.join(BASE_DATA_DIR, "discord")

# Fichier tracker situé dans C:\dev\assistant-jeux\data
TRACKER_FILE = os.path.join(BASE_DATA_DIR, "last_exports_tracker.json")

# Taille maximale par fichier texte (2.5 Mo pour sécurité avec NotebookLM)
MAX_FILE_SIZE_BYTES = 2.5 * 1024 * 1024

# Organisation par jeu et par canaux
GAMES_CONFIG = {
    "BasketVibe": {
        "base_filename": "discord_BasketVibe",
        "force_reset": False,
        "channels": [
            "1510571166857953352",
            "1539663351292887090",
            "1521611628326424606",
            "1526656853495255050",
            "1523685558331773068",
            "1527703000041263215",
            "1527691744903168222",
            "1527691744903168222",
            "1527691999224922162",
            "1527704270558990387",
            "1527726380081483979",
            "1534935676242624613",
            "1547637850663559188"
        ]
    },
    "WorldAces": {
        "base_filename": "discord_WorldAces",
        "force_reset": False,
        "channels": [
            "1512222819981725756",
            "1512222994083221696",
            "1516171190018900209",
            "1529972954840961034",
            "1542897443123896330",
            "1512432773238100028",
            "1512482097212948752",
            "1517571783123927092",
            "1516025736090095746"
        ]
    },
    "DerbyManager": {
        "base_filename": "discord_DerbyManager",
        "force_reset": False,
        "channels": [
            "1105756654366117938",
            "1102900630080733184",
            "1109060986582872114",
            "1102896771878879263",
            "1102892256630943754",
            "530678438164430862",
            "1102900729116635178",
            "1109404600869605426",
            "1102892022005780541",
            "1102891896038236211",
            "1102891809614610473",
            "1102891926371438623",
            "1102891976120082442",
            "1554105695010422806"
        ]
    },
    "SixZeroLeague": {
        "base_filename": "discord_SixZeroLeague",
        "force_reset": False,
        "channels": [
            "1549040122270584973",
            "1492995699217006598",
            "1549747527195299971",
            "1492995699217006600"
        ]
    },
    "KickOffBoss": {
        "base_filename": "discord_KickOffBoss",
        "force_reset": False,
        "channels": [
            "1249689955400290304",
            "1242874530846867537",
            "1248014601308606604",
            "1529848048992256191",
            "1248030856526823439",
            "1248017485358436534",
            "1248017773729419329",
            "1248017851504394414",
            "1326537584448507915",
            "1270105062341087272",
            "1270105230100402216",
            "1270105765536993383",
            "1270112167982530590",
            "1272656817348153354",
            "1273298699673665538",
            "1278066962374721608"
        ]
    },
    "VM": {
        "base_filename": "discord_VM",
        "force_reset": False,
        "channels": [
            "802965807072018436",
            "1267142241705787454",
            "1266767848215150623",
            "1281216948146933812",
            "1281748148091355297",
            "1477404324555526286"
        ]
    },
    "FinalWhistle": {
        "base_filename": "discord_FinalWhistle",
        "force_reset": False,
        "channels": [
            "710088497763057698",
            "710100750822408232",
            "710100928333611120",
            "737724784963485826",
            "710101709807943811",
            "710394966496641086",
            "722760513016299590"
        ]
    },
    "BuzzerBeater": {
        "base_filename": "discord_BuzzerBeater",
        "force_reset": False,
        "channels": [
            "1130517733201678439",
            "1132657055392600094",
            "1130875035515625664",
            "1131323953407856791",
            "1131324341431316590",
            "1138021897095884833",
            "1130519912880803980",
            "1415390632846954587",
            "1144195012037460059",
            "1130518556451291176",
            "1130838613404438548",
            "1169673914771836998",
            "1173219705146855514",
            "1172179727734296676",
            "1311744494433079296",
            "1339295444165066876",
            "1346158819155378248",
            "1130518169669337159",
            "1139482570455793734",
            "1132675613824659639",
            "1132676423790903296",
            "1132676100842082425"
        ]
    },
    "RedZoneAction": {
        "base_filename": "discord_RZA",
        "force_reset": False,
        "channels": [
            "1422755014765576254",
            "1422755620196712508"
        ]
    },
    "Hardwood": {
        "base_filename": "discord_HW",
        "force_reset": False,
        "channels": [
            "410154228292780042",
            "567195205430804511",
            "595769726597070869",
            "512865316825464838",
            "512865299381616651"
        ]
    },
    "FromThePavillon": {
        "base_filename": "discord_FromThePavillon",
        "force_reset": False,
        "channels": [
            "481436738460450816",
            "1538850317398052874",
            "1435882060618399745",
            "1498476434295885987",
            "1542066220692545557"
        ]
    },
    "FMP": {
        "base_filename": "discord_FMP",
        "force_reset": False,
        "channels": [
            "1020944123529797682",
            "1021108387473264780",
            "1020606215044202527",
            "984750914541875212",
            "1429524722877599855",
            "1194323501847433356",
            "1428763719919341780",
            "1103623621345300510",
            "1213135768848175154",
            "1103798214483779654",
            "1095684907050737784",
            "1192887069106765924"
        ]
    },
    "HockeyNation": {
        "base_filename": "discord_HN",
        "force_reset": False,
        "channels": [
            "1267768929519013950",
            "922093338595831811",
            "922094392163041280",
            "922453947095064577",
            "1429524722877599855",
            "925405608641974352"
        ]
    },
    "Perso": {
        "base_filename": "discord_Perso",
        "force_reset": False,  # 👈Passe cette valeur à True
        "channels": [
            "1461389039419658435",
            "1422297287769587766",
            "1285875405189943306",
        ]
    },
}

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_tracker(tracker_data):
    # Crée le dossier C:\dev\assistant-jeux\data si nécessaire
    os.makedirs(BASE_DATA_DIR, exist_ok=True)
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(tracker_data, f, indent=4)

def get_channel_name(channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json().get("name", channel_id)
    return channel_id

def save_chunks_to_files(game_name, base_name, messages_list):
    """Découpe les messages en fichiers de 2.5 Mo max dans le dossier du jeu."""
    # Création automatique du dossier du jeu : C:\dev\assistant-jeux\data\discord\<game_name>
    game_dir = os.path.join(DISCORD_DATA_DIR, game_name)
    os.makedirs(game_dir, exist_ok=True)

    part_number = 1
    current_chunk = []
    current_size = 0
    generated_files = []

    for msg in messages_list:
        msg_bytes = len(msg.encode('utf-8')) + 1  # +1 pour le saut de ligne
        if current_size + msg_bytes > MAX_FILE_SIZE_BYTES and current_chunk:
            file_path = os.path.join(game_dir, f"{base_name}_part{part_number}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(current_chunk))
            generated_files.append(file_path)
            
            part_number += 1
            current_chunk = []
            current_size = 0

        current_chunk.append(msg)
        current_size += msg_bytes

    if current_chunk:
        file_path = os.path.join(game_dir, f"{base_name}_part{part_number}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(current_chunk))
        generated_files.append(file_path)

    return generated_files

def export_game_data(game_name, config, tracker):
    print(f"\n==========================================")
    print(f"🎮 DÉBUT DE L'EXPORT : {game_name}")
    print(f"==========================================")
    
    full_export = []
    
    for channel_id in config["channels"]:
        channel_name = get_channel_name(channel_id)
        last_seen_id = None if config.get("force_reset", False) else tracker.get(channel_id, None)
        
        print(f"\n📥 Canal #{channel_name} ({channel_id})...")
        limit = 100
        before = None
        channel_messages = []
        newest_msg_id = None
        stop_fetching = False

        while not stop_fetching:
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
            if before:
                url += f"&before={before}"
                
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                print(f"❌ Erreur {res.status_code}: {res.text}")
                break
                
            messages = res.json()
            if not messages:
                break

            if not newest_msg_id and len(messages) > 0:
                newest_msg_id = messages[0]["id"]

            for msg in messages:
                if last_seen_id and msg["id"] == last_seen_id:
                    stop_fetching = True
                    break

                author = msg["author"]["username"]
                content = msg["content"].replace("\n", " ")
                
                raw_time = msg["timestamp"]
                try:
                    dt = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    formatted_time = raw_time
                
                if content.strip():
                    channel_messages.append(f"[{formatted_time}] {author} : {content}")

            before = messages[-1]["id"]
            print(f"  -> {len(channel_messages)} messages récupérés...")

        if channel_messages:
            channel_messages.reverse()
            full_export.append(f"==========================================")
            full_export.append(f"=== CANAL : #{channel_name} ===")
            full_export.append(f"==========================================")
            full_export.extend(channel_messages)
            
            if newest_msg_id:
                tracker[channel_id] = newest_msg_id

    if full_export:
        files = save_chunks_to_files(game_name, config["base_filename"], full_export)
        print(f"\n✅ Export terminé ! Fichier(s) découpé(s) généré(s) :")
        for f in files:
            print(f"  👉 {f}")
    else:
        print(f"\nℹ️ Aucun nouveau message à ajouter pour {game_name}.")

if __name__ == "__main__":
    tracker = load_tracker()
    for game_name in GAMES_TO_RUN:
        if game_name in GAMES_CONFIG:
            export_game_data(game_name, GAMES_CONFIG[game_name], tracker)
    save_tracker(tracker)
    print("\n🎉 Terminé !")