#!/usr/bin/env python3
"""
Export final JSON snapshot of sierra28k dataset
Local-only version (no Turso push)
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "sierra28k.db")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "sierra28k_snapshot.json")

def export_snapshot():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    snapshot = {
        "metadata": {
            "dataset_name": "sierra28k",
            "description": "Sierra Nevada Tourism Research Dataset",
            "exported_at": datetime.now().isoformat(),
            "version": "1.0.0"
        },
        "zones": [],
        "places": [],
        "activities": [],
        "sources": []
    }
    
    # Export zones
    cur.execute("SELECT * FROM zones ORDER BY id")
    for row in cur.fetchall():
        snapshot["zones"].append({
            "id": row["id"],
            "name": row["name"],
            "region": row["region"],
            "description": row["description"],
            "validated": bool(row["validated"]),
            "validation_notes": row["validation_notes"]
        })
    
    # Export places
    cur.execute("SELECT * FROM places ORDER BY id")
    for row in cur.fetchall():
        snapshot["places"].append({
            "id": row["id"],
            "zone_id": row["zone_id"],
            "name": row["name"],
            "place_type": row["place_type"],
            "lat": row["lat"],
            "lng": row["lng"],
            "address": row["address"],
            "parking_notes": row["parking_notes"],
            "kid_friendly": bool(row["kid_friendly"])
        })
    
    # Export activities
    cur.execute("SELECT * FROM activities ORDER BY id")
    for row in cur.fetchall():
        snapshot["activities"].append({
            "id": row["id"],
            "place_id": row["place_id"],
            "activity_type": row["activity_type"],
            "difficulty": row["difficulty"],
            "distance_km": row["distance_km"],
            "elevation_gain_m": row["elevation_gain_m"],
            "notes": row["notes"],
            "run_type": row["run_type"]
        })
    
    # Export sources
    cur.execute("SELECT * FROM sources ORDER BY id")
    for row in cur.fetchall():
        snapshot["sources"].append({
            "id": row["id"],
            "place_id": row["place_id"],
            "url": row["url"],
            "source_type": row["source_type"],
            "retrieved_at": row["retrieved_at"]
        })
    
    # Calculate summary stats
    snapshot["summary"] = {
        "total_zones": len(snapshot["zones"]),
        "total_places": len(snapshot["places"]),
        "total_activities": len(snapshot["activities"]),
        "total_sources": len(snapshot["sources"]),
        "activities_by_type": {},
        "places_by_zone": {}
    }
    
    # Activity counts
    for activity in snapshot["activities"]:
        atype = activity["activity_type"]
        snapshot["summary"]["activities_by_type"][atype] = \
            snapshot["summary"]["activities_by_type"].get(atype, 0) + 1
    
    # Places by zone
    for place in snapshot["places"]:
        zid = place["zone_id"]
        snapshot["summary"]["places_by_zone"][zid] = \
            snapshot["summary"]["places_by_zone"].get(zid, 0) + 1
    
    # Write JSON
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("=" * 70)
    print("FINAL JSON SNAPSHOT EXPORTED")
    print("=" * 70)
    print(f"\nFile: {OUTPUT_PATH}")
    print(f"Size: {os.path.getsize(OUTPUT_PATH):,} bytes")
    print(f"\nContents:")
    print(f"  Zones: {snapshot['summary']['total_zones']}")
    print(f"  Places: {snapshot['summary']['total_places']}")
    print(f"  Activities: {snapshot['summary']['total_activities']}")
    print(f"  Sources: {snapshot['summary']['total_sources']}")
    print(f"\nActivity Types:")
    for atype, count in sorted(snapshot["summary"]["activities_by_type"].items(), 
                                key=lambda x: x[1], reverse=True):
        print(f"  {atype}: {count}")
    
    conn.close()
    print(f"\n✓ Snapshot ready for use")
    print(f"\nDatasette: http://localhost:8001")

if __name__ == "__main__":
    export_snapshot()
