# Combat System - Semi-Automated Implementation

## Overview

Combat is semi-automated: player clicks "Attack" each round, system generates random numbers, calculates damage, and updates health. Combat continues until one combatant reaches 0 Endurance.

## Combat Flow

```
1. Enter Combat Section
   ↓
2. Display Combat Intro
   - Show enemy stats
   - Show player stats
   - Sixth Sense warning (if applicable)
   - Can evade? (if allowed)
   ↓
3. Combat Loop:
   - Player clicks "Attack"
   - Generate random number (0-9)
   - Calculate Combat Ratio
   - Look up damage on Combat Results Table
   - Apply damage to both combatants
   - Display round result
   - Check for victory/defeat
   - If not ended, repeat
   ↓
4. Combat Resolution
   - Victory: Continue to next section
   - Defeat: Death screen (restart book)
```

## Combat Rules (from Book)

### Combat Ratio Calculation

```
Combat Ratio = (Player's COMBAT SKILL + modifiers) - Enemy's COMBAT SKILL

Modifiers:
+ Weaponskill bonus (+2 if using skilled weapon)
+ Mindblast bonus (+2 if have discipline and enemy not immune)
- No weapon penalty (-4 if no weapon equipped)
```

**Example:**
```
Player CS: 15
Disciplines: Mindblast
Weapon: Axe (no weaponskill)

Enemy CS: 20

Calculation:
15 (base CS) + 2 (Mindblast) - 20 (enemy CS) = -3

Combat Ratio: -3
```

### Combat Results Table

For each round:
1. Calculate Combat Ratio
2. Generate random number (0-9)
3. Cross-reference on Combat Results Table
4. Apply damage to both combatants

**Combat Results Table:**

```
Combat Ratio:    -11  -10  -9   -8   -7   -6   -5   -4   -3   -2   -1    0   +1   +2   +3   +4   +5   +6   +7   +8   +9  +10  +11

Random Number:
0               K    K    K    K    K    K    8    8    7    6    6    5    5    4    3    3    2    2    1    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     0    0    0    0    0    0    6    6    5    4    3    3    2    2    1    0    0    0    0    0    0    0    0

1               K    K    K    K    K    8    7    6    6    5    5    4    4    3    2    2    1    1    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     0    0    0    0    0    6    5    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0

2               K    K    K    K    8    7    6    6    5    5    4    4    3    3    2    2    1    1    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     0    0    0    0    6    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0

3               K    K    K    8    7    6    6    5    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     0    0    0    6    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0

4               K    K    8    7    6    6    5    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     0    0    6    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0

5               K    8    7    6    6    5    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     0    6    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0

6               8    7    6    5    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     6    5    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0

7               7    6    5    4    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     5    4    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0

8               6    5    4    3    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     4    3    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0

9               5    4    3    2    2    1    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0
                     LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW   LW
                     3    2    1    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0    0

E = Enemy loses this many ENDURANCE points
LW = Lone Wolf loses this many ENDURANCE points
K = Lone Wolf is killed (instant death)
```

### Implementation as Data Structure

```javascript
// Combat Results Table as 2D array
// combatTable[randomNumber][combatRatio]
const COMBAT_TABLE = {
  // Random Number: { Combat Ratio: { enemy: damage, player: damage } }
  0: {
    '-11': { enemy: 0, player: 'KILL' },
    '-10': { enemy: 0, player: 'KILL' },
    '-9': { enemy: 0, player: 'KILL' },
    '-8': { enemy: 0, player: 'KILL' },
    '-7': { enemy: 0, player: 'KILL' },
    '-6': { enemy: 0, player: 'KILL' },
    '-5': { enemy: 6, player: 8 },
    '-4': { enemy: 6, player: 8 },
    '-3': { enemy: 5, player: 7 },
    '-2': { enemy: 4, player: 6 },
    '-1': { enemy: 3, player: 6 },
    '0': { enemy: 3, player: 5 },
    '1': { enemy: 2, player: 5 },
    '2': { enemy: 2, player: 4 },
    '3': { enemy: 1, player: 3 },
    '4': { enemy: 0, player: 3 },
    '5': { enemy: 0, player: 2 },
    '6': { enemy: 0, player: 2 },
    '7': { enemy: 0, player: 1 },
    '8': { enemy: 0, player: 0 },
    '9': { enemy: 0, player: 0 },
    '10': { enemy: 0, player: 0 },
    '11': { enemy: 0, player: 0 }
  },
  // ... (similar structure for random numbers 1-9)
};

// Helper function to look up combat result
function getCombatResult(randomNumber, combatRatio) {
  // Clamp combat ratio to valid range (-11 to +11)
  const clampedRatio = Math.max(-11, Math.min(11, combatRatio));

  return COMBAT_TABLE[randomNumber][clampedRatio.toString()];
}
```

## Combat Implementation

### Combat Engine Class

```typescript
class CombatEngine {
  player: {
    name: string;
    combatSkill: number;
    endurance: number;
    weapon: string | null;
    disciplines: string[];
  };

  enemy: {
    name: string;
    combatSkill: number;
    endurance: number;
    immuneToMindblast: boolean;
  };

  combatLog: CombatRound[];
  currentRound: number;
  canEvade: boolean;

  constructor(player, enemy, canEvade = false) {
    this.player = { ...player };
    this.enemy = { ...enemy };
    this.combatLog = [];
    this.currentRound = 0;
    this.canEvade = canEvade;
  }

  calculateCombatRatio(): number {
    let playerCS = this.player.combatSkill;

    // Apply Weaponskill bonus
    if (this.player.disciplines.includes('weaponskill') && this.player.weapon) {
      playerCS += 2;
    }

    // Apply Mindblast bonus
    if (this.player.disciplines.includes('mindblast') && !this.enemy.immuneToMindblast) {
      playerCS += 2;
    }

    // No weapon penalty
    if (!this.player.weapon) {
      playerCS -= 4;
    }

    return playerCS - this.enemy.combatSkill;
  }

  executeRound(): CombatRoundResult {
    this.currentRound++;

    // Generate random number (0-9)
    const randomNumber = Math.floor(Math.random() * 10);

    // Calculate combat ratio
    const combatRatio = this.calculateCombatRatio();

    // Look up result from combat table
    const result = getCombatResult(randomNumber, combatRatio);

    // Check for instant kill
    if (result.player === 'KILL') {
      return {
        round: this.currentRound,
        randomNumber,
        combatRatio,
        playerDamage: this.player.endurance, // All HP
        enemyDamage: 0,
        playerEndurance: 0,
        enemyEndurance: this.enemy.endurance,
        outcome: 'player_killed'
      };
    }

    // Apply damage
    this.player.endurance -= result.player;
    this.enemy.endurance -= result.enemy;

    // Determine outcome
    let outcome: 'ongoing' | 'player_victory' | 'player_defeat' | 'player_killed' = 'ongoing';

    if (this.player.endurance <= 0) {
      outcome = 'player_defeat';
      this.player.endurance = 0;
    } else if (this.enemy.endurance <= 0) {
      outcome = 'player_victory';
      this.enemy.endurance = 0;
    }

    const roundResult = {
      round: this.currentRound,
      randomNumber,
      combatRatio,
      playerDamage: result.player,
      enemyDamage: result.enemy,
      playerEndurance: this.player.endurance,
      enemyEndurance: this.enemy.endurance,
      outcome
    };

    this.combatLog.push(roundResult);
    return roundResult;
  }

  evadeCombat(): EvadeResult {
    if (!this.canEvade) {
      throw new Error('Cannot evade this combat');
    }

    // If already in combat, player takes damage from final round
    if (this.currentRound > 0) {
      const lastRound = this.combatLog[this.combatLog.length - 1];
      return {
        success: true,
        damageTaken: lastRound.playerDamage,
        message: `You flee from the ${this.enemy.name}, taking ${lastRound.playerDamage} damage!`
      };
    }

    return {
      success: true,
      damageTaken: 0,
      message: `You avoid combat with the ${this.enemy.name}!`
    };
  }
}
```

## UI Design - Combat Screen

```
╔═══════════════════════════════════════════════════════╗
║              COMBAT: GIAK WARRIOR                      ║
╠═══════════════════════════════════════════════════════╣
║                                                        ║
║  [Enemy Portrait/Image]                                ║
║                                                        ║
║  GIAK WARRIOR                                          ║
║  CS: 13    HP: ████████░░ 8/10                        ║
║                                                        ║
║  ━━━━━━━━━━━━━━━ VS ━━━━━━━━━━━━━━━                   ║
║                                                        ║
║  LONE WOLF (YOU)                                       ║
║  CS: 15    HP: ████████████████░░░░ 16/20             ║
║                                                        ║
╠═══════════════════════════════════════════════════════╣
║  COMBAT LOG                                            ║
║  ─────────────────────────────────────────────────────║
║  Round 3:                                              ║
║  You rolled a 6!                                       ║
║  Combat Ratio: +2                                      ║
║  ➜ You deal 4 damage to the Giak!                     ║
║  ➜ The Giak deals 2 damage to you!                    ║
║  ─────────────────────────────────────────────────────║
║  Round 2:                                              ║
║  You rolled a 3!                                       ║
║  Combat Ratio: +2                                      ║
║  ➜ You deal 2 damage to the Giak!                     ║
║  ➜ The Giak deals 4 damage to you!                    ║
║  ─────────────────────────────────────────────────────║
║                                                        ║
╠═══════════════════════════════════════════════════════╣
║  [🗡️ ATTACK]     [🏃 EVADE] (if allowed)              ║
╚═══════════════════════════════════════════════════════╝
```

### Mobile-Friendly Version

```
┌───────────────────────┐
│   GIAK WARRIOR        │
│   CS: 13              │
│   HP: ████████░░ 8/10 │
│                       │
│   [Enemy Image]       │
│                       │
│   ━━━━━ VS ━━━━━      │
│                       │
│   YOU                 │
│   CS: 15              │
│   HP: ████████░░ 16/20│
│                       │
├───────────────────────┤
│ 📜 COMBAT LOG         │
├───────────────────────┤
│ Round 3:              │
│ Rolled: 6             │
│ You hit! -4 HP        │
│ Enemy hit! -2 HP      │
│                       │
│ [Tap to see more]     │
│                       │
├───────────────────────┤
│                       │
│  [  ⚔️ ATTACK  ]      │
│                       │
│  [  🏃 EVADE  ]       │
│                       │
└───────────────────────┘
```

## Combat Sequence Example

### Example Combat: Lone Wolf vs Giak

**Setup:**
- Lone Wolf CS: 15, Endurance: 25
- Disciplines: Mindblast
- Weapon: Axe (no weaponskill)
- Giak CS: 13, Endurance: 10
- Giak is NOT immune to Mindblast
- Cannot evade

**Round 1:**
```
Combat Ratio = (15 + 2 Mindblast) - 13 = +4

Player clicks [ATTACK]
Random number: 3

Look up table[3][+4] = { enemy: 1, player: 1 }

Giak takes 1 damage (10 → 9)
Lone Wolf takes 1 damage (25 → 24)

Display:
"You rolled a 3!"
"Combat Ratio: +4"
"➜ You deal 1 damage to the Giak!"
"➜ The Giak deals 1 damage to you!"
```

**Round 2:**
```
Combat Ratio = +4 (unchanged)

Player clicks [ATTACK]
Random number: 7

Look up table[7][+4] = { enemy: 0, player: 0 }

No damage to either combatant

Display:
"You rolled a 7!"
"Combat Ratio: +4"
"➜ Both combatants dodge!"
```

**Round 3:**
```
Combat Ratio = +4

Player clicks [ATTACK]
Random number: 2

Look up table[2][+4] = { enemy: 2, player: 2 }

Giak takes 2 damage (9 → 7)
Lone Wolf takes 2 damage (24 → 22)

Display:
"You rolled a 2!"
"Combat Ratio: +4"
"➜ You deal 2 damage to the Giak!"
"➜ The Giak deals 2 damage to you!"
```

**Round 4:**
```
Combat Ratio = +4

Player clicks [ATTACK]
Random number: 1

Look up table[1][+4] = { enemy: 2, player: 3 }

Giak takes 2 damage (7 → 5)
Lone Wolf takes 3 damage (22 → 19)

Display:
"You rolled a 1!"
"Combat Ratio: +4"
"➜ You deal 2 damage to the Giak!"
"➜ The Giak deals 3 damage to you!"
```

**Round 5:**
```
Combat Ratio = +4

Player clicks [ATTACK]
Random number: 0

Look up table[0][+4] = { enemy: 0, player: 3 }

Giak takes 0 damage (5 → 5)
Lone Wolf takes 3 damage (19 → 16)

Display:
"You rolled a 0!"
"Combat Ratio: +4"
"➜ The Giak dodges your attack!"
"➜ The Giak deals 3 damage to you!"
```

**Round 6:**
```
Combat Ratio = +4

Player clicks [ATTACK]
Random number: 8

Look up table[8][+4] = { enemy: 0, player: 0 }

No damage

... combat continues until one reaches 0 Endurance
```

## Evasion Rules

**From Book:**
- If evade option available, player can flee
- If already in combat (round 1+), player must complete that round
- Player takes damage from that round
- Enemy takes NO damage from that round
- Then player escapes

**Implementation:**
```javascript
function handleEvade(combat) {
  if (combat.currentRound > 0) {
    // Execute one more round, but ignore enemy damage
    const round = combat.executeRound();
    const playerDamage = round.playerDamage;

    // Ignore enemy damage
    combat.enemy.endurance += round.enemyDamage;

    return {
      success: true,
      message: `You flee, taking ${playerDamage} damage!`,
      damageTaken: playerDamage
    };
  } else {
    return {
      success: true,
      message: 'You avoid combat!',
      damageTaken: 0
    };
  }
}
```

## Victory & Defeat

### Victory Screen
```
┌─────────────────────────┐
│   ⚔️ VICTORY! ⚔️         │
│                         │
│ You have defeated       │
│ the Giak Warrior!       │
│                         │
│ Your Endurance: 16/25   │
│                         │
│ [Healing available?]    │
│ • Use Healing: +1 END   │
│ • Healing Potion: +4 END│
│                         │
│ [💰 Loot]               │
│ • 3 Gold Crowns found   │
│                         │
│ [  Continue  ]          │
└─────────────────────────┘
```

### Defeat Screen
```
┌─────────────────────────┐
│      💀 DEFEAT 💀        │
│                         │
│ You have been slain     │
│ by the Giak Warrior!    │
│                         │
│ The adventure ends here.│
│                         │
│ Books Completed: 0      │
│ Sections Visited: 15    │
│ Enemies Defeated: 2     │
│                         │
│ [ Restart Book ]        │
│ [ Main Menu ]           │
└─────────────────────────┘
```

## Special Combat Mechanics

### Sixth Sense Warning
If player has Sixth Sense, warn before combat:
```
"Your Sixth Sense warns you of danger ahead!"
```

### Mindshield Protection
If enemy has Mindblast and player has Mindshield:
```
"The enemy's Mindblast has no effect on you!"
(No additional damage)
```

### Healing After Combat
If player has Healing discipline:
```
"You rest and use your Healing skill."
"+1 Endurance restored"
```

## Testing Checklist

- [ ] Combat ratio calculates correctly
- [ ] Random number generation is truly random
- [ ] Combat table lookups are accurate
- [ ] Damage applies correctly
- [ ] Combat ends when Endurance reaches 0
- [ ] Instant kill ("K") works correctly
- [ ] Evade mechanics work (if allowed)
- [ ] Victory leads to next section
- [ ] Defeat leads to game over
- [ ] Combat log displays correctly
- [ ] Mobile UI is touch-friendly
- [ ] Animations are smooth
- [ ] Healing post-combat works
- [ ] Mindblast/Mindshield interactions work
- [ ] No weapon penalty applies correctly (-4 CS)
