#!/usr/bin/env python3
"""Phase 3 enrichment: add 1 bouldering place to each zone at minimum (5)."""
import sys; sys.path.insert(0, '.')
from db_insert import insert_zone, zone_summary

places = [
    # NORTH LAKE TAHOE — add Big Chief Crag bouldering
    # Real granite formation at base of Alpine Meadows Rd, Tahoe National Forest
    {
        "name": "Big Chief Crag — Bouldering Base",
        "place_type": "starting_point",
        "lat": 39.1831, "lng": -120.2508,
        "address": "Alpine Meadows Rd, Olympic Valley, CA 96146",
        "parking_notes": "Roadside pullout on Alpine Meadows Rd just off Hwy 89, ~0.3 mi from junction. Free, no permit. Tahoe National Forest land.",
        "kid_friendly": False,
        "activities": [
            {
                "activity_type": "bouldering",
                "difficulty": 3,
                "distance_km": 0.5,
                "elevation_gain_m": 40,
                "notes": "Granite crag at the base of Alpine Meadows Road with established bouldering problems on the lower cliffs. Part of the Tahoe National Forest. Mix of V0–V6 problems on solid Sierra granite. Developed by local Tahoe climbers; best accessed via short scramble from roadside pullout. Often quieter than Donner Summit on weekends. Year-round access when snow-free (May–Oct typical). No permit required.",
                "run_type": None,
            }
        ],
        "source_url": "https://www.mountainproject.com/area/105798796/big-chief",
        "source_type": "web_search",
    },

    # SOUTH LAKE TAHOE — add Pie Shop Crag bouldering
    # Established bouldering/sport area directly below Lover's Leap on Hwy 50
    {
        "name": "Pie Shop Crag — Bouldering",
        "place_type": "starting_point",
        "lat": 38.8303, "lng": -120.1472,
        "address": "Hwy 50 (US-50), Twin Bridges, CA 95735",
        "parking_notes": "Roadside pullout on south side of US-50 at Twin Bridges, El Dorado National Forest. Free, no fee. 0.2 mi walk to Pie Shop wall.",
        "kid_friendly": False,
        "activities": [
            {
                "activity_type": "bouldering",
                "difficulty": 2,
                "distance_km": 0.4,
                "elevation_gain_m": 20,
                "notes": "Pie Shop is a popular El Dorado National Forest granite crag at the base of the Lover's Leap formation on US-50, with accessible bouldering on the lower walls. Problems range V0–V5, on excellent featured Sierra granite. A shorter approach than the main Lover's Leap routes makes this a convenient session stop. Also a key transition wall for beginners moving from bouldering to sport climbing. Best season May–October. No permit required.",
                "run_type": None,
            }
        ],
        "source_url": "https://www.mountainproject.com/area/105731688/lovers-leap",
        "source_type": "web_search",
    },

    # TUOLUMNE MEADOWS — add Pywiack Dome bouldering
    # Granite dome NE of Tenaya Lake, classic Tuolumne friction bouldering
    {
        "name": "Pywiack Dome — Tuolumne Bouldering",
        "place_type": "starting_point",
        "lat": 37.8327, "lng": -119.4620,
        "address": "Tenaya Lake East Parking, Tioga Rd (Hwy 120), Yosemite NP, CA 95389",
        "parking_notes": "East Tenaya Lake picnic lot on Tioga Rd. Free with park entrance fee. 0.4 mi walk to Pywiack Dome base. Summer shuttle stop nearby.",
        "kid_friendly": False,
        "activities": [
            {
                "activity_type": "bouldering",
                "difficulty": 2,
                "distance_km": 0.8,
                "elevation_gain_m": 50,
                "notes": "Pywiack Dome is a glacier-polished granite dome east of Tenaya Lake in Tuolumne Meadows with accessible low-angle slab bouldering at its base. Characteristic Tuolumne friction problems on exfoliated granite at 8,150 ft. Grades V0–V4 on clean, sun-warmed slabs. Often combined with Tenaya Lake swimming. NPS rock-climbing regulations apply; no permit needed for bouldering at base. Best season July–September. Part of the same high-altitude dome cluster as Lembert and Pothole Dome.",
                "run_type": None,
            }
        ],
        "source_url": "https://www.mountainproject.com/area/106097598/pywiack-dome",
        "source_type": "web_search",
    },
]

ZONE_MAP = {
    "Big Chief Crag — Bouldering Base": 1,
    "Pie Shop Crag — Bouldering": 2,
    "Pywiack Dome — Tuolumne Bouldering": 3,
}

if __name__ == "__main__":
    import sqlite3
    conn = sqlite3.connect('sierra28k.db')
    cur = conn.cursor()

    for p in places:
        zone_id = ZONE_MAP[p["name"]]
        existing = {r[0] for r in cur.execute(
            'SELECT name FROM places WHERE zone_id=?', (zone_id,)).fetchall()}
        if p["name"] in existing:
            print(f"SKIP (exists): {p['name']}")
            continue
        pc, ac, sc = insert_zone(zone_id, [p])
        print(f"Inserted zone {zone_id}: {p['name']} ({pc} place, {ac} activity)")

    conn.close()

    # Final summary
    for zone_id, name in [(1, "North Lake Tahoe"), (2, "South Lake Tahoe"), (3, "Tuolumne Meadows")]:
        zone_summary(zone_id, name)
