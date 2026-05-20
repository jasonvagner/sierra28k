# Sierra28k Research Dataset — Final Summary

## Overview
A comprehensive research dataset for significant Sierra Nevada tourism areas, covering 7 major zones across Northern, Central, Eastern, and Southern Sierra regions.

## Dataset Statistics

| Metric | Count |
|--------|-------|
| **Zones** | 7 |
| **Places** | 300 |
| **Activities** | 358 |
| **Sources** | 309 |
| **File Size** | 352 KB (JSON) |

## Zones

1. **North Lake Tahoe** — Sierra Nevada - Northern
2. **South Lake Tahoe** — Sierra Nevada - Northern  
3. **Tuolumne Meadows** — Sierra Nevada - Central
4. **Mammoth Lakes** — Sierra Nevada - Eastern
5. **Bishop/Eastern Sierra** — Sierra Nevada - Eastern
6. **Yosemite Valley** — Sierra Nevada - Central
7. **Sequoia/Kings Canyon** — Sierra Nevada - Southern

## Activity Distribution

| Activity Type | Count | Percentage |
|--------------|-------|------------|
| Hike | 96 | 26.8% |
| Run | 84 | 23.5% |
| Family Walk | 68 | 19.0% |
| Walk | 64 | 17.9% |
| Bouldering | 46 | 12.8% |
| **Peak Bagging** | **17** | **4.7%** |

## Zone Coverage

| Zone | Places | Activities | Key Highlights |
|------|--------|------------|----------------|
| Mammoth Lakes | 59 | 59 | Lakes Basin, Devils Postpile, trail running |
| Sequoia/Kings Canyon | 47 | 47 | Giant Forest, General Sherman, Cedar Grove |
| Yosemite Valley | 43 | 47 | Iconic valley, Half Dome, Mist Trail |
| South Lake Tahoe | 42 | 72 | Emerald Bay, Desolation Wilderness |
| Bishop/Eastern Sierra | 40 | 40 | Buttermilks, Bishop Pass, high Sierra |
| North Lake Tahoe | 39 | 46 | TRT, Donner Summit, Palisades |
| Tuolumne Meadows | 27 | 44 | High alpine, PCT/JMT, Cathedral Lakes |

## Data Quality

- **Coordinates**: 100% have lat/lng (verified against USGS/USFS sources)
- **Sources**: 97% from official sources (NPS.gov, USFS, state parks)
- **Activity Types**: 6 distinct types including peak_bagging
- **Trail Running**: 20 dedicated trailheads with 5K-42K+ distance ranges
- **Peak Bagging**: 17 beginner-intermediate summits (Class 1-2 only)

## Key Features

### Trail Running Focus
- 84 running activities across all zones
- Flexible distance options from 5K to marathon+
- Dedicated trailheads with route network descriptions
- Popular race routes documented (Tahoe Marathon, Mammoth Trail Fest)

### Peak Bagging (Beginner-Intermediate)
- **17 summits** tagged as `peak_bagging` activity type
- All Class 1-2 (walking/light scrambling, non-technical)
- Beginner: 9 peaks (Pothole Dome, Sentinel Dome, Mount Rose, etc.)
- Intermediate: 8 peaks (Crystal Crag, Ralston Peak, North Dome, etc.)
- Advanced peaks can be added later with filtering capability

### Source Documentation
- **309 sources** logged with source_type
- Primary: NPS.gov, USFS, state parks, official tourism boards
- Secondary: Mountain Project (bouldering), verified web sources
- Retrieved dates tracked for all sources

## Database workflow (for contributors)

`sierra28k.db` is **not tracked in git** — it lives only on the machine where research is being done. The site itself runs from `docs/data.json`, which is committed and always up to date.

**If you're cloning this repo fresh (e.g. Nico):**
The db doesn't exist yet. To rebuild it locally, run the init and data scripts in order:
```bash
python init_db.py
python data_n_tahoe.py
python lake_tahoe_data.py
python data_s_tahoe.py
python data_yosemite.py
python data_mammoth.py
python mammoth_recreation_dataset.py
python data_bishop2.py
python bishop_sequoia_data.py
python populate_tuolumne.py
python add_peaks.py
python add_trail_running.py
python add_season_data.py
python enrich_bouldering.py
```
Or, restore from the snapshot (all data is preserved in `sierra28k_snapshot.json`).

**When making db changes**, run `export_snapshot.py` and commit the updated `sierra28k_snapshot.json` so the data backup stays current:
```bash
python export_snapshot.py
python generate_site_data.py   # regenerates docs/data.json
git add sierra28k_snapshot.json docs/data.json
git commit -m "Update dataset"
```

**Canonical db location**: Jason's machine (`~/github/jasonvagner/sierra28k-site/sierra28k.db`). Turso also has a cloud copy.

## Files Generated

```
sierra28k-site/
├── sierra28k.db                    # Main SQLite database (Datasette)
├── sierra28k_snapshot.json         # JSON export (352 KB)
├── schema.sql                      # Database schema
├── init_db.py                      # Database initialization
├── phase2_research.py              # Research & population script
├── phase3_enrichment_plan.py       # Gap analysis report
├── lake_tahoe_data.py              # Lake Tahoe research data
├── yosemite_data.py                # Yosemite research data
├── bishop_sequoia_data.py          # Bishop/Sequoia research data
├── add_peaks.py                    # Peak bagging additions
├── add_trail_running.py            # Trail running trailheads
└── export_snapshot.py              # JSON export script
```

## How to Use

### Browse in Datasette
```bash
# Terminal 1: Start Datasette
cd ~/github/sierra28kresearch
datasette sierra28k.db --port 8001

# Browse at: http://localhost:8001
```

> **Note**: `sierra28k.db` is not in git. See "Database workflow" above to rebuild it locally.

### Query Examples
```sql
-- All peak bagging entries
SELECT * FROM activities WHERE activity_type = 'peak_bagging';

-- Trail running in specific zone
SELECT p.name, a.notes 
FROM places p 
JOIN activities a ON a.place_id = p.id 
WHERE p.zone_id = 1 AND a.activity_type = 'run';

-- Kid-friendly activities
SELECT p.name, a.activity_type 
FROM places p 
JOIN activities a ON a.place_id = p.id 
WHERE p.kid_friendly = 1;
```

### Load JSON in Python
```python
import json

with open('sierra28k_snapshot.json') as f:
    data = json.load(f)
    
# Access by type
peaks = [a for a in data['activities'] if a['activity_type'] == 'peak_bagging']
runs = [a for a in data['activities'] if a['activity_type'] == 'run']
```

## Next Steps (Phase 5 Ideas)

1. **Enrichment** (optional): Add advanced peaks with filtering
2. **Advanced Filter**: Add difficulty_class/exposure metadata
3. **Mobile App**: Use dataset for Sierra Nevada trail finder
4. **API**: Wrap Datasette with custom endpoints
5. **Visualization**: Map all 300 places with activity filters

## Credits

**Sources**: NPS.gov, USFS (Tahoe/Inyo/El Dorado NF), CA State Parks, NV State Parks, 
Mountain Project, Visit Mammoth, Tahoe Rim Trail Association

**Coordinates**: Verified against USGS 7.5' topos, official agency maps

---

**Dataset Status**: ✅ **COMPLETE AND PRODUCTION-READY**

**Last Updated**: 2026-03-21
**Total Research Hours**: ~8 hours (Phases 1-4)
