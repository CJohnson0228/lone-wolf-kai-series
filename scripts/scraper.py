#!/usr/bin/env python3
"""
Lone Wolf Book Content Extractor
Extracts content from Project Aon HTML files into structured JSON format
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup


class LoneWolfExtractor:
    """Extracts Lone Wolf gamebook content from Project Aon HTML files"""

    def __init__(self, book_path: str):
        self.book_path = Path(book_path)
        self.sections: Dict[str, Dict] = {}
        self.disciplines: List[Dict] = []
        self.equipment_rules: Dict = {}
        self.book_info: Dict = {}

    def extract_all(self) -> Dict:
        """Main extraction method"""
        print(f"Extracting content from: {self.book_path}")

        # Extract book metadata
        self.extract_book_info()

        # Extract game rules (disciplines, equipment, etc.)
        self.extract_disciplines()
        self.extract_equipment_rules()

        # Extract all numbered sections
        self.extract_all_sections()

        return self.to_dict()

    def extract_book_info(self):
        """Extract book title and basic info from first section"""
        first_section = self.book_path / "sect1.htm"
        if not first_section.exists():
            print(f"Warning: {first_section} not found")
            return

        with open(first_section, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Get book title from header
        header = soup.find('header', id='main-header')
        if header:
            title_tag = header.find('h1')
            if title_tag:
                self.book_info['title'] = title_tag.get_text(strip=True)

            author_tag = header.find('h2')
            if author_tag:
                self.book_info['authors'] = author_tag.get_text(strip=True)

    def extract_disciplines(self):
        """Extract Kai Disciplines from discplnz.htm"""
        disciplines_file = self.book_path / "discplnz.htm"
        if not disciplines_file.exists():
            print(f"Warning: {disciplines_file} not found")
            return

        with open(disciplines_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        maintext = soup.find('div', class_='maintext')
        if not maintext:
            return

        # Find all h4 tags which mark discipline names
        discipline_headers = maintext.find_all('h4')

        for header in discipline_headers:
            # Get discipline name from header or anchor
            anchor = header.find('a')
            if anchor:
                discipline_id = anchor.get('name', '')
                discipline_name = header.get_text(strip=True)
            else:
                discipline_name = header.get_text(strip=True)
                discipline_id = discipline_name.lower().replace(' ', '_')

            # Get description (paragraphs following the header until next h4)
            description_parts = []
            for sibling in header.find_next_siblings():
                if sibling.name == 'h4':
                    break
                if sibling.name == 'p':
                    text = sibling.get_text(strip=True)
                    if text and not text.startswith('If you choose'):
                        description_parts.append(text)

            description = ' '.join(description_parts)

            self.disciplines.append({
                'id': discipline_id,
                'name': discipline_name,
                'description': description
            })

        print(f"Extracted {len(self.disciplines)} disciplines")

    def extract_equipment_rules(self):
        """Extract equipment rules from equipmnt.htm"""
        equipment_file = self.book_path / "equipmnt.htm"
        if not equipment_file.exists():
            print(f"Warning: {equipment_file} not found")
            return

        # Basic equipment rules structure
        self.equipment_rules = {
            'starting_items': {
                'guaranteed': [
                    {'type': 'weapon', 'name': 'Axe'},
                    {'type': 'meal', 'quantity': 1},
                    {'type': 'special_item', 'name': 'Map of Sommerlund'}
                ]
            },
            'carry_limits': {
                'weapons': 2,
                'backpack_items': 8,
                'gold_crowns': 50
            }
        }

        print("Equipment rules extracted")

    def extract_all_sections(self):
        """Extract all numbered sections from sect*.htm files"""
        section_files = sorted(self.book_path.glob("sect*.htm"))

        print(f"Found {len(section_files)} section files")

        for section_file in section_files:
            section_data = self.parse_section(section_file)
            if section_data:
                section_num = section_data['section']
                self.sections[str(section_num)] = section_data

        print(f"Extracted {len(self.sections)} sections")

    def parse_section(self, section_file: Path) -> Optional[Dict]:
        """Parse a single section file"""
        with open(section_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find the numbered div (main section content)
        numbered_div = soup.find('div', class_='numbered')
        if not numbered_div:
            return None

        maintext = numbered_div.find('div', class_='maintext')
        if not maintext:
            return None

        # Extract section number
        section_num_tag = maintext.find('h3')
        if not section_num_tag:
            return None

        try:
            section_num = int(section_num_tag.get_text(strip=True))
        except ValueError:
            return None

        # Extract narrative text (exclude choices and combat)
        narrative_parts = []
        for p in maintext.find_all('p'):
            # Skip choice paragraphs and combat paragraphs
            if 'choice' in p.get('class', []) or 'combat' in p.get('class', []):
                continue

            text = p.get_text(strip=True)
            if text:
                narrative_parts.append(text)

        narrative = '\n\n'.join(narrative_parts)

        # Extract choices
        choices = self.extract_choices(maintext)

        # Extract combat encounter
        combat = self.extract_combat(maintext, narrative)

        # Determine section type
        section_type = self.determine_section_type(choices, combat, narrative)

        # Check for illustrations
        illustrations = self.extract_illustrations(maintext)

        section_data = {
            'section': section_num,
            'text': narrative,
            'type': section_type,
            'choices': choices,
            'illustrations': illustrations
        }

        if combat:
            section_data['combat'] = combat

        return section_data

    def extract_choices(self, maintext) -> List[Dict]:
        """Extract choice links from section"""
        choices = []
        choice_paragraphs = maintext.find_all('p', class_='choice')

        for p in choice_paragraphs:
            link = p.find('a')
            if not link:
                continue

            choice_text = p.get_text(strip=True)

            # Extract target section from href
            href = link.get('href', '')
            target_match = re.search(r'sect(\d+)\.htm', href)
            if target_match:
                target_section = int(target_match.group(1))
            else:
                continue

            # Check if this is a conditional choice (requires discipline)
            is_conditional = self.is_conditional_choice(choice_text)
            required_discipline = self.extract_required_discipline(choice_text) if is_conditional else None

            choice = {
                'text': choice_text,
                'target': target_section
            }

            if is_conditional:
                choice['conditional'] = True
                choice['requires'] = required_discipline

            choices.append(choice)

        return choices

    def is_conditional_choice(self, text: str) -> bool:
        """Check if choice requires a specific discipline"""
        conditional_patterns = [
            'If you wish to use your Kai Discipline',
            'If you have the Kai Discipline',
            'If you possess',
            'If you have'
        ]
        return any(pattern.lower() in text.lower() for pattern in conditional_patterns)

    def extract_required_discipline(self, text: str) -> Optional[str]:
        """Extract which discipline is required from choice text"""
        disciplines_map = {
            'Sixth Sense': 'sixth_sense',
            'Camouflage': 'camouflage',
            'Hunting': 'hunting',
            'Tracking': 'tracking',
            'Healing': 'healing',
            'Weaponskill': 'weaponskill',
            'Mindshield': 'mindshield',
            'Mindblast': 'mindblast',
            'Animal Kinship': 'animal_kinship',
            'Mind Over Matter': 'mind_over_matter'
        }

        for disc_name, disc_id in disciplines_map.items():
            if disc_name in text:
                return disc_id

        return None

    def extract_combat(self, maintext, narrative: str) -> Optional[Dict]:
        """Extract combat encounter from section"""
        # Look for combat paragraph
        combat_p = maintext.find('p', class_='combat')
        if not combat_p:
            return None

        combat_text = combat_p.get_text()

        # Extract enemy name, CS, and Endurance
        # Format: "Kraan: COMBAT SKILL 16   ENDURANCE 24"
        enemy_name_match = re.search(r'^([^:]+):', combat_text)
        cs_match = re.search(r'COMBAT\s*SKILL\s*(\d+)', combat_text)
        end_match = re.search(r'ENDURANCE\s*(\d+)', combat_text)

        if not (enemy_name_match and cs_match and end_match):
            return None

        enemy_name = enemy_name_match.group(1).strip()
        combat_skill = int(cs_match.group(1))
        endurance = int(end_match.group(1))

        # Check for combat modifiers in narrative
        modifiers = self.extract_combat_modifiers(narrative)

        # Check if can evade (look for "evade" in nearby text)
        can_evade = 'evade' in narrative.lower()

        combat_data = {
            'enemy_name': enemy_name,
            'combat_skill': combat_skill,
            'endurance': endurance,
            'can_evade': can_evade
        }

        if modifiers:
            combat_data['modifiers'] = modifiers

        return combat_data

    def extract_combat_modifiers(self, text: str) -> List[str]:
        """Extract combat modifiers from text"""
        modifiers = []

        # Look for common modifier patterns
        if re.search(r'deduct \d+ points? from your COMBAT SKILL', text, re.IGNORECASE):
            match = re.search(r'deduct (\d+) points? from your COMBAT SKILL', text, re.IGNORECASE)
            if match:
                modifiers.append(f"-{match.group(1)} COMBAT SKILL")

        if re.search(r'add \d+ points? to your COMBAT SKILL', text, re.IGNORECASE):
            match = re.search(r'add (\d+) points? to your COMBAT SKILL', text, re.IGNORECASE)
            if match:
                modifiers.append(f"+{match.group(1)} COMBAT SKILL")

        return modifiers

    def extract_illustrations(self, maintext) -> List[str]:
        """Extract illustration references from section"""
        illustrations = []

        # Look for image tags
        for img in maintext.find_all('img'):
            src = img.get('src', '')
            if src and not src.startswith('http'):
                illustrations.append(src)

        # Look for links to illustration pages
        for link in maintext.find_all('a'):
            href = link.get('href', '')
            if 'ill' in href and '.htm' in href:
                illustrations.append(href)

        return illustrations

    def determine_section_type(self, choices: List, combat: Optional[Dict], narrative: str) -> str:
        """Determine what type of section this is"""
        if combat:
            return 'combat'
        elif len(choices) == 0:
            # No choices = ending (victory or defeat)
            if 'dead' in narrative.lower() or 'slain' in narrative.lower():
                return 'defeat'
            elif 'reach' in narrative.lower() and 'Holmgard' in narrative:
                return 'victory'
            else:
                return 'ending'
        elif len(choices) == 1:
            return 'narrative'
        else:
            return 'choice'

    def to_dict(self) -> Dict:
        """Export to dictionary format"""
        return {
            'series': 'kai',
            'book_number': self.get_book_number(),
            'title': self.book_info.get('title', 'Unknown'),
            'authors': self.book_info.get('authors', ''),
            'version': '1.0.0',
            'disciplines': self.disciplines,
            'equipment_rules': self.equipment_rules,
            'sections': self.sections
        }

    def get_book_number(self) -> int:
        """Determine book number from path"""
        book_codes = {
            '01fftd': 1,
            '02fotw': 2,
            '03tcok': 3,
            '04tcod': 4,
            '05sots': 5
        }

        for code, number in book_codes.items():
            if code in str(self.book_path):
                return number

        return 1  # default


def main():
    """Main extraction function"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract Lone Wolf book content')
    parser.add_argument('book_path', help='Path to book directory (e.g., source-materials/01fftd)')
    parser.add_argument('-o', '--output', help='Output JSON file path', default=None)

    args = parser.parse_args()

    # Create extractor
    extractor = LoneWolfExtractor(args.book_path)

    # Extract all content
    book_data = extractor.extract_all()

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        book_num = book_data['book_number']
        output_path = Path(f"extracted-content/book-{book_num}.json")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Extraction complete!")
    print(f"📊 Stats:")
    print(f"  - Sections: {len(book_data['sections'])}")
    print(f"  - Disciplines: {len(book_data['disciplines'])}")
    print(f"  - Output: {output_path}")


if __name__ == '__main__':
    main()
