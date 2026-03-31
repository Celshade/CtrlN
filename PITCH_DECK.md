# CKEY: CTRL+N — Pitch Deck

**[Watch the demo on YouTube](https://youtu.be/hiHF5U4OsPU)** — 90-seconds of in-app usage with commentary

## 🎮 The Game

**CTRL+N** is a fast-paced, skill-based mobile action game with hand-crafted pixel art — developed with a passion for indie games and code itself. Tap to dodge, compete against your fellow degens, unlock new playable characters (keys), flex your rank roles in the community, and have fun. Swipe mechanics coming soon for advanced maneuvers.

---

## 🎯 Core Loop

1. **Select Character** — Choose from unlockable keyboard keys (characters with unique audio signatures)
2. **Play** — Tap to dodge procedurally-challenging obstacles (birds, trees, hazards); higher score = better rank
3. **Compete** — Compare scores on global/friend leaderboards; earn rank tiers (Bamboo → Iron → Bronze → Gold → Platinum → Diamond)
4. **Progress** — Unlock new key characters, achievements, cosmetics, and audio packs

**Key Mechanics**: One-button tap + swipe for advanced maneuvers (coming soon), real-time competition, cross-chain asset integration via Matrica

---

## ✨ Key Features

### 📊 Player Progression
- **Energy System**: 5 free matches per session/day (TBD); Energy regenerates over time or via $SKR purchase
- **Achievement System**: Unlock badges and titles (free + purchasable cosmetics)
- **Character Unlocks**: Earn new playable characters and abilities through gameplay
- **Rank Tiers**: Progress through competitive ranks (Unranked → Bamboo → ... → Diamond)
- **Profile Customization**: Equipped character, avatar, bio (cosmetics via $SKR)
- **Cross-Chain Asset Integration**: Unlock bonuses, characters, and abilities by validating existing NFT traits/assets via Matrica (Ethereum NFTs, Solana collections; Bitcoin Ordinals coming soon)

### 🎵 Audio Packs
- **Keyboard-Based Audio Identity**: Each playable character is a key from a keyboard; gameplay includes dynamic keypress sounds that vary by equipped audio pack
- **Unlockable Audio Packs**: Players unlock different keyboard audio packs through gameplay progression or $SKR store purchases
- **Authentic Keyboard Recordings**: Each audio pack contains keypress sounds recorded from actual mechanical/membrane keyboards with distinct acoustic signatures
- **Per-Keyboard Variety**: Multiple packs available (Cherry MX Red, Cherry MX Blue, Topre, Membrane, etc.) — each with authentic keycap click/clack characteristics
- **Audio Feedback Loop**: Tie visual character identity (the "key") directly to audio feedback, reinforcing the keyboard theme and adding personality to each play session

### 🚀 Gameplay Evolution (Future Iterations)
- **Swipe Mechanics**: Advanced input system for complex maneuvers
- **Unique Player Abilities**: Character-specific gameplay mechanics and power-ups
- **Level Expansions**: Day, Night, Snow, ???, Miami [Bonus], ??? (3-6 additional levels already planned)

### 👥 Social & Engagement
- **Global Leaderboards**: Real-time competitive ranking
- **Friend Rankings**: Compare scores with friends
- **Achievements**: Visible badges and milestones
- **Cosmetics**: Character skins and visual items

### ⚙️ Technical
- **Cross-Platform**: Android (iOS coming Q3 2026) via Godot 4.6
- **Desktop Support**: Python 3.12 + Pygame for development/testing
- **Cloud Saves**: Profile tied to login
  - **Matrica OAuth** (primary): Multi-chain social login (Discord, X, Telegram + all major Web3 wallets -> including native solana mobile wallet)
  - **Solana Wallet Adapter** (secondary, coming soon): Direct wallet signing via Mobile Wallet Adapter 2.0
- **Energy System**: Tracks playtime, regeneration, and purchases
- **SKR Integration**: In-game store powered by Solana Mobile token
- **Website Companion**: Enhanced leaderboard metrics, detailed player stats, achievement tracking (coming Q3 2026)
- **Instant Restarts**: Quick retry loops for skill development

---

## 🔐 Web3 Integration: Optional Profile NFT Minting

**CTRL+N profiles can be optionally minted as NFTs on Solana**, giving players enhanced security and portability:

### Value Proposition
_* = TBD_

- **Cost**: $1-5* (+ network fees) one-time (optional to mint)
- **Benefits**:
  - Enhanced security: Profile backed by on-chain assets
  - Portability: Use profile across compatible games
  - Permanence: Leaderboard history immutably stored
  - Composability: Future games can read CtrlN achievements
  - **Leaderboard Participation***: Required to compete in seasonal leaderboards (free-to-play players can still play; profile data saves locally and to database with less frequent syncs, but not on-chain)

**Future Expansion**: Bitcoin Ordinal profiles planned for a future iteration, allowing players to mint profiles as Bitcoin NFTs alongside Solana options.

### On-Chain Storage

- **Account Data**
  - Public portfolio (score, rank, cosmetics)
  - Achievements and unlock history
  - Timestamps and progression milestones
  
- **Character Ownership**
  - Equipped character NFT (if any)
  - Unlocked character collection
  - Visual metadata (colors, animations)

- **On-Chain Metadata**: Profile data stored on Solana/Bitcoin blockchain with NFT/Inscription protocols

### Technical Architecture

```
┌─────────────┐
│   Player    │
└──────┬──────┘
       │
       ├─ Login: Matrica OAuth (primary) or Solana Wallet (secondary)
       ├─ Profile created/loaded
       │
       ├─ Energy System: 5 free matches per session
       ├─ Store: Purchase $SKR for playtime/cosmetics/power-ups
       │
       ├─ [OPTIONAL] Mint Profile as NFT
       │   ├─ Cost: mint/inscription cost + $1-5*
       │   ├─ Unlocks: Leaderboard participation, portability, cross-game play
       │   └─ NFT metadata on Solana/Bitcoin blockchain
       │       └─ Character unlocks, achievements, cosmetics
       │
       └─ Leaderboard: Ranked participation requires minted profile NFT
```

---

## 🎨 Visual & Art Direction

- **Minimalist Style**: Clean pixel-art characters and obstacles
- **Responsive Feedback**: Particle effects, screen shake, sound cues
- **Playable Key Characters**: Keyboard keys with distinct visual personalities and audio signatures; unlockable variants
- **Dynamic Obstacles**: Birds, trees, platforms, and hazards that escalate in speed/complexity

---

## 👥 Development Team

**CtrlN** was created by a **single developer** with support from community artists:

- **Celshade** (Developer): Game design, programming, player sprites, effects and animation, UI design, infrastructure, marketing, partnerships, and community administration
- **Psy** (Artist): Level backgrounds and obstacle art/animation
- **MomoBones** (Artist): Concept art and logo design

**Vision**: Proof-of-concept that indie games can achieve quality production through focused individual development and collaborative community partnerships.

This lean structure allows for rapid iteration while maintaining artistic quality and community involvement.

---

## 🌍 Target Audience

- **Primary**: Casual mobile gamers (18-35) seeking quick, skill-based (but relaxed) action
- **Secondary**: Mobile streamers & competitive skill-based speedrunners
- **Tertiary**: Web3 gamers seeking optional blockchain profile verification & cross-game portability

---

## 💰 Monetization Strategy

### Core Model: Energy-Based Free-to-Play

- **Base Game**: Free-to-play with energy system
  - 5 matches per session (free playtime)
  - Energy regenerates over time (configurable timers)
  - Optional paid energy/fast-regen via $SKR

### Solana NFT Profiles (Optional, One-Time)

- **Cost**: $1-5* (+ network fees) one-time
- **Benefits**: Enhanced data security, portability across games, leaderboard participation
- **Not required**: Players can enjoy full game without NFT Profile

### In-Store Purchases ($SKR)

All premium purchases use **$SKR (Solana Mobile Token)**:

- **Cosmetics**: Character skins, effects, avatars
- **Playtime**: Additional energy/matches
- **Power-ups**: Temporary gameplay enhancements
- **Battle Pass** (future): Seasonal cosmetic bundles

---

## � Development Status

**Current**: v0.1.1 **Demo** (Public Prototype) — [Download on GitHub Releases](https://github.com/Celshade/CtrlN/releases/tag/v0.1.1-demo)

| Status | Description | Timeline |
|--------|-------------|----------|
| **Demo** (NOW) | Single level, core gameplay, auth integrated. | April-May 2026 |
| **Alpha** (v0.2.0+) | Store system, cosmetics, broader feature set. | May-June 2026 |
| **Beta** (v0.5.0+) | Full monetization, NFT minting UI, save data stable. | July-August 2026 |
| **Release** (v1.0.0) | Tournaments, portability, cross-platform optimization. | Q3-Q4 2026 |

---

## 🚀 Go-to-Market

**Phase 1: Demo → Soft Launch (Q2 2026)**
- Public demo on GitHub Releases with Matrica OAuth integration
- Level 1 (Day-Time) with core gameplay and energy system operational
- In-game leaderboards and $SKR cosmetic store live
- Community feedback gathering

**Phase 2: Alpha → Full Launch (Q3 2026)**
- Level 2 (Night Time) with unique mechanics
- Solana NFT Profile minting available ($1-5* SOL + network fees)
- Website companion with enhanced leaderboard metrics and player stats
- Global iOS/Android release

**Phase 3: Web3 Expansion (Q4 2026+)**
- Level 3 (Snow) with expanded audio pack ecosystem
- Marketplace foundation and tournament system
- Cross-game character portability (trilogy foundation)

---

## 🎮 Competitive Advantage

1. **Web3 Native** — Leverages Matrica's multi-chain asset verification (Solana, Ethereum, Bitcoin) for cross-blockchain integration
2. **Optional Ownership** — Play free, or mint profile as NFT for portability & permanence
3. **Verified Community** — Discord roles tied to on-chain assets prevent farming and boost trust
4. **Creator-Friendly** — Documented, verifiable progress visible on leaderboards
5. **Trilogy Architecture** — Shared portable profiles across 3 unique games with distinct mechanics
6. **Quality + Indie Ethos** — Hand-crafted pixel art (no AI), solo developer model with community collaboration

---

## 📈 Key Metrics (Target)

- **First Month**: 1K downloads
- **DAU/MAU**: 30% day-1 → 8% 30-day retention
- **Average Session**: 3-11 minutes
- **ARPU**: $2-5/month (energy purchases + cosmetics)
- **NFT Adoption**: 10-15% of players opt to mint profile (optional)

---
## 💬 Pitch Summary

**CTRL+N** is a skill-based mobile action game where each playable character is a keyboard key with a unique audio identity. Players earn 5 free daily matches in the Day-Time environment, then optionally purchase playtime, cosmetics, and audio packs via $SKR. Those seeking permanence can mint their profile as an NFT ($1-5\* SOL/BTC TBA), unlocking leaderboard participation and cross-game portability.

**Core differentiators**: Hand-crafted pixel art, authentic keyboard audio feedback system with unlockable packs, optional Web3 (not mandatory), multi-chain asset verification, and a trilogy of games with distinct mechanics.

**Monetization**: Free-to-play base + energy/cosmetics/audio ($SKR) + optional NFT profiles (SOL).

**Vision**: Web3-ready game built on audio identity and player choice.

---

## 📋 Roadmap

| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| **Soft Launch** | Q2 2026 | Level 1 (Day-Time), Matrica OAuth, Energy system |
| **Global Launch** | Q3 2026 | Level 2 (Night Time), Solana NFT Profiles, Store, Unique abilities |
| **Level 3 Release** | Q4 2026 | Level 3 (Snow), Unique abilities, Swipe mechanics |
| **Level 4 & Ecosystem** | Q1 2027+ | Level 4 (Tron Grid/Miami), Trilogy games, Cross-game portability |

---

## 🎯 Call to Action

**Investors**: Ideally, no seed/investor rounds outside of grants, donations, and in-game purchases
**Partners**: Integrate CTRL+N profile NFTs into your games  
**Players**: Join the beta and mint your first profile NFT 

---

## 📞 Contact

**Website**: celkeys.io (site available, but no game on there yet)
**Email**: celkeys@proton.me
**Twitter**: @CelKeysNFT  
**Discord**: https://discord.gg/ckey (core server gated; game section coming soon)
