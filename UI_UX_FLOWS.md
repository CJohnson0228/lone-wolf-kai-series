# UI/UX Flows - Mobile-Friendly Web + Desktop

## Design Philosophy

**Core Principles:**
1. **Mobile-first**: Design for smallest screen, scale up
2. **Responsive**: Single codebase works on phone, tablet, desktop
3. **Touch-friendly**: Large tap targets, swipe gestures
4. **Readable**: Large fonts, high contrast, clear hierarchy
5. **Immersive**: Book-like reading experience
6. **Gamified**: Progress bars, animations, achievements

## Technology Stack

### Frontend Framework: Tauri + React

**Tauri:**
- Rust-based, smaller bundle than Electron
- Better performance
- Native OS integration
- Builds for Windows, macOS, Linux

**React:**
- Component-based architecture
- Large ecosystem
- Easy state management
- Good for complex UIs

**UI Library Options:**
- **Tailwind CSS**: Utility-first, highly customizable
- **shadcn/ui**: Beautiful components, accessible
- **Radix UI**: Headless components for accessibility
- **Framer Motion**: Smooth animations

**Recommendation**: React + Tailwind + shadcn/ui + Framer Motion

### Responsive Breakpoints

```css
/* Mobile (default) */
@media (min-width: 0px) { ... }

/* Tablet */
@media (min-width: 768px) { ... }

/* Desktop */
@media (min-width: 1024px) { ... }

/* Large Desktop */
@media (min-width: 1440px) { ... }
```

## App Structure

### Main Navigation

```
┌────────────────────────────────┐
│  LONE WOLF: KAI SERIES         │
├────────────────────────────────┤
│                                │
│  [📖 Play]                      │
│  [👤 Characters]                │
│  [⚙️ Settings]                  │
│  [ℹ️ About]                     │
│                                │
└────────────────────────────────┘
```

**Mobile (Phone):**
- Full-screen views
- Bottom tab navigation
- Swipe gestures for common actions

**Tablet:**
- Side navigation drawer
- More content visible at once
- Split view for character sheet + story

**Desktop:**
- Persistent sidebar navigation
- Multi-column layouts
- Larger illustrations

## Screen Flows

### 1. Main Menu → Character Creation → Game

```
Main Menu
    ↓
New Game
    ↓
Character Creation
    ├─ Roll Stats
    ├─ Choose Disciplines
    ├─ Generate Equipment
    └─ Name Character
    ↓
Book Selection (Kai Series)
    ├─ Book 1: Flight from the Dark
    ├─ Book 2: Fire on the Water (locked)
    ├─ Book 3: The Caverns of Kalte (locked)
    ├─ Book 4: The Chasm of Doom (locked)
    └─ Book 5: Shadow on the Sand (locked)
    ↓
Story Intro
    ↓
Section 1 (Game Loop Begins)
```

### 2. Game Loop

```
Display Section
    ↓
Is it a choice section?
    ├─ Yes → Show choices
    │         ↓
    │     Player selects choice
    │         ↓
    │     Navigate to target section
    │
    ├─ Combat section?
    │     ↓
    │   Enter combat
    │     ↓
    │   Combat loop (attack rounds)
    │     ↓
    │   Victory or Defeat
    │     ├─ Victory → Continue to next section
    │     └─ Defeat → Game Over screen
    │
    ├─ Item pickup?
    │     ↓
    │   Show item dialog
    │     ↓
    │   Add to inventory
    │     ↓
    │   Continue
    │
    └─ Ending section?
          ↓
        Victory screen
          ↓
        Unlock next book
          ↓
        Add discipline
          ↓
        Return to menu
```

## Screen Designs

### Main Menu

**Mobile:**
```
┌─────────────────────┐
│                     │
│  [🐺 Kai Series]    │
│    Logo/Title       │
│                     │
├─────────────────────┤
│                     │
│  Continue Game      │
│  ▶ Book 1, Sect 42  │
│  Lone Wolf, HP: 22  │
│                     │
├─────────────────────┤
│                     │
│  [ 📖 New Game ]    │
│                     │
│  [ 👤 Characters ]  │
│                     │
│  [ ⚙️ Settings ]    │
│                     │
│  [ ℹ️ About ]       │
│                     │
└─────────────────────┘
```

**Desktop:**
```
┌────────────────────────────────────────────────┐
│  ┌──────┐  LONE WOLF: KAI SERIES               │
│  │ 🐺   │  The Journey Begins...                │
│  └──────┘                                       │
├────────────────────────────────────────────────┤
│  Sidebar       │  Main Content                  │
│  ───────       │  ──────────────────────────    │
│  📖 Play        │  [Large Hero Image]            │
│  👤 Characters  │                                │
│  ⚙️ Settings    │  Continue Your Adventure:      │
│  ℹ️ About       │  ┌────────────────────────┐  │
│                │  │ Book 1: Flight from Dark│  │
│                │  │ Section 42              │  │
│                │  │ Lone Wolf               │  │
│                │  │ HP: 22/25   CS: 16      │  │
│                │  │ [Continue Playing]      │  │
│                │  └────────────────────────┘  │
│                │                                │
│                │  [New Game] [Load Game]        │
└────────────────────────────────────────────────┘
```

### Character Creation - Stats Rolling

**Mobile:**
```
┌───────────────────────────┐
│  ⚔️ CREATE YOUR KAI LORD  │
├───────────────────────────┤
│                           │
│  Rolling for Combat Skill │
│                           │
│  [Dice animation 🎲]      │
│                           │
│  You rolled: 6            │
│                           │
│  ╔═══════════════════╗    │
│  ║ COMBAT SKILL: 16  ║    │
│  ╚═══════════════════╝    │
│                           │
│  "A skilled warrior!"     │
│                           │
├───────────────────────────┤
│                           │
│    [ Continue ]           │
│                           │
│  Progress: ●○○○○ (1/5)    │
│                           │
└───────────────────────────┘
```

### Character Creation - Discipline Selection

**Mobile (Scrollable):**
```
┌───────────────────────────┐
│  Choose 5 Kai Disciplines │
│  Selected: 3/5 ●●●○○      │
├───────────────────────────┤
│                           │
│  ┌───────────────────┐    │
│  │ 🔮 Sixth Sense    │    │
│  │ Warns of danger   │    │
│  │ [Selected ✓]      │    │
│  └───────────────────┘    │
│                           │
│  ┌───────────────────┐    │
│  │ 🎯 Tracking       │    │
│  │ Find paths        │    │
│  │ [Select]          │    │
│  └───────────────────┘    │
│                           │
│  ┌───────────────────┐    │
│  │ ⚔️ Weaponskill     │    │
│  │ Master a weapon   │    │
│  │ [Selected ✓]      │    │
│  └───────────────────┘    │
│                           │
│  [Scroll for more...]     │
│                           │
├───────────────────────────┤
│  [ Continue ] (disabled)  │
└───────────────────────────┘
```

**Desktop (Grid):**
```
┌─────────────────────────────────────────────────┐
│  Choose Your Kai Disciplines (5/10)  ●●●○○      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │🔮 Sixth   │ │🏕️ Camou  │ │🎯 Track  │       │
│  │  Sense    │ │  flage   │ │  ing     │       │
│  │ Selected✓ │ │ [Select] │ │ [Select] │       │
│  └──────────┘ └──────────┘ └──────────┘       │
│                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │💚 Healing │ │⚔️ Weapon │ │🛡️ Mind   │       │
│  │           │ │  skill   │ │  shield  │       │
│  │ Selected✓ │ │ Selected✓│ │ [Select] │       │
│  └──────────┘ └──────────┘ └──────────┘       │
│                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │🧠 Mind    │ │🐾 Animal │ │🔮 Mind   │       │
│  │  blast    │ │  Kinship │ │  Over    │       │
│  │ Selected✓ │ │ [Select] │ │  Matter  │       │
│  └──────────┘ └──────────┘ │ [Select] │       │
│                             └──────────┘       │
│                                                 │
├─────────────────────────────────────────────────┤
│                    [ Continue ]                 │
└─────────────────────────────────────────────────┘
```

### Reading Section (Story View)

**Mobile:**
```
┌───────────────────────────┐
│  ☰  Section 1        💚22 │ ← Header (sticky)
├───────────────────────────┤
│                           │
│  [Illustration if exists] │
│                           │
│  You must make haste for  │
│  you sense it is not safe │
│  to linger by the smoking │
│  remains of the ruined    │
│  monastery...             │
│                           │
│  [Scroll for more text]   │
│                           │
│  Fighting back tears, you │
│  bid farewell to your dead│
│  kinsmen...               │
│                           │
│  At the foot of the hill, │
│  the path splits into two │
│  directions...            │
│                           │
├───────────────────────────┤
│  YOUR CHOICES:            │
│                           │
│  ┌─────────────────────┐  │
│  │ Take the right path │  │
│  │ Turn to 85          │  │
│  └─────────────────────┘  │
│                           │
│  ┌─────────────────────┐  │
│  │ Take the left path  │  │
│  │ Turn to 275         │  │
│  └─────────────────────┘  │
│                           │
└───────────────────────────┘
```

**Desktop:**
```
┌──────────┬───────────────────────────────────┬──────────┐
│  ☰ Menu  │  Section 1                        │ 📊 Stats  │
├──────────┴───────────────────────────────────┴──────────┤
│                                                          │
│  [Larger Illustration]                                   │
│                                                          │
│  You must make haste for you sense it is not safe to    │
│  linger by the smoking remains of the ruined monastery. │
│  The black-winged beasts could return at any moment.    │
│  You must set out for the Sommlending capital of        │
│  Holmgard and tell the King the terrible news...        │
│                                                          │
│  Fighting back tears, you bid farewell to your dead     │
│  kinsmen. Silently, you promise that their deaths will  │
│  be avenged. You turn away from the ruins and carefully │
│  descend the steep track.                               │
│                                                          │
│  At the foot of the hill, the path splits into two      │
│  directions, both leading into a large wood.            │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ Take the right path into the wood (Turn to 85) │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ Follow the left track (Turn to 275)           │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Character Sheet Overlay

**Mobile (Slide-up drawer):**
```
┌───────────────────────────┐
│  ─ [Swipe down to close]  │
├───────────────────────────┤
│  👤 LONE WOLF              │
│                           │
│  ⚔️ Combat Skill: 16       │
│  💚 Endurance: 22 / 25     │
│  💰 Gold Crowns: 8         │
│                           │
│  ───────────────────────  │
│  KAI DISCIPLINES:         │
│  • Sixth Sense            │
│  • Healing                │
│  • Weaponskill (Axe)      │
│  • Mindblast              │
│  • Tracking               │
│                           │
│  ───────────────────────  │
│  WEAPONS (2 max):         │
│  • Axe (+2 CS)            │
│  • Sword                  │
│                           │
│  ───────────────────────  │
│  BACKPACK (5/8):          │
│  • Meal x2                │
│  • Healing Potion         │
│  • Rope                   │
│                           │
│  [Scroll for more...]     │
│                           │
└───────────────────────────┘
```

**Desktop (Sidebar):**
```
┌────────────────────────────────────────┐
│  Story View     │  Character Sheet     │
│                 │  ─────────────────   │
│  Section text   │  👤 LONE WOLF         │
│  appears here   │                      │
│  ...            │  ⚔️ CS: 16   💚 22/25 │
│                 │  💰 Gold: 8           │
│                 │                      │
│                 │  KAI DISCIPLINES:    │
│                 │  🔮 Sixth Sense      │
│                 │  💚 Healing          │
│                 │  ⚔️ Weaponskill (Axe)│
│                 │  🧠 Mindblast        │
│                 │  🎯 Tracking         │
│                 │                      │
│                 │  WEAPONS (2):        │
│                 │  • Axe (+2 CS)       │
│                 │  • Sword             │
│                 │                      │
│                 │  BACKPACK (5/8):     │
│                 │  • Meal x2           │
│                 │  • Healing Potion    │
│                 │  • Rope              │
│                 │                      │
└────────────────────────────────────────┘
```

### Combat Screen

(See COMBAT_SYSTEM.md for detailed combat UI)

**Mobile:**
- Full-screen combat
- Tap "Attack" button
- Swipe-up for combat log
- Large, visible HP bars

**Desktop:**
- Larger enemy portraits
- Side-by-side combat log
- More detailed stats visible

## Responsive Components

### Navigation

**Mobile:** Bottom tab bar
```
┌───────────────────────────┐
│                           │
│  [Main content area]      │
│                           │
├───────────────────────────┤
│  📖    👤    📊    ⚙️     │
│ Story  Char Stats Settings│
└───────────────────────────┘
```

**Tablet:** Side drawer (swipe or tap to open)
```
┌────┬──────────────────────┐
│ ☰  │                      │
│    │  [Main content]      │
│    │                      │
└────┴──────────────────────┘

[Swipe right] →

┌──────────┬───────────────┐
│ 📖 Story │               │
│ 👤 Char  │ [Main content]│
│ 📊 Stats │               │
│ ⚙️ Set   │               │
└──────────┴───────────────┘
```

**Desktop:** Persistent sidebar
```
┌─────────┬──────────────────┐
│ 📖 Play │                  │
│ 👤 Char │  [Main content]  │
│ 📊 Stats│                  │
│ ⚙️ Set  │                  │
└─────────┴──────────────────┘
```

### Typography

**Mobile:**
```css
body {
  font-size: 16px; /* Base */
  line-height: 1.6;
}

h1 { font-size: 1.75rem; } /* 28px */
h2 { font-size: 1.5rem; }  /* 24px */
h3 { font-size: 1.25rem; } /* 20px */

p {
  font-size: 1rem;         /* 16px */
  line-height: 1.6;
  margin-bottom: 1rem;
}
```

**Desktop:**
```css
body {
  font-size: 18px; /* Larger base */
}

h1 { font-size: 2.5rem; }  /* 40px */
h2 { font-size: 2rem; }    /* 32px */
h3 { font-size: 1.5rem; }  /* 24px */

p {
  font-size: 1.125rem;     /* 18px */
  max-width: 70ch;         /* Optimal reading line length */
}
```

### Touch Targets

All interactive elements should be **at least 44x44px** for touch-friendliness.

```css
button, .choice-button {
  min-height: 44px;
  padding: 12px 24px;
  font-size: 16px;
}

/* Desktop: Can be smaller */
@media (min-width: 1024px) {
  button {
    min-height: 36px;
    padding: 8px 16px;
  }
}
```

## Animations & Transitions

### Page Transitions

```javascript
// Framer Motion example
<motion.div
  initial={{ opacity: 0, x: 100 }}
  animate={{ opacity: 1, x: 0 }}
  exit={{ opacity: 0, x: -100 }}
  transition={{ duration: 0.3 }}
>
  {/* Section content */}
</motion.div>
```

### Dice Rolling Animation

```javascript
<motion.div
  animate={{
    rotate: [0, 360, 720],
    scale: [1, 1.2, 1]
  }}
  transition={{ duration: 0.5 }}
>
  🎲
</motion.div>
```

### Health Bar Update

```javascript
<motion.div
  className="health-bar"
  initial={{ width: '100%' }}
  animate={{ width: `${(currentHP / maxHP) * 100}%` }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
/>
```

## Accessibility

### Features to Include

- **Keyboard navigation**: Tab through choices, Enter to select
- **Screen reader support**: Proper ARIA labels
- **High contrast mode**: Option for better visibility
- **Font size adjustment**: User preference
- **Reduce motion**: Respect prefers-reduced-motion
- **Focus indicators**: Clear focus states
- **Alt text**: All images have descriptive alt text

```css
/* Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Settings Screen

```
┌───────────────────────────┐
│  ⚙️ SETTINGS               │
├───────────────────────────┤
│                           │
│  DISPLAY                  │
│  ─────────────────────    │
│  Theme: [Dark ▼]          │
│  Font Size: [M] - + [L]   │
│  Reduce Motion: [ ] Off   │
│                           │
│  AUDIO                    │
│  ─────────────────────    │
│  Sound Effects: [✓] On    │
│  Music: [✓] On            │
│  Volume: ──●─────── 70%   │
│                           │
│  GAMEPLAY                 │
│  ─────────────────────    │
│  Auto-save: [✓] On        │
│  Confirm choices: [ ] Off │
│  Skip animations: [ ] Off │
│                           │
│  DATA                     │
│  ─────────────────────    │
│  [ Export Save Data ]     │
│  [ Import Save Data ]     │
│  [ Clear All Data ]       │
│                           │
└───────────────────────────┘
```

## Dark Mode

**Light Theme:**
- Background: #F5F5DC (parchment)
- Text: #2C1810 (dark brown)
- Accent: #8B4513 (saddle brown)

**Dark Theme:**
- Background: #1A1A1A (near black)
- Text: #E0E0E0 (light gray)
- Accent: #4A9B5B (forest green)

```css
/* CSS Variables for theming */
:root {
  --bg-primary: #F5F5DC;
  --text-primary: #2C1810;
  --accent: #8B4513;
}

[data-theme='dark'] {
  --bg-primary: #1A1A1A;
  --text-primary: #E0E0E0;
  --accent: #4A9B5B;
}
```

## Implementation Checklist

**Mobile:**
- [ ] Bottom navigation
- [ ] Swipe gestures
- [ ] Full-screen sections
- [ ] Touch-friendly buttons (44x44px min)
- [ ] Responsive images
- [ ] Mobile-optimized combat UI

**Tablet:**
- [ ] Side drawer navigation
- [ ] Split-view (story + character sheet)
- [ ] Larger touch targets
- [ ] More content visible

**Desktop:**
- [ ] Persistent sidebar
- [ ] Multi-column layouts
- [ ] Keyboard shortcuts
- [ ] Hover states
- [ ] Larger illustrations

**General:**
- [ ] Dark mode toggle
- [ ] Font size adjustment
- [ ] Reduce motion option
- [ ] Screen reader support
- [ ] Keyboard navigation
- [ ] Save state persistence
- [ ] Smooth animations
