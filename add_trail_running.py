#!/usr/bin/env python3
"""
Add Trail Running Trailheads for 5K to Marathon Distances
Focus on trail networks where runners can build their own routes
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sierra28k.db")

def get_zone_id(cur, zone_name):
    result = cur.execute("SELECT id FROM zones WHERE name = ?", (zone_name,)).fetchone()
    return result[0] if result else None

def add_trailhead(cur, conn, zone_id, data):
    """Add a trailhead with running activity."""
    # Insert place
    cur.execute("""
        INSERT INTO places (zone_id, name, place_type, lat, lng, address, parking_notes, kid_friendly)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (zone_id, data['name'], data['place_type'], 
          data['lat'], data['lng'], data.get('address'),
          data.get('parking_notes'), 0))  # Not kid-friendly for trail running
    
    place_id = cur.lastrowid
    
    # Insert run activity
    notes = f"[TRAIL RUNNING - {data['distance_range']}] {data['notes']}"
    
    cur.execute("""
        INSERT INTO activities (place_id, activity_type, difficulty, distance_km, elevation_gain_m, notes, run_type)
        VALUES (?, 'run', ?, ?, ?, ?, 'route')
    """, (place_id, data['difficulty'], data['base_distance_km'], 
          data['elevation_gain_m'], notes))
    
    # Add sources
    for url, source_type in data.get('sources', []):
        cur.execute("""
            INSERT INTO sources (place_id, url, source_type, retrieved_at)
            VALUES (?, ?, ?, datetime('now'))
        """, (place_id, url, source_type))
    
    conn.commit()
    return place_id

# TRAIL RUNNING TRAILHEADS - 5K to Marathon distances
# Each entry represents a trailhead with flexible route options
TRAIL_RUNNING_DATA = [
    # NORTH LAKE TAHOE
    {
        "zone": "North Lake Tahoe",
        "name": "Tahoe City Commons Beach Trail Run Hub",
        "place_type": "starting_point",
        "lat": 39.1689,
        "lng": -120.1411,
        "address": "Commons Beach, 400 North Lake Blvd, Tahoe City, CA 96145",
        "parking_notes": "Free public lot; fills weekends; early arrival recommended",
        "distance_range": "5K-21K FLEXIBLE",
        "difficulty": 2,
        "base_distance_km": 10.0,
        "elevation_gain_m": 90,
        "notes": "Central trail running hub. Connects to: Truckee River Legacy Trail (8K out-and-back), Tahoe City to Squaw Valley bike path (16K one way), Burton Creek trails (5K-15K loop options). Paved and dirt mix. Flat to rolling. Multiple bailout points. Popular morning running destination.",
        "sources": [("https://www.placer.ca.gov/departments/works/trails", "official")]
    },
    {
        "zone": "North Lake Tahoe",
        "name": "Sawtooth Ridge Trail Complex - PCT Access",
        "place_type": "trailhead",
        "lat": 39.2456,
        "lng": -120.0894,
        "address": "Sawtooth Ridge Trailhead, Tahoe National Forest, CA 96148",
        "parking_notes": "USFS dirt lot; free; high clearance recommended; snow-free June-Oct",
        "distance_range": "10K-42K+ TECHNICAL",
        "difficulty": 4,
        "base_distance_km": 21.0,
        "elevation_gain_m": 450,
        "notes": "PCT access point for serious trail runners. Options: 10K loop on old logging roads, 21K lollipop on PCT to Watson Lake, 42K+ point-to-point to Donner Summit. Technical singletrack, significant elevation. Training ground for ultra runners. Views of Lake Tahoe. Bring water—limited sources.",
        "sources": [("https://www.fs.usda.gov/tahoe", "official")]
    },
    {
        "zone": "North Lake Tahoe",
        "name": "Brockway Summit Trail Running Center",
        "place_type": "trailhead",
        "lat": 39.2422,
        "lng": -120.0322,
        "address": "Brockway Summit, Hwy 431, Tahoe Vista, CA 96148",
        "parking_notes": "USFS lot on Hwy 431; no facilities; winter closure Nov-May",
        "distance_range": "5K-15K LOOP OPTIONS",
        "difficulty": 3,
        "base_distance_km": 8.0,
        "elevation_gain_m": 280,
        "notes": "High-altitude trail running at 8,300 ft. TRT connectors, fire road loops, meadow trails. Popular 5K interval loops, 10K figure-8, 15K TRT out-and-back. Soft singletrack. Alpine flowers July-Aug. Morning best—afternoon thunderstorms common. Good for VO2 max training.",
        "sources": [("https://tahoerimtrail.org/", "official")]
    },
    {
        "zone": "North Lake Tahoe",
        "name": "Northstar California Trail Network",
        "place_type": "trailhead",
        "lat": 39.2639,
        "lng": -120.1211,
        "address": "Northstar California Resort, 5001 Northstar Dr, Truckee, CA 96161",
        "parking_notes": "Village parking $5-15; free after 4pm; summer operations only",
        "distance_range": "5K-25K GROOMED",
        "difficulty": 3,
        "base_distance_km": 12.0,
        "elevation_gain_m": 350,
        "notes": "Resort-maintained trail network for summer use. 20+ miles of marked trails. 5K time-trial loop, 10K perimeter, 21K full network. Mix of singletrack and fire road. Maps at village. Water stops at resort base. Good for tempo runs. Chairlift access for downhill-only options.",
        "sources": [("https://www.northstarcalifornia.com/summer-activities/hiking-biking.html", "official")]
    },
    
    # SOUTH LAKE TAHOE
    {
        "zone": "South Lake Tahoe",
        "name": "Spooner Summit Trail Running Hub",
        "place_type": "trailhead",
        "lat": 39.1058,
        "lng": -119.8889,
        "address": "Spooner Summit, Hwy 50, South Lake Tahoe, NV 89449",
        "parking_notes": "NV State Park lot; $10 day use; large paved area; restrooms",
        "distance_range": "5K-30K+ POINT-TO-POINT",
        "difficulty": 3,
        "base_distance_km": 15.0,
        "elevation_gain_m": 320,
        "notes": "FLume Trail north access point. World-famous lake-view running. 5K preview loop, 10K to Marlette Lake, 21K to Tunnel Creek, 30K+ point-to-point to Incline Village. High elevation 7,000-8,500 ft. Exposed—early start essential. Bucket-list Sierra running destination. Bring electrolytes.",
        "sources": [("https://parks.nv.gov/parks/lake-tahoe-nevada-state-park", "official")]
    },
    {
        "zone": "South Lake Tahoe",
        "name": "Powerline Trail Network - Meyers Access",
        "place_type": "trailhead",
        "lat": 38.8564,
        "lng": -119.9908,
        "address": "Meyers, CA 96150 (Powerline Trail access via Pioneer Trail)",
        "parking_notes": "Dirt lot at trail junction; free; no facilities; 4WD helpful",
        "distance_range": "5K-20K HILL TRAINING",
        "difficulty": 3,
        "base_distance_km": 10.0,
        "elevation_gain_m": 400,
        "notes": "Old powerline service roads converted to trails. Consistent 5-8% grades—perfect hill training. 5K repeats, 10K out-and-back, 20K point-to-point to Christmas Valley. Views of Freel Peak. Less crowded than lakeside trails. Good for winter training when high trails snowed in. Self-sufficient required.",
        "sources": [("https://www.eldoradocounty.org/publicworks/roads/trails", "official")]
    },
    {
        "zone": "South Lake Tahoe",
        "name": "Fallen Leaf Lake Trail Running Base",
        "place_type": "trailhead",
        "lat": 38.9378,
        "lng": -120.0542,
        "address": "Fallen Leaf Lake Marina, Fallen Leaf Lake Rd, South Lake Tahoe, CA 96150",
        "parking_notes": "Marina lot $5; street parking on Fallen Leaf Rd; fills weekends",
        "distance_range": "8K-25K ALPINE",
        "difficulty": 4,
        "base_distance_km": 16.0,
        "elevation_gain_m": 520,
        "notes": "Glen Alpine Trail access for mountain runners. 8K to Glen Alpine Falls, 16K lollipop to Susie Lake, 25K+ to Gilmore Lake/Desolation Wilderness boundary. 6,300-8,500 ft elevation. Technical rocky sections. Cascade views, alpine lakes. Bear country awareness. Popular with ultra training groups.",
        "sources": [("https://www.fs.usda.gov/recarea/ltbmu/recarea/?recid=11754", "official")]
    },
    
    # TUOLUMNE MEADOWS
    {
        "zone": "Tuolumne Meadows",
        "name": "Tuolumne Meadows Trail Running Epicenter",
        "place_type": "trailhead",
        "lat": 37.8736,
        "lng": -119.3594,
        "address": "Tuolumne Meadows Wilderness Center, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "NPS gravel lots; $35 park entrance; fills by 9am; seasonal June-Oct",
        "distance_range": "5K-42K+ HIGH ALPINE",
        "difficulty": 3,
        "base_distance_km": 20.0,
        "elevation_gain_m": 180,
        "notes": "World-class high-altitude running at 8,600 ft. PCT/JMT corridor access. 5K meadow loop, 10K to Soda Springs, 21K to Lyell Canyon bridge, 42K+ to Donohue Pass. Gentle grades, perfect tread. Must-do for any serious mountain runner. Acclimatization essential—don't sprint first day. Afternoon thunderstorms rule.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official")]
    },
    {
        "zone": "Tuolumne Meadows",
        "name": "Tenaya Lake Trailhead - High Country Running",
        "place_type": "trailhead",
        "lat": 37.8325,
        "lng": -119.4572,
        "address": "Tenaya Lake, Tioga Rd (Hwy 120), Yosemite National Park, CA 95389",
        "parking_notes": "NPS day-use lots; free with park entrance; multiple access points",
        "distance_range": "10K-30K TECHNICAL ALPINE",
        "difficulty": 4,
        "base_distance_km": 16.0,
        "elevation_gain_m": 480,
        "notes": "8,150 ft alpine lake trailhead. Connects to Clouds Rest trail, Sunrise Lakes, Half Dome approach. 10K Sunrise Lakes loop, 16K to Clouds Rest junction, 30K+ Half Dome summit return. Technical rocky sections. Dramatic high country. Snow patches into July. Serious mountain running requiring preparation.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tenaya.htm", "official")]
    },
    
    # MAMMOTH LAKES
    {
        "zone": "Mammoth Lakes",
        "name": "Mammoth Mountain Trail Running Base",
        "place_type": "trailhead",
        "lat": 37.6514,
        "lng": -119.0369,
        "address": "Mammoth Mountain Main Lodge, 10001 Minaret Rd, Mammoth Lakes, CA 93546",
        "parking_notes": "Main lodge lots; $10-25/day; gondola access for downhill runs",
        "distance_range": "5K-42K SKI RESORT TRAILS",
        "difficulty": 3,
        "base_distance_km": 15.0,
        "elevation_gain_m": 380,
        "notes": "Summer use of ski resort trail network. 5K switchback loops, 10K to Panorama Dome, 21K to Reds Meadow, 42K point-to-point to Devils Postpile. Marked summer trails. 7,800-11,000 ft. Chairlift up/run down options. Mammoth Trail Festival race course. Excellent training at altitude. Café/amenities at lodge.",
        "sources": [
            ("https://www.mammothmountain.com/summer/trails", "official"),
            ("https://mammothtrailfest.com/", "official")
        ]
    },
    {
        "zone": "Mammoth Lakes",
        "name": "Shady Rest Park Running Hub",
        "place_type": "starting_point",
        "lat": 37.6486,
        "lng": -118.9750,
        "address": "Shady Rest Park, Sawmill Cutoff Rd, Mammoth Lakes, CA 93546",
        "parking_notes": "Town park lot; free; restrooms; all-season access",
        "distance_range": "5K-15K TOWN CONNECTOR",
        "difficulty": 2,
        "base_distance_km": 8.0,
        "elevation_gain_m": 120,
        "notes": "Town-based trail network connecting to forest service trails. 5K paved loop through town, 8K to Old Mammoth Rd trails, 15K to Lakes Basin path. Flat to gentle grades. Good for: recovery runs, tempo work, evening runs. Lit sections in town. Safe solo running. Connects to Mammoth Creek trail system.",
        "sources": [("https://www.mammothtrails.org/", "official")]
    },
    {
        "zone": "Mammoth Lakes",
        "name": "Lakes Basin Trail Complex - Main Trailhead",
        "place_type": "trailhead",
        "lat": 37.6094,
        "lng": -118.9824,
        "address": "Lake Mary Rd, Mammoth Lakes, CA 93546 (Lake Mary Campground area)",
        "parking_notes": "USFS fee lots $5; 5 trailheads in 2-mile stretch; seasonal June-Oct",
        "distance_range": "5K-30K+ ALPINE LAKES",
        "difficulty": 3,
        "base_distance_km": 18.0,
        "elevation_gain_m": 450,
        "notes": "7 alpine lakes trail network. 5K Lake Mary loop, 10K Mary+George, 18K Duck Pass, 30K+ to PCT junction. 8,900-10,500 ft. Granite and aspen. Water sources available. Multi-loop options. Trail running paradise. Active bear population—follow food storage rules. Afternoon T-storms July-Aug.",
        "sources": [("https://www.fs.usda.gov/recarea/inyo/recarea/?recid=20606", "official")]
    },
    
    # BISHOP/EASTERN SIERRA
    {
        "zone": "Bishop/Eastern Sierra",
        "name": "Bishop Creek Trail Running Base - South Lake Access",
        "place_type": "trailhead",
        "lat": 37.2361,
        "lng": -118.6111,
        "address": "South Lake Trailhead, North Lake Rd, Bishop, CA 93514",
        "parking_notes": "USFS lot $5; bear canisters required overnight; fills weekends",
        "distance_range": "10K-42K+ HIGH SIERRA",
        "difficulty": 4,
        "base_distance_km": 22.0,
        "elevation_gain_m": 600,
        "notes": "Gateway to John Muir Trail section. 10K to Chocolate Lakes, 22K to Bishop Pass, 42K+ to Dusy Basin/JMT junction. 7,800-11,972 ft. Epic Sierra high country. Alpine lakes, glaciers, 13,000 ft peaks. Must-do for experienced mountain runners. Acclimatize at lower elevations first. Weather changes fast.",
        "sources": [("https://www.fs.usda.gov/recarea/inyo/recarea/?recid=20340", "official")]
    },
    {
        "zone": "Bishop/Eastern Sierra",
        "name": "Buttermilk Country Running Trails",
        "place_type": "trailhead",
        "lat": 37.3367,
        "lng": -118.6456,
        "address": "Buttermilk Rd, Bishop, CA 93514",
        "parking_notes": "BLM free lot; 4WD helpful but not required; fills with climbers",
        "distance_range": "5K-15K HILL INTERVALS",
        "difficulty": 3,
        "base_distance_km": 10.0,
        "elevation_gain_m": 350,
        "notes": "Desert bouldering area service roads and singletrack. 5K rolling warm-up, 10K out-and-back to Sagehen Meadows, 15K loop via old mining roads. 5,200-6,200 ft. Exposed—morning/evening best. Views of Owens Valley, White Mountains. Good for heat training. Less crowded than creek canyon trails. Watch for snakes in summer.",
        "sources": [("https://www.blm.gov/visit/bishop-area", "official")]
    },
    
    # YOSEMITE VALLEY
    {
        "zone": "Yosemite Valley",
        "name": "Yosemite Valley Loop Trail Network",
        "place_type": "starting_point",
        "lat": 37.7456,
        "lng": -119.5969,
        "address": "Yosemite Village, multiple access points, Yosemite National Park, CA 95389",
        "parking_notes": "Day-use lots fill early; use free shuttle; bike/run in from Curry Village",
        "distance_range": "5K-21K VALLEY FLOOR",
        "difficulty": 2,
        "base_distance_km": 11.0,
        "elevation_gain_m": 90,
        "notes": "Paved bike path and dirt trail combo around valley floor. 5K east valley, 10K full loop, 21K combined with Mirror Lake extension. 4,000 ft elevation. Flat to gentle grades. Iconic views throughout. Start 5am to avoid crowds. Run beneath El Cap, past Yosemite Falls. Bucket list even for non-runners. Crowded mid-day.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/valleytrails.htm", "official")]
    },
    {
        "zone": "Yosemite Valley",
        "name": "Glacier Point Road Trail Running Access",
        "place_type": "trailhead",
        "lat": 37.7231,
        "lng": -119.5856,
        "address": "Glacier Point Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Multiple pullouts along road; seasonal May-Nov; $35 park entrance",
        "distance_range": "10K-30K HIGH ELEVATION",
        "difficulty": 3,
        "base_distance_km": 16.0,
        "elevation_gain_m": 280,
        "notes": "7,000-7,500 ft running along paved road (closed to cars in AM before 9am or after 4pm). Connects Sentinel Dome, Taft Point, McGurk Meadow, Bridalveil Creek trails. 10K to Sentinel Dome and back, 16K to Ostrander Lake trailhead, 30K+ point-to-point to Wawona. High Sierra meadows, sequoia groves. Less crowded than valley.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/glacierpoint.htm", "official")]
    },
    {
        "zone": "Yosemite Valley",
        "name": "Wawona Meadow Loop - Historic Running",
        "place_type": "starting_point",
        "lat": 37.5367,
        "lng": -119.6544,
        "address": "Wawona Hotel, Wawona, Yosemite National Park, CA 95389",
        "parking_notes": "Hotel lot for guests or day use fee; free along Wawona Rd",
        "distance_range": "5K-12K MELLOW",
        "difficulty": 2,
        "base_distance_km": 6.4,
        "elevation_gain_m": 60,
        "notes": "Historic 4-mile loop around Wawona Meadow. Gentle, rolling, forested. Historic hotel views. 5K out-and-back on meadow edge, 6.4K full loop, 12K combined with Swinging Bridge. 4,000 ft elevation. Accessible year-round (snow possible Dec-Mar). Quiet alternative to valley crowds. Good for recovery runs.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/wawona.htm", "official")]
    },
    
    # SEQUOIA/KINGS CANYON
    {
        "zone": "Sequoia/Kings Canyon",
        "name": "Grant Grove Village Trail Running Hub",
        "place_type": "starting_point",
        "lat": 36.7486,
        "lng": -118.9664,
        "address": "Grant Grove Village, Generals Hwy, Kings Canyon National Park, CA 93633",
        "parking_notes": "Village lots; free with park entrance; visitor center restrooms",
        "distance_range": "5K-20K FOREST MEADOWS",
        "difficulty": 2,
        "base_distance_km": 12.0,
        "elevation_gain_m": 180,
        "notes": "6,500 ft forest trail network. 5K General Grant loop, 10K Bobcat Point trail, 20K connector to Redwood Mountain Grove. Sequoia forest running—unique experience. Gentle grades, soft duff trails. Good for tempo runs. Bear frequent—stay alert. Seasonal road closure possible winter.",
        "sources": [("https://www.nps.gov/seki/planyourvisit/grantgrove.htm", "official")]
    },
    {
        "zone": "Sequoia/Kings Canyon",
        "name": "Cedar Grove River Trail Network",
        "place_type": "trailhead",
        "lat": 36.7947,
        "lng": -118.6658,
        "address": "Cedar Grove Visitor Center, Kings Canyon National Park, CA 93633",
        "parking_notes": "Visitor center lot; free; seasonal April-Nov; road closes with snow",
        "distance_range": "5K-25K CANYON RUNNING",
        "difficulty": 3,
        "base_distance_km": 16.0,
        "elevation_gain_m": 240,
        "notes": "4,600 ft canyon floor running along South Fork Kings River. 5K Zumwalt Meadow loop, 10K Roads End trail, 16K Mist Falls, 25K+ to Paradise Valley. Canyon walls 4,000 ft overhead. River crossings (easy). Dramatic scenery unique to this zone. Hot midday—early morning best. Limited shade—bring water.",
        "sources": [("https://www.nps.gov/seki/planyourvisit/cedargrove.htm", "official")]
    },
    {
        "zone": "Sequoia/Kings Canyon",
        "name": "Giant Forest Main Trailhead",
        "place_type": "trailhead",
        "lat": 36.5800,
        "lng": -118.7519,
        "address": "Giant Forest Museum, Generals Hwy, Sequoia National Park, CA 93262",
        "parking_notes": "Museum lot or shuttle; fills by 9am; $35 park entrance; seasonal shuttle",
        "distance_range": "5K-15K SEQUOIA FOREST",
        "difficulty": 2,
        "base_distance_km": 8.0,
        "elevation_gain_m": 150,
        "notes": "6,500 ft trail running among world's largest trees. 5K Big Trees Trail, 8K Crescent Meadow loop, 15K Moro Rock connector. Surreal running experience—giants overhead. Mix of paved, dirt, boardwalk. Combine multiple trails for marathon training. Less crowded than Sherman Tree area. Must-stop: Parker Group sequoias.",
        "sources": [("https://www.nps.gov/seki/planyourvisit/giantforest.htm", "official")]
    },
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    added_count = 0
    
    for trailhead in TRAIL_RUNNING_DATA:
        zone_id = get_zone_id(cur, trailhead["zone"])
        if zone_id:
            add_trailhead(cur, conn, zone_id, trailhead)
            added_count += 1
            print(f"✓ Added: {trailhead['name']} ({trailhead['zone']})")
        else:
            print(f"✗ Zone not found: {trailhead['zone']}")
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Added {added_count} trail running trailheads")
    
    # Show updated run activity breakdown
    print("\nUpdated Trail Running Routes:")
    cur.execute("SELECT COUNT(*) FROM activities WHERE activity_type='run'")
    total_runs = cur.fetchone()[0]
    print(f"  Total running activities: {total_runs}")
    
    # Show flexible distance options
    cur.execute("""
        SELECT 
            CASE 
                WHEN notes LIKE '%FLEXIBLE%' THEN 'Flexible Distance'
                WHEN notes LIKE '%5K%' OR notes LIKE '%10K%' OR notes LIKE '%21K%' OR notes LIKE '%42K%' THEN 'Distance Specific'
                ELSE 'Other'
            END as route_type,
            COUNT(*)
        FROM activities 
        WHERE activity_type='run'
        GROUP BY route_type
    """)
    for row in cur.fetchall():
        if row[0] != 'Other':
            print(f"  {row[0]}: {row[1]}")
    
    conn.close()
    print(f"\nDatasette URL: http://localhost:8001")

if __name__ == "__main__":
    main()
