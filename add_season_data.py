#!/usr/bin/env python3
"""Add best_months and conditions_note to activities; image_url to places."""
import sqlite3, os, re

DB = os.path.join(os.path.dirname(__file__), 'sierra28k.db')

# ── Zone-level defaults ────────────────────────────────────────────────────────
# (best_months, conditions_note_or_None)
ZONE_DEFAULTS = {
    1: {  # North Lake Tahoe
        'walk':         ('May–October',  None),
        'family_walk':  ('May–October',  None),
        'run':          ('June–October', None),
        'hike':         ('June–October', None),
        'bouldering':   ('May–October',  None),
        'peak_bagging': ('July–September', 'Start early Jul–Aug; afternoon thunderstorms common above treeline'),
    },
    2: {  # South Lake Tahoe
        'walk':         ('May–October',  None),
        'family_walk':  ('May–October',  None),
        'run':          ('June–October', None),
        'hike':         ('June–October', None),
        'bouldering':   ('May–October',  None),
        'peak_bagging': ('July–September', 'Start early Jul–Aug; afternoon thunderstorms common above treeline'),
    },
    3: {  # Tuolumne Meadows — road-gated
        'walk':         ('July–September', 'Tioga Road typically closes November–May; verify at nps.gov/yose'),
        'family_walk':  ('July–September', 'Tioga Road typically closes November–May; verify at nps.gov/yose'),
        'run':          ('July–September', 'Tioga Road closes November–May; start early to avoid afternoon storms'),
        'hike':         ('July–September', 'Tioga Road closes November–May; afternoon thunderstorms Jul–Aug — summit by noon'),
        'bouldering':   ('July–September', 'Tioga Road closes November–May; rock can overheat midday in August'),
        'peak_bagging': ('July–September', 'Tioga Road closes November–May; afternoon thunderstorms Jul–Aug — off exposed terrain by noon'),
    },
    4: {  # Mammoth Lakes
        'walk':         ('May–October',  None),
        'family_walk':  ('May–October',  None),
        'run':          ('June–October', None),
        'hike':         ('June–October', None),
        'bouldering':   ('May–October',  None),
        'peak_bagging': ('July–September', 'Start early Jul–Aug; afternoon thunderstorms common above treeline'),
    },
    5: {  # Bishop / Eastern Sierra — broader season but split by elevation
        'walk':         ('March–November', None),
        'family_walk':  ('March–November', None),
        'run':          ('April–October',  'Summer midday temps in the Owens Valley can exceed 95°F; early morning strongly preferred June–September'),
        'hike':         ('May–October',    None),
        'bouldering':   ('October–April',  'Bishop bouldering peaks October–April when cooler temps preserve friction; summer heat significantly degrades performance'),
        'peak_bagging': ('July–September', 'High-elevation routes; afternoon thunderstorms possible — summit before noon'),
    },
    6: {  # Yosemite Valley — longer season, lower elevation
        'walk':         ('March–November', None),
        'family_walk':  ('March–November', None),
        'run':          ('March–November', None),
        'hike':         ('April–October',  None),
        'bouldering':   ('March–November', 'Avoid wet or damp rock; Camp 4 area accessible year-round when dry'),
        'peak_bagging': ('May–October',    'Start early Jul–Aug; afternoon thunderstorms on exposed terrain'),
    },
    7: {  # Sequoia / Kings Canyon
        'walk':         ('April–October', None),
        'family_walk':  ('April–October', None),
        'run':          ('May–October',   None),
        'hike':         ('May–October',   None),
        'bouldering':   ('April–October', None),
        'peak_bagging': ('July–September', 'High elevation; afternoon thunderstorms possible — off summit by 1pm'),
    },
}

# ── Place-name pattern overrides ───────────────────────────────────────────────
# Each entry: (pattern, {activity_type_or_'*': (best_months, conditions_note)})
# '*' applies to all activity types at that place
PLACE_OVERRIDES = [
    ('Taylor Creek',      {'*': ('May–November',  'Kokanee salmon spawn typically mid-October — the main event')}),
    ('Cascade Falls',     {'*': ('April–July',    'Peak flow April–June from snowmelt; can be dry by August')}),
    ('Bridalveil',        {'*': ('March–June',    'Peak flow March–May; substantially reduced by mid-summer')}),
    ('Yosemite Fall',     {'*': ('April–June',    'Peak flow April–May from snowmelt; upper falls may cease by August')}),
    ('Mist Trail',        {'*': ('April–October', 'Peak flow April–May; expect heavy mist — waterproof layers recommended')}),
    ('Vernal Fall',       {'*': ('April–October', 'Peak flow April–May; mist can be heavy spring — waterproof layers')}),
    ('Nevada Fall',       {'*': ('April–October', 'Peak flow April–May')}),
    ('Rainbow Falls',     {'*': ('June–October',  'Peak flow June–July from snowmelt')}),
    ('Minaret Falls',     {'*': ('June–July',     'Peak flow June–July; significantly reduced by August')}),
    ('Tokopah Falls',     {'*': ('May–July',      'Peak flow May–June from snowmelt')}),
    ('Tokopah Valley',    {'*': ('May–October',   None)}),
    ('Roaring River',     {'*': ('May–July',      'Peak flow May–June')}),
    ('Mist Falls',        {'*': ('May–July',      'Peak flow May–June from snowmelt')}),
    ('Hot Creek',         {'*': ('Year-round',    'Swimming prohibited since 2006; geothermal steam most visible on cold mornings')}),
    ('Buttermilk',        {'bouldering': ('October–April', 'Classic Bishop bouldering; summer heat ruins friction — plan for temps below 65°F')}),
    ('Happy Boulder',     {'bouldering': ('October–April', 'Best October–April; summer heat degrades volcanic rock friction')}),
    ('Sad Boulder',       {'bouldering': ('October–April', 'Best October–April; summer heat degrades volcanic rock friction')}),
    ('Devils Postpile',   {'*': ('June–October',  'Mandatory shuttle from Mammoth Mountain required June–September')}),
    ('Devils Postpile Formation', {'*': ('June–October', 'Mandatory shuttle from Mammoth Mountain required June–September')}),
    ('Lake Tahoe Marathon',  {'run': ('October', 'Annual October event — verify dates at laketahoemarathon.com')}),
    ('Mammoth Trail Fest',   {'run': ('July',    'Annual July event — verify schedule at mammothtrailfest.com')}),
    ('Woolly',               {'run': ('July',    'Annual July event held during Mammoth Trail Fest weekend')}),
    ('Sequoia Half Marathon',{'run': ('May',     'Annual May event — verify dates and NPS permit status before registering')}),
    ('Yosemite Half Marathon',{'run': ('August', 'Annual August event — verify dates and entry at recreation.gov')}),
    ('Emerald Bay',       {'*': ('May–October',   'Hwy 89 may close in winter; parking fills by 9am on summer weekends')}),
    ('D.L. Bliss',        {'*': ('May–October',   'State park entrance; day use fee applies')}),
    ('Reds Meadow',       {'*': ('June–October',  'Mandatory shuttle from Mammoth Mountain required June–September')}),
    ('Sentinel Dome',     {'*': ('May–October',   'Glacier Point Road seasonal — typically May through November')}),
    ('Taft Point',        {'*': ('May–October',   'Glacier Point Road seasonal; serious unguarded cliff exposure — keep children close')}),
    ('Glacier Point',     {'*': ('May–October',   'Road typically open May–November; check nps.gov/yose for current status')}),
    ('Tioga Pass',        {'*': ('July–September','Highest paved road crossing in Sierra; typically open July–October')}),
    ('General Sherman',   {'*': ('Year-round',    'Accessible year-round from Lodgepole; trail may be snowy December–March')}),
    ('Congress Trail',    {'*': ('Year-round',    'Accessible year-round; may have snow patches December–March')}),
    ('Big Trees Trail',   {'*': ('Year-round',    'Round Meadow boardwalk; accessible most of year')}),
    ('Auto Log',          {'*': ('April–November',None)}),
    ('Moro Rock',         {'*': ('May–October',   'Staircase may be icy in early season; exposed summit — clear days best for views')}),
    ('Volcanic Tablelands',{'*': ('October–April','Owens Valley heat makes summer uncomfortable; spring wildflowers late February–April')}),
]

# ── Event override: any activity with run_type='event' ────────────────────────
EVENT_NOTE = 'Annual event — verify current dates and registration before planning your trip'


def best_season(zone_id, atype, place_name, notes, run_type):
    """Return (best_months, conditions_note) for an activity."""
    name_lc = place_name.lower()
    notes_lc = (notes or '').lower()

    # Check place-name overrides first
    for pattern, overrides in PLACE_OVERRIDES:
        if pattern.lower() in name_lc:
            rule = overrides.get(atype) or overrides.get('*')
            if rule:
                return rule

    # Events get a generic note
    if run_type == 'event':
        default = ZONE_DEFAULTS.get(zone_id, {}).get(atype, ('June–October', None))
        return (default[0], EVENT_NOTE)

    # Zone default
    zone = ZONE_DEFAULTS.get(zone_id, {})
    return zone.get(atype, ('June–October', None))


def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Add columns if they don't exist
    existing_act = {r[1] for r in cur.execute("PRAGMA table_info(activities)").fetchall()}
    existing_pl  = {r[1] for r in cur.execute("PRAGMA table_info(places)").fetchall()}

    if 'best_months' not in existing_act:
        cur.execute("ALTER TABLE activities ADD COLUMN best_months TEXT")
        print("Added activities.best_months")
    if 'conditions_note' not in existing_act:
        cur.execute("ALTER TABLE activities ADD COLUMN conditions_note TEXT")
        print("Added activities.conditions_note")
    if 'image_url' not in existing_pl:
        cur.execute("ALTER TABLE places ADD COLUMN image_url TEXT")
        print("Added places.image_url")

    conn.commit()

    # Populate
    rows = cur.execute("""
        SELECT a.id, a.activity_type, a.run_type, a.notes, p.zone_id, p.name
        FROM activities a JOIN places p ON a.place_id = p.id
    """).fetchall()

    updated = 0
    for act_id, atype, run_type, notes, zone_id, place_name in rows:
        months, cond = best_season(zone_id, atype, place_name, notes, run_type)
        cur.execute(
            "UPDATE activities SET best_months=?, conditions_note=? WHERE id=?",
            (months, cond, act_id)
        )
        updated += 1

    conn.commit()
    conn.close()
    print(f"Populated {updated} activities with best_months + conditions_note")

    # Quick check
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    sample = cur.execute("""
        SELECT p.name, a.activity_type, a.best_months, a.conditions_note
        FROM activities a JOIN places p ON a.place_id=p.id
        WHERE a.conditions_note IS NOT NULL
        ORDER BY RANDOM() LIMIT 8
    """).fetchall()
    print("\nSample entries with conditions notes:")
    for r in sample:
        print(f"  [{r[1]}] {r[0]}: {r[2]} | {r[3][:60] if r[3] else '–'}")
    conn.close()


if __name__ == '__main__':
    main()
