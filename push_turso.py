#!/usr/bin/env python3
"""Push sierra28k.db to Turso via HTTP API."""
import sqlite3, json, urllib.request, os, sys

# Load .env manually
env_path = os.path.join(os.path.dirname(__file__), '.env')
env = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

TOKEN = env['TURSO_AUTH_TOKEN']
DB_URL = "https://sierra28kresearch-jvagner.aws-us-west-2.turso.io"
DB_PATH = os.path.join(os.path.dirname(__file__), 'sierra28k.db')

def execute_turso(statements: list[str]) -> dict:
    """Execute a batch of SQL statements via Turso HTTP API v2/pipeline."""
    requests_payload = [{"type": "execute", "stmt": {"sql": s}} for s in statements]
    requests_payload.append({"type": "close"})
    body = json.dumps({"requests": requests_payload}).encode()
    req = urllib.request.Request(
        f"{DB_URL}/v2/pipeline",
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())

def execute_batch(stmts, label=""):
    result = execute_turso(stmts)
    errors = [r for r in result.get("results", []) if r.get("type") == "error"]
    if errors:
        print(f"  ERROR in {label}: {errors[0]}")
        sys.exit(1)
    print(f"  ✓ {label} ({len(stmts)} statements)")
    return result

def quote(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("=== Pushing sierra28k to Turso ===\n")

    # 1. Drop and recreate schema
    print("Step 1: Schema setup")
    schema_stmts = [
        "DROP TABLE IF EXISTS sources",
        "DROP TABLE IF EXISTS activities",
        "DROP TABLE IF EXISTS places",
        "DROP TABLE IF EXISTS zones",
        """CREATE TABLE IF NOT EXISTS zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            region TEXT NOT NULL,
            description TEXT,
            validated INTEGER NOT NULL DEFAULT 0,
            validation_notes TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_id INTEGER NOT NULL REFERENCES zones(id),
            name TEXT NOT NULL,
            place_type TEXT NOT NULL,
            lat REAL,
            lng REAL,
            address TEXT,
            parking_notes TEXT,
            kid_friendly INTEGER NOT NULL DEFAULT 0,
            image_url TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id INTEGER NOT NULL REFERENCES places(id),
            activity_type TEXT NOT NULL,
            difficulty INTEGER,
            distance_km REAL,
            elevation_gain_m REAL,
            notes TEXT,
            run_type TEXT,
            best_months TEXT,
            conditions_note TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id INTEGER NOT NULL REFERENCES places(id),
            url TEXT NOT NULL,
            source_type TEXT NOT NULL,
            retrieved_at TEXT NOT NULL DEFAULT (datetime('now'))
        )""",
        "CREATE INDEX IF NOT EXISTS idx_places_zone_id ON places(zone_id)",
        "CREATE INDEX IF NOT EXISTS idx_activities_place_id ON activities(place_id)",
        "CREATE INDEX IF NOT EXISTS idx_sources_place_id ON sources(place_id)",
        "CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(activity_type)",
    ]
    execute_batch(schema_stmts, "schema drop+create+index")

    # 2. Zones
    print("\nStep 2: Zones")
    zones = cur.execute("SELECT * FROM zones ORDER BY id").fetchall()
    stmts = []
    for z in zones:
        stmts.append(
            f"INSERT INTO zones (id, name, region, description, validated, validation_notes) "
            f"VALUES ({z['id']}, {quote(z['name'])}, {quote(z['region'])}, "
            f"{quote(z['description'])}, {z['validated']}, {quote(z['validation_notes'])})"
        )
    execute_batch(stmts, f"{len(zones)} zones")

    # 3. Places (batch by 50)
    print("\nStep 3: Places")
    places = cur.execute("SELECT * FROM places ORDER BY id").fetchall()
    BATCH = 50
    for i in range(0, len(places), BATCH):
        chunk = places[i:i+BATCH]
        stmts = []
        for p in chunk:
            stmts.append(
                f"INSERT INTO places (id, zone_id, name, place_type, lat, lng, address, parking_notes, kid_friendly, image_url) "
                f"VALUES ({p['id']}, {p['zone_id']}, {quote(p['name'])}, {quote(p['place_type'])}, "
                f"{quote(p['lat'])}, {quote(p['lng'])}, {quote(p['address'])}, "
                f"{quote(p['parking_notes'])}, {p['kid_friendly']}, {quote(p['image_url'])})"
            )
        execute_batch(stmts, f"places {i+1}–{i+len(chunk)}")

    # 4. Activities (batch by 50)
    print("\nStep 4: Activities")
    acts = cur.execute("SELECT * FROM activities ORDER BY id").fetchall()
    for i in range(0, len(acts), BATCH):
        chunk = acts[i:i+BATCH]
        stmts = []
        for a in chunk:
            stmts.append(
                f"INSERT INTO activities (id, place_id, activity_type, difficulty, distance_km, elevation_gain_m, notes, run_type, best_months, conditions_note) "
                f"VALUES ({a['id']}, {a['place_id']}, {quote(a['activity_type'])}, "
                f"{quote(a['difficulty'])}, {quote(a['distance_km'])}, {quote(a['elevation_gain_m'])}, "
                f"{quote(a['notes'])}, {quote(a['run_type'])}, {quote(a['best_months'])}, {quote(a['conditions_note'])})"
            )
        execute_batch(stmts, f"activities {i+1}–{i+len(chunk)}")

    # 5. Sources (batch by 50)
    print("\nStep 5: Sources")
    srcs = cur.execute("SELECT * FROM sources ORDER BY id").fetchall()
    for i in range(0, len(srcs), BATCH):
        chunk = srcs[i:i+BATCH]
        stmts = []
        for s in chunk:
            stmts.append(
                f"INSERT INTO sources (id, place_id, url, source_type, retrieved_at) "
                f"VALUES ({s['id']}, {s['place_id']}, {quote(s['url'])}, "
                f"{quote(s['source_type'])}, {quote(s['retrieved_at'])})"
            )
        execute_batch(stmts, f"sources {i+1}–{i+len(chunk)}")

    conn.close()

    # 6. Verify remote counts
    print("\nStep 6: Verification")
    for table in ['zones', 'places', 'activities', 'sources']:
        result = execute_turso([f"SELECT COUNT(*) as cnt FROM {table}"])
        cnt = result['results'][0]['response']['result']['rows'][0][0]['value']
        print(f"  {table}: {cnt}")

    print("\n✓ Push complete")

if __name__ == "__main__":
    main()
