#!/usr/bin/env python3
"""
Add 'peak_bagging' as a separate activity_type
Requires recreating the activities table with updated CHECK constraint
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sierra28k.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Step 1: Create new activities table with updated constraint
print("Step 1: Creating new activities table...")
cur.execute("""
    CREATE TABLE activities_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id INTEGER NOT NULL REFERENCES places(id),
        activity_type TEXT NOT NULL CHECK(activity_type IN ('walk', 'family_walk', 'run', 'hike', 'bouldering', 'peak_bagging')),
        difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5),
        distance_km REAL,
        elevation_gain_m REAL,
        notes TEXT,
        run_type TEXT CHECK(run_type IN ('route', 'event') OR run_type IS NULL)
    )
""")

# Step 2: Copy all existing data
print("Step 2: Copying existing data...")
cur.execute("""
    INSERT INTO activities_new (id, place_id, activity_type, difficulty, distance_km, elevation_gain_m, notes, run_type)
    SELECT id, place_id, activity_type, difficulty, distance_km, elevation_gain_m, notes, run_type
    FROM activities
""")

# Step 3: Update peak bagging entries to have activity_type='peak_bagging' and clean up notes
print("Step 3: Updating peak bagging entries...")

# Get all activities with PEAK BAGGING in notes
cur.execute("SELECT id, notes FROM activities_new WHERE notes LIKE '%[PEAK BAGGING%'")
peak_entries = cur.fetchall()

for entry_id, notes in peak_entries:
    # Remove the [PEAK BAGGING - LEVEL] tag from notes
    import re
    clean_notes = re.sub(r'\[PEAK BAGGING - [^\]]+\]\s*', '', notes)
    
    # Update to peak_bagging type
    cur.execute("""
        UPDATE activities_new 
        SET activity_type = 'peak_bagging', notes = ?
        WHERE id = ?
    """, (clean_notes, entry_id))
    
    print(f"  ✓ Updated ID {entry_id} to peak_bagging")

# Step 4: Drop old table and rename
print("Step 4: Replacing old table...")
cur.execute("DROP TABLE activities")
cur.execute("ALTER TABLE activities_new RENAME TO activities")

# Step 5: Recreate indexes
print("Step 5: Recreating indexes...")
cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_place_id ON activities(place_id)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(activity_type)")

conn.commit()

# Step 6: Verify
print("\n" + "="*50)
print("VERIFICATION")
print("="*50)

cur.execute("SELECT activity_type, COUNT(*) FROM activities GROUP BY activity_type ORDER BY COUNT(*) DESC")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

print(f"\n✓ Schema updated successfully!")
print(f"✓ {len(peak_entries)} entries converted to peak_bagging")

conn.close()
