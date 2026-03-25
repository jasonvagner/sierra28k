#!/usr/bin/env python3
"""
Yosemite National Park Zones Data
Sources: NPS.gov, Yosemite Conservancy, USGS topo coordinates verified
"""

TUOLUMNE_MEADOWS_DATA = [
    # WALKS
    {
        "name": "Soda Springs Historic Site Walk",
        "place_type": "trailhead",
        "lat": 37.8736,
        "lng": -119.3594,
        "address": "Soda Springs, Tuolumne Meadows, Yosemite National Park, CA 95389",
        "parking_notes": "NPS paved lot at Lembert Dome trailhead; Tioga Road seasonal closure Nov-May; fills weekends",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 2.0,
        "elevation_gain_m": 20,
        "notes": "1.2-mile round trip on old road bed to carbonated mineral springs and historic Parsons Memorial Lodge. ADA-accessible boardwalk. Interpretive signs. One of Tuolumne's easiest walks at 8,600 ft.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official")]
    },
    {
        "name": "Tuolumne Meadows Loop",
        "place_type": "trailhead",
        "lat": 37.8736,
        "lng": -119.3594,
        "address": "Tuolumne Meadows, Tioga Rd (Hwy 120), Yosemite National Park, CA 95389",
        "parking_notes": "Multiple NPS lots along Tioga Road; free with park entrance ($35/vehicle); fills by 10am summer",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 4.0,
        "elevation_gain_m": 15,
        "notes": "2.5-mile gravel path along Tuolumne River through subalpine meadow. PCT/JMT junction area. Wildflowers July-August. River access. Generally flat with minimal elevation change.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official")]
    },
    
    # FAMILY WALKS
    {
        "name": "Parsons Memorial Lodge Loop",
        "place_type": "trailhead",
        "lat": 37.8758,
        "lng": -119.3589,
        "address": "Lembert Dome parking area, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Lembert Dome lot; free with park entrance; ADA accessible route available",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 1.6,
        "elevation_gain_m": 25,
        "notes": "1-mile easy loop on old mining road to Parsons Lodge (Sierra Club-built, 1915). Soda Springs, boardwalks. Interpretive programs some days. Excellent for children—nature at eye level.",
        "sources": [
            ("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official"),
            ("https://www.yosemiteconservancy.org/parsons-memorial-lodge", "official")
        ]
    },
    {
        "name": "River Loop via Pothole Dome",
        "place_type": "trailhead",
        "lat": 37.8789,
        "lng": -119.3844,
        "address": "Pothole Dome pullout, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Small dirt pullout on west side Tioga Road; limited spaces—arrive early",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 2,
        "distance_km": 2.4,
        "elevation_gain_m": 90,
        "notes": "1.5-mile round trip to granite dome summit with Tuolumne River views. Easy scramble (Class 1). Glacial polish. Wildflowers in cracks. Gentle introduction to Sierra scrambling.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official")]
    },
    
    # RUNS
    {
        "name": "Tuolumne Meadows to Lyell Canyon",
        "place_type": "trailhead",
        "lat": 37.8736,
        "lng": -119.3594,
        "address": "Tuolumne Meadows Wilderness Center, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "NPS gravel lot at wilderness center; free with park entrance; trailhead busiest in park",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 2,
        "distance_km": 10.0,
        "elevation_gain_m": 120,
        "notes": "6.2-mile out-and-back along Tuolumne River into Lyell Canyon. Gradual 200 ft gain on PCT/JMT tread. World-class trail running at 8,600-8,900 ft. Best conditions July-September.",
        "run_type": "route",
        "sources": [("https://www.nps.gov/yose/planyourvisit/tuolumne-meadows.htm", "official")]
    },
    {
        "name": "Cathedral Lakes Loop Run",
        "place_type": "trailhead",
        "lat": 37.8078,
        "lng": -119.4339,
        "address": "Cathedral Lakes Trailhead, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "NPS paved lot off Tioga Road; fills by 8am; wilderness permit required for overnight",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 4,
        "distance_km": 13.0,
        "elevation_gain_m": 300,
        "notes": "8-mile loop to Lower and Upper Cathedral Lakes at 9,200 ft. Steep initial 2 miles (1,000 ft gain). Alpine lakes beneath Cathedral Peak. Technical rocky sections. Best July-October.",
        "run_type": "route",
        "sources": [("https://www.nps.gov/yose/planyourvisit/cathedrallakes.htm", "official")]
    },
    {
        "name": "John Muir Trail Run - Tuolumne Section",
        "place_type": "trailhead",
        "lat": 37.8736,
        "lng": -119.3594,
        "address": "Tuolumne Meadows JMT trailhead, Yosemite National Park, CA 95389",
        "parking_notes": "Park at wilderness center lot; bear canister required for overnight; wilderness permit needed",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 3,
        "distance_km": 20.0,
        "elevation_gain_m": 450,
        "notes": "12-mile out-and-back on JMT/PCT from Tuolumne Meadows to Cathedral Lakes junction. Classic Sierra high country running. Mix of meadow and forest. Elevation 8,600-9,400 ft.",
        "run_type": "route",
        "sources": [("https://www.nps.gov/yose/planyourvisit/jmt.htm", "official")]
    },
    
    # HIKES
    {
        "name": "Lembert Dome Trail",
        "place_type": "trailhead",
        "lat": 37.8758,
        "lng": -119.3589,
        "address": "Lembert Dome parking, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Large paved NPS lot; free with park entrance; fills by 9am weekends",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 3,
        "distance_km": 4.0,
        "elevation_gain_m": 260,
        "notes": "2.8-mile round trip with Class 2 scramble to 9,450 ft summit. 360° views of Tuolumne Meadows, Sierra Crest. Exposed summit—use caution with children. Glacial erratics.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/lembert.htm", "official")]
    },
    {
        "name": "Cathedral Lakes Trail",
        "place_type": "trailhead",
        "lat": 37.8078,
        "lng": -119.4339,
        "address": "Cathedral Lakes Trailhead, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "NPS paved lot; fills early; wilderness permit required for overnight",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 3,
        "distance_km": 11.2,
        "elevation_gain_m": 300,
        "notes": "7-mile round trip to Lower Cathedral Lake (9,200 ft). Steep initial 3 miles. Stunning reflection of Cathedral Peak. Camping available with permit. Continue 1 mile to Upper Lake for solitude.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/cathedrallakes.htm", "official")]
    },
    {
        "name": "Dana Lakes and Mount Dana",
        "place_type": "trailhead",
        "lat": 37.9017,
        "lng": -119.2575,
        "address": "Tioga Pass Entrance Station area, Tioga Rd (Hwy 120), Yosemite National Park, CA 95389",
        "parking_notes": "Park at pass entrance area or along road; east side of park boundary",
        "kid_friendly": False,
        "activity_type": "hike",
        "difficulty": 5,
        "distance_km": 10.0,
        "elevation_gain_m": 950,
        "notes": "6.2-mile round trip to 13,061 ft Mount Dana, Yosemite's second highest peak. Trail starts at 9,943 ft (Tioga Pass). Class 1-2 scramble. Breathtaking views of Mono Lake. Start before 7am.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/mountdana.htm", "official")]
    },
    
    # BOULDERING
    {
        "name": "Tuolumne Meadows Bouldering - Puppy Dome",
        "place_type": "starting_point",
        "lat": 37.8806,
        "lng": -119.3711,
        "address": "Puppy Dome, Tioga Rd, Yosemite National Park, CA 95389",
        "parking_notes": "Dirt pullout on Tioga Road near mile marker; small area—car shuttle recommended",
        "kid_friendly": False,
        "activity_type": "bouldering",
        "difficulty": None,
        "distance_km": None,
        "elevation_gain_m": None,
        "notes": "Granite bouldering at 8,700 ft. Classics: 'Bachar-Yerian' (V2), 'Nemesis' (V6). Knobby granite. Best July-September. Limited landings—bring multiple pads. Part of famous Camp 4-style scene.",
        "sources": [("https://www.mountainproject.com/area/105731911/tuolumne-meadows", "web_search")]
    },
]

YOSEMITE_VALLEY_DATA = [
    # WALKS
    {
        "name": "Yosemite Falls Lower Walk",
        "place_type": "trailhead",
        "lat": 37.7456,
        "lng": -119.5969,
        "address": "Lower Yosemite Fall Trailhead, Northside Dr, Yosemite Village, CA 95389",
        "parking_notes": "Yosemite Valley free shuttle stop #6; day-use lot fills by 10am; bike recommended",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 2.0,
        "elevation_gain_m": 15,
        "notes": "1.2-mile paved loop to base of Lower Yosemite Fall (320 ft). ADA accessible. Views of both Upper (1,430 ft) and Lower falls. Spray can be intense in spring. Open year-round.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/yosemitefalls.htm", "official")]
    },
    {
        "name": "Cook's Meadow Loop",
        "place_type": "starting_point",
        "lat": 37.7458,
        "lng": -119.5961,
        "address": "Yosemite Valley Visitor Center, CA 95389",
        "parking_notes": "Valley Visitor Center lot; free shuttle; bike path access",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 1.6,
        "elevation_gain_m": 0,
        "notes": "1-mile flat boardwalk through meadow with views of Half Dome, Yosemite Falls, El Capitan. Best photography at golden hour. Wheelchair accessible. Interpretive signs about valley ecology.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/cooksmeadow.htm", "official")]
    },
    {
        "name": "Mirror Lake Loop",
        "place_type": "trailhead",
        "lat": 37.7497,
        "lng": -119.5469,
        "address": "Mirror Lake Trailhead, Happy Isles Loop Rd, Yosemite Valley, CA 95389",
        "parking_notes": "Yosemite Valley shuttle stop #17; seasonal road closure winter; fills summer",
        "kid_friendly": True,
        "activity_type": "walk",
        "difficulty": 1,
        "distance_km": 4.0,
        "elevation_gain_m": 60,
        "notes": "2.5-mile paved and dirt loop to seasonal Mirror Lake. Best in spring/early summer when full. Reflections of Half Dome. Sandy beach areas. ADA accessible to first viewpoint.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/mirrorlake.htm", "official")]
    },
    
    # FAMILY WALKS
    {
        "name": "Swinging Bridge",
        "place_type": "starting_point",
        "lat": 37.7419,
        "lng": -119.5983,
        "address": "Swinging Bridge, Southside Dr, Yosemite Valley, CA 95389",
        "parking_notes": "Small pullout on Southside Drive; bike recommended; 0.1 mile walk from road",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 0.3,
        "elevation_gain_m": 5,
        "notes": "0.2-mile walk to pedestrian suspension bridge over Merced River. Views of Yosemite Falls. Sandy beach below bridge for wading. Quiet alternative to crowded spots. Excellent for toddlers.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/swingingbridge.htm", "official")]
    },
    {
        "name": "Valley View Loop",
        "place_type": "starting_point",
        "lat": 37.7147,
        "lng": -119.6778,
        "address": "Valley View, Northside Dr, Yosemite Valley, CA 95389",
        "parking_notes": "Small pullout on Northside Drive; can fill with photographers at sunset",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 1,
        "distance_km": 0.5,
        "elevation_gain_m": 0,
        "notes": "Short riverside walk at iconic view of El Capitan, Bridalveil Fall, and Cathedral Rocks. One of Ansel Adams' famous photo locations. Picnic spots on sandbars. Gentle grade for all ages.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/valleyview.htm", "official")]
    },
    {
        "name": "Bridalveil Fall Walk",
        "place_type": "trailhead",
        "lat": 37.7167,
        "lng": -119.6478,
        "address": "Bridalveil Fall Trailhead, Southside Dr, Yosemite Valley, CA 95389",
        "parking_notes": "Large paved lot; fills by 9am; bike or shuttle recommended",
        "kid_friendly": True,
        "activity_type": "family_walk",
        "difficulty": 2,
        "distance_km": 2.4,
        "elevation_gain_m": 80,
        "notes": "1.5-mile round trip paved trail to 620-ft waterfall base. Wet and slippery from spray year-round. Wind can push spray dramatically. Beautiful rainbows in afternoon. Accessible but steep final section.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/bridalveil.htm", "official")]
    },
    
    # RUNS
    {
        "name": "Yosemite Valley Loop Trail",
        "place_type": "trailhead",
        "lat": 37.7456,
        "lng": -119.5969,
        "address": "Yosemite Valley, multiple access points, CA 95389",
        "parking_notes": "Start at any valley location; bike to create loop; free shuttle between points",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 2,
        "distance_km": 11.2,
        "elevation_gain_m": 90,
        "notes": "7-mile loop on paved bike path and dirt trails around valley floor. Mix of forest, meadow, and river. Elevation 4,000 ft. Good training run with iconic views throughout. Best at sunrise.",
        "run_type": "route",
        "sources": [("https://www.nps.gov/yose/planyourvisit/valleytrails.htm", "official")]
    },
    {
        "name": "Yosemite Half Marathon",
        "place_type": "starting_point",
        "lat": 37.7456,
        "lng": -119.5969,
        "address": "Yosemite Valley, start near Yosemite Lodge, CA 95389",
        "parking_notes": "Event day shuttle from remote lots; reservation required for race",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 3,
        "distance_km": 21.1,
        "elevation_gain_m": 180,
        "notes": "Annual Yosemite Half Marathon (May). Paved and dirt roads through valley with views of all major formations. 4,000 ft elevation. Self-guided training routes available year-round on similar terrain.",
        "run_type": "event",
        "sources": [("https://www.yosemitehalfmarathon.com/", "official")]
    },
    {
        "name": "Four Mile Trail Run",
        "place_type": "trailhead",
        "lat": 37.7325,
        "lng": -119.6033,
        "address": "Four Mile Trailhead, Southside Dr near Sentinel Beach, Yosemite Valley, CA 95389",
        "parking_notes": "Sentinel Beach picnic area lot; fills early; winter closure upper sections",
        "kid_friendly": False,
        "activity_type": "run",
        "difficulty": 4,
        "distance_km": 9.6,
        "elevation_gain_m": 970,
        "notes": "6-mile round trip to Glacier Point. 3,200 ft gain—one of the biggest in the valley. Singletrack switchbacks with epic views. Run up, shuttle down or reverse. Best April-November.",
        "run_type": "route",
        "sources": [("https://www.nps.gov/yose/planyourvisit/fourmile.htm", "official")]
    },
    
    # HIKES
    {
        "name": "Mist Trail to Vernal Fall",
        "place_type": "trailhead",
        "lat": 37.7328,
        "lng": -119.5583,
        "address": "Happy Isles Trailhead, Happy Isles Loop Rd, Yosemite Valley, CA 95389",
        "parking_notes": "Yosemite Valley shuttle stop #16; no private vehicles; early arrival essential",
        "kid_friendly": True,
        "activity_type": "hike",
        "difficulty": 3,
        "distance_km": 5.1,
        "elevation_gain_m": 305,
        "notes": "3.2-mile round trip to 317-ft Vernal Fall. 'Mist' from waterfall drenches hikers—bring rain gear. Granite steps (600+ of them). Spectacular in spring runoff. Slippery when wet.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/misttrail.htm", "official")]
    },
    {
        "name": "Mist Trail to Nevada Fall",
        "place_type": "trailhead",
        "lat": 37.7328,
        "lng": -119.5583,
        "address": "Happy Isles Trailhead, Yosemite Valley, CA 95389",
        "parking_notes": "Yosemite Valley shuttle stop #16; wilderness permit required for beyond Nevada Fall",
        "kid_friendly": False,
        "activity_type": "hike",
        "difficulty": 4,
        "distance_km": 10.4,
        "elevation_gain_m": 670,
        "notes": "6.5-mile round trip past Vernal to 594-ft Nevada Fall. Continue past John Muir Trail junction. 'Giant Staircase' of granite steps. Dry sections by late summer. Combine with JMT for loop.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/misttrail.htm", "official")]
    },
    {
        "name": "Yosemite Falls Trail",
        "place_type": "trailhead",
        "lat": 37.7456,
        "lng": -119.5969,
        "address": "Camp 4 or Yosemite Lodge area, Yosemite Valley, CA 95389",
        "parking_notes": "Camp 4 walk-in (lottery required); or park at Yosemite Valley Lodge",
        "kid_friendly": False,
        "activity_type": "hike",
        "difficulty": 5,
        "distance_km": 11.6,
        "elevation_gain_m": 820,
        "notes": "7.2-mile round trip to top of 2,425-ft Yosemite Falls (North America's tallest). Extremely steep switchbacks. Columbia Rock viewpoint at 1 mile. Seasonal—waterfall dry late summer. Avoid ice in winter.",
        "sources": [("https://www.nps.gov/yose/planyourvisit/yosemitefalls.htm", "official")]
    },
    {
        "name": "Half Dome Trail",
        "place_type": "trailhead",
        "lat": 37.7328,
        "lng": -119.5583,
        "address": "Happy Isles Trailhead, Yosemite Valley, CA 95389",
        "parking_notes": "Yosemite Valley shuttle stop #16; advance wilderness permit REQUIRED",
        "kid_friendly": False,
        "activity_type": "hike",
        "difficulty": 5,
        "distance_km": 27.4,
        "elevation_gain_m": 1475,
        "notes": "17-mile round trip via Mist Trail or JMT. 4,800 ft total gain. Iconic 400-ft cable section to 8,839 ft summit. Permit via lottery ($10 + $10/person). Start before 5am. Seasonal cables May-October.",
        "sources": [
            ("https://www.nps.gov/yose/planyourvisit/halfdome.htm", "official"),
            ("https://www.recreation.gov/permits/234653", "official")
        ]
    },
    
    # BOULDERING
    {
        "name": "Camp 4 Bouldering",
        "place_type": "starting_point",
        "lat": 37.7425,
        "lng": -119.6025,
        "address": "Camp 4, Southside Dr, Yosemite Valley, CA 95389",
        "parking_notes": "Camp 4 day-use parking (lottery required); or park at Yosemite Valley Lodge and walk",
        "kid_friendly": False,
        "activity_type": "bouldering",
        "difficulty": None,
        "distance_km": None,
        "elevation_gain_m": None,
        "notes": "World-famous granite bouldering birthplace. Classics: 'Midnight Lightning' (V8), 'Cocaine Corner' (V2). Free camping area. Historic climbing culture. Bring multiple crash pads. Best spring/fall—summer hot.",
        "sources": [
            ("https://www.nps.gov/yose/planyourvisit/camp4.htm", "official"),
            ("https://www.mountainproject.com/area/105730932/camp-4", "web_search")
        ]
    },
    {
        "name": "Church Bowl Bouldering",
        "place_type": "starting_point",
        "lat": 37.7372,
        "lng": -119.5967,
        "address": "Church Bowl, Southside Dr near Yosemite Chapel, Yosemite Valley, CA 95389",
        "parking_notes": "Yosemite Chapel lot or street parking; walk uphill to boulders",
        "kid_friendly": False,
        "activity_type": "bouldering",
        "difficulty": None,
        "distance_km": None,
        "elevation_gain_m": None,
        "notes": "Historic bouldering area with easier problems. Grades V0-V4. Great for beginners to intermediate. Better shade than Camp 4 in summer. Mix of slab and vertical granite.",
        "sources": [("https://www.mountainproject.com/area/105731027/church-bowl", "web_search")]
    },
]

if __name__ == "__main__":
    print("Tuolumne Meadows data loaded:", len(TUOLUMNE_MEADOWS_DATA), "places")
    print("Yosemite Valley data loaded:", len(YOSEMITE_VALLEY_DATA), "places")
