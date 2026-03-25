#!/usr/bin/env python3
"""Initialize sierra28k.db with schema and seed zones."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sierra28k.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def init():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    zones = [
        (
            "North Lake Tahoe",
            "Sierra Nevada - Northern",
            "The quieter, outdoor-recreation-focused side of Lake Tahoe encompassing Truckee, Tahoe City, Kings Beach, and Incline Village. Features extensive trail networks, ski resorts (Palisades Tahoe, Northstar), and access to the Tahoe Rim Trail.",
            1,
            "KEEP: Strong multi-activity hub with hiking, running, walking, and bouldering options. Distinct from South Lake Tahoe in character — more wilderness-oriented. One of the most visited outdoor recreation destinations in California. Sources: NPS, Tahoe National Forest, Visit Lake Tahoe."
        ),
        (
            "South Lake Tahoe",
            "Sierra Nevada - Northern",
            "The larger, entertainment-and-recreation resort side of Lake Tahoe, featuring Heavenly ski resort, Emerald Bay State Park, Desolation Wilderness, and numerous beaches. Distinct from North Tahoe in visitor demographics and amenity profile.",
            1,
            "KEEP: Distinct destination with massive annual visitation (3M+). Strong outdoor recreation including hiking in Desolation Wilderness, trail running, and some bouldering. Justifies its own zone separate from North Lake Tahoe. Sources: California State Parks, El Dorado National Forest."
        ),
        (
            "Tuolumne Meadows",
            "Sierra Nevada - Central",
            "High-alpine subalpine meadow at 8,619 ft in Yosemite National Park, accessed via Tioga Road (Highway 120). Distinct from Yosemite Valley — more remote, less crowded, with access to PCT/JMT, Cathedral Lakes, and extensive high-country hiking. Summer-only access (road closes Nov–May).",
            1,
            "ADDED: Significant tourism destination distinct from Yosemite Valley in character, elevation, and activity profile. World-class hiking, some of the best high-altitude trail running in California, and high granite domes with bouldering/scrambling. 600,000+ annual visitors. Sources: NPS Yosemite."
        ),
        (
            "Mammoth Lakes",
            "Sierra Nevada - Eastern",
            "Major Eastern Sierra resort town at 7,800 ft with year-round tourism. Home to Mammoth Mountain ski area, Devils Postpile National Monument, Inyo National Forest trail networks, June Mountain, and proximity to the JMT southern terminus area.",
            1,
            "KEEP: One of California's top outdoor recreation destinations. Strong multi-activity profile — hiking (Mammoth Lakes Basin, Duck Pass), trail running (Mammoth Trail Fest), walking (bike path network), and bouldering (Mammoth Rock area). Sources: Inyo National Forest, Town of Mammoth Lakes."
        ),
        (
            "Bishop/Eastern Sierra",
            "Sierra Nevada - Eastern",
            "Gateway city to the Eastern Sierra at the foot of the White Mountains, most famous for world-class bouldering at the Buttermilks and Happy Boulders. Also offers premier high-altitude hiking (Bishop Pass, Pine Creek), multi-day JMT access, and year-round trail running.",
            1,
            "KEEP: World-class bouldering destination (Buttermilks featured in major climbing competitions). Premier zone for all four activity types. Bishop Creek Canyon offers exceptional hiking and walking. Trail running is huge here due to 300+ sunny days. Sources: Bishop Visitor Center, Inyo National Forest, Mountain Project."
        ),
        (
            "Yosemite Valley",
            "Sierra Nevada - Central",
            "Iconic 7-mile glacially carved valley at 3,970 ft in Yosemite National Park, featuring El Capitan, Half Dome, Bridalveil Fall, and Yosemite Falls. World-famous hiking, world-class big wall climbing/bouldering (Camp 4), and family-friendly valley walks. 4M+ annual visitors.",
            1,
            "KEEP: Most visited national park unit in the Sierra Nevada. Justifies its own zone — distinct from Tuolumne Meadows in elevation, accessibility, and crowd profile. World-class bouldering at Camp 4 area. Sources: NPS Yosemite."
        ),
        (
            "Sequoia/Kings Canyon",
            "Sierra Nevada - Southern",
            "Twin national parks encompassing the Giant Forest (world's largest trees by volume), Kings Canyon (North America's deepest canyon), Cedar Grove, and General Grant Grove. Strong hiking, walking, and family recreation. Managed jointly by NPS but distinct in character.",
            1,
            "KEEP (combined): While Sequoia and Kings Canyon are distinct parks, they share an entrance fee, adjoining road network, and are commonly visited together. Combined zone avoids artificial fragmentation for this dataset's purposes. Strong activity support — hiking, family walks around groves, some trail running. Note: Placerville/El Dorado Foothills was REMOVED — it is Gold Country foothills geography, not Sierra Nevada proper, and lacks the multi-activity mountain recreation profile needed for this dataset. Sources: NPS Sequoia/Kings Canyon."
        ),
    ]

    cur.executemany(
        "INSERT OR IGNORE INTO zones (name, region, description, validated, validation_notes) VALUES (?,?,?,?,?)",
        zones
    )
    conn.commit()

    # Print summary
    print("=== sierra28k.db initialized ===")
    print(f"DB path: {DB_PATH}\n")

    for row in cur.execute("SELECT id, name, region, validated FROM zones ORDER BY id"):
        status = "✓" if row["validated"] else "○"
        print(f"  {status} Zone {row['id']}: {row['name']} ({row['region']})")

    print(f"\nTotal zones: {cur.execute('SELECT COUNT(*) FROM zones').fetchone()[0]}")

    conn.close()
    print("\nSchema & zones loaded successfully.")

if __name__ == "__main__":
    init()
