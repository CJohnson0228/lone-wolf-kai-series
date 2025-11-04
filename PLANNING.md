# Lone Wolf Gamebook Digitalization - Planning Document

## Project Overview

Convert Joe Dever's "Lone Wolf" gamebooks into an interactive desktop/web application with account management, character persistence, and automated gameplay systems.

## Core Requirements

### 1. Authentication & User Management

- User account creation/login
- Password authentication (consider OAuth options later)
- Session management
- Multiple characters per user (optional consideration)

### 2. Character System

- Character creation/stat tracking
- Abilities tracking (Sixth Sense, Healing, etc.)
- Equipment management
- Combat stats (CS, END, etc.)
- Character progression across books

### 3. Series Structure

- **Kai Series**: Books 1-4 (or 1-5?)
- **Magnakai Series**: Books 5/6-10
- **Kai Master Series**: Books 11+

Each series as a separate app/module allows:

- Smaller download sizes
- Easier maintenance
- Progressive feature additions
- Clear progression milestones

## Architecture Decisions

### Content Storage: Database vs App-Bundled

#### Option A: Database Storage (Recommended for Long-term)

**Pros:**

- Easy updates/corrections without app redeployment
- Can add user-generated content later
- Analytics on reading patterns
- Version control for book content
- A/B testing different narrative paths
- Multi-language support easier

**Cons:**

- Requires internet connection (unless cached)
- Initial setup complexity
- Database size considerations
- More complex deployment

**Implementation:**

- Store book text, choices, combat encounters in PostgreSQL
- Use JSONB columns for flexible structure
- Cache content locally for offline play
- Periodic sync for updates

#### Option B: App-Bundled Content

**Pros:**

- Fully offline capable
- Simpler initial architecture
- Faster access (no network calls)
- Smaller database footprint

**Cons:**

- App updates required for content changes
- Harder to track user progress through content
- No easy way to add community content
- Larger app bundle size

#### Recommendation: Hybrid Approach

- **Database**: Store user progress, character state, choices made
- **App Bundled**: Core book content (JSON files) for offline play
- **Sync**: Database tracks progression, book content in app
- **Updates**: Content updates can be downloaded as patches

This gives you:

- Offline capability
- Progress tracking
- Analytics capability
- Easy updates without full app redeployment

### Database Schema (PostgreSQL)

```sql
-- Users & Authentication
users (
  id UUID PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  created_at TIMESTAMP,
  last_login TIMESTAMP
)

-- Characters
characters (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(100),
  series VARCHAR(50), -- 'kai', 'magnakai', 'kai_master'
  current_book INTEGER,
  current_section INTEGER, -- paragraph number
  created_at TIMESTAMP,
  last_played TIMESTAMP
)

-- Character Stats
character_stats (
  character_id UUID REFERENCES characters(id),
  combat_skill INTEGER,
  endurance INTEGER,
  current_endurance INTEGER,
  gold_crowns INTEGER,
  backpack JSONB, -- array of items
  equipment JSONB, -- equipped items
  special_items JSONB, -- Kai items, Magnakai disciplines, etc.
  abilities JSONB -- Sixth Sense, Healing, etc.
)

-- Character Progress
character_progress (
  character_id UUID REFERENCES characters(id),
  book_number INTEGER,
  sections_visited JSONB, -- array of section numbers visited
  choices_made JSONB, -- array of {section: X, choice: Y, timestamp}
  combat_encounters JSONB, -- array of encounters fought
  items_acquired JSONB, -- items found in this book
  completed BOOLEAN DEFAULT FALSE,
  completed_at TIMESTAMP
)

-- Book Content (if storing in DB)
book_content (
  id SERIAL PRIMARY KEY,
  series VARCHAR(50),
  book_number INTEGER,
  section_number INTEGER,
  content_text TEXT,
  is_choice_point BOOLEAN,
  choices JSONB, -- array of {text: "...", target_section: X, requirements: {...}}
  combat_encounter JSONB, -- {enemy_cs: X, enemy_end: Y, ...}
  conditional_content JSONB -- {ability: "sixth_sense", target_section: X}
)
```

## Conditional Logic System

### Character Abilities & Requirements

Example: Sixth Sense ability

- When player reaches section with multiple choices
- Check character abilities
- If Sixth Sense exists, show third option OR automatically continue to Sixth Sense path
- Hide/show choices based on abilities

### Implementation Pattern:

```javascript
// Pseudo-code structure
{
  section: 1,
  text: "You stand at a crossroads...",
  choices: [
    { text: "Go left", target: 10, requirements: null },
    { text: "Go right", target: 20, requirements: null },
    {
      text: "Sense the hidden path",
      target: 30,
      requirements: { ability: "sixth_sense" },
      is_hidden: true // Hide if requirement not met
    }
  ],
  auto_continue: {
    condition: { ability: "sixth_sense" },
    target: 30,
    hide_other_choices: true // Show only "Continue" button
  }
}
```

## Feature Breakdown

### 1. Character Creation

- **Automated**: Pre-fill stats based on book rules
- Generate random Combat Skill (10 + dice roll)
- Generate random Endurance (20 + dice roll)
- Ability selection (player choice or random)
- Starting equipment
- **Streamlined**: Single screen with all choices, instant creation

### 2. Combat System

- **Automated**:
  - Roll dice automatically
  - Track combat rounds
  - Apply damage automatically
  - Handle special abilities (Sixth Sense warnings, Healing, etc.)
- **Streamlined**:
  - Visual combat log
  - "Attack" button (no manual dice rolling)
  - Show hit probabilities
  - Auto-resolve when possible

### 3. Equipment Management

- Visual inventory
- Drag-and-drop equipping
- Auto-equip suggestions
- Equipment effects automatically applied
- Backpack limit enforcement

### 4. Progress Tracking

- Books completed counter
- Section-by-section progress
- Achievement system (optional)
- Save/load at any point
- Multiple save slots per character

## Tech Stack - CONFIRMED ✅

### Frontend (Desktop/Web)

**Primary Choice: Tauri + React**
- ✅ Tauri chosen over Electron (smaller bundle, better performance)
- ✅ React for UI framework
- ✅ Tailwind CSS for styling
- ✅ shadcn/ui for component library
- ✅ Framer Motion for animations
- ✅ Cross-platform desktop (Windows, macOS, Linux)
- ✅ Can build web version from same codebase
- ✅ PWA support for mobile "install"

**Why Tauri over Electron:**
- Smaller binary size (~3-5MB vs ~120MB)
- Lower memory usage (Rust-based)
- Better performance
- Learning opportunity

### Backend API

**Options:**
- **Node.js + Express** (recommended for JS ecosystem consistency)
- **Python + FastAPI** (alternative if prefer Python)

**Features:**
- RESTful API for auth, character management
- WebSocket for real-time features (optional)
- JWT authentication
- CORS for web version

### Database

**PostgreSQL** ✅
- Via Cloudflare Tunnel for secure home server access
- Connection pooling for performance
- Stores: users, characters, progress, metadata
- Does NOT store book content (that's bundled in app)

### Authentication

- JWT tokens for sessions
- bcrypt (or Argon2) for password hashing
- Refresh token rotation
- Optional OAuth (Google, GitHub) later

### Content Delivery

**Hybrid Approach** ✅
- **Book content**: Bundled as JSON files in app
- **User data**: PostgreSQL database
- **Images**: Bundled in app, optimized for web/desktop
- **Updates**: Optional content patch download system

## UI/UX Considerations

### Book Reading Experience

- Large, readable fonts
- Dark mode option
- Smooth transitions between sections
- Visual indicators for:
  - Choices available
  - Combat encounters
  - Ability checks
  - Save points

### Character Dashboard

- Current stats prominently displayed
- Equipment visual slots
- Quick access to inventory
- Progress bar for current book

### Combat Interface

- Visual combat log
- Enemy stat display
- Round counter
- Current health bars
- Special ability buttons

## Implementation Phases

### Phase 1: MVP (Kai Series Book 1)

- Basic authentication
- Character creation
- Book 1 content (app-bundled JSON)
- Simple choice navigation
- Basic combat system
- Save/load functionality

### Phase 2: Database Integration

- Move to PostgreSQL
- User accounts and character storage
- Progress tracking
- Cloudflare tunnel setup

### Phase 3: Enhanced Features

- Conditional logic system
- Equipment management
- Multiple books in series
- Character progression

### Phase 4: Series Completion

- Complete Kai series
- Polish and optimization
- User feedback integration

### Phase 5: Next Series

- Magnakai series app
- Cross-series character import (if applicable)
- Advanced features

## CONFIRMED DECISIONS ✅

### Tech Stack
- **Framework**: Tauri + React (learn Tauri, smaller bundle than Electron)
- **UI Library**: Tailwind CSS + shadcn/ui + Framer Motion
- **Backend**: Node.js + Express (or Python + FastAPI)
- **Database**: PostgreSQL (via Cloudflare Tunnel)
- **Content Storage**: Hybrid approach (bundled JSON + DB for user data)

### App Structure
- **Separate Apps per Series**: Kai, Magnakai, Grand Master as separate apps
  - Reason: Portfolio/passion project, showcases creative UI work
  - Easier to maintain and release incrementally
  - Smaller downloads per app

### Series Structure
- **Kai Series**: Books 1-5
- **Magnakai Series**: Books 6-10 (fresh start with new mechanics)
- **Grand Master Series**: Books 11+

### Character Progression
- **Within Series**: Characters carry over between books
  - All equipment, stats, gold carry over
  - Gain +1 discipline per book completed (max 10 total)
  - Endurance resets to max at start of new book
- **Between Series**: Fresh start (Kai → Magnakai = new character)
  - Different mechanics (Kai vs Magnakai disciplines)
  - Justifies separate apps

### Combat System
- **Semi-Automated**:
  - Player clicks "Attack" each round
  - System generates random number (0-9)
  - Calculates damage using Combat Results Table
  - Visual combat log shows each round
  - Combat continues until one reaches 0 Endurance

### Character Creation
- **Mirrors Book Experience**:
  - Roll random (0-9) + 10 = Combat Skill (10-19)
  - Roll random (0-9) + 20 = Endurance (20-29)
  - Choose 5 Kai Disciplines from 10 available
  - If Weaponskill chosen, roll for weapon type
  - Roll for starting gold (0-9)
  - Roll for one additional starting item (0-9)
  - Start with: Axe, 1 Meal, Map of Sommerlund

### Content Source
- **Project Aon HTML Files**: ✅ AVAILABLE
  - Need to build Python scraper to extract content
  - Parse HTML into structured JSON format
  - Extract text, choices, combat stats, conditionals
  - Copy and optimize images

### Platform Target
- **Both Desktop and Web Simultaneously**:
  - Tauri builds for desktop (Windows, macOS, Linux)
  - Web version is mobile-friendly (responsive design)
  - Single React codebase for both
  - PWA capabilities for "install" on mobile

### Offline/Online
- **Offline-First**:
  - Content bundled in app (JSON files)
  - Works fully offline
  - Optional sync to cloud (PostgreSQL) for cross-device play
  - Auto-save locally + cloud sync

## Open Questions to Resolve

1. ~~**Book Range**: Confirm exact book numbers for each series~~ ✅ RESOLVED
   - Kai: Books 1-5
   - Magnakai: Books 6-10
   - Grand Master: Books 11+

2. ~~**Character Transfer**: Can characters carry over between series?~~ ✅ RESOLVED
   - Yes within series, No between series

3. ~~**Content Licensing**~~ ✅ RESOLVED
   - Using Project Aon open content (legally approved)

4. ~~**Offline Priority**~~ ✅ RESOLVED
   - Offline-first with optional cloud sync

5. **Multiplayer/Sharing**: ⏳ TO BE DECIDED
   - Share character builds?
   - Compare progress?
   - Leaderboards?

6. ~~**Platform Priority**~~ ✅ RESOLVED
   - Both desktop and web simultaneously

## Next Steps - Development Roadmap

### Phase 0: Planning & Setup ✅ COMPLETED
- [x] Confirm tech stack (Tauri + React)
- [x] Confirm app structure (separate apps per series)
- [x] Document character creation flow
- [x] Document combat system
- [x] Document UI/UX flows
- [x] Plan content extraction strategy

### Phase 1: Content Extraction (NEXT)
1. **Build Python Scraper**
   - Parse Project Aon HTML files
   - Extract sections, choices, combat encounters
   - Extract disciplines and equipment rules
   - Export to JSON format
   - Validate extracted content

2. **Process Book 1 Content**
   - Extract all 350 sections
   - Verify links and choices
   - Optimize and organize images
   - Create content manifest

3. **Test Content**
   - Manual verification of key sections
   - Test conditional logic extraction
   - Validate combat encounters
   - Check for missing or malformed data

### Phase 2: MVP Development
1. **Setup Tauri + React Project**
   - Initialize Tauri app
   - Setup React with TypeScript
   - Configure Tailwind CSS
   - Setup routing (React Router)

2. **Implement Character Creation**
   - Stats rolling screen
   - Discipline selection
   - Equipment generation
   - Character summary

3. **Implement Story Reader**
   - Section display component
   - Choice rendering
   - Navigation between sections
   - Image display

4. **Implement Combat System**
   - Combat engine logic
   - Combat UI
   - Combat results table
   - Victory/defeat handling

5. **Implement Save System**
   - LocalStorage for MVP
   - Save/load character
   - Save progress
   - Auto-save

### Phase 3: Database Integration
1. **Setup PostgreSQL**
   - Database schema creation
   - Cloudflare Tunnel setup
   - Connection pooling

2. **Build Backend API**
   - User authentication
   - Character CRUD operations
   - Progress tracking
   - Cloud save/load

3. **Integrate Frontend**
   - API client
   - Authentication flow
   - Cloud sync
   - Offline support

### Phase 4: Polish & Complete Book 1
1. **UI Polish**
   - Responsive design refinement
   - Animations and transitions
   - Dark mode
   - Accessibility improvements

2. **Testing**
   - Playthrough Book 1 completely
   - Bug fixes
   - Balance testing
   - Performance optimization

3. **Additional Features**
   - Inventory management UI
   - Equipment screen
   - Stats dashboard
   - Settings screen

### Phase 5: Books 2-5 (Kai Series Completion)
1. **Extract Books 2-5 Content**
2. **Implement Book Progression**
   - Character carry-over
   - Discipline unlocking
   - Book completion flow

3. **Series Completion**
   - All 5 books playable
   - Achievements/tracking
   - Full series experience

### Phase 6: Release & Iteration
1. **Beta Testing**
2. **Package for Distribution**
   - Desktop builds (Windows, macOS, Linux)
   - Web deployment
3. **Release Kai Series App**
4. **Gather Feedback**
5. **Plan Magnakai Series App**

## Resources

- Project Aon: https://www.projectaon.org/ (Open source Lone Wolf content)
- Lone Wolf Wiki: For rules clarification
- Original gamebook mechanics documentation
