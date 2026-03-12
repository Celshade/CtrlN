# CtrlN

Fast-paced, skill-based mobile action game with hand-crafted pixel art - developed with a passion for indie games and code itself [🐍]. Tap to dodge, swipe to [TBA], compete against your fellow degens, unlock new characters (keys), flex your rank roles in the community, and have fun!

Built with Python 3.12 + Godot 4.6 | Web3-ready with optional Solana + Bitcoin ordinal (coming soon) profiles | Energy-based free-to-play | Powered by Solana + Bitcoin + **Matrica**

![Godot](https://img.shields.io/badge/Godot-4.6-478CBF?logo=godotengine&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)
![Platform](https://img.shields.io/badge/Platform-Android-3DDC84?logo=android&logoColor=white)
![Solana](https://img.shields.io/badge/Solana-14F195?logo=solana&logoColor=black)
![Bitcoin](https://img.shields.io/badge/Bitcoin-Ordinals-F7931A?logo=bitcoin&logoColor=white)
![License](https://img.shields.io/badge/License-GPL--3.0%20%2B%20Commons%20Clause-purple)

---

## 🚀 [Download v0.1.0 Demo](https://github.com/Celshade/CtrlN/releases/tag/v0.1.0-demo)

**Playable Android demo** with Matrica login. [See what's included →](https://github.com/Celshade/CtrlN/releases/tag/v0.1.0-demo)

### 🚧 Early-Stage Development

This project is actively under development and not yet available in app stores. All releases (including demos) are maintained on the [GitHub Releases page](https://github.com/Celshade/CtrlN/releases).

Licensed under **GPL-3.0 + Commons Clause**. Permitted uses:
- ✅ Personal play & testing
- ✅ Educational projects & portfolios
- ✅ Contributing improvements to this repository
- ❌ Commercial use or selling derivatives

See [LICENSE](LICENSE) for full terms.

---

## Quick Links

- **Pitch Deck**: [PITCH_DECK.md](PITCH_DECK.md) — Game overview, monetization, roadmap
- **Solana Wallet Integration**: [docs/SOLANA_WALLET_LOGIN.md](docs/SOLANA_WALLET_LOGIN.md) — Architecture & setup
- **Setup Instructions**: [SOLANA_SETUP.md](SOLANA_SETUP.md) — 3-step quick start

---

## Getting Started

### Try the Demo (Easiest)

Download the latest release from the [Releases page](https://github.com/Celshade/CtrlN/releases) and install `ctrln.apk` on Android 8+.

### Build from Source (Developers)

**Prerequisites:**
- Godot 4.6.1.stable
- Android SDK for mobile builds
- Python 3.12+ (optional, for desktop testing)
- Optional: Phantom or Solflare wallet app for testing Solana authentication

**Build Steps:**

```bash
cd godot
./build-release.sh
```

Output: `ctrln.apk` (Android)

---

## Features

### Gameplay
- One-button tap mechanics with deep skill ceiling
- Procedurally challenging obstacle escalation
- Real-time global leaderboards
- Unlock characters and achievements

### Monetization
- **Energy System**: 4-5 free matches per session (demo is open play)
- **$SKR Store**: In-game cosmetics, playtime (energy), action-item purchases
- **Optional NFT**: Mint profile as NFT portability, permanence, and bonuses

### Web3 Integration
- **Matrica OAuth**: Multi-chain social login
  - includes all major web3 wallets (including native solana mobile wallet)
  - includes social login via discord, x, and tg
- **Solana Wallet**: Direct wallet signing via Mobile Wallet Adapter (coming soon)
- **Cross-Chain Assets**: Unlock bonuses by validating Bitcoin/Ethereum NFTs via Matrica (coming soon)
- **Discord**: Rank-based roles verified via multi-chain asset verification (coming soon)

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
├── player_data/           # Sample player profiles (Pygame)
└── docs/                  # Technical documentation
```

---

## Development

### Godot Editor Setup
1. Open `godot/project.godot` in Godot 4.6+
2. Go to **Project → Project Settings → Plugins**
3. Enable **SolanaSDK** (if testing wallet login)
4. Scenes live in `godot/scenes/`, scripts in `godot/scripts/`


### Testing
- **Demo**: Download the latest release from [Releases](https://github.com/Celshade/CtrlN/releases)
- **Desktop**: Run scenes directly in Godot editor or call `main.py` with a python setup
- **Android**: Build APK and test on device with any web3 wallet/social login
- **Web**: Portfolio/metrics dashboard at celkeys.io (coming soon)

---

## Roadmap

| Phase | Timeline | Features |
|-------|----------|----------|
| **Soft Launch** | Q2 2026 | Level 1 (Day-Time), Matrica OAuth, Energy system |
| **Global Launch** | Q3 2026 | Level 2 (Night Time), Solana NFT Profiles, Store, Unique abilities |
| **Level 3** | Q4 2026 | Level 3 (Snow), Unique abilities, Swipe mechanics |
| **Level 4+ Ecosystem** | Q1 2027+ | Level 4 (Tron Grid/Miami), Trilogy games, Cross-game portability |

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

**Developer**: Celshade — game design, programming, player sprites/effects and animation, UI design, infra, marketing, collabs, community admin

**Community Artists**:
- **Psy** — Level background and obstacle art/animation
- **MomoBones** — Concept and logo art

_<3 indie games_

---

## Contact

- **Website**: [celkeys.io](https://celkeys.io)
- **Email**: celkeys@proton.me
- **X**: [@CelKeysNFT](https://x.com/CelKeysNFT)
- **Discord**: Private server (coming at launch)
