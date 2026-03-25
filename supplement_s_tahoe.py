#!/usr/bin/env python3
"""Supplement South Lake Tahoe (zone 2) with missing walks, family walks, and bouldering."""
import sys; sys.path.insert(0,'.')
from db_insert import insert_zone, zone_summary

places = [
    # WALKS
    {"name":"Taylor Creek Stream Trail","place_type":"trail","lat":38.9403,"lng":-120.0525,
     "address":"Taylor Creek Visitor Center, 870 Emerald Bay Rd, South Lake Tahoe, CA 96150",
     "parking_notes":"Free parking at Taylor Creek Visitor Center (USFS). Fills on summer weekends. Flush toilets on site.",
     "kid_friendly":True,
     "activities":[
         {"activity_type":"walk","difficulty":1,"distance_km":1.6,"elevation_gain_m":5,
          "notes":"USFS-designated easy interpretive walk along Taylor Creek to Lake Tahoe. Famous for annual Kokanee salmon spawn (Oct). Boardwalk through meadow and willows. Wheelchair accessible sections. Stream profile chamber lets visitors view fish underwater.","run_type":None},
         {"activity_type":"family_walk","difficulty":1,"distance_km":1.6,"elevation_gain_m":5,
          "notes":"NPS/USFS top family pick for South Lake Tahoe. Salmon viewing in October is an unmissable kid experience. Flat boardwalk trail, stroller accessible. Visitor Center has hands-on exhibits. Restrooms at trailhead.","run_type":None},
     ],
     "source_url":"https://www.fs.usda.gov/recarea/ltbmu/recreation/recarea/?recid=11790","source_type":"official"},

    {"name":"Emerald Bay State Park — Shoreline Walk","place_type":"trail","lat":38.9538,"lng":-120.1038,
     "address":"Emerald Bay State Park, Emerald Bay Rd (Hwy 89), South Lake Tahoe, CA 96150",
     "parking_notes":"Emerald Bay Overlook parking on Hwy 89 (day use fee). Shuttle from South Lake Tahoe recommended in summer — lot fills by 9 AM. Vikingsholm parking lot is lower and larger.",
     "kid_friendly":True,
     "activities":[
         {"activity_type":"walk","difficulty":2,"distance_km":3.2,"elevation_gain_m":160,
          "notes":"Walk from Vikingsholm parking area down to Emerald Bay beach and historic Vikingsholm Castle (tours available summer). 160 m descent/ascent. California State Parks-managed. Strenuous for small children on return. One of the most photographed spots in California.","run_type":None},
         {"activity_type":"family_walk","difficulty":2,"distance_km":3.2,"elevation_gain_m":160,
          "notes":"Family walk to Vikingsholm Castle on Emerald Bay — rated one of the finest examples of Scandinavian architecture in North America. Free to walk to; castle tours fee. Beach at bay bottom. Bring water and snacks; no services below overlook.","run_type":None},
     ],
     "source_url":"https://www.parks.ca.gov/?page_id=506","source_type":"official"},

    {"name":"Cascade Falls","place_type":"trailhead","lat":38.9414,"lng":-120.0920,
     "address":"Bayview Campground Trailhead, Hwy 89, South Lake Tahoe, CA 96150",
     "parking_notes":"Bayview Campground parking area on east side of Hwy 89. Day use parking on shoulder. No fee for day use at trailhead. Fills quickly on summer weekends.",
     "kid_friendly":True,
     "activities":[
         {"activity_type":"walk","difficulty":2,"distance_km":3.2,"elevation_gain_m":130,
          "notes":"El Dorado National Forest trail to Cascade Falls — 100+ ft waterfall on Cascade Creek. 1.6 km each way. Rocky terrain, some boulder scrambling near falls. Best flow spring through early July. Spectacular views of Cascade Lake below.","run_type":None},
         {"activity_type":"family_walk","difficulty":2,"distance_km":3.2,"elevation_gain_m":130,
          "notes":"Popular family destination for waterfall viewing. Short enough for older kids (5+). Rocky terrain requires sturdy shoes. Peak flow late spring. Stay back from waterfall edges — rocks are slippery. No restrooms at trailhead.","run_type":None},
     ],
     "source_url":"https://www.fs.usda.gov/recarea/eldorado/recreation/recarea/?recid=12803","source_type":"official"},

    # BOULDERING supplement
    {"name":"Phantom Spires Bouldering — El Dorado NF","place_type":"trail","lat":38.7810,"lng":-120.1540,
     "address":"Phantom Spires Trailhead, Ice House Rd, El Dorado National Forest, CA 95726",
     "parking_notes":"Small parking pullout on Ice House Road, El Dorado National Forest. No fee. Rough road access — high clearance recommended.",
     "kid_friendly":False,
     "activities":[
         {"activity_type":"bouldering","difficulty":3,"distance_km":2.0,"elevation_gain_m":150,
          "notes":"El Dorado National Forest volcanic rock bouldering and top-rope climbing area near Sierra-at-Tahoe resort. Several distinct spires and boulder fields. Grades range V0–V8. Solitude compared to Lover's Leap. Best season May–October. No permit required.","run_type":None},
     ],
     "source_url":"https://www.fs.usda.gov/eldorado","source_type":"official"},

    {"name":"D.L. Bliss State Park — Shoreline Walk","place_type":"trail","lat":38.9740,"lng":-120.1040,
     "address":"D.L. Bliss State Park, Hwy 89, Tahoma, CA 96142",
     "parking_notes":"D.L. Bliss State Park entrance off Hwy 89. Day use fee. Rubicon Trail parking near Calawee Cove Beach.","kid_friendly":True,
     "activities":[
         {"activity_type":"walk","difficulty":1,"distance_km":4.0,"elevation_gain_m":30,
          "notes":"California State Parks shoreline trail through D.L. Bliss SP along the western shore of Lake Tahoe. Crystal-clear water, granite boulders, and forested slopes. Connects to Vikingsholm/Emerald Bay as part of the Rubicon Trail. Light traffic compared to busier South Shore spots.","run_type":None},
         {"activity_type":"family_walk","difficulty":1,"distance_km":2.0,"elevation_gain_m":15,
          "notes":"Family walk to Calawee Cove — one of Lake Tahoe's best accessible sandy beaches within D.L. Bliss SP. Short walk from parking. Restrooms at beach. Calmer water than open South Shore. Good for small kids.","run_type":None},
     ],
     "source_url":"https://www.parks.ca.gov/?page_id=507","source_type":"official"},
]

if __name__ == "__main__":
    import sqlite3
    conn = sqlite3.connect('sierra28k.db')
    cur = conn.cursor()
    existing = {r[0] for r in cur.execute('SELECT name FROM places WHERE zone_id=2').fetchall()}
    conn.close()
    new = [p for p in places if p['name'] not in existing]
    print(f"S Lake Tahoe: {len(new)} new places to insert")
    if new:
        pc, ac, sc = insert_zone(2, new)
        print(f"Inserted {pc} places, {ac} activities")
    zone_summary(2, "South Lake Tahoe")
