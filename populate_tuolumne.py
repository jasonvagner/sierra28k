#!/usr/bin/env python3
"""Populate Tuolumne Meadows zone (zone_id=3)."""
import sqlite3, os
from datetime import datetime

DB = os.path.join(os.path.dirname(__file__), "sierra28k.db")

places = [
    # WALKS
    {"name":"Parsons Lodge & Soda Springs","place_type":"trail","lat":37.8758,"lng":-119.3537,"address":"Tuolumne Meadows, Yosemite NP, CA 95389","parking_notes":"Lembert Dome lot or VC lot, free with park entry","kid_friendly":1,
     "activities":[{"activity_type":"walk","difficulty":1,"distance_km":2.3,"elevation_gain_m":15,"notes":"Flat stroll to carbonated Soda Springs and historic Parsons Memorial Lodge. Where Muir and Johnson conceived Yosemite NP. Unpaved, well-maintained.","run_type":None},
                   {"activity_type":"family_walk","difficulty":1,"distance_km":2.3,"elevation_gain_m":15,"notes":"NPS top family pick: kids love touching carbonated spring water. Mostly flat, stroller-accessible. Bring sunscreen at 8,600 ft.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Pothole Dome","place_type":"trail","lat":37.8720,"lng":-119.4162,"address":"Pothole Dome Pullout, Tioga Rd, Yosemite NP, CA 95389","parking_notes":"Small roadside pullout, ~10 cars, south side Tioga Rd west end of meadow","kid_friendly":1,
     "activities":[{"activity_type":"walk","difficulty":1,"distance_km":1.6,"elevation_gain_m":60,"notes":"Short walk then easy granite scramble. First panoramic view of Tuolumne Meadows from summit. Slippery when wet.","run_type":None},
                   {"activity_type":"family_walk","difficulty":1,"distance_km":1.6,"elevation_gain_m":60,"notes":"NPS-listed short family option. Easy scramble for kids 5+. Granite friction — closed-toe shoes recommended.","run_type":None},
                   {"activity_type":"bouldering","difficulty":1,"distance_km":0.8,"elevation_gain_m":60,"notes":"Low-angle exfoliation dome — beginner granite friction. Potholes (glacial melt features) at base. Good family intro to Tuolumne granite. No permit needed.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Tuolumne River Walk — Lyell Fork to Twin Bridges","place_type":"trail","lat":37.8723,"lng":-119.3372,"address":"Dog Lake Trailhead, Tuolumne Meadows, Yosemite NP, CA 95389","parking_notes":"Dog Lake lot, north side Tioga Rd east of VC. Free. Overflow at Wilderness Center.","kid_friendly":1,
     "activities":[{"activity_type":"walk","difficulty":1,"distance_km":4.8,"elevation_gain_m":20,"notes":"Flat JMT along Lyell Fork to Twin Bridges — scenic wading spot. Mostly flat, uneven terrain. Excellent early-morning light on river.","run_type":None},
                   {"activity_type":"family_walk","difficulty":1,"distance_km":2.4,"elevation_gain_m":10,"notes":"Turn-around version for families. Easy wading access at multiple points. Marmots and deer frequently seen.","run_type":None},
                   {"activity_type":"run","difficulty":2,"distance_km":19.3,"elevation_gain_m":213,"notes":"One of the finest high-altitude trail runs in the Sierra. Flat runnable JMT/PCT corridor to Lyell Base Camp (~9.7 km one-way). Elevation 8,700–9,500 ft. Wilderness permit for overnight; day use free.","run_type":"route"}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Tenaya Lake Shore","place_type":"trail","lat":37.8370,"lng":-119.4680,"address":"Tenaya Lake West Picnic Area, Tioga Rd, Yosemite NP, CA 95389","parking_notes":"Two picnic lots (east/west). West lot wheelchair accessible. Both free with park entry. Fills by mid-morning weekends.","kid_friendly":1,
     "activities":[{"activity_type":"walk","difficulty":1,"distance_km":3.2,"elevation_gain_m":10,"notes":"Informal trail circling Tenaya Lake at 8,150 ft. Swimming, paddleboarding, kayaking from shore. No permit required.","run_type":None},
                   {"activity_type":"family_walk","difficulty":1,"distance_km":1.5,"elevation_gain_m":5,"notes":"Flat shoreline walk with sandy beaches — one of Yosemite's best family swimming spots. Water cold even in July. Accessible picnic tables.","run_type":None},
                   {"activity_type":"run","difficulty":2,"distance_km":11.3,"elevation_gain_m":160,"notes":"Point-to-point trail run, Tenaya Lake east to Tuolumne Meadows. Mix of use trails and Tioga Rd shoulder. Elevation 8,150–8,600 ft. Car shuttle or park shuttle needed for one-way.","run_type":"route"}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tm.htm","source_type":"official"},

    {"name":"Olmsted Point Viewpoint","place_type":"starting_point","lat":37.8195,"lng":-119.4900,"address":"Olmsted Point Parking, Tioga Rd, Yosemite NP, CA 95389","parking_notes":"Large pullout, south side Tioga Rd. Restrooms on site. Free with park entry.","kid_friendly":1,
     "activities":[{"activity_type":"walk","difficulty":1,"distance_km":0.8,"elevation_gain_m":20,"notes":"Short informal walk across glacier-polished granite to viewpoint. Half Dome visible. Glacial erratics scattered across slabs. No maintained trail.","run_type":None},
                   {"activity_type":"family_walk","difficulty":1,"distance_km":0.8,"elevation_gain_m":20,"notes":"Kids enjoy exploring glacial erratic boulders. Educational NPS geology signage on site. Good photo stop.","run_type":None},
                   {"activity_type":"bouldering","difficulty":1,"distance_km":0.5,"elevation_gain_m":25,"notes":"Glacier-polished slabs and large erratics offer informal scrambling immediately from parking. Natural beginner granite environment. No established problems. NPS geology interpretation on site.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tm.htm","source_type":"official"},

    # RUNS (dedicated)
    {"name":"Glen Aulin Trailhead — Lembert Dome","place_type":"trailhead","lat":37.8797,"lng":-119.3492,"address":"Lembert Dome Parking, Tuolumne Meadows, Yosemite NP, CA 95389","parking_notes":"Large lot, north side Tioga Rd. Free with park entry. Flush toilets. Also summer shuttle stop.","kid_friendly":0,
     "activities":[{"activity_type":"run","difficulty":3,"distance_km":17.7,"elevation_gain_m":240,"notes":"Glen Aulin trail run: JMT/PCT singletrack follows Tuolumne River 8.9 km to Glen Aulin HSC and back. Net downhill going (240 m gain on return). Passes Tuolumne Falls and White Cascade. Elevation 8,600–7,800 ft.","run_type":"route"},
                   {"activity_type":"run","difficulty":4,"distance_km":22.0,"elevation_gain_m":400,"notes":"Young Lakes Loop trail run via Glen Aulin or Dog Lake. NPS lists as 13.6-mile day hike. Classic trail running objective reaching Young Lakes at 10,000 ft.","run_type":"route"},
                   {"activity_type":"hike","difficulty":3,"distance_km":17.7,"elevation_gain_m":240,"notes":"Classic NPS hike: 'Follow the Tuolumne River 5.5 miles as it drops to Glen Aulin.' Passes Tuolumne Falls and White Cascade. Glen Aulin HSC at end. Optional extension to Waterwheel Falls (+3 miles).","run_type":None},
                   {"activity_type":"hike","difficulty":3,"distance_km":6.1,"elevation_gain_m":260,"notes":"Lembert Dome summit hike: 3.8-mile round trip via Dog Lake trail with steep final approach on open granite to summit at 9,450 ft. Panoramic views of meadows and peaks. NPS: 'Stay off domes during thunderstorms.'","run_type":None},
                   {"activity_type":"bouldering","difficulty":3,"distance_km":0.3,"elevation_gain_m":30,"notes":"Lembert Dome base bouldering on world-class Tuolumne granite. NPS: 'pinching crystals on sun-drenched Tuolumne Meadows domes.' Slab climbing and established problems. Helmets recommended. No permit needed.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Tuolumne Meadows Visitor Center Trailhead","place_type":"trailhead","lat":37.8760,"lng":-119.3620,"address":"Tuolumne Meadows Visitor Center, 14000 Tioga Rd, Yosemite NP, CA 95389","parking_notes":"VC lot, south side Tioga Rd. Free with park entry. Summer shuttle stop. Can fill by 8 AM weekends.","kid_friendly":1,
     "activities":[{"activity_type":"run","difficulty":2,"distance_km":8.0,"elevation_gain_m":80,"notes":"Informal meadow loop combining meadow paths, Tuolumne River corridor, Soda Springs, Parsons Lodge. Nearly flat at 8,600 ft. Popular with lodge guests. Mix of dirt trail and grass — muddy early season.","run_type":"route"},
                   {"activity_type":"run","difficulty":3,"distance_km":21.1,"elevation_gain_m":350,"notes":"Yosemite Half Marathon: annual road/trail event utilizing Tioga Rd and Tuolumne Meadows. High altitude racing at 8,600 ft. Verify 2026 date and NPS permit status at recreation.gov.","run_type":"event"},
                   {"activity_type":"hike","difficulty":3,"distance_km":12.2,"elevation_gain_m":305,"notes":"Cathedral Lakes: NPS 'most popular trail climbs steadily to Upper Cathedral Lake.' Lower at 9,288 ft, Upper at 9,585 ft beneath Cathedral Peak (10,911 ft). Wildflowers peak late July. Wilderness permit for overnight.","run_type":None},
                   {"activity_type":"hike","difficulty":3,"distance_km":11.0,"elevation_gain_m":305,"notes":"Elizabeth Lake: 'Glacier-carved lake at the base of Unicorn Peak' (9,503 ft). Steady climb over first 2 miles. Less crowded than Cathedral Lakes. Optional 1-mile loop around lake. No day use permit needed.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    # HIKES (dedicated)
    {"name":"Dog Lake Trailhead","place_type":"trailhead","lat":37.8797,"lng":-119.3492,"address":"Dog Lake Parking, Tuolumne Meadows, Yosemite NP, CA 95389","parking_notes":"Adjacent to Lembert Dome lot, north of Tioga Rd. Overnight quota: 12 lottery / 8 first-come.","kid_friendly":0,
     "activities":[{"activity_type":"hike","difficulty":2,"distance_km":5.0,"elevation_gain_m":170,"notes":"Dog Lake (9,170 ft): shallow, warm-for-Sierra swimming lake. Can be combined with Lembert Dome for 6.1 km loop. Forested trail, less exposed on stormy days. Good on days with afternoon thunderstorm risk.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Rafferty Creek / Wilderness Center Trailhead","place_type":"trailhead","lat":37.8723,"lng":-119.3372,"address":"Wilderness Center Parking, Tuolumne Meadows, Yosemite NP, CA 95389","parking_notes":"Wilderness Center lot, north of Tioga Rd. Overnight quota: 12 lottery / 8 first-come (Rafferty Creek).","kid_friendly":0,
     "activities":[{"activity_type":"hike","difficulty":4,"distance_km":24.1,"elevation_gain_m":570,"notes":"Vogelsang via Rafferty Creek: long day hike to Vogelsang HSC at 10,330 ft. 570 m gain into high alpine zone. Stunning Clark Range and Cathedral Range views. Wilderness permit for overnight. Classic backpacking route.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/trailheads.htm","source_type":"official"},

    {"name":"Tioga Pass Entrance Trailhead","place_type":"trailhead","lat":37.9083,"lng":-119.2573,"address":"Tioga Pass Entrance Station, Hwy 120, Yosemite NP, CA 95389","parking_notes":"Small pullout inside Tioga Pass entrance, ~20 cars. Often full summer mornings. Highest trailhead in park at 9,945 ft.","kid_friendly":0,
     "activities":[{"activity_type":"hike","difficulty":2,"distance_km":4.2,"elevation_gain_m":152,"notes":"Gaylor Lakes: 'Climb steadily to ridge with spectacular views of Dana Meadows.' Middle Gaylor Lake then optional cross-country to Great Sierra Mine ruins. Start at 9,945 ft. Best short high-altitude hike in Yosemite.","run_type":None},
                   {"activity_type":"hike","difficulty":5,"distance_km":9.7,"elevation_gain_m":945,"notes":"Mount Dana (13,061 ft): 2nd highest peak in Yosemite. ~9.7 km RT with 945 m gain, all above 9,945 ft. No maintained trail — cross-country on use trail. Outstanding views of Mono Lake and Sierra crest. Afternoon thunderstorms July–Aug.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Mono Pass Trailhead — Dana Meadows","place_type":"trailhead","lat":37.8967,"lng":-119.2700,"address":"Mono Pass Trailhead, Tioga Rd at Dana Meadows, Yosemite NP, CA 95389","parking_notes":"Small roadside parking on Tioga Rd ~1.5 mi west of Tioga Pass. Limited spaces. Overnight quota: 9 lottery / 6 first-come.","kid_friendly":0,
     "activities":[{"activity_type":"hike","difficulty":3,"distance_km":12.9,"elevation_gain_m":300,"notes":"Mono Pass: 'Climb steadily for views of Mono Lake and eastern Sierra.' Trail gains 300 m to Mono Pass at 10,604 ft on Yosemite boundary. Historic mining-era cabins at pass. Views east to Mono Lake and Great Basin.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/tmhikes.htm","source_type":"official"},

    {"name":"Tuolumne High Country Domes — Bouldering","place_type":"starting_point","lat":37.8600,"lng":-119.4000,"address":"Various Tioga Rd pullouts, Yosemite NP, CA 95389","parking_notes":"Fairview Dome pullout at ~37.860, -119.400. Daff Dome and Stately Pleasure Dome from nearby pullouts. Cathedral Peak bouldering from Cathedral Lakes trailhead.","kid_friendly":0,
     "activities":[{"activity_type":"bouldering","difficulty":3,"distance_km":1.5,"elevation_gain_m":100,"notes":"World-renowned high-altitude granite bouldering. Established problems at Fairview Dome base (grades V0–V8), Daff Dome, Stately Pleasure Dome. NPS: 'pinching crystals on sun-drenched Tuolumne domes.' Best season July–Sept. NPS climbing regs apply. No permit for bouldering.","run_type":None}],
     "source_url":"https://www.nps.gov/yose/planyourvisit/climbing.htm","source_type":"official"},
]

def insert_zone_data(zone_id, places_data):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    place_count = 0
    activity_count = 0
    source_count = 0

    for p in places_data:
        cur.execute("""INSERT INTO places (zone_id, name, place_type, lat, lng, address, parking_notes, kid_friendly)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (zone_id, p["name"], p["place_type"], p["lat"], p["lng"],
                     p.get("address"), p.get("parking_notes"), p["kid_friendly"]))
        place_id = cur.lastrowid
        place_count += 1

        for a in p["activities"]:
            cur.execute("""INSERT INTO activities (place_id, activity_type, difficulty, distance_km, elevation_gain_m, notes, run_type)
                           VALUES (?,?,?,?,?,?,?)""",
                        (place_id, a["activity_type"], a["difficulty"], a["distance_km"],
                         a["elevation_gain_m"], a["notes"], a["run_type"]))
            activity_count += 1

        cur.execute("""INSERT INTO sources (place_id, url, source_type, retrieved_at)
                       VALUES (?,?,?,?)""",
                    (place_id, p["source_url"], p["source_type"], datetime.utcnow().isoformat()))
        source_count += 1

    conn.commit()
    conn.close()
    return place_count, activity_count, source_count

if __name__ == "__main__":
    pc, ac, sc = insert_zone_data(3, places)
    print(f"Tuolumne Meadows: {pc} places, {ac} activities, {sc} sources inserted")
