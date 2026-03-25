#!/usr/bin/env python3
"""
Add Beginner-Intermediate Peak Bagging Entries
Focus on Class 1-2 non-technical summits with established trails.
Avoid: Class 3+ scrambling, technical routes, serious exposure, roped climbing.
Tag format: "[PEAK BAGGING - SKILL_LEVEL]" in notes
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "sierra28k.db")

def get_zone_id(cur, zone_name):
    result = cur.execute("SELECT id FROM zones WHERE name = ?", (zone_name,)).fetchone()
    return result[0] if result else None

def add_place_and_activity(cur, conn, zone_id, place_data):
    """Add a place with peak bagging activity."""
    # Insert place
    cur.execute("""
        INSERT INTO places (zone_id, name, place_type, lat, lng, address, parking_notes, kid_friendly)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (zone_id, place_data['name'], place_data['place_type'], 
          place_data['lat'], place_data['lng'], place_data.get('address'),
          place_data.get('parking_notes'), 1 if place_data.get('kid_friendly') else 0))
    
    place_id = cur.lastrowid
    
    # Insert activity with peak bagging tag
    notes = f"[PEAK BAGGING - {place_data['skill_level']}] {place_data['notes']}"
    
    cur.execute("""
        INSERT INTO activities (place_id, activity_type, difficulty, distance_km, elevation_gain_m, notes, run_type)
        VALUES (?, 'hike', ?, ?, ?, ?, NULL)
    """, (place_id, place_data['difficulty'], place_data['distance_km'], 
          place_data['elevation_gain_m'], notes))
    
    # Add sources
    for url, source_type in place_data.get('sources', []):
        cur.execute("""
            INSERT INTO sources (place_id, url, source_type, retrieved_at)
            VALUES (?, ?, ?, datetime('now'))
        """, (place_id, url, source_type))
    
    conn.commit()
    return place_id

# BEGINNER-INTERMEDIATE PEAKS DATA
# All are Class 1-2, non-technical, well-defined trails
BEGINNER_PEAKS = [
    # NORTH LAKE TAHOE
    {
        "zone": "North Lake Tahoe",
        "name": "Donner Peak Trail",
        "place_type": "trailhead",
        "lat": 39.3167,
        "lng": -120.3167,
        "address": "Donner Summit, Pacific Crest Trail access, Truckee, CA 96161",
        "parking_notes": "Donner Ski Ranch or Sugar Bowl Academy lot; PCT access free",
        "kid_friendly": False,
        "skill_level": "BEGINNER",
        "difficulty": 3,
        "distance_km": 6.0,
        "elevation_gain_m": 450,
        "notes": "4-mile round trip to 8,019 ft summit via PCT. Well-maintained trail, no scrambling. Views of Donner Lake, Sierra Crest. Good first peak—clear trail, obvious summit. Some granite slabs near top but walkable.",
        "sources": [("https://www.fs.usda.gov/recarea/tahoe/recarea/?recid=80929", "official")]
    },
    {
        "zone": "North Lake Tahoe", 
        "name": "Mount Judah Loop Peak",
        "place_type": "trailhead",
        "lat": 39.3033,
        "lng": -120.2956,
        "address": "Donner Pass Rd, Soda Springs, CA 95728",
        "parking_notes": "Pacific Crest Trailhead lot at Donner Pass; free",
        "kid_friendly": False,
        "skill_level": "BEGINNER",
        "difficulty": 3,
        "distance_km": 8.0,
        "elevation_gain_m": 520,
        "notes": "5-mile loop combining PCT and Pacific Crest alternate. Summit 8,243 ft. Old volcanic terrain, great views of Donner Summit area. Trail well-marked. Some loose rock on final approach but non-technical. Excellent intro to Sierra scrambling.",
        "sources": [("https://www.fs.usda.gov/recarea/tahoe/recarea/?recid=80929", "official")]
    },
    
    # SOUTH LAKE TAHOE
    {
        "zone": "South Lake Tahoe",
        "name": "Ralston Peak Trail",
        "place_type": "trailhead",
        "lat": 38.8083,
        "lng": -120.1333,
        "address": "Ralston Peak Trailhead, US-50 near Wrights Lake, CA 95720",
        "parking_notes": "Wrights Lake Rd then 4WD forest road; high clearance recommended",
        "kid_friendly": False,
        "skill_level": "INTERMEDIATE",
        "difficulty": 4,
        "distance_km": 11.0,
        "elevation_gain_m": 790,
        "notes": "7-mile round trip to 9,235 ft. Steep but well-defined trail through forest to granite summit. 360° views of Lake Tahoe and Desolation Wilderness. Last 200 yards are loose scree—take your time. Good fitness test peak.",
        "sources": [("https://www.fs.usda.gov/recarea/eldorado/recarea/?recid=4080", "official")]
    },
    {
        "zone": "South Lake Tahoe",
        "name": "Mount Rose Summit Walk-up",
        "place_type": "trailhead", 
        "lat": 39.3167,
        "lng": -119.9000,
        "address": "Mount Rose Summit Trailhead, NV-431, NV 89411",
        "parking_notes": "NV State Park lot at 8,911 ft; $10 day use; seasonal closure winter",
        "kid_friendly": False,
        "skill_level": "BEGINNER",
        "difficulty": 3,
        "distance_km": 4.0,
        "elevation_gain_m": 320,
        "notes": "2.5-mile round trip to 10,779 ft—highest peak in Tahoe basin. Trail from summit parking. Gradual grade, wide switchbacks. Dramatic views of Lake Tahoe. Often snow until July. Good for building altitude tolerance. No scrambling required.",
        "sources": [("https://parks.nv.gov/parks/mount-rose", "official")]
    },
    
    # TUOLUMNE MEADOWS
    {
        "zone": "Tuolumne Meadows",
        "name": "Pothole Dome Summit",
        "place_type": "trailhead",
        "lat": 37.8789,
        "lng": -119.3844,
        "address": "Pothole Dome pullout, Tioga Rd (Hwy 120), Yosemite National Park, CA 95389",
        "parking_notes": "Small pullout on Tioga Road; free with park entrance",
        "kid_friendly": True,
        "skill_level": "BEGINNER",
        "difficulty": 2,
        "distance_km": 2.0,
        "elevation_gain_m": 120,
        "notes": "1.2-mile round trip to granite dome summit at 8,700 ft. Class 1 walking—no real scrambling. Tuolumne River views, meadow panorama. Perfect first dome for kids/families. Can link with meadow walk for longer day.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official")]
    },
    {
        "zone": "Tuolumne Meadows",
        "name": "Marmot Dome via Young Lakes Trail",
        "place_type": "trailhead",
        "lat": 37.8656,
        "lng": -119.3733,
        "address": "Tuolumne Meadows Wilderness Center, Yosemite National Park, CA 95389",
        "parking_notes": "Wilderness center lot; free with park entrance; wilderness permit needed if continuing to Young Lakes",
        "kid_friendly": False,
        "skill_level": "INTERMEDIATE",
        "difficulty": 3,
        "distance_km": 6.4,
        "elevation_gain_m": 380,
        "notes": "4-mile out-and-back to Marmot Dome (9,800 ft) on way to Young Lakes. Cross-country last 0.3 miles but obvious route. Class 1-2. Views of Tuolumne Meadows and surrounding peaks. Good practice for cross-country navigation. Continue to Young Lakes for full day.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/younglakes.htm", "official")]
    },
    
    # MAMMOTH LAKES
    {
        "zone": "Mammoth Lakes",
        "name": "Crystal Crag Peak",
        "place_type": "trailhead",
        "lat": 37.6167,
        "lng": -118.9833,
        "address": "Lake George Rd, Mammoth Lakes, CA 93546",
        "parking_notes": "Lake George area; USFS day use; $5 fee summer",
        "kid_friendly": False,
        "skill_level": "INTERMEDIATE",
        "difficulty": 4,
        "distance_km": 8.0,
        "elevation_gain_m": 550,
        "notes": "5-mile round trip to 10,377 ft via Duck Pass Trail then fork to Crystal Lake/Crag. Moderately steep forest trail, then talus field to summit block. Class 2 scrambling on granite final 100 yards. Not technical but requires route-finding. Views of Mammoth Lakes basin.",
        "sources": [("https://www.fs.usda.gov/recarea/inyo/recarea/?recid=20618", "official")]
    },
    {
        "zone": "Mammoth Lakes",
        "name": "San Joaquin Mountain via Minaret Summit",
        "place_type": "trailhead",
        "lat": 37.6283,
        "lng": -119.0833,
        "address": "Minaret Summit, Mammoth Lakes, CA 93546",
        "parking_notes": "Minaret Vista pullout; free; seasonal closure Nov-May",
        "kid_friendly": False,
        "skill_level": "BEGINNER",
        "difficulty": 3,
        "distance_km": 7.2,
        "elevation_gain_m": 400,
        "notes": "4.5-mile round trip to 11,600 ft via old road then cross-country ridge walk. Spectacular views of Ritter Range, Minarets, Banner/Ritter peaks. Walkable ridge—no scrambling. Good intro to cross-country travel with obvious goal. Windy on ridge.",
        "sources": [("https://www.fs.usda.gov/recarea/inyo/recarea/?recid=20606", "official")]
    },
    {
        "zone": "Mammoth Lakes",
        "name": "Mammoth Rock (West Slope)",
        "place_type": "trailhead",
        "lat": 37.6458,
        "lng": -119.0250,
        "address": "Mammoth Rock Trail, Mammoth Lakes, CA 93546",
        "parking_notes": "Old Mammoth Rd access; trailhead parking limited",
        "kid_friendly": False,
        "skill_level": "INTERMEDIATE",
        "difficulty": 3,
        "distance_km": 4.0,
        "elevation_gain_m": 290,
        "notes": "2.5-mile round trip to 9,400 ft volcanic rock summit. Western approach is walkable—eastern side has cliffs to avoid. Good views of Mammoth Mountain. Trail fades near top but cairns mark route. Used for both hiking and bouldering access.",
        "sources": [("https://www.mammothtrails.org/trail/64/mammoth-rock/", "official")]
    },
    
    # BISHOP/EASTERN SIERRA
    {
        "zone": "Bishop/Eastern Sierra",
        "name": "Chocolate Peak (North Slope)",
        "place_type": "trailhead",
        "lat": 37.2333,
        "lng": -118.6167,
        "address": "South Lake Trailhead, Bishop Creek Canyon, Bishop, CA 93514",
        "parking_notes": "USFS fee lot $5; wilderness permit area but day use ok without",
        "kid_friendly": False,
        "skill_level": "INTERMEDIATE",
        "difficulty": 4,
        "distance_km": 11.2,
        "elevation_gain_m": 680,
        "notes": "7-mile round trip to 11,682 ft. Cross-country after Chocolate Lakes. Class 2 on loose talus. North side only—south face is technical. Views of entire Bishop Creek basin, Hurd Peak, Dusy Basin approach. Good practice with loose rock.",
        "sources": [("https://www.fs.usda.gov/recarea/inyo/recarea/?recid=20340", "official")]
    },
    {
        "zone": "Bishop/Eastern Sierra",
        "name": "Mount Tom Trail to False Summit",
        "place_type": "trailhead",
        "lat": 37.3611,
        "lng": -118.7333,
        "address": "North Lake Rd, Bishop, CA 93514",
        "parking_notes": "Bishop area access via dirt roads; 4WD recommended",
        "kid_friendly": False,
        "skill_level": "BEGINNER",
        "difficulty": 3,
        "distance_km": 9.6,
        "elevation_gain_m": 520,
        "notes": "6-mile round trip to 12,600+ ft false summit area on Mt Tom shoulder. Old mining road then trail. Not true summit but high point with excellent views of Owens Valley, White Mountains. Good for acclimatization. Route continues to true summit but requires Class 2+.",
        "sources": [("https://www.fs.usda.gov/recarea/inyo/recarea/?recid=20343", "official")]
    },
    
    # YOSEMITE VALLEY
    {
        "zone": "Yosemite Valley",
        "name": "North Dome via Yosemite Falls Trail",
        "place_type": "trailhead",
        "lat": 37.7456,
        "lng": -119.5969,
        "address": "Camp 4 or Yosemite Lodge, Yosemite Valley, CA 95389",
        "parking_notes": "Camp 4 day use (lottery) or park at Yosemite Valley Lodge",
        "kid_friendly": False,
        "skill_level": "INTERMEDIATE",
        "difficulty": 3,
        "distance_km": 14.0,
        "elevation_gain_m": 520,
        "notes": "8.7-mile round trip to 7,542 ft dome with 360° views of Half Dome, Valley, Yosemite Falls. Trail to Yosemite Falls, then traverse to North Dome. Mostly walking with brief Class 2 section. One of best valley viewpoints without technical climbing. Return via Indian Rock or same route.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/northdome.htm", "official")]
    },
    {
        "zone": "Yosemite Valley",
        "name": "Sentinel Dome (Walk-up Route)",
        "place_type": "trailhead",
        "lat": 37.7231,
        "lng": -119.5856,
        "address": "Sentinel Dome Trailhead, Glacier Point Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Glacier Point Rd lot; $35 park entrance; road seasonal May-Oct",
        "kid_friendly": True,
        "skill_level": "BEGINNER",
        "difficulty": 2,
        "distance_km": 3.2,
        "elevation_gain_m": 80,
        "notes": "2-mile round trip to 8,122 ft granite dome summit. Paved to dirt trail then granite walk-up—no scrambling required. Arguably best easy summit in Yosemite: views of Half Dome, El Capitan, Yosemite Falls, entire valley. Accessible to most fitness levels. Sunset spectacular.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/sentinel.htm", "official")]
    },
    {
        "zone": "Yosemite Valley",
        "name": "Taft Point to The Fissures",
        "place_type": "trailhead",
        "lat": 37.7131,
        "lng": -119.5856,
        "address": "Taft Point Trailhead, Glacier Point Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Glacier Point Rd pullout; $35 park entrance; seasonal road",
        "kid_friendly": True,
        "skill_level": "BEGINNER",
        "difficulty": 1,
        "distance_km": 3.2,
        "elevation_gain_m": 15,
        "notes": "2-mile easy walk to 7,503 ft viewpoint—more viewpoint than peak but included for perspective. Dramatic vertical cliff edge (fissures) with valley views. Flat trail, minimal elevation. Good for building comfort with heights. Keep children back from cliff edge—serious exposure here.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/taftpoint.htm", "official")]
    },
    
    # SEQUOIA/KINGS CANYON
    {
        "zone": "Sequoia/Kings Canyon",
        "name": "Buena Vista Peak (via old fire road)",
        "place_type": "trailhead",
        "lat": 36.5644,
        "lng": -118.7444,
        "address": "Buena Vista Peak Rd, Giant Forest, Sequoia National Park, CA 93262",
        "parking_notes": "Giant Forest area access; seasonal road closure; $35 park entrance",
        "kid_friendly": False,
        "skill_level": "INTERNERMEDIATE",
        "difficulty": 3,
        "distance_km": 6.4,
        "elevation_gain_m": 340,
        "notes": "4-mile round trip to 7,600+ ft summit via old fire road then short cross-country. Views of western divide, Central Valley. Often overlooked peak in Giant Forest area. Class 1 walking. Good for practicing map reading—trail not always obvious.",
        "sources": [("https://www.nps.gov/seki/planyourvisit/giantforest.htm", "official")]
    },
    {
        "zone": "Sequoia/Kings Canyon",
        "name": "Panoramic Point (Drive-up then short walk)",
        "place_type": "starting_point",
        "lat": 36.7183,
        "lng": -118.9689,
        "address": "Panoramic Point, Grant Grove Village, Kings Canyon National Park, CA 93633",
        "parking_notes": "Grant Grove access road; paved; free with park entrance; closes in heavy snow",
        "kid_friendly": True,
        "skill_level": "BEGINNER",
        "difficulty": 1,
        "distance_km": 0.6,
        "elevation_gain_m": 20,
        "notes": "0.4-mile paved path to 7,520 ft viewpoint—more accessible summit experience. 360° views of Great Western Divide, Sierra Crest. Good for beginners, children, those testing altitude. Interpretive signs. Combine with Grant Grove loop for longer outing.",
        "sources": [("https://www.nps.gov/seki/planyourvisit/panoramicpoint.htm", "official")]
    },
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    added_count = 0
    
    for peak in BEGINNER_PEAKS:
        zone_id = get_zone_id(cur, peak["zone"])
        if zone_id:
            add_place_and_activity(cur, conn, zone_id, peak)
            added_count += 1
            print(f"✓ Added: {peak['name']} ({peak['zone']})")
        else:
            print(f"✗ Zone not found: {peak['zone']}")
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Added {added_count} beginner-intermediate peaks")
    
    # Show updated activity counts
    print("\nUpdated Activity Counts (with peak bagging):")
    cur.execute("SELECT activity_type, COUNT(*) FROM activities GROUP BY activity_type ORDER BY COUNT(*) DESC")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # Show peak bagging breakdown
    print("\nPeak Bagging Entries:")
    cur.execute("""
        SELECT 
            CASE 
                WHEN notes LIKE '%[PEAK BAGGING - BEGINNER]%' THEN 'Beginner'
                WHEN notes LIKE '%[PEAK BAGGING - INTERMEDIATE]%' THEN 'Intermediate'
            END as level,
            COUNT(*)
        FROM activities 
        WHERE notes LIKE '%[PEAK BAGGING%'
        GROUP BY level
    """)
    for row in cur.fetchall():
        if row[0]:
            print(f"  {row[0]}: {row[1]} peaks")
    
    conn.close()
    print(f"\nDatasette URL: http://localhost:8001")

if __name__ == "__main__":
    main()
