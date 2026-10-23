"""Import des exports Discord (DiscordChatExporter, format texte) dans bronze.discord_messages.

Usage : python pipelines/import_discord.py basketvibe [--tz Europe/Paris] [--dry-run]

Lit tous les .txt de data/discord/<jeu>/. Réimporter un fichier est sans effet :
la base ignore les messages déjà présents (même salon, auteur, minute et texte).
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
BATCH = 500

RULE = re.compile(r"^={20,}$")
MESSAGE = re.compile(r"^\[(\d{2}/\d{2}/\d{4} \d{2}:\d{2})\] (.+)$")
SECTION = re.compile(r"^\{([A-Za-z][A-Za-z ]*)\}$")
FOOTER = re.compile(r"^Exported \d+ message\(s\)$")


CANAL = re.compile(r"^=== CANAL : (.+?) ===$")
CANAL_MESSAGE = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+?) : (.*)$")


def parse_canal(path: Path, game: str, tz: ZoneInfo, channel: str | None = None) -> list[dict]:
    """Format de userscripts/export_discord.py : `=== CANAL : #salon ===`, puis `[AAAA-MM-JJ HH:MM] auteur : texte`."""
    items, msg = [], None

    def close():
        nonlocal msg
        if msg is None:
            return
        content = "\n".join(msg["lines"]).strip()
        posted = datetime.strptime(msg["posted"], "%Y-%m-%d %H:%M").replace(tzinfo=tz)
        items.append({
            "game": game,
            "guild": game,
            "channel": channel,
            "author": msg["author"],
            "posted_local": posted.strftime("%d/%m/%Y %H:%M"),
            "posted_at": posted.isoformat(),
            "source_file": path.name,
            "payload": {"content": content, "sections": {}, "raw": content},
        })
        msg = None

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if RULE.match(line):
            continue
        c = CANAL.match(line)
        if c:
            close()
            channel = c.group(1).strip()
            continue
        m = CANAL_MESSAGE.match(line)
        if m and channel:
            close()
            msg = {"posted": m.group(1), "author": m.group(2).strip(), "lines": [m.group(3)]}
        elif msg is not None:
            msg["lines"].append(line)
    close()
    return items


def parse(path: Path, game: str, tz: ZoneInfo, carry: str | None = None) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    # fichier sans en-tête de salon (suite d'un export coupé à 2,5 Mo) : salon du fichier précédent
    first = next((l for l in text.splitlines() if l.strip()), "")
    if re.search(r"^=== CANAL : ", text, re.M) or (carry and CANAL_MESSAGE.match(first)):
        return parse_canal(path, game, tz, carry)
    lines = text.splitlines()
    items, guild, channel, msg = [], None, None, None
    in_header = False

    def close():
        nonlocal msg
        if msg is None:
            return
        body, sections, current = [], {}, None
        for line in msg["lines"]:
            m = SECTION.match(line)
            if m:
                current = m.group(1)
                sections[current] = []
            elif current:
                sections[current].append(line)
            else:
                body.append(line)
        posted = datetime.strptime(msg["posted_local"], "%d/%m/%Y %H:%M").replace(tzinfo=tz)
        items.append({
            "game": game,
            "guild": guild,
            "channel": channel,
            "author": msg["author"],
            "posted_local": msg["posted_local"],
            "posted_at": posted.isoformat(),
            "source_file": path.name,
            "payload": {
                "content": "\n".join(body).strip(),
                "sections": {k: "\n".join(v).strip() for k, v in sections.items()},
                "raw": "\n".join(msg["lines"]).strip(),
            },
        })
        msg = None

    for line in lines:
        if RULE.match(line):
            close()
            in_header = not in_header
            continue
        if in_header:
            if line.startswith("Guild: "):
                guild = line[7:].strip()
            elif line.startswith("Channel: "):
                channel = line[9:].strip()
            continue
        m = MESSAGE.match(line)
        if m and channel:
            close()
            msg = {"posted_local": m.group(1), "author": m.group(2).strip(), "lines": []}
        elif msg is not None and not FOOTER.match(line):
            msg["lines"].append(line)
    close()
    return items


def send(items: list[dict]) -> int:
    url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/rpc/ingest_discord_messages"
    key = os.environ["SUPABASE_PUBLISHABLE_KEY"]
    data = json.dumps({"p_token": os.environ["INGEST_TOKEN"], "p_items": items}).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return int(json.load(r))
    except urllib.error.HTTPError as e:
        sys.exit(f"Erreur Supabase {e.code} : {e.read().decode(errors='replace')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game")
    ap.add_argument("--tz", default="Europe/Paris", help="fuseau horaire du PC qui a fait l'export")
    ap.add_argument("--dry-run", action="store_true", help="analyser sans envoyer")
    ap.add_argument("--only", help="ne traiter que ce fichier du dossier (nom exact)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows en cp1252

    load_dotenv(ROOT / ".env")
    folder = ROOT / "data" / "discord" / args.game
    files = sorted(folder.glob("*.txt"))
    if args.only:
        files = [f for f in files if f.name == args.only]
    if not files:
        sys.exit(f"Aucun fichier .txt dans {folder}")

    tz = ZoneInfo(args.tz)
    carry = None
    for f in files:
        items = parse(f, args.game, tz, carry)
        if items:
            carry = items[-1]["channel"]
        channels = {i["channel"] for i in items}
        if args.dry_run:
            print(f"{f.name} : {len(items)} messages, {len(channels)} salons (non envoyé)")
            continue
        inserted = sum(send(items[i:i + BATCH]) for i in range(0, len(items), BATCH))
        print(f"{f.name} : {len(items)} messages lus, {inserted} nouveaux en bronze, {len(channels)} salons")


if __name__ == "__main__":
    main()
