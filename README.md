# CtrlN

Fast-paced, skill-based mobile action game. Tap to dodge, compete globally, unlock characters.

Built with Godot 4.6 | Web3-ready with optional Solana NFT profiles | Energy-based free-to-play | Powered by Solana + Matrica

---

## Quick Links

- **Pitch Deck**: [PITCH_DECK.md](PITCH_DECK.md) — Game overview, monetization, roadmap
- **Solana Wallet Integration**: [docs/SOLANA_WALLET_LOGIN.md](docs/SOLANA_WALLET_LOGIN.md) — Architecture & setup
- **Setup Instructions**: [SOLANA_SETUP.md](SOLANA_SETUP.md) — 3-step quick start

---

## Getting Started

### Prerequisites
- Godot 4.6.1.stable
- Python 3.9+ (for desktop version)
- Android SDK for mobile builds
- Solana wallet app (Phantom or Solflare)
  - only needed for native solana wallet login
  - Matrica login is primary, and supports all major wallets across each chain, while offering discord, X, and TG login options as well

### Build

```bash
cd godot
./build-release.sh
```

Output: `ctrln.apk` (mobile) or web build

---

## Features

### Gameplay
- One-button tap mechanics with deep skill ceiling
- Procedurally challenging obstacle escalation
- Real-time global leaderboards
- Unlock characters and achievements

### Monetization
- **Energy System**: 4-5 free matches per session
- **$SKR Store**: In-game cosmetics & playtime purchases
- **Optional NFT**: Mint profile as NFT for $1-3 SOL (portability, permanence)

### Web3 Integration
- **Matrica OAuth**: Multi-chain social login
- **Solana Wallet**: Direct wallet signing via Mobile Wallet Adapter
- **Cross-Chain Assets**: Unlock bonuses by validating Bitcoin/Ethereum NFTs via Matrica
- **Discord**: Rank-based roles verified via multi-chain asset verification

---

## Project Structure

```
CtrlN/
├── godot/                 # Game project (Godot 4.6)
│   ├── scenes/            # .tscn scene files
│   ├── scripts/           # GDScript gameplay logic
│   │   └── autoload/      # Singletons (MatricaAuth, SolanaAuth)
│   └── addons/            # Plugins (SolanaSDK GDExtension)
├── src/                   # Python desktop version (Pygame)
├── CelKeysIO/             # Backend API (Node.js + Vercel)
├── player_data/           # Sample player profiles
├── BuildResources/        # Game design docs & references
└── docs/                  # Technical documentation
```

---

## Development

### Godot Editor Setup
1. Open `godot/project.godot` in Godot 4.6+
2. Go to **Project → Project Settings → Plugins**
3. Enable **SolanaSDK** (if testing wallet login)
4. Scenes live in `godot/scenes/`, scripts in `godot/scripts/`

### Backend Setup
1. Deploy CelKeysIO to Vercel (or local Node.js)
2. Set environment variables (Redis URL, Database connection)
3. Endpoints: `/api/auth/start`, `/api/auth/callback`, `/api/auth/poll`, `/api/auth/wallet/verify`

### Testing
- **Desktop**: Run scenes directly in Godot editor
- **Android**: Build APK and test on device with Phantom/Solflare wallet
- **Web**: Portfolio/metrics dashboard at celkeys.io (coming soon)

---

## Roadmap

| Phase | Timeline | Features |
|-------|----------|----------|
| **Soft Launch** | Q2 2026 | Level 1, Matrica OAuth, Energy system |
| **Global** | Q3 2026 | Level 2, Solana NFT minting, Website |
| **Level 3** | Q4 2026 | Snow environment, Tournament system |
| **Ecosystem** | Q1 2027+ | Level 4, Swipe mechanics, Trilogy games |

---

## License

**GPL-3.0 + Commons Clause**

See [LICENSE](LICENSE) for full details.

**Summary:**
- ✅ Open source: study, modify, contribute
- ✅ Personal use, education, portfolio projects
- ❌ No commercial use: can't sell or monetize derivatives
- ℹ️ Creator retains full commercial rights to CtrlN

**For licensing inquiries**: celkeys@proton.me

---

## Credits

**Developer**: Single developer — game design, programming, player sprites, effects

**Community Artists**: Level backgrounds, environmental design, concept art

Proof-of-concept: indie games can achieve quality production through focused development + collaborative community support.

---

## Contact

- **Website**: [celkeys.io](https://celkeys.io)
- **Email**: celkeys@proton.me
- **Twitter**: [@CelKeysNFT](https://twitter.com/CelKeysNFT)
- **Discord**: Private server (coming at launch)
