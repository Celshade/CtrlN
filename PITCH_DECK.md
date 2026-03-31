# CtrlN — Pitch Deck

**[Watch the demo on YouTube](https://youtu.be/hiHF5U4OsPU)** — 90-seconds of in-app usage with commentary

## 🎮 The Game

**CtrlN** is a fast-paced, skill-based mobile action game with hand-crafted pixel art — developed with a passion for indie games and code itself. Tap to dodge, compete against your fellow degens, unlock new playable characters (keys), flex your rank roles in the community, and have fun. Swipe mechanics coming soon for advanced maneuvers.

---

## 🎯 Core Concept

- **One-button gameplay**: Simple tap and swipe mechanics, deep skill ceiling
- **Procedurally challenging**: Obstacles escalate in speed and complexity
- **Real-time competition**: Live leaderboards and ranking system
- **Social & Multiplayer**: Rankings, achievements, character cosmetics
- **Multi-chain Engagement**: Launched in the Solana dApp store, but not limited to Solana users.

---

## 🕹️ Gameplay Loop

1. **Select Character** — Choose from a roster of unlockable characters with unique visuals
2. **Play** — Tap to dodge obstacles; higher score = better rank
3. **Compete** — Compare scores against global and friend leaderboards
4. **Progress** — Unlock new characters and achievements through gameplay

---

## ✨ Key Features

### Player Progression
- **Energy System**: 5 free matches per session; Energy regenerates over time or via $SKR purchase
- **Achievement System**: Unlock badges and titles (free + purchasable cosmetics)
- **Character Unlocks**: Earn new playable characters and abilities through gameplay
- **Rank Tiers**: Progress through competitive ranks (Unranked → Bamboo → ... → Diamond)
- **Profile Customization**: Equipped character, avatar, bio (cosmetics via $SKR)
- **Cross-Chain Asset Integration**: Unlock bonuses, characters, and abilities by validating existing NFT traits/assets via Matrica (Ethereum NFTs, Solana collections; Bitcoin Ordinals coming soon)

### Gameplay Evolution (Future Iterations)
- **Swipe Mechanics**: Advanced input system for complex maneuvers
- **Unique Player Abilities**: Character-specific gameplay mechanics and power-ups
- **Level Expansions**: Night Time, Snow, Tron Grid, Miami Bonus (3-4 additional levels planned)

### Social & Engagement
- **Global Leaderboards**: Real-time competitive ranking
- **Friend Rankings**: Compare scores with friends
- **Achievements**: Visible badges and milestones
- **Cosmetics**: Character skins and visual items

### Technical
- **Cross-Platform**: Android (iOS coming Q3 2026) via Godot 4.6
- **Desktop Support**: Python 3.12 + Pygame for development/testing
- **Cloud Saves**: Profile tied to login
  - **Matrica OAuth** (primary): Multi-chain social login (Discord, X, Telegram + all major Web3 wallets -> including native solana mobile wallet)
  - **Solana Wallet Adapter** (secondary): Direct wallet signing via Mobile Wallet Adapter 2.0
- **Energy System**: Tracks playtime, regeneration, and purchases
- **SKR Integration**: In-game store powered by Solana Mobile token
- **Website Companion**: Enhanced leaderboard metrics, detailed player stats, achievement tracking (coming Q3 2026)
- **Instant Restarts**: Quick retry loops for skill development

---

## 🔐 Web3 Integration: Optional Profile NFT Minting

**CtrlN profiles can be optionally minted as NFTs on Solana**, giving players enhanced security and portability:

### Profile NFT Value Proposition

- **Cost**: $1-3 SOL one-time overhead charge (optional)
- **Benefits**:
  - Enhanced security: Profile backed by on-chain assets
  - Portability: Use profile across compatible games
  - Permanence: Leaderboard history immutably stored
  - Composability: Future games can read CtrlN achievements

### What's Stored in Profile NFTs

- **Account Data**
  - Public portfolio (score, rank, cosmetics)
  - Achievements and unlock history
  - Timestamps and progression milestones
  
- **Character Ownership**
  - Equipped character NFT
  - Unlocked character collection
  - Visual metadata (colors, animations)

- **Portability**
  - Players own their profile NFT outright
  - Transferable across games/platforms using blockchain standards
  - Metadata stored on-chain

### Optional NFT Benefits

For players who choose to mint their profile NFT ($1-3 SOL):

✅ **True Ownership** — Profile backed by blockchain  
✅ **Portability** — Use your character across compatible games  
✅ **Permanence** — Leaderboard history immutably recorded  
✅ **Composability** — Future games can read your CtrlN achievements

### Technical Architecture

```
┌─────────────┐
│   Player    │
└──────┬──────┘
       │
       ├─ Login: Matrica OAuth (primary) or Solana Wallet (secondary)
       ├─ Profile created in Redis (10-min cache)
       │
       ├─ Energy System: 5 free matches per session
       ├─ Store: Purchase $SKR for playtime/cosmetics/power-ups
       │
       ├─ [OPTIONAL] Mint Profile as NFT
       │   ├─ Cost: mint/inscription cost + <=$5
       │   ├─ Unlocks: Leaderboard verification, portability, etc
       │   └─ NFT metadata on Solana/Bitcoin blockchain
       │       └─ Character unlocks, achievements, cosmetics
       │
       └─ Leaderboard: Rankings synced with/without NFT
```

---

## 🎨 Visual & Art Direction

- **Minimalist Style**: Clean pixel-art characters and obstacles
- **Responsive Feedback**: Particle effects, screen shake, sound cues
- **Colorful Characters**: Distinct visual personalities (Black Bird, Yellow Bird, etc.)
- **Themed Obstacles**: Procedural trees, platforms, hazards

---

## 👥 Development Team

**CtrlN** was created by a **single developer** with generous support from community artists:

- **Celshade** (Developer): Game design, programming, player sprites, effects and animation, UI design, infrastructure, marketing, partnerships, and community administration
- **Psy** (Artist): Level backgrounds and obstacle art/animation
- **MomoBones** (Artist): Concept art and logo design

**Vision**: Proof-of-concept that indie games can achieve quality production through focused individual development and collaborative community partnerships.

This lean structure allows for rapid iteration while maintaining artistic quality and community involvement.

---

## 🌍 Target Audience

- **Primary**: Casual mobile gamers (18-35) seeking quick, skill-based challenges
- **Secondary**: Mobile game speedrunners and competitive niches
- **Tertiary**: Web3-curious players interested in on-chain profile ownership

---

## 💰 Monetization Strategy

### Core Model: Energy-Based Free-to-Play

- **Base Game**: Free-to-play with energy system
  - 5 matches per session (free playtime)
  - Energy regenerates over time (configurable timers)
  - Optional paid energy/fast-regen via $SKR

### Solana NFT Profiles (Optional, One-Time)

- **Cost**: $1-3 SOL one-time
- **Benefits**: Enhanced security, portability across games, leaderboard verification
- **Not required**: Players can enjoy full game without NFT Profile

### In-Store Purchases ($SKR)

All premium purchases use **$SKR (Solana Mobile Token)**:

- **Cosmetics**: Character skins, effects, avatars
- **Playtime**: Additional energy/matches
- **Power-ups**: Temporary gameplay enhancements
- **Battle Pass** (future): Seasonal cosmetic bundles

---

## 📊 Business Model

```
Revenue Streams:
├─ Energy/Playtime sales ($SKR)
├─ Cosmetics ($SKR)
├─ Power-ups ($SKR)
└─ Solana NFT Profiles (SOL)

Player Lifetime Value (pLTV):
├─ Casual: $0-2 (free players, occasional purchase)
├─ Engaged: $10-30 ($SKR cosmetics + playtime)
└─ Hardcore: $50-200+ (cosmetics + playtime + power-ups + NFT Profiles + marketplace)
```

---

## � Development Status

**Current**: v0.1.0 **Demo** (Public Prototype) — [Download on GitHub Releases](https://github.com/Celshade/CtrlN/releases/tag/v0.1.0-demo)

| Status | Description | Timeline |
|--------|-------------|----------|
| **Demo** (NOW) | Single level, core gameplay, auth integrated. Playable, limited scope proof-of-concept. | March 2026 |
| **Alpha** (v0.2.0+) | Multiple levels, store system, cosmetics. Broader feature set; occasional bugs expected. | April-May 2026 |
| **Beta** (v0.5.0+) | 3/4 levels, full monetization, NFT minting UI. Public testing; save data stable. | June 2026 |
| **Release** (v1.0.0) | Full feature set: 4 levels, tournaments, portability. Production-ready. | Q3 2026 |

---

## �🚀 Go-to-Market

### Phase 1: Soft Launch (Q2 2026)
- Public demo on GitHub Releases
- **Level 1 (Day-Time)**: Launched with Matrica OAuth + Solana wallet login
- **Energy System**: Active (5 free matches per session, regeneration over time or $SKR purchase)
- In-game leaderboards operational
- $SKR cosmetic store operational
- Gather analytics and balance gameplay
- Community feedback integration

### Phase 2: Full Launch (Q3 2026)
- Global iOS/Android release
- **Level 2 (Night Time)**: New environment with unique mechanics
- **Solana NFT Profiles**: Optional minting ($1-3 SOL)
- $SKR in-store purchases (playtime, cosmetics, power-ups)
- **Website companion launch**: Enhanced leaderboard metrics, player stats, achievement profiles
- Leaderboard reset with season 1
- Marketing campaign

### Phase 3: Web3 Expansion (Q4 2026)
- **Level 3 (Snow)**: Third environment released
- Marketplace foundation and trading mechanics
- Tournament system with prize pools
- Cross-game character portability (trilogy foundation)
- DAO governance exploration

---

## 🎮 Competitive Advantage

1. **Web3 Native Progression** — One of the first casual games leveraging Matrica's enterprise-level multi-chain API for cross-blockchain asset integration (Solana, Ethereum, Bitcoin Ordinals, etc.)
2. **Portable Profile** — Players own & transfer their achievement history
3. **Creator-Friendly** — Streamers benefit from documented, verifiable progress
4. **Composable Assets** — Future games can recognize CtrlN achievements
5. **Deep Gameplay** — One-button control doesn't mean shallow mechanics
6. **Trilogy Architecture** — CtrlN is Part 1 of a 3-series; each game plays uniquely with shared profile continuity

---

## 📈 Key Metrics (Target)

- **First Month**: 10K downloads
- **DAU/MAU**: 30% day-1 → 8% 30-day retention
- **Average Session**: 8-12 minutes
- **ARPU**: $2-5/month (energy purchases + cosmetics)
- **NFT Adoption**: 10-15% of players opt to mint profile (optional)

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|------------|
| **Game Engine** | Godot Engine 4.6 |
| **Mobile** | Android (iOS coming) |
| **Desktop** | Python + Pygame |
| **Backend** | Node.js + Vercel |
| **Authentication** | Matrica OAuth + Solana Mobile Wallet Adapter |
| **Blockchain** | Solana + Bitcoin (NFT storage) |
| **Database** | Redis (session), PostgreSQL (analytics) |
| **Wallet Integration** | godot-solana-sdk v1.4.5 GDExtension |

---

## � Community & Discord Integration

**CtrlN Discord Server** provides exclusive community features tied to in-game progress:

### Rank-Based Roles

Players earn Discord roles automatically based on in-game competitive rank:
(These are actual game ranks)

- 🥚 **Unranked** — New players (0-99 XP)
- 🎋 **Bamboo** — Rank 7 (100-499 XP)
- ⚙️ **Iron** — Rank 6 (500-1,499 XP)
- 🥉 **Bronze** — Rank 5 (1,500-2,999 XP)
- 🥈 **Silver** — Rank 4 (3,000-4,999 XP)
- 🥇 **Gold** — Rank 3 (5,000-7,499 XP)
- 💜 **Platinum** — Rank 2 (7,500-9,999 XP)
- 💎 **Diamond** — Rank 1 (10,000+ XP)

### Achievement Badges

Special roles unlocked via gameplay achievements:
(Examples)

- 🔥 **Speedrunner** — Clear 1000 levels
- 💎 **Perfectionist** — Record 50 consecutive flawless runs
- 🏆 **Rank 1** — Reach #1 global leaderboard
- 🎯 **Accumulator** — Unlock all 15 characters
- 🌟 **Achiever** — Complete 20 achievements

### Community Features

- **Leaderboard Integration**: Discord embeds show live global rankings
- **Achievement Notifications**: Announce major milestones in #achievements
- **Role Verification**: Roles automatically sync with in-game profile + on-chain assets verified via Matrica (Solana, Ethereum, Bitcoin, etc.)
- **Exclusive Channels**: High-rank players unlock strategy and competitive channels
- **Community Events**: Seasonal tournaments with Discord-exclusive rewards

### Anti-Sybil Protection

Discord roles are **verified against on-chain assets via Matrica**, which can see across multiple blockchains:

- **Solana**: CtrlN profile NFT + wallet assets
- **Ethereum**: NFT collections, token holdings
- **Bitcoin**: Ordinals inscriptions, token ownership
- **Other chains**: Any asset Matrica supports

This multi-chain asset verification prevents:
- Role farming via fake accounts
- Rank spoofing
- Achievement boosting

Players control role visibility in their privacy settings. Roles sync automatically when on-chain asset ownership changes.

---

## 💬 Pitch Summary

**CtrlN** is a skill-based mobile action game with an energy-based free-to-play model and optional Web3 profile ownership. Players get 4-5 free matches daily in a day-time environment, then can purchase playtime, cosmetics, and power-ups using $SKR (Solana Mobile token). Those who want lasting portfolio permanence can optionally mint their profile as an NFT on SOL or Ordinal on BTC (coming soon), unlocking leaderboard access/participation, and cross-game portability across our trilogy of games.

By combining accessible gameplay with optional Web3 integration and a planned series of unique environments (night time, snow, tron grid, miami), we capture both casual and crypto-native players. Our differentiation: **hand-crafted (no AI)** pixel and concept art, **optional on-chain profiles** (not mandatory), leveraging **Matrica's multi-chain asset verification** for Discord community roles, monetizing through **$SKR in-store purchases**, and building a **portable player identity across a trilogy of games**, each with distinct mechanics and level designs.

**We're building a Web3-ready game that respects player choice: play for free, upgrade optionally.**

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
**Partners**: Integrate CtrlN profile NFTs into your games  
**Players**: Join the beta and own your first profile NFT 

---

## 📞 Contact

**Website**: celkeys.io (site available, but no game on there yet)
**Email**: celkeys@proton.me
**Twitter**: @CelKeysNFT  
**Discord**: (private server until release)
