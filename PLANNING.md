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

## Tech Stack Recommendations

### Frontend (Desktop/Web)

- **Electron + React** or **Tauri + React/Vue**
  - Cross-platform desktop app
  - Web tech stack (easier development)
  - Can build web version from same codebase
- **Alternative: Progressive Web App (PWA)**
  - Single codebase for web and mobile
  - Can be "installed" on desktop
  - Offline capability with service workers

### Backend API

- **Node.js + Express** or **Python + FastAPI**
- RESTful API for auth, character management
- GraphQL optional for complex queries

### Database

- **PostgreSQL** (as specified)
- Cloudflare Tunnel for secure access
- Connection pooling for performance

### Authentication

- JWT tokens for sessions
- bcrypt for password hashing
- Refresh token rotation

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

## Open Questions to Resolve

1. **Book Range**: Confirm exact book numbers for each series

   - Kai: 1-4 or 1-5?
   - Magnakai: 5-10 or 6-10?

2. **Character Transfer**: Can characters carry over between series?

   - Equipment/items?
   - Stats?
   - Or fresh start per series?

3. **Content Licensing**:

   - Have rights to digitize text?
   - Need to use Project Aon open content?

4. **Offline Priority**:

   - Must work fully offline?
   - Or online-first acceptable?

5. **Multiplayer/Sharing**:

   - Share character builds?
   - Compare progress?
   - Leaderboards?

6. **Platform Priority**:
   - Desktop first?
   - Web-first?
   - Both simultaneously?

## Next Steps

1. **Confirm Series Structure**: Lock down exact book numbers
2. **Content Source**: Verify licensing/use Project Aon content
3. **Tech Stack Selection**: Choose frontend framework
4. **Database Design**: Finalize schema based on storage decision
5. **Prototype**: Build MVP for Book 1, Section 1-10 to test flow

## Resources

- Project Aon: https://www.projectaon.org/ (Open source Lone Wolf content)
- Lone Wolf Wiki: For rules clarification
- Original gamebook mechanics documentation
