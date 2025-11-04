# Content Extraction Strategy - Project Aon HTML to App Format

## Overview

You have the Project Aon HTML files which contain all book content. We need to parse these into a structured JSON format that the app can consume.

## HTML Structure Analysis

Based on the provided examples:

### Section Files
- **Naming**: `sect1.htm`, `sect141.htm`, `sect275.htm`, etc.
- **Location**: Likely in numbered directories (e.g., `/lw/01fftd/sect*.htm`)
- **Structure**: Each section has:
  - Section number (in `<h3>` tag)
  - Narrative text (in `<p>` tags)
  - Choices (in `<p class="choice">` tags with `<a>` links)
  - Images (in `<div class="illustration">` sections)
  - Combat encounters (need to identify patterns)
  - Conditional logic (text like "If you wish to use your Kai Discipline...")

### Rules/Setup Files
- `gamerulz.htm` - Combat Skill and Endurance generation
- `discplnz.htm` - Kai Disciplines list
- `equipmnt.htm` - Starting equipment rules
- `cmbtrulz.htm` - Combat mechanics
- `levels.htm` - Progression system

### Assets
- Images referenced: `title.png`, `bckgrnd.png`, weapon images, item images, etc.
- Random number table: `random.htm`
- Action chart: `action.htm`
- Map: `map.htm`

## Extraction Strategy

### Phase 1: Python Scraper

Create a Python script using Beautiful Soup to parse HTML files.

**Tools:**
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser
- `json` - Output format
- `requests` - If fetching from Project Aon website
- `pathlib` - File system navigation

**Script Structure:**

```python
# scraper/extract_book.py

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

class LoneWolfExtractor:
    def __init__(self, book_path):
        self.book_path = Path(book_path)
        self.sections = {}
        self.disciplines = []
        self.equipment = []
        self.combat_table = {}

    def extract_all(self):
        """Main extraction method"""
        self.extract_disciplines()
        self.extract_equipment_rules()
        self.extract_combat_rules()
        self.extract_sections()
        self.extract_images()
        return self.to_json()

    def extract_sections(self):
        """Extract all numbered sections"""
        # Find all sect*.htm files
        # Parse each section
        # Extract choices and conditional logic
        pass

    def extract_disciplines(self):
        """Extract Kai Disciplines from discplnz.htm"""
        pass

    def parse_section(self, section_file):
        """Parse a single section file"""
        with open(section_file) as f:
            soup = BeautifulSoup(f, 'lxml')

        # Extract section number
        section_num = self.get_section_number(soup)

        # Extract narrative text (exclude choices)
        narrative = self.get_narrative_text(soup)

        # Extract choices
        choices = self.get_choices(soup)

        # Detect combat encounters
        combat = self.detect_combat(soup, narrative)

        # Detect item pickups
        items = self.detect_items(soup, narrative)

        # Detect conditional logic
        conditionals = self.detect_conditionals(soup, choices)

        return {
            'section': section_num,
            'text': narrative,
            'type': self.determine_section_type(choices, combat),
            'choices': choices,
            'combat': combat,
            'items': items,
            'conditionals': conditionals,
            'images': self.extract_section_images(soup)
        }

    def get_choices(self, soup):
        """Extract choice links from section"""
        choices = []
        choice_paragraphs = soup.find_all('p', class_='choice')

        for p in choice_paragraphs:
            link = p.find('a')
            if link:
                choice_text = p.get_text().strip()
                target_section = self.parse_section_link(link['href'])

                # Detect if this is a conditional choice
                is_conditional = self.is_conditional_choice(choice_text)
                required_discipline = self.extract_required_discipline(choice_text)

                choices.append({
                    'text': choice_text,
                    'target': target_section,
                    'conditional': is_conditional,
                    'requires': required_discipline
                })

        return choices

    def is_conditional_choice(self, text):
        """Check if choice requires a specific discipline"""
        conditional_patterns = [
            'If you wish to use',
            'If you have the Kai Discipline',
            'If you possess',
            'If you have'
        ]
        return any(pattern in text for pattern in conditional_patterns)

    def extract_required_discipline(self, text):
        """Extract which discipline is required"""
        disciplines = [
            'Sixth Sense', 'Camouflage', 'Hunting', 'Tracking',
            'Healing', 'Weaponskill', 'Mindshield', 'Mindblast',
            'Animal Kinship', 'Mind Over Matter'
        ]

        for disc in disciplines:
            if disc in text:
                return disc.lower().replace(' ', '_')
        return None

    def detect_combat(self, soup, text):
        """Detect if section contains combat"""
        # Look for combat keywords
        combat_keywords = ['COMBAT SKILL', 'ENDURANCE', 'fight', 'combat']

        # Look for stat patterns like "COMBAT SKILL: 18"
        combat_pattern = r'COMBAT SKILL[:\s]+(\d+)'
        endurance_pattern = r'ENDURANCE[:\s]+(\d+)'

        cs_match = re.search(combat_pattern, text)
        end_match = re.search(endurance_pattern, text)

        if cs_match and end_match:
            # Extract enemy name (usually before stats)
            enemy_name = self.extract_enemy_name(text, cs_match.start())

            return {
                'enemy_name': enemy_name,
                'combat_skill': int(cs_match.group(1)),
                'endurance': int(end_match.group(1)),
                'can_evade': self.can_evade_combat(text)
            }

        return None

    def detect_items(self, soup, text):
        """Detect items that can be picked up"""
        # Items are typically in CAPITAL LETTERS in Project Aon format
        # Look for patterns like "you find a SWORD" or "pick up the HEALING POTION"

        item_pattern = r'([A-Z][A-Z\s]+(?:[A-Z]+)?)'
        potential_items = re.findall(item_pattern, text)

        # Filter out common capitalized words that aren't items
        exclude = ['COMBAT SKILL', 'ENDURANCE', 'KAI', 'SOMMERLUND', ...]
        items = [item for item in potential_items if item not in exclude]

        return items

    def determine_section_type(self, choices, combat):
        """Determine what type of section this is"""
        if combat:
            return 'combat'
        elif len(choices) > 1:
            return 'choice'
        elif len(choices) == 1:
            return 'narrative'
        else:
            return 'ending'  # No choices = death or victory

    def to_json(self):
        """Export to JSON format for app"""
        return {
            'series': 'kai',
            'book_number': 1,
            'title': 'Flight from the Dark',
            'version': '1.0.0',
            'disciplines': self.disciplines,
            'equipment_rules': self.equipment,
            'combat_table': self.combat_table,
            'sections': self.sections
        }
```

### Phase 2: Data Structure Output

The scraper outputs JSON files in this format:

```json
{
  "series": "kai",
  "book_number": 1,
  "title": "Flight from the Dark",
  "version": "1.0.0",

  "disciplines": [
    {
      "id": "sixth_sense",
      "name": "Sixth Sense",
      "description": "This skill may warn a Kai Lord of imminent danger...",
      "effect": "conditional_paths"
    },
    {
      "id": "healing",
      "name": "Healing",
      "description": "This Discipline can be used to restore ENDURANCE points...",
      "effect": "+1 ENDURANCE per section without combat"
    }
  ],

  "equipment_rules": {
    "starting_items": {
      "guaranteed": [
        { "type": "weapon", "name": "Axe" },
        { "type": "meal", "quantity": 1 },
        { "type": "special_item", "name": "Map of Sommerlund" }
      ],
      "random_gold": { "min": 0, "max": 9 },
      "random_item": {
        "0": { "type": "weapon", "name": "Broadsword" },
        "1": { "type": "weapon", "name": "Sword" },
        "2": { "type": "special_item", "name": "Helmet", "endurance_bonus": 2 },
        "3": { "type": "meal", "quantity": 2 },
        "4": { "type": "special_item", "name": "Chainmail Waistcoat", "endurance_bonus": 4 },
        "5": { "type": "weapon", "name": "Mace" },
        "6": { "type": "backpack_item", "name": "Healing Potion", "effect": "+4 ENDURANCE" },
        "7": { "type": "weapon", "name": "Quarterstaff" },
        "8": { "type": "weapon", "name": "Spear" },
        "9": { "type": "gold", "quantity": 12 }
      }
    },
    "carry_limits": {
      "weapons": 2,
      "backpack_items": 8,
      "gold_crowns": 50
    }
  },

  "sections": {
    "1": {
      "text": "You must make haste for you sense it is not safe to linger...",
      "type": "choice",
      "choices": [
        {
          "text": "If you wish to take the right path into the wood",
          "target": 85,
          "conditional": false
        },
        {
          "text": "If you wish to follow the left track",
          "target": 275,
          "conditional": false
        },
        {
          "text": "If you wish to use your Kai Discipline of Sixth Sense",
          "target": 141,
          "conditional": true,
          "requires": "sixth_sense",
          "auto_continue": true
        }
      ],
      "images": []
    },

    "42": {
      "text": "A savage Giak leaps at you from the shadows!",
      "type": "combat",
      "combat": {
        "enemy_name": "Giak",
        "combat_skill": 13,
        "endurance": 10,
        "can_evade": false,
        "immune_to_mindblast": false
      },
      "victory_section": 43,
      "defeat_section": 0,
      "images": ["giak.png"]
    },

    "100": {
      "text": "You have reached the capital city of Holmgard...",
      "type": "ending",
      "ending_type": "victory",
      "choices": []
    }
  }
}
```

## Extraction Challenges & Solutions

### Challenge 1: Conditional Logic Variations

The books have many ways to express conditionals:
- "If you wish to use your Kai Discipline of Sixth Sense..."
- "If you have Camouflage, turn to..."
- "If you possess the skill of Healing..."

**Solution**: Pattern matching with regex + discipline name extraction

### Challenge 2: Combat Encounters

Combat stats appear in various formats:
- "COMBAT SKILL: 18  ENDURANCE: 25"
- "Combat Skill 18"
- Sometimes in tables, sometimes inline

**Solution**: Multiple regex patterns + manual verification of parsed data

### Challenge 3: Item Detection

Items are capitalized but so are proper nouns:
- "You find a SWORD" (item)
- "The DARKLORDS attack" (not an item)

**Solution**: Whitelist of known items + context analysis

### Challenge 4: Images

Images are referenced but need to be:
- Extracted from HTML
- Renamed/organized for app use
- Possibly converted to web-friendly formats

**Solution**: Copy image files, create image manifest, optimize for web

## Manual Verification Checklist

After automated extraction:

- [ ] Verify all 350 sections extracted (Book 1)
- [ ] Check all choice links point to valid sections
- [ ] Validate all combat encounters have CS and END
- [ ] Confirm conditional choices detected correctly
- [ ] Test that "death" sections are marked as endings
- [ ] Verify victory sections are marked correctly
- [ ] Check item names are standardized
- [ ] Confirm discipline names match across book
- [ ] Validate random number table structure
- [ ] Test combat results table parsing

## Content Validation Script

```python
# scraper/validate_content.py

def validate_book_content(json_data):
    """Validate extracted book content"""
    errors = []
    warnings = []

    # Check all section links are valid
    all_sections = set(json_data['sections'].keys())
    for sect_num, section in json_data['sections'].items():
        for choice in section.get('choices', []):
            target = str(choice['target'])
            if target not in all_sections and target != '0':
                errors.append(f"Section {sect_num}: Invalid link to {target}")

    # Check combat sections have victory/defeat paths
    for sect_num, section in json_data['sections'].items():
        if section['type'] == 'combat':
            if 'victory_section' not in section:
                errors.append(f"Section {sect_num}: Combat missing victory path")

    # Check conditional choices have valid disciplines
    valid_disciplines = [d['id'] for d in json_data['disciplines']]
    for sect_num, section in json_data['sections'].items():
        for choice in section.get('choices', []):
            if choice.get('conditional'):
                if choice.get('requires') not in valid_disciplines:
                    warnings.append(f"Section {sect_num}: Unknown discipline {choice.get('requires')}")

    return errors, warnings
```

## Directory Structure for Extracted Content

```
content/
├── kai-series/
│   ├── book-1/
│   │   ├── book-1.json          # Main content file
│   │   ├── metadata.json        # Book metadata
│   │   └── images/
│   │       ├── title.png
│   │       ├── illustrations/
│   │       └── items/
│   ├── book-2/
│   ├── book-3/
│   ├── book-4/
│   └── book-5/
├── magnakai-series/
└── grand-master-series/

scraper/
├── extract_book.py              # Main extraction script
├── validate_content.py          # Validation script
├── optimize_images.py           # Image processing
└── requirements.txt             # Python dependencies
```

## Next Steps

1. **Write Python scraper** for Book 1
2. **Run extraction** on Project Aon HTML files
3. **Manually verify** extracted content
4. **Iterate on patterns** based on edge cases
5. **Repeat for Books 2-5** (Kai Series)
6. **Document content format** for app developers

## Image Extraction Notes

Images to extract:
- **Illustrations**: Section-specific artwork
- **Item images**: Sword, helmet, potions, etc.
- **Title/branding**: Book cover, logos
- **UI elements**: Borders, backgrounds

Image optimization:
- Convert to WebP for web (smaller file size)
- Keep PNG for desktop app
- Generate multiple sizes for responsive design
- SVG for icons where possible

## Testing the Extraction

Test the scraper with Section 1 first:
1. Parse `sect1.htm`
2. Verify text extraction
3. Confirm 3 choices detected
4. Validate conditional choice (Sixth Sense) flagged correctly
5. Check links parse correctly (85, 275, 141)

Then expand to:
- Section with combat
- Section with items
- Section with death (ending)
- Section with complex conditionals
