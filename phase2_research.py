#!/usr/bin/env python3
"""
Phase 2: Research & Population Script for sierra28k Dataset
Imports existing Mammoth data and researches additional zones.
Uses Google Places API and official sources.
"""
import sqlite3
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "sierra28k.db")

class SierraDatasetBuilder:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.stats = {'places': 0, 'activities': 0, 'sources': 0}
        
    def get_zone_id(self, zone_name):
        """Get zone ID by name."""
        result = self.cur.execute(
            "SELECT id FROM zones WHERE name = ?", (zone_name,)
        ).fetchone()
        return result['id'] if result else None
    
    def add_place(self, zone_id, name, place_type, lat, lng, address=None, 
                  parking_notes=None, kid_friendly=False):
        """Add a place and return its ID."""
        self.cur.execute("""
            INSERT INTO places (zone_id, name, place_type, lat, lng, 
                              address, parking_notes, kid_friendly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (zone_id, name, place_type, lat, lng, address, 
              parking_notes, 1 if kid_friendly else 0))
        self.conn.commit()
        place_id = self.cur.lastrowid
        self.stats['places'] += 1
        return place_id
    
    def add_activity(self, place_id, activity_type, difficulty=None, 
                     distance_km=None, elevation_gain_m=None, notes=None, run_type=None):
        """Add an activity to a place."""
        self.cur.execute("""
            INSERT INTO activities (place_id, activity_type, difficulty, 
                                   distance_km, elevation_gain_m, notes, run_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (place_id, activity_type, difficulty, distance_km, 
              elevation_gain_m, notes, run_type))
        self.conn.commit()
        self.stats['activities'] += 1
        return self.cur.lastrowid
    
    def add_source(self, place_id, url, source_type):
        """Add a source URL for a place."""
        self.cur.execute("""
            INSERT INTO sources (place_id, url, source_type, retrieved_at)
            VALUES (?, ?, ?, datetime('now'))
        """, (place_id, url, source_type))
        self.conn.commit()
        self.stats['sources'] += 1
        return self.cur.lastrowid
    
    def import_mammoth_data(self):
        """Import existing Mammoth Lakes dataset."""
        print("\n=== Zone: Mammoth Lakes ===")
        try:
            from mammoth_recreation_dataset import places as mammoth_places
        except ImportError:
            print("ERROR: mammoth_recreation_dataset.py not found")
            return
        
        zone_id = self.get_zone_id("Mammoth Lakes")
        if not zone_id:
            print("ERROR: Mammoth Lakes zone not found")
            return
        
        zone_stats = {'places': 0, 'activities': 0}
        
        for place_data in mammoth_places:
            # Add place
            place_id = self.add_place(
                zone_id=zone_id,
                name=place_data['name'],
                place_type=place_data['place_type'],
                lat=place_data['lat'],
                lng=place_data['lng'],
                address=place_data.get('address'),
                parking_notes=place_data.get('parking_notes'),
                kid_friendly=place_data.get('kid_friendly', False)
            )
            zone_stats['places'] += 1
            
            # Add activity
            self.add_activity(
                place_id=place_id,
                activity_type=place_data['activity_type'],
                difficulty=place_data.get('difficulty'),
                distance_km=place_data.get('distance_km'),
                elevation_gain_m=place_data.get('elevation_gain_m'),
                notes=place_data.get('notes'),
                run_type=place_data.get('run_type')
            )
            zone_stats['activities'] += 1
            
            # Add source
            self.add_source(
                place_id=place_id,
                url=place_data['source_url'],
                source_type=place_data.get('source_type', 'official')
            )
        
        print(f"  ✓ Imported {zone_stats['places']} places, {zone_stats['activities']} activities")
        return zone_stats
    
    def search_google_places(self, query, location=None, radius=50000):
        """Search Google Places API (New)."""
        if not GOOGLE_PLACES_API_KEY:
            print("WARNING: No GOOGLE_PLACES_API_KEY found")
            return []
        
        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.types"
        }
        
        payload = {"textQuery": query}
        if location:
            payload["locationBias"] = {
                "circle": {
                    "center": {"latitude": location[0], "longitude": location[1]},
                    "radius": radius
                }
            }
        
        try:
            response = httpx.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('places', [])
        except Exception as e:
            print(f"  API Error: {e}")
            return []
    
    def add_zone_data(self, zone_name, places_data):
        """Add data for a zone."""
        print(f"\n=== Zone: {zone_name} ===")
        zone_id = self.get_zone_id(zone_name)
        if not zone_id:
            print(f"ERROR: Zone '{zone_name}' not found")
            return {'places': 0, 'activities': 0}
        
        zone_stats = {'places': 0, 'activities': 0}
        
        for place_info in places_data:
            try:
                # Add place
                place_id = self.add_place(
                    zone_id=zone_id,
                    name=place_info['name'],
                    place_type=place_info.get('place_type', 'trailhead'),
                    lat=place_info['lat'],
                    lng=place_info['lng'],
                    address=place_info.get('address'),
                    parking_notes=place_info.get('parking_notes'),
                    kid_friendly=place_info.get('kid_friendly', False)
                )
                zone_stats['places'] += 1
                
                # Add activity
                self.add_activity(
                    place_id=place_id,
                    activity_type=place_info['activity_type'],
                    difficulty=place_info.get('difficulty'),
                    distance_km=place_info.get('distance_km'),
                    elevation_gain_m=place_info.get('elevation_gain_m'),
                    notes=place_info.get('notes'),
                    run_type=place_info.get('run_type')
                )
                zone_stats['activities'] += 1
                
                # Add source(s)
                sources = place_info.get('sources', [])
                if not sources and place_info.get('source_url'):
                    sources = [(place_info['source_url'], place_info.get('source_type', 'official'))]
                
                for url, source_type in sources:
                    self.add_source(place_id, url, source_type)
                    
            except Exception as e:
                print(f"  ERROR adding {place_info.get('name')}: {e}")
                continue
        
        print(f"  ✓ Added {zone_stats['places']} places, {zone_stats['activities']} activities")
        return zone_stats
    
    def print_summary(self):
        """Print overall dataset summary."""
        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)
        
        # Zone breakdown
        print("\nBy Zone:")
        for row in self.cur.execute("""
            SELECT z.name, z.region,
                   COUNT(DISTINCT p.id) as places,
                   COUNT(DISTINCT a.id) as activities
            FROM zones z
            LEFT JOIN places p ON p.zone_id = z.id
            LEFT JOIN activities a ON a.place_id = p.id
            GROUP BY z.id
            ORDER BY z.id
        """):
            print(f"  {row['name']} ({row['region']})")
            print(f"    Places: {row['places']}, Activities: {row['activities']}")
        
        # Activity type breakdown
        print("\nBy Activity Type:")
        for row in self.cur.execute("""
            SELECT activity_type, COUNT(*) as count 
            FROM activities 
            GROUP BY activity_type 
            ORDER BY count DESC
        """):
            print(f"  {row['activity_type']}: {row['count']}")
        
        # Source breakdown
        print("\nBy Source Type:")
        for row in self.cur.execute("""
            SELECT source_type, COUNT(*) as count 
            FROM sources 
            GROUP BY source_type
        """):
            print(f"  {row['source_type']}: {row['count']}")
        
        print(f"\nTotal: {self.stats['places']} places, {self.stats['activities']} activities, {self.stats['sources']} sources")
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    builder = SierraDatasetBuilder()
    
    # Import Mammoth Lakes data (already researched)
    builder.import_mammoth_data()
    
    # Import Lake Tahoe data
    from lake_tahoe_data import NORTH_TAHOE_DATA, SOUTH_TAHOE_DATA
    builder.add_zone_data("North Lake Tahoe", NORTH_TAHOE_DATA)
    builder.add_zone_data("South Lake Tahoe", SOUTH_TAHOE_DATA)
    
    # Import Yosemite data
    from yosemite_data import TUOLUMNE_MEADOWS_DATA, YOSEMITE_VALLEY_DATA
    builder.add_zone_data("Tuolumne Meadows", TUOLUMNE_MEADOWS_DATA)
    builder.add_zone_data("Yosemite Valley", YOSEMITE_VALLEY_DATA)
    
    # Import Bishop and Sequoia data
    from bishop_sequoia_data import BISHOP_EASTERN_SIERRA_DATA, SEQUOIA_KINGS_CANYON_DATA
    builder.add_zone_data("Bishop/Eastern Sierra", BISHOP_EASTERN_SIERRA_DATA)
    builder.add_zone_data("Sequoia/Kings Canyon", SEQUOIA_KINGS_CANYON_DATA)
    
    builder.print_summary()
    builder.close()
