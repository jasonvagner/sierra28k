#!/usr/bin/env python3
"""Shared utility: insert a places list into sierra28k.db for a given zone_id."""
import sqlite3, os
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), "sierra28k.db")

def insert_zone(zone_id: int, places: list) -> tuple:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    pc = ac = sc = 0
    for p in places:
        cur.execute(
            "INSERT INTO places (zone_id,name,place_type,lat,lng,address,parking_notes,kid_friendly) VALUES (?,?,?,?,?,?,?,?)",
            (zone_id, p["name"], p["place_type"], p.get("lat"), p.get("lng"),
             p.get("address"), p.get("parking_notes"), 1 if p.get("kid_friendly") else 0)
        )
        pid = cur.lastrowid; pc += 1
        for a in p.get("activities", []):
            cur.execute(
                "INSERT INTO activities (place_id,activity_type,difficulty,distance_km,elevation_gain_m,notes,run_type) VALUES (?,?,?,?,?,?,?)",
                (pid, a["activity_type"], a.get("difficulty"), a.get("distance_km"),
                 a.get("elevation_gain_m"), a.get("notes"), a.get("run_type"))
            )
            ac += 1
        cur.execute(
            "INSERT INTO sources (place_id,url,source_type,retrieved_at) VALUES (?,?,?,?)",
            (pid, p["source_url"], p["source_type"], datetime.utcnow().isoformat())
        )
        sc += 1
    conn.commit(); conn.close()
    return pc, ac, sc

def zone_summary(zone_id: int, name: str):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    pc = cur.execute("SELECT COUNT(*) FROM places WHERE zone_id=?", (zone_id,)).fetchone()[0]
    ac = cur.execute("SELECT COUNT(*) FROM activities a JOIN places p ON a.place_id=p.id WHERE p.zone_id=?", (zone_id,)).fetchone()[0]
    sc = cur.execute("SELECT COUNT(*) FROM sources s JOIN places p ON s.place_id=p.id WHERE p.zone_id=?", (zone_id,)).fetchone()[0]
    breakdown = cur.execute(
        "SELECT a.activity_type, COUNT(*) FROM activities a JOIN places p ON a.place_id=p.id WHERE p.zone_id=? GROUP BY a.activity_type",
        (zone_id,)
    ).fetchall()
    conn.close()
    print(f"\n{'='*50}")
    print(f"Zone {zone_id}: {name}")
    print(f"  Places: {pc} | Activities: {ac} | Sources: {sc}")
    for atype, cnt in sorted(breakdown):
        print(f"    {atype:15s} {cnt}")
    print(f"{'='*50}")
