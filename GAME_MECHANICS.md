### File: docs/GAME_MECHANICS.md

# Game Mechanics

## Core Gameplay Loop

1. **Oracle Selection**: Choose from available oracles
2. **Exploration Phase**: Learn about oracle's domain
3. **Puzzle Phase**: Solve oracle-specific puzzle
4. **Battle Phase**: Combat with oracle's army
5. **Confrontation Phase**: Final dialogue/choice
6. **Reward Phase**: Receive army units, weapons, resources
7. **Progression**: Unlock next stage, world state changes

## Oracle Mechanics

Each of the 13 oracles has unique mechanics:

### Chronos (Time)
- Rewinds puzzles if you fail
- Can cancel your last reward
- Time limits decrease with difficulty

### Nyx (Shadow)
- 50% of hints are lies
- Hides critical puzzle elements
- Shadow stalker assassins

### Proteus (Illusion)
- Changes puzzle rules mid-solve
- Map routes shift
- Fake exits appear

### Aresion (War)
- Forces combat-focused challenges
- Boosts enemy armies after other defeats
- Elite spartan units

### Athenaia (Wisdom)
- Increases puzzle complexity dynamically
- Acts like chess engine
- Strategic buffs for armies

### Helios (Solar)
- Burns away overused clues
- Fire-based attacks
- Light reveals but also destroys

### Boreas (Storm)
- Freezes troops mid-route
- Ice hazards in puzzles
- Frost damage over time

### Gaia (Earth)
- Puzzles physically shift while solving
- Earth-based army units
- Resource bonuses from controlled territories

### Themis (Law)
- Punishes moral contradictions
- Balance-based puzzles
- Karmic justice mechanics

### Echo (Sound)
- Audio-based puzzles
- Sound illusions
- Voice manipulation

### Selene (Moon)
- Dream sequences alter choices
- Lunar phases affect difficulty
- Phantom units

### DelphiX (Prophecy)
- Predicts player moves
- Pre-emptive counters
- Prophetic visions as hints

### Typhon (Chaos - Final Boss)
- Rewrites own rules dynamically
- Combines all previous mechanics
- Three-phase final battle

## Resource Management

### Gold
- Recruit additional units
- Purchase potions
- Upgrade weapons

### Insight Tokens
- Ask for hints from knowledge oracle
- Limited resource (gain from victories)
- Strategic decision when to use

### Healing Draughts
- Restore army health
- Limited quantity
- Critical for difficult battles

### Weapons
- Each oracle defeat grants unique weapon
- Weapons unlock new puzzle types
- Combat bonuses

### Special Items
- Quest rewards
- Unlock secret paths
- Provide passive bonuses

## Army System

### Unit Types
- Infantry: Balanced stats
- Cavalry: High speed, flanking
- Archers: Ranged attacks
- Special: Unique abilities
- Giants: High health, slow

### Combat Mechanics
- Turn-based with real-time elements
- Attack/Defense calculations
- Morale affects performance
- Experience levels grant bonuses
- Element affinities (fire > ice > shadow)

### Deployment
- Choose which units to deploy
- Formation matters
- Reserves can reinforce

## Progression System

### Stages
- 13 total stages (one per oracle)
- Non-linear progression possible
- Some oracles require prerequisites

### World State
- Defeating oracles changes global rules
- Alliances form between remaining oracles
- Hostilities increase
- New paths unlock

### Difficulty Scaling
- Later oracles use combined mechanics
- Enemy armies grow stronger
- Puzzle complexity increases
- Time limits tighten

## Agent Behavior

### Learning
- Agents remember player patterns
- Adapt strategies based on victories/defeats
- Share information with other agents

### Deception
- Some agents lie or misdirect
- Hidden agendas revealed over time
- Trust becomes a mechanic

### Diplomacy
- Negotiate with oracles
- Form temporary alliances
- Betray or be betrayed

##      const response = await oracleAPI.solvePuzzle(
        gameId!,
        1, // Would be actual oracle state ID
        solution
      )

      if (response.data.valid) {
        setNotification('Correct! Moving to battle phase...')
        setCurrentPhase('battle')
      } else {
        setNotification('Incorrect solution. Try again.')
      }
      setTimeout(() => setNotification(null), 3000)
    } catch (error) {
      console.error('Failed to submit solution:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="puzzle-renderer">
      <h3>Puzzle Challenge</h3>
      <div className="puzzle-description">
        <p>Solve the puzzle to proceed to battle...</p>
        <p>Type: Logic Puzzle</p>
      </div>

      <div className="puzzle-input-area">
        <textarea
          value={solution}
          onChange={(e) => setSolution(e.target.value)}
          placeholder="Enter your solution..."
          rows={4}
          className="puzzle-input"
        />
      </div>

      <div className="puzzle-actions">
        <button onClick={handleSubmitSolution} disabled={loading} className="submit-btn">
          {loading ? 'Checking...' : 'Submit Solution'}
        </button>
        <button onClick={() => setShowHint(!showHint)} className="hint-btn">
          {showHint ? 'Hide Hint' : 'Show Hint'}
        </button>
      </div>

      {showHint && (
        <div className="puzzle-hint">
          <p>Hint: Consider the pattern carefully...</p>
        </div>
      )}
    </div>
  )
}

export default PuzzleRenderer