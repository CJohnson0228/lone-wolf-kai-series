# Content Extraction Scripts

This directory contains scripts for extracting Lone Wolf gamebook content from Project Aon HTML files into structured JSON format.

## Scripts

### `scraper.py`

Main extraction script that parses Project Aon HTML files and outputs structured JSON.

**Features:**
- Extracts all 350+ sections per book
- Parses Kai Disciplines with descriptions
- Identifies combat encounters with stats
- Detects conditional choices (discipline-based)
- Categorizes sections by type (choice, combat, narrative, ending)
- Handles special characters and formatting

**Usage:**
```bash
# Extract single book
python3 scraper.py source-materials/01fftd

# Extract with custom output path
python3 scraper.py source-materials/01fftd -o custom-output.json

# Extract all books
for book in 01fftd 02fotw 03tcok 04tcod 05sots; do
    python3 scraper.py source-materials/$book
done
```

### `validate.py`

Validation script that checks extracted JSON for quality issues.

**Checks:**
- Missing sections
- Broken links between sections
- Invalid combat data
- Section type distribution
- Conditional choice detection

**Usage:**
```bash
python3 validate.py
```

## Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Dependencies:
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser

## Extracted Data Format

The extracted JSON has this structure:

```json
{
  "series": "kai",
  "book_number": 1,
  "title": "Flight from the Dark",
  "authors": "Joe Dever and Gary Chalk",
  "version": "1.0.0",
  "disciplines": [
    {
      "id": "sixth_sense",
      "name": "Sixth Sense",
      "description": "This skill may warn a Kai Lord..."
    }
  ],
  "equipment_rules": {
    "starting_items": {...},
    "carry_limits": {...}
  },
  "sections": {
    "1": {
      "section": 1,
      "text": "You must make haste...",
      "type": "choice",
      "choices": [
        {
          "text": "If you wish to use Sixth Sense...",
          "target": 141,
          "conditional": true,
          "requires": "sixth_sense"
        }
      ],
      "illustrations": []
    },
    "17": {
      "section": 17,
      "text": "You raise your weapon...",
      "type": "combat",
      "combat": {
        "enemy_name": "Kraan",
        "combat_skill": 16,
        "endurance": 24,
        "can_evade": false
      },
      "choices": [...]
    }
  }
}
```

## Extraction Statistics

Successfully extracted all 5 Kai Series books:

| Book | Sections | Combat | Conditional | Size |
|------|----------|--------|-------------|------|
| Book 1: Flight from the Dark | 350 | 29 | 39 | 242KB |
| Book 2: Fire on the Water | 350 | 31 | 53 | 287KB |
| Book 3: The Caverns of Kalte | 350 | 30 | 85 | 297KB |
| Book 4: The Chasm of Doom | 350 | 45 | 55 | 293KB |
| Book 5: Shadow on the Sand | 400 | 39 | 71 | 364KB |
| **TOTAL** | **1,800** | **174** | **303** | **1.5MB** |

✅ **Validation Result:** All books passed with **0 errors** and **0 warnings**

## Section Types

The scraper categorizes sections into these types:

- **choice**: Multiple paths available (most common)
- **narrative**: Single path forward
- **combat**: Combat encounter
- **ending**: Book ending (victory, defeat, or other)
- **defeat**: Player death

## Conditional Logic Detection

The scraper automatically detects conditional choices that require specific Kai Disciplines:

- Sixth Sense (most common)
- Camouflage
- Hunting
- Tracking
- Healing
- Weaponskill
- Mindshield
- Mindblast
- Animal Kinship
- Mind Over Matter

## Next Steps

The extracted JSON files in `extracted-content/` are ready to be:

1. Bundled with the Tauri + React app
2. Used for game logic and navigation
3. Displayed in the story reader component
4. Referenced for combat encounters
5. Used to implement conditional choice logic

## Known Limitations

- Illustrations are noted but not extracted (image files remain in source-materials)
- Combat modifiers are in text but not parsed into structured format
- Item pickups are mentioned in text but not extracted as separate objects
- Random number checks are in text but not structured

These can be enhanced in future iterations if needed.
