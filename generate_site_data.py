#!/usr/bin/env python3
"""
Generate docs/data.json — structured site data with canonical links,
season info, and search fallback links.
"""
import sqlite3, json, os, urllib.parse
from collections import defaultdict

DB = os.path.join(os.path.dirname(__file__), "sierra28k.db")
OUT = os.path.join(os.path.dirname(__file__), "docs", "data.json")

# ── Canonical link priority (checked in order against the URL) ───────────────
# If a source URL contains one of these domains/paths, prefer it.
PREFERRED_DOMAINS = [
    "nps.gov",
    "fs.usda.gov",
    "parks.ca.gov",
    "recreation.gov",
    "alltrails.com",
    "mountainproject.com",
    "thecrag.com",
    "mammothtrails.org",
    "townofmammothlakes.ca.gov",
    "visitmammoth.com",
    "visittahoesouth.com",
    "gotahoenorth.com",
    "yosemite.com",
]

FALLBACK_SITE_HINTS = {
    # zone_id → preferred site: operator for Google search fallback
    1: "site:nps.gov OR site:alltrails.com OR site:tahoetrails.com",
    2: "site:nps.gov OR site:alltrails.com",
    3: "site:nps.gov",            # Yosemite
    4: "site:mammothtrails.org OR site:alltrails.com OR site:nps.gov",
    5: "site:fs.usda.gov OR site:alltrails.com OR site:mountainproject.com",
    6: "site:nps.gov OR site:alltrails.com",  # Yosemite Valley
    7: "site:nps.gov OR site:alltrails.com",  # Sequoia/Kings Canyon
}

ACTIVITY_LABELS = {
    "walk": "Walk",
    "family_walk": "Family Walk",
    "run": "Run",
    "hike": "Hike",
    "bouldering": "Bouldering",
    "peak_bagging": "Peak Bagging",
}

DIFFICULTY_LABELS = {1: "Very Easy", 2: "Easy", 3: "Moderate", 4: "Hard", 5: "Very Hard"}


def pick_url(sources, zone_id):
    """Return the best canonical URL from a list of source dicts."""
    if not sources:
        return None
    # Score each URL
    def score(url):
        for i, domain in enumerate(PREFERRED_DOMAINS):
            if domain in url:
                return len(PREFERRED_DOMAINS) - i  # higher = better
        return 0
    return max(sources, key=lambda s: score(s["url"]))["url"]


def google_search_url(place_name, zone_name, activity_type, zone_id):
    hint = FALLBACK_SITE_HINTS.get(zone_id, "site:alltrails.com OR site:nps.gov")
    query = f'{place_name} {zone_name} {ACTIVITY_LABELS.get(activity_type, "")} ({hint})'
    return "https://www.google.com/search?q=" + urllib.parse.quote(query)


def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    zones = {r["id"]: dict(r) for r in cur.execute("SELECT * FROM zones ORDER BY id").fetchall()}

    # places keyed by id
    places = {r["id"]: dict(r) for r in cur.execute("SELECT * FROM places ORDER BY id").fetchall()}

    # activities
    activities = cur.execute("SELECT * FROM activities ORDER BY id").fetchall()

    # sources grouped by place_id
    sources_by_place = defaultdict(list)
    for r in cur.execute("SELECT * FROM sources").fetchall():
        sources_by_place[r["place_id"]].append(dict(r))
    conn.close()

    # Build zone → places → activities tree
    zone_data = []
    for zone_id, zone in zones.items():
        zone_places = [p for p in places.values() if p["zone_id"] == zone_id]

        place_list = []
        for place in sorted(zone_places, key=lambda p: p["name"]):
            pid = place["id"]
            src = sources_by_place.get(pid, [])
            canonical_url = pick_url(src, zone_id)

            place_acts = [dict(a) for a in activities if a["place_id"] == pid]
            if not place_acts:
                continue  # skip places with no activities

            act_list = []
            for a in sorted(place_acts, key=lambda x: x["activity_type"]):
                search_url = google_search_url(
                    place["name"], zone["name"], a["activity_type"], zone_id
                )
                act_list.append({
                    "id": a["id"],
                    "activity_type": a["activity_type"],
                    "activity_label": ACTIVITY_LABELS.get(a["activity_type"], a["activity_type"]),
                    "difficulty": a["difficulty"],
                    "difficulty_label": DIFFICULTY_LABELS.get(a["difficulty"]),
                    "distance_km": a["distance_km"],
                    "elevation_gain_m": a["elevation_gain_m"],
                    "notes": a["notes"],
                    "run_type": a["run_type"],
                    "best_months": a["best_months"],
                    "conditions_note": a["conditions_note"],
                    "search_url": search_url,
                })

            place_list.append({
                "id": pid,
                "name": place["name"],
                "place_type": place["place_type"],
                "lat": place["lat"],
                "lng": place["lng"],
                "address": place["address"],
                "parking_notes": place["parking_notes"],
                "kid_friendly": bool(place["kid_friendly"]),
                "image_url": place["image_url"],
                "canonical_url": canonical_url,
                "activities": act_list,
            })

        zone_data.append({
            "id": zone_id,
            "name": zone["name"],
            "region": zone["region"],
            "description": zone["description"],
            "places": place_list,
        })

    output = {
        "meta": {
            "generated_at": __import__("datetime").datetime.now().isoformat(),
            "total_zones": len(zone_data),
            "total_places": sum(len(z["places"]) for z in zone_data),
            "total_activities": sum(
                len(p["activities"]) for z in zone_data for p in z["places"]
            ),
        },
        "zones": zone_data,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Written: {OUT}")
    print(f"  Zones: {output['meta']['total_zones']}")
    print(f"  Places: {output['meta']['total_places']}")
    print(f"  Activities: {output['meta']['total_activities']}")


if __name__ == "__main__":
    main()
