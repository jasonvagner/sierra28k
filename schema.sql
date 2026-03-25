-- Sierra Nevada Tourism Research Dataset Schema

CREATE TABLE IF NOT EXISTS zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    description TEXT,
    validated INTEGER NOT NULL DEFAULT 0,  -- 0=false, 1=true
    validation_notes TEXT
);

CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id INTEGER NOT NULL REFERENCES zones(id),
    name TEXT NOT NULL,
    place_type TEXT NOT NULL CHECK(place_type IN ('trail', 'trailhead', 'parking', 'starting_point')),
    lat REAL,
    lng REAL,
    address TEXT,
    parking_notes TEXT,
    kid_friendly INTEGER NOT NULL DEFAULT 0  -- 0=false, 1=true
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER NOT NULL REFERENCES places(id),
    activity_type TEXT NOT NULL CHECK(activity_type IN ('walk', 'family_walk', 'run', 'hike', 'bouldering', 'peak_bagging')),
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 5),
    distance_km REAL,
    elevation_gain_m REAL,
    notes TEXT,
    run_type TEXT CHECK(run_type IN ('route', 'event') OR run_type IS NULL)
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER NOT NULL REFERENCES places(id),
    url TEXT NOT NULL,
    source_type TEXT NOT NULL CHECK(source_type IN ('official', 'places_api', 'web_search')),
    retrieved_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_places_zone_id ON places(zone_id);
CREATE INDEX IF NOT EXISTS idx_activities_place_id ON activities(place_id);
CREATE INDEX IF NOT EXISTS idx_sources_place_id ON sources(place_id);
CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(activity_type);
