# Character Creation Flow - Exact Book Rules

## Overview

Character creation should mirror the book experience but be streamlined and automated. The goal is to make it fast (< 2 minutes) while maintaining the excitement of random generation.

## Character Creation Steps

### Step 1: Generate Combat Skill

**Rules from Book:**
- Pick random number (0-9) from random number table
- Add 10 to the result
- Result is your COMBAT SKILL (10-19)

**UI Flow:**
```
Screen: "Measuring Your Kai Training"

[Animated dice roll or number generator]

"Roll for Combat Skill..."
[Button: Roll Dice]

Result: "You rolled a 6!"
"Your Combat Skill is: 16" (6 + 10)

[Button: Continue]
```

**Implementation:**
```javascript
function generateCombatSkill() {
  const roll = Math.floor(Math.random() * 10); // 0-9
  const combatSkill = roll + 10; // 10-19
  return { roll, combatSkill };
}
```

### Step 2: Generate Endurance

**Rules from Book:**
- Pick random number (0-9)
- Add 20 to the result
- Result is your ENDURANCE (20-29)

**UI Flow:**
```
"Roll for Endurance..."
[Button: Roll Dice]

Result: "You rolled a 7!"
"Your Endurance is: 27" (7 + 20)

[Button: Continue]
```

**Implementation:**
```javascript
function generateEndurance() {
  const roll = Math.floor(Math.random() * 10); // 0-9
  const endurance = roll + 20; // 20-29
  return { roll, endurance };
}
```

### Step 3: Choose 5 Kai Disciplines

**Rules from Book:**
- Choose 5 from the list of 10 Kai Disciplines
- Each has specific effects
- Choice matters for gameplay

**UI Flow:**
```
Screen: "Choose Your Kai Disciplines"

"As a Kai Initiate, you have mastered 5 of the 10 Kai Disciplines.
Choose carefully, as each will help you in different situations."

[Grid of 10 Discipline Cards - player selects 5]

Each card shows:
- Discipline name
- Icon
- Description
- Game effect

Example:
┌─────────────────────────┐
│  🔮 Sixth Sense          │
│                         │
│ Warns of danger and     │
│ reveals true intentions │
│                         │
│ Effect: Unlock hidden   │
│ paths and warnings      │
│                         │
│ [Select] or [Selected✓] │
└─────────────────────────┘

Counter: "Selected: 3/5"

[Button: Continue] (disabled until 5 selected)
```

**Disciplines List:**

1. **Camouflage**
   - Effect: Hide in countryside, blend in towns
   - Game: Unlock stealth options

2. **Hunting**
   - Effect: Never starve, move stealthily
   - Game: No meal required when told to eat

3. **Sixth Sense**
   - Effect: Warn of danger, reveal true purpose
   - Game: Unlock hidden paths, get warnings

4. **Tracking**
   - Effect: Find paths, locate people/objects
   - Game: Unlock tracking options

5. **Healing**
   - Effect: Restore endurance
   - Game: +1 END per section without combat

6. **Weaponskill**
   - Effect: Master one weapon type
   - Game: +2 CS when using that weapon

7. **Mindshield**
   - Effect: Protect against Mindforce attacks
   - Game: No damage from Mindblast attacks

8. **Mindblast**
   - Effect: Attack with mind
   - Game: +2 CS (some enemies immune)

9. **Animal Kinship**
   - Effect: Communicate with animals
   - Game: Unlock animal-related options

10. **Mind Over Matter**
    - Effect: Move small objects with mind
    - Game: Unlock telekinesis options

### Step 4: Weaponskill Selection (if chosen)

**Rules from Book:**
- If player chose Weaponskill, roll 0-9 for weapon type
- This determines which weapon grants +2 CS bonus

**UI Flow:**
```
[If Weaponskill selected]

"Roll to determine your weapon specialization..."
[Button: Roll Dice]

Result: "You rolled a 4!"
"You are skilled with the Broadsword!"

[Image of Broadsword]

"When wielding a Broadsword in combat, you gain +2 Combat Skill"

[Button: Continue]
```

**Weapon Table:**
- 0 = Dagger
- 1 = Spear
- 2 = Mace
- 3 = Short Sword
- 4 = Warhammer
- 5 = Sword
- 6 = Axe (lucky! you start with this)
- 7 = Sword
- 8 = Quarterstaff
- 9 = Broadsword

### Step 5: Generate Starting Gold

**Rules from Book:**
- Roll 0-9
- Result = number of Gold Crowns you start with

**UI Flow:**
```
"Roll for starting gold..."
[Button: Roll Dice]

Result: "You rolled a 5!"
"You start with 5 Gold Crowns"

[Coin animation]

[Button: Continue]
```

### Step 6: Roll for Additional Starting Item

**Rules from Book:**
- Roll 0-9 for one additional item
- Each number corresponds to specific item

**UI Flow:**
```
"While searching the monastery ruins, you find..."
[Button: Search Ruins]

Result: "You rolled a 2!"
"You found a Helmet!"

[Image of Helmet]

"The Helmet adds +2 to your Endurance"
"Your Endurance is now: 29" (27 + 2)

[Button: Continue]
```

**Starting Item Table:**
- 0 = Broadsword (weapon)
- 1 = Sword (weapon)
- 2 = Helmet (+2 END, special item)
- 3 = 2 Meals (backpack items)
- 4 = Chainmail Waistcoat (+4 END, special item)
- 5 = Mace (weapon)
- 6 = Healing Potion (+4 END when used, backpack item)
- 7 = Quarterstaff (weapon)
- 8 = Spear (weapon)
- 9 = 12 Gold Crowns (belt pouch)

### Step 7: Summary Screen

**UI Flow:**
```
Screen: "Your Kai Lord"

[Optional: Name your character]
Input: Character Name: [_____________]

═══════════════════════════════════

COMBAT SKILL: 16
ENDURANCE: 29 / 29

WEAPONS (2 max):
• Axe (starting weapon)
• Helmet

KAI DISCIPLINES (5):
🔮 Sixth Sense
🎯 Tracking
⚔️ Weaponskill (Axe)
💚 Healing
🧠 Mindblast

BACKPACK (8 max):
• Meal x1

BELT POUCH (50 max):
• Gold Crowns: 5

SPECIAL ITEMS:
• Map of Sommerlund
• Helmet (+2 END)

═══════════════════════════════════

[Button: Begin Adventure]
[Button: Re-roll Character] (optional)
```

## Character Data Model

```typescript
interface Character {
  id: string;
  userId: string;
  name: string;
  series: 'kai' | 'magnakai' | 'grand_master';

  // Stats
  combatSkill: number;        // Base CS (10-19)
  currentCombatSkill: number; // Modified CS during gameplay
  maxEndurance: number;       // Max END (20-29 + bonuses)
  currentEndurance: number;   // Current END

  // Disciplines
  disciplines: string[];      // Array of 5 discipline IDs
  weaponSkillType?: string;   // If has weaponskill

  // Inventory
  weapons: string[];          // Max 2
  backpackItems: string[];    // Max 8 (includes meals)
  specialItems: string[];     // No limit
  goldCrowns: number;         // Max 50

  // Progress
  currentBook: number;
  currentSection: number;
  booksCompleted: number;

  // Metadata
  createdAt: string;
  lastPlayed: string;
}
```

## Implementation Notes

### Option 1: Full Manual Control

Players click "Roll" for each stat, making it feel like the book experience.

**Pros:**
- Engaging, feels like dice rolling
- Builds anticipation
- True to book experience

**Cons:**
- Takes longer
- Can be tedious

### Option 2: Quick Create

Single "Create Character" button that rolls all stats at once, then shows results.

**Pros:**
- Fast (< 30 seconds)
- Good for repeat playthroughs

**Cons:**
- Less engaging
- Loses some magic

### Recommended: Hybrid Approach

```
Option 1: "Roll My Character" (auto-roll all stats)
Option 2: "Manual Creation" (step-by-step rolls)

Default to auto-roll with option to switch to manual
```

### Animations & Feedback

Make the random generation feel good:
- Dice rolling animation
- Number counter spinning
- Satisfying sound effects
- Celebratory feedback for good rolls
- Encouraging feedback for low rolls

Example:
```
Roll: 9 for Combat Skill → CS: 19
"Excellent! You are a formidable warrior!"

Roll: 1 for Combat Skill → CS: 11
"Your skills may be modest, but your courage is unmatched!"
```

## Accessibility Considerations

- **Skip animations** option for users who want speed
- **Reroll limits**: Allow rerolls but track attempts (prevent farming perfect stats)
- **Keyboard navigation**: Tab through disciplines, Enter to select
- **Screen reader**: Announce rolls and results clearly
- **Mobile**: Touch-friendly discipline cards with good spacing

## Character Progression Between Books

When completing a book and moving to next in series:

**What Carries Over:**
- Combat Skill (static)
- Max Endurance (may increase with items)
- All 5 disciplines + 1 new discipline (now have 6)
- Equipment
- Gold Crowns
- Special Items (some are book-specific)

**What Resets:**
- Current Endurance (restored to max)
- Current section (starts at 1 in new book)

**Progression Flow:**
```
Complete Book 1 → Screen: "Congratulations!"
"You have completed Flight from the Dark!"

"As a Kai Lord, you have grown stronger."
"Choose 1 additional Kai Discipline:"

[Show remaining 5 disciplines not yet selected]
[Player selects 1]

"Your character will carry over to Book 2: Fire on the Water"
[Export Character Data]

[Button: Continue to Book 2]
[Button: Return to Main Menu]
```

## Save Character Data

Character data should be saved:
- **Locally**: localStorage/IndexedDB for offline play
- **Cloud**: PostgreSQL for cross-device sync
- **Export**: JSON file for manual backup

```javascript
// Example save structure
const characterSaveData = {
  character: { /* full character object */ },
  progress: {
    currentSection: 1,
    sectionsVisited: [1, 2, 5, 10],
    choicesMade: [
      { section: 1, choice: 'Take right path', target: 85, timestamp: '2024-...' }
    ],
    combatsWon: 3,
    itemsFound: ['Sword', 'Gold Crowns x5']
  },
  metadata: {
    saveDate: '2024-11-04T12:34:56Z',
    playtime: 3600, // seconds
    deaths: 0
  }
};
```

## Testing Checklist

- [ ] Combat Skill generates correctly (10-19)
- [ ] Endurance generates correctly (20-29)
- [ ] Can select exactly 5 disciplines (no more, no less)
- [ ] Weaponskill rolls correct weapon type
- [ ] Starting gold rolls correctly (0-9)
- [ ] Random starting item rolls correctly (0-9)
- [ ] Item bonuses apply correctly (Helmet +2 END, Chainmail +4 END)
- [ ] Character data structure is valid
- [ ] Can save and load character
- [ ] Summary screen shows all correct data
- [ ] Can name character (optional)
- [ ] Animations are smooth and skippable
