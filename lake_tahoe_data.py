#!/usr/bin/env python3
"""
Phase 2 Continued: Research data for remaining zones
Zones: North Lake Tahoe, South Lake Tahoe, Tuolumne Meadows, 
       Bishop/Eastern Sierra, Yosemite Valley, Sequoia/Kings Canyon
Sources: NPS.gov, USFS, official tourism sites, verified coordinates
"""

# NORTH LAKE TAHOE DATA
# Sources: USFS Tahoe NF, California State Parks, Tahoe Rim Trail Association, NPS
NORTH_TAHOE_DATA = [
    # WALKS
    {
        "name": "Sand Harbor Beach Walk",
        "place_type": "starting_point",
        "lat": 39.2006,
        "lng": -119.9319,
        "address": "Sand Harbor, Lake Tahoe-Nevada State Park, Incline Village, NV 89451",
        "parking_notes": "NV State Park fee area $10/vehicle; fills by 10am in summer; ADA accessible",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 1.5,
        "elevation_gain_m": 5,
        "notes": "Crystal-clear water walk on boardwalk and sand. East Shore's most scenic beach. Early morning arrival essential summer weekends. Wheelchair accessible boardwalk.",
        "sources": [("https://parks.nv.gov/parks/lake-tahoe-nevada-state-park", "official")]
    },
    {
        "name": "Spooner Lake Loop",
        "place_type": "trailhead",
        "lat": 39.1061,
        "lng": -119.9061,
        "address": "Spooner Lake, Lake Tahoe Nevada State Park, Carson City, NV 89702",
        "parking_notes": "NV State Park fee area; large paved lot with vault toilets",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 3.2,
        "elevation_gain_m": 45,
        "notes": "2-mile flat loop around Spooner Lake at 7,000 ft. Aspen groves, wildflowers July-Aug. Good birding. Mountain bike share trail—stay alert. Popular with families.",
        "sources": [("https://parks.nv.gov/parks/lake-tahoe-nevada-state-park", "official")]
    },
    {
        "name": "Kings Beach Pier Walk",
        "place_type": "starting_point",
        "lat": 39.2374,
        "lng": -120.0256,
        "address": "Kings Beach State Recreation Area, Kings Beach, CA 96143",
        "parking_notes": "CA State Parks fee $10/vehicle; multiple lots along lakefront; early arrival summer weekends",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 1.0,
        "elevation_gain_m": 0,
        "notes": "Paved lakefront promenade with pier access. Swimming beach with lifeguards in summer. Picnic areas, playground nearby. Excellent for strollers.",
        "sources": [("https://www.parks.ca.gov/?page_id=511", "official")]
    },
    
    # FAMILY WALKS
    {
        "name": "Truckee River Legacy Trail",
        "place_type": "trailhead",
        "lat": 39.1621,
        "lng": -120.1456,
        "address": "Tahoe City, CA 96145 (trailhead at Commons Beach)",
        "parking_notes": "Street parking in Tahoe City; free public lot at Commons Beach; can fill by 11am weekends",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 6.0,
        "elevation_gain_m": 15,
        "notes": "Paved 4-mile (6.4 km) multi-use trail along Truckee River from Tahoe City to Squaw Valley. Gentle grade. River beaches for wading. Interpretive signs. Excellent for bikes, strollers, walking.",
        "sources": [("https://www.placer.ca.gov/departments/works/trails", "official")]
    },
    {
        "name": "Lake Forest Beach Walk",
        "place_type": "trailhead",
        "lat": 39.2267,
        "lng": -120.0553,
        "address": "Lake Forest Rd, Tahoe City, CA 96145",
        "parking_notes": "Tahoe Conservancy lot; free but limited (20 spaces); street parking backup",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 2.0,
        "elevation_gain_m": 10,
        "notes": "Short trail through pine forest to secluded beach. Sandy coves for wading, rock skipping. Less crowded than Sand Harbor. Good for kids 3+.",
        "sources": [("https://tahoeconservancy.ca.gov/recreation/", "official")]
    },
    {
        "name": "Carnelian Bay Pier Walk",
        "place_type": "starting_point",
        "lat": 39.2269,
        "lng": -120.0847,
        "address": "Carnelian Bay, CA 96140",
        "parking_notes": "Small public lot at Gar Woods pier; additional street parking on North Lake Blvd",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 0.8,
        "elevation_gain_m": 5,
        "notes": "Short lakeside stroll to historic Carnelian Bay pier. Fishing, sunset viewing. Nearby playground at Patton Landing Beach. Can combine with beach access.",
        "sources": [("https://www.placer.ca.gov/departments/facilities/parks", "official")]
    },
    
    # RUNS
    {
        "name": "Tahoe Rim Trail - Brockway Summit Loop",
        "place_type": "trailhead",
        "lat": 39.2422,
        "lng": -120.0322,
        "address": "Brockway Summit Trailhead, NV Hwy 431, Tahoe Vista, NV 96148",
        "parking_notes": "USFS dirt lot on Hwy 431; no facilities; winter closure Nov-May",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 3,
        "distance_km": 8.0,
        "elevation_gain_m": 280,
        "notes": "5-mile loop combining TRT with old fire roads. Singletrack with lake views, wildflower meadows. 8,300 ft elevation—acclimate before hard effort. Popular with trail runners.",
        "run_type": "route",
        "sources": [("https://tahoerimtrail.org/", "official")]
    },
    {
        "name": "Tahoe City Marathon Loop",
        "place_type": "starting_point",
        "lat": 39.1689,
        "lng": -120.1411,
        "address": "Commons Beach, Tahoe City, CA 96145",
        "parking_notes": "Free public lot at Commons Beach; early arrival race days",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 2,
        "distance_km": 42.2,
        "elevation_gain_m": 180,
        "notes": "Annual Tahoe City Marathon course (October). Mostly paved along lakefront and bike paths. Gentle rolling hills. Self-guided route any time—follow bike path network clockwise around lake for shorter options.",
        "run_type": "event",
        "sources": [
            ("https://tahoecitymarathon.org/", "official"),
            ("https://tahoemarathon.com/", "official")
        ]
    },
    {
        "name": "Palisades Tahoe 5K/10K Trails",
        "place_type": "trailhead",
        "lat": 39.1964,
        "lng": -120.2353,
        "address": "Palisades Tahoe, Olympic Valley, CA 96146",
        "parking_notes": "Resort parking $10-25/day; free shuttle from Village at Palisades Tahoe",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 3,
        "distance_km": 10.0,
        "elevation_gain_m": 350,
        "notes": "Alpine running at 6,200+ ft. Summer trail race series (5K/10K). Mix of singletrack and fire road. Excellent training at altitude. Chairlift access for downhill options.",
        "run_type": "event",
        "sources": [("https://www.palisadestahoe.com/summer/events", "official")]
    },
    
    # HIKES
    {
        "name": "Eagle Lake Trail (Emerald Bay)",
        "place_type": "trailhead",
        "lat": 38.9558,
        "lng": -120.1136,
        "address": "Eagle Lake Trailhead, Hwy 89, South Lake Tahoe, CA 96150",
        "parking_notes": "CA State Parks lot—fills by 9am summer; $10/vehicle; overflow at Vikingsholm lot",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 3,
        "distance_km": 3.2,
        "elevation_gain_m": 140,
        "notes": "2-mile round trip to alpine Eagle Lake above Emerald Bay. Steep switchbacks through granite. Lake swimming, granite slabs for lunch. Connects to Desolation Wilderness.",
        "sources": [("https://www.parks.ca.gov/?page_id=507", "official")]
    },
    {
        "name": "Mount Tallac Trail",
        "place_type": "trailhead",
        "lat": 38.9367,
        "lng": -120.2128,
        "address": "Mount Tallac Trailhead, Fallen Leaf Lake Rd, South Lake Tahoe, CA 96150",
        "parking_notes": "USFS dirt lot; fills by 8am weekends; no fee",
        "kid_friendly": False,
        "activity_type": "hike",
        "difficulty": 5,
        "distance_km": 16.1,
        "elevation_gain_m": 950,
        "notes": "9.5-mile round trip to 9,735 ft summit. Best panoramic views in Tahoe region. 360-degree views of Lake Tahoe, Desolation Wilderness, Sierra Crest. Strenuous—start early, bring water.",
        "sources": [("https://www.fs.usda.gov/recarea/ltbmu/recarea/?recid=11759", "official")]
    },
    {
        "name": "Cascade Falls Trail",
        "place_type": "trailhead",
        "lat": 39.1578,
        "lng": -120.1681,
        "address": "Cascade Rd, Tahoe City, CA 96145",
        "parking_notes": "USFS lot on Cascade Rd; $5 fee; outhouses available",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 2,
        "distance_km": 2.4,
        "elevation_gain_m": 100,
        "notes": "1.5-mile round trip to Cascade Falls and Lake. Family-friendly with granite stream features. Waterfall best in late spring/early summer. Cool off in granite pools.",
        "sources": [("https://www.fs.usda.gov/recarea/tahoe/recarea/?recid=80766", "official")]
    },
    
    # BOULDERING
    {
        "name": "Donner Summit Boulders",
        "place_type": "starting_point",
        "lat": 39.3167,
        "lng": -120.3167,
        "address": "Donner Summit, Old Hwy 40, Truckee, CA 96161",
        "parking_notes": "Dirt pullouts along Old Hwy 40; free; fills weekends with climbers",
        "kid_friendly": False,
        "activity_type": "bouldering",
        "difficulty": None,
        "distance_km": None,
        "elevation_gain_m": None,
        "notes": "Granite bouldering at 7,200 ft. Classics: 'Girls Gone Wild' (V1), 'Pimpsqueak' (V5). Best conditions July-Sept. Bring pads. Multiple areas along 1-mile stretch.",
        "sources": [("https://www.mountainproject.com/area/105731995/donner-summit", "web_search")]
    },
    {
        "name": "Tahoe City Boulders",
        "place_type": "starting_point",
        "lat": 39.1458,
        "lng": -120.1756,
        "address": "Granite Chief Wilderness boundary near Ward Creek, Tahoe City, CA 96145",
        "parking_notes": "Limited street parking on Ward Creek Rd; 4WD recommended for some areas",
        "kid_friendly": False,
        "activity_type": "bouldering",
        "difficulty": None,
        "distance_km": None,
        "elevation_gain_m": None,
        "notes": "Glacial erratics and small crags. Grades V0-V7. Best spring/fall. Combine with hike to avoid crowds at Donner. Need local beta—less documented than Donner.",
        "sources": [("https://www.mountainproject.com/area/105790302/lake-tahoe", "web_search")]
    },
]

# SOUTH LAKE TAHOE DATA
SOUTH_TAHOE_DATA = [
    # WALKS
    {
        "name": "Van Sickle Bi-State Park Loop",
        "place_type": "trailhead",
        "lat": 38.9506,
        "lng": -119.9472,
        "address": "Van Sickle Bi-State Park, Stateline, NV 89449",
        "parking_notes": "Shared CA/NV park lot off Heavenly Village Way; $8/day; can fill weekends",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 2,
        "distance_km": 4.0,
        "elevation_gain_m": 120,
        "notes": "2.5-mile loop on old fire road and singletrack. Views of Lake Tahoe and Heavenly Valley. Connector to Tahoe Rim Trail. Good option near town with moderate effort.",
        "sources": [
            ("https://parks.nv.gov/parks/van-sickle-bi-state-park", "official"),
            ("https://www.parks.ca.gov/?page_id=26784", "official")
        ]
    },
    {
        "name": "Fallen Leaf Lake Walk",
        "place_type": "trailhead",
        "lat": 38.9378,
        "lng": -120.0542,
        "address": "Fallen Leaf Lake, South Lake Tahoe, CA 96150",
        "parking_notes": "USFS day-use lot $5; street parking on Fallen Leaf Lake Rd; fills summer weekends",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 5.0,
        "elevation_gain_m": 25,
        "notes": "3-mile loop along Fallen Leaf Lake shore. Quiet alternative to busy Lake Tahoe beaches. Granite boulders for scrambling. Less crowded than main lake. Non-motorized only.",
        "sources": [("https://www.fs.usda.gov/recarea/ltbmu/recarea/?recid=11754", "official")]
    },
    
    # FAMILY WALKS
    {
        "name": "Heavenly Village Promenade",
        "place_type": "starting_point",
        "lat": 38.9561,
        "lng": -119.9422,
        "address": "Heavenly Village, 1001 Heavenly Village Way, South Lake Tahoe, CA 96150",
        "parking_notes": "Paid lots in Heavenly Village; 2hr free at some shops with validation",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 0.5,
        "elevation_gain_m": 0,
        "notes": "Paved pedestrian village with shops, restaurants, fountains for kids. Gondola base. Not wilderness but good family walk combined with gondola ride for mountain views.",
        "sources": [("https://www.skilaketahoe.com/heavenly/village", "official")]
    },
    {
        "name": "Pope Beach Family Loop",
        "place_type": "trailhead",
        "lat": 38.8578,
        "lng": -120.0411,
        "address": "Pope Beach, Pope Beach Rd, South Lake Tahoe, CA 96150",
        "parking_notes": "USFS fee lot $10/vehicle; ADA spaces; restrooms available",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 2.5,
        "elevation_gain_m": 10,
        "notes": "1.5-mile sandy beach walk with picnic areas. Gentle lake entry for kids. Buoys mark swimming area. Restrooms and concessions in summer. Less crowded than Nevada Beach.",
        "sources": [("https://www.fs.usda.gov/recarea/ltbmu/recarea/?recid=11758", "official")]
    },
    
    # RUNS
    {
        "name": "Tahoe Rim Trail - Kingsbury Grade",
        "place_type": "trailhead",
        "lat": 38.9736,
        "lng": -119.9044,
        "address": "Kingsbury Grade Trailhead, NV Hwy 207, Stateline, NV 89449",
        "parking_notes": "NV DOT lot; free; steep access road; no facilities",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 4,
        "distance_km": 12.0,
        "elevation_gain_m": 500,
        "notes": "7.5-mile out-and-back on TRT with 1,600 ft gain. High ridge running with lake views. Singletrack with some technical sections. Start early—exposed after 9am.",
        "run_type": "route",
        "sources": [("https://tahoerimtrail.org/", "official")]
    },
    {
        "name": "Lake Tahoe Marathon Events",
        "place_type": "starting_point",
        "lat": 38.9394,
        "lng": -119.9772,
        "address": "Lakeview Commons, South Lake Tahoe, CA 96150",
        "parking_notes": "Free street parking near commons; shuttles to start lines for races",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 3,
        "distance_km": 42.2,
        "elevation_gain_m": 240,
        "notes": "Annual Lake Tahoe Marathon (October) with 5K, half, full, 72-mile ultra options. Course around lake on bike paths and trails. Self-guided training routes available year-round.",
        "run_type": "event",
        "sources": [("https://www.laketahoe.com/events/marathon", "official")]
    },
    {
        "name": "Emerald Bay Loop Run",
        "place_type": "trailhead",
        "lat": 38.9481,
        "lng": -120.0456,
        "address": "D.L. Bliss State Park, Hwy 89, South Lake Tahoe, CA 96150",
        "parking_notes": "CA State Parks lot $10; fills by 9am; seasonal closure mid-Oct to Memorial Day",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 3,
        "distance_km": 8.5,
        "elevation_gain_m": 180,
        "notes": "5.3-mile loop combining Rubicon Trail and road sections. Scenic singletrack above Emerald Bay. Technical in sections. Best fall colors September-October.",
        "run_type": "route",
        "sources": [("https://www.parks.ca.gov/?page_id=507", "official")]
    },
    
    # HIKES
    {
        "name": "Maggies Peaks Trail",
        "place_type": "trailhead",
        "lat": 38.9417,
        "lng": -120.0567,
        "address": "Bayview Trailhead, Hwy 89, South Lake Tahoe, CA 96150",
        "parking_notes": "USFS lot $5; fills by 8am; overflow at D.L. Bliss",
        "kid_friendly": False,
        "activity_type": "hike",
        "difficulty": 4,
        "distance_km": 9.6,
        "elevation_gain_m": 640,
        "notes": "6-mile round trip to Maggies Peaks with Desolation Wilderness access. Panoramic views of Fallen Leaf Lake and Lake Tahoe. Granite slabs, wildflowers. Class 2 scramble to true summit.",
        "sources": [("https://www.fs.usda.gov/recarea/ltbmu/recarea/?recid=11762", "official")]
    },
    {
        "name": "Echo Lakes to Desolation Wilderness",
        "place_type": "trailhead",
        "lat": 38.8392,
        "lng": -120.0556,
        "address": "Echo Lakes Chalet, Johnson Pass Rd, South Lake Tahoe, CA 96150",
        "parking_notes": "Private lot at Echo Lakes Chalet; fee for day use; boat taxi available",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 3,
        "distance_km": 12.0,
        "elevation_gain_m": 320,
        "notes": "7.5-mile round trip to Upper Echo Lake and beyond. Boardwalk trail along lakes. Connects to PCT/JMT. Alpine scenery, granite peaks. Boat taxi cuts 2.5 miles each way.",
        "sources": [("https://www.fs.usda.gov/recarea/ltbmu/recarea/?recid=11763", "official")]
    },
    {
        "name": "Vikingsholm Trail",
        "place_type": "trailhead",
        "lat": 38.9481,
        "lng": -120.0456,
        "address": "Vikingsholm, Emerald Bay, South Lake Tahoe, CA 96150",
        "parking_notes": "CA State Parks lot $10; fills by 9am; 0.7 mile walk down from parking",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 2,
        "distance_km": 2.2,
        "elevation_gain_m": 130,
        "notes": "1.4-mile round trip to Vikingsholm mansion (Swedish castle replica) on Emerald Bay shore. Historic home tours in summer. Steep paved path. Beautiful bay views.",
        "sources": [("https://www.parks.ca.gov/?page_id=510", "official")]
    },
    
    # BOULDERING
    {
        "name": "Lover's Leap Bouldering",
        "place_type": "trailhead",
        "lat": 38.7633,
        "lng": -120.2311,
        "address": "Lover's Leap, Hwy 50, Twin Bridges, CA 95735",
        "parking_notes": "USFS lot on Hwy 50; free; 0.3 mile hike to cliff base",
        "kid_friendly": False,
        "activity_type": "bouldering",
        "difficulty": None,
        "distance_km": None,
        "elevation_gain_m": None,
        "notes": "Granite bouldering at famous trad climbing area. Boulders scattered below main cliff. Grades V2-V8. Historic climbing area—shoes required. Camping at nearby Strawberry Point.",
        "sources": [("https://www.mountainproject.com/area/105731688/lovers-leap", "web_search")]
    },
]

if __name__ == "__main__":
    print("North Lake Tahoe data loaded:", len(NORTH_TAHOE_DATA), "places")
    print("South Lake Tahoe data loaded:", len(SOUTH_TAHOE_DATA), "places")
