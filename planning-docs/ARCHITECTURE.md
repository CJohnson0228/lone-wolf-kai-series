# Technical Architecture - Conditional Logic & Game Flow

## Conditional Choice System

### The Problem

In Lone Wolf books, certain choices are only available if the character has specific abilities. For example:

- Section 1: "You see two paths..."
  - Choice A: Go left (always available)
  - Choice B: Go right (always available)
  - Choice C: Use Sixth Sense to detect hidden path (only if character has Sixth Sense)

### Solution Design

#### Approach 1: Filter Choices (Show/Hide)

When rendering choices, filter out options the character doesn't qualify for.

**Pros:**

- Cleaner UI
- Player doesn't see impossible options
- Reduces confusion

**Cons:**

- Player might miss that an ability is useful
- Less educational about what abilities unlock

#### Approach 2: Auto-Continue (Recommended)

When character has required ability, automatically show single "Continue" button that takes them to the ability-specific path.

**Pros:**

- Feels natural and magical
- Abilities feel powerful
- Streamlined experience
- Player doesn't need to know which choice uses which ability

**Cons:**

- Less transparent about what happened
- Might want to show what ability was used

#### Approach 3: Highlighted/Suggested Choice

Show all choices, but highlight or suggest the one using the ability.

**Pros:**

- Educational
- Player sees what their ability unlocked
- Still gives choice

**Cons:**

- More cluttered UI
- Might confuse new players

### Recommended Implementation: Hybrid

```javascript
// Content Structure
{
  section: 42,
  text: "You stand at a crossroads. Two paths lead away...",

  // Standard choices (always visible)
  choices: [
    { text: "Take the left path", target: 150 },
    { text: "Take the right path", target: 200 }
  ],

  // Conditional choices (ability-specific)
  conditional_choices: [
    {
      ability: "sixth_sense",
      text: "Your Sixth Sense detects a hidden third path",
      target: 250,
      auto_continue: true, // Show "Continue" button instead of choice
      message: "Your Sixth Sense ability allows you to detect the hidden path."
    }
  ],

  // Or if ability should override normal choices
  ability_override: {
    ability: "sixth_sense",
    target: 250,
    hide_normal_choices: true, // Only show continue button
    message: "Your Sixth Sense warns you about both paths. You detect a safer hidden route."
  }
}
```

### Rendering Logic

```javascript
function renderChoices(section, character) {
  const choices = [];

  // Check for ability override first
  if (section.ability_override) {
    const hasAbility = characterHasAbility(
      character,
      section.ability_override.ability
    );
    if (hasAbility) {
      return {
        type: "continue",
        message: section.ability_override.message,
        target: section.ability_override.target,
      };
    }
  }

  // Add standard choices
  choices.push(...section.choices);

  // Add conditional choices if ability present
  if (section.conditional_choices) {
    section.conditional_choices.forEach((condChoice) => {
      if (characterHasAbility(character, condChoice.ability)) {
        if (condChoice.auto_continue) {
          // This becomes a continue button, not a choice
          return {
            type: "continue",
            message: condChoice.message,
            target: condChoice.target,
          };
        } else {
          choices.push({
            text: condChoice.text,
            target: condChoice.target,
            highlighted: true, // Visual indicator
          });
        }
      }
    });
  }

  return {
    type: "choices",
    choices: choices,
  };
}
```

## Combat Automation

### Combat Flow

```
1. Enter combat section
   ↓
2. Display enemy stats (CS: X, END: Y)
   ↓
3. Player sees: "Attack" button
   ↓
4. Auto-roll dice (both sides)
   ↓
5. Calculate damage
   ↓
6. Update endurance
   ↓
7. Display round result
   ↓
8. Check for victory/defeat
   ↓
9. If continue: back to step 3
   ↓
10. If over: proceed to next section
```

### Special Ability Integration

**Sixth Sense in Combat:**

- Warn before combat: "Your Sixth Sense warns you of danger ahead"
- Show enemy stats before combat begins
- Option to avoid combat if possible

**Healing:**

- After combat: "Use Healing to restore X END?" button
- Auto-calculate healing amount
- Update endurance

**Hunting:**

- During wilderness sections: "Use Hunting to find food?" button
- Restore endurance automatically

**Mindshield:**

- Auto-protect against mind attacks
- No player action needed

## Content Structure Examples

### Standard Section

```json
{
  "section": 1,
  "text": "You are Lone Wolf, last of the Kai Lords...",
  "type": "narrative",
  "next_section": 2
}
```

### Choice Section

```json
{
  "section": 42,
  "text": "You see two paths. Which do you take?",
  "type": "choice",
  "choices": [
    { "text": "Left path", "target": 150 },
    { "text": "Right path", "target": 200 }
  ],
  "conditional_logic": {
    "sixth_sense": {
      "type": "auto_continue",
      "target": 250,
      "message": "Your Sixth Sense detects a hidden third path"
    }
  }
}
```

### Combat Section

```json
{
  "section": 87,
  "text": "A Giak warrior blocks your path!",
  "type": "combat",
  "enemy": {
    "name": "Giak Warrior",
    "combat_skill": 18,
    "endurance": 22
  },
  "sixth_sense_warning": true,
  "can_avoid": false,
  "victory_section": 88,
  "defeat_section": 200
}
```

### Ability Check Section

```json
{
  "section": 156,
  "text": "You need to climb a steep cliff.",
  "type": "ability_check",
  "required_ability": "climbing",
  "success_section": 157,
  "failure_section": 158,
  "alternate_path": {
    "text": "You can try to find another way around",
    "target": 159
  }
}
```

## Character State Management

### What to Track

- Current section number
- Current endurance
- Combat skill (usually static)
- Equipment list
- Backpack contents
- Special items (Kai weapons, etc.)
- Gold crowns
- Abilities/Disciplines
- Book progress
- Previous choices (for some story branches)

### Save Points

- Auto-save after every section
- Manual save at any point
- Multiple save slots
- Save to cloud (database)

## Data Flow

```
User Action
    ↓
Frontend (React/Electron)
    ↓
Game Logic Engine
    ↓
Character State Update
    ↓
Render New Section
    ↓
[Optional] Sync to Database
```

## Performance Considerations

### Content Loading

- Load book content on app start (if bundled)
- Lazy load subsequent books
- Cache frequently accessed sections

### Database Sync

- Sync on section change (debounced)
- Batch updates if offline
- Optimistic UI updates

### Offline Support

- Store book content locally
- Queue character updates if offline
- Sync when connection restored
