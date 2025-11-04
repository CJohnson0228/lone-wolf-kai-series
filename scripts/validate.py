#!/usr/bin/env python3
"""
Validation script for extracted Lone Wolf content
Checks for data quality issues, broken links, missing sections, etc.
"""

import json
from pathlib import Path
from collections import Counter


def validate_book(json_path: Path) -> dict:
    """Validate a single book's extracted data"""
    print(f"\n{'='*60}")
    print(f"Validating: {json_path.name}")
    print(f"{'='*60}")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    errors = []
    warnings = []
    stats = {}

    # Basic metadata checks
    stats['title'] = data.get('title', 'Unknown')
    stats['book_number'] = data.get('book_number', 0)
    stats['total_sections'] = len(data.get('sections', {}))
    stats['disciplines'] = len(data.get('disciplines', []))

    sections = data.get('sections', {})
    all_section_nums = set(int(k) for k in sections.keys())

    # Check for missing sections (should be consecutive from 1 to max)
    max_section = max(all_section_nums) if all_section_nums else 0
    expected_sections = set(range(1, max_section + 1))
    missing_sections = expected_sections - all_section_nums

    if missing_sections:
        errors.append(f"Missing sections: {sorted(missing_sections)}")

    # Validate each section
    section_types = Counter()
    broken_links = []
    conditional_choices = 0
    combat_encounters = 0
    sections_with_no_choices = []

    for sect_num, section in sections.items():
        section_num = int(sect_num)
        section_types[section.get('type', 'unknown')] += 1

        # Check choices
        choices = section.get('choices', [])

        if len(choices) == 0 and section.get('type') not in ['defeat', 'victory', 'ending']:
            sections_with_no_choices.append(section_num)

        for choice in choices:
            target = choice.get('target')

            # Check if target section exists
            if target and str(target) not in sections:
                broken_links.append({
                    'from': section_num,
                    'to': target,
                    'text': choice.get('text', '')[:50]
                })

            # Count conditional choices
            if choice.get('conditional'):
                conditional_choices += 1

        # Check combat encounters
        if section.get('combat'):
            combat_encounters += 1
            combat = section['combat']

            # Validate combat has required fields
            if not combat.get('enemy_name'):
                errors.append(f"Section {section_num}: Combat missing enemy name")
            if not combat.get('combat_skill'):
                errors.append(f"Section {section_num}: Combat missing CS")
            if not combat.get('endurance'):
                errors.append(f"Section {section_num}: Combat missing END")

    stats['section_types'] = dict(section_types)
    stats['conditional_choices'] = conditional_choices
    stats['combat_encounters'] = combat_encounters

    # Report findings
    print(f"\n📊 Statistics:")
    print(f"  Title: {stats['title']}")
    print(f"  Book Number: {stats['book_number']}")
    print(f"  Total Sections: {stats['total_sections']}")
    print(f"  Disciplines: {stats['disciplines']}")
    print(f"  Combat Encounters: {combat_encounters}")
    print(f"  Conditional Choices: {conditional_choices}")

    print(f"\n📈 Section Types:")
    for stype, count in section_types.most_common():
        print(f"  {stype}: {count}")

    # Report errors
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for error in errors[:10]:  # Show first 10
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    # Report warnings
    if broken_links:
        print(f"\n⚠️  Broken Links ({len(broken_links)}):")
        for link in broken_links[:10]:  # Show first 10
            print(f"  - Section {link['from']} → {link['to']}: {link['text']}")
        if len(broken_links) > 10:
            print(f"  ... and {len(broken_links) - 10} more")

    if sections_with_no_choices:
        print(f"\n⚠️  Sections with No Choices ({len(sections_with_no_choices)}):")
        print(f"  {sorted(sections_with_no_choices)[:20]}")
        if len(sections_with_no_choices) > 20:
            print(f"  ... and {len(sections_with_no_choices) - 20} more")

    # Success summary
    if not errors and not broken_links:
        print(f"\n✅ Validation PASSED - No critical issues found!")
    elif not errors:
        print(f"\n⚠️  Validation passed with {len(broken_links)} warnings")
    else:
        print(f"\n❌ Validation FAILED - {len(errors)} errors found")

    return {
        'errors': errors,
        'warnings': broken_links,
        'stats': stats
    }


def main():
    """Validate all extracted books"""
    extracted_dir = Path('extracted-content')

    if not extracted_dir.exists():
        print("❌ No extracted-content directory found!")
        return

    json_files = sorted(extracted_dir.glob('book-*.json'))

    if not json_files:
        print("❌ No book JSON files found!")
        return

    print(f"Found {len(json_files)} books to validate\n")

    all_results = []
    for json_file in json_files:
        result = validate_book(json_file)
        all_results.append(result)

    # Overall summary
    print(f"\n\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")

    total_sections = sum(r['stats']['total_sections'] for r in all_results)
    total_combat = sum(r['stats']['combat_encounters'] for r in all_results)
    total_conditional = sum(r['stats']['conditional_choices'] for r in all_results)
    total_errors = sum(len(r['errors']) for r in all_results)
    total_warnings = sum(len(r['warnings']) for r in all_results)

    print(f"\n📚 Books Validated: {len(all_results)}")
    print(f"📄 Total Sections: {total_sections}")
    print(f"⚔️  Combat Encounters: {total_combat}")
    print(f"🔮 Conditional Choices: {total_conditional}")
    print(f"❌ Total Errors: {total_errors}")
    print(f"⚠️  Total Warnings: {total_warnings}")

    if total_errors == 0:
        print(f"\n✅ All books validated successfully!")
    else:
        print(f"\n❌ Validation issues found - please review errors above")


if __name__ == '__main__':
    main()
