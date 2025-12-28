# 🎮 FNF Custom Content - WEEK D (DANIEL)

Custom content for Friday Night Funkin' (Codename Engine)

## Features

- **Song**: DANIEL (129.2 BPM, 3:07 duration)
- **Characters**: Green Stick (opponent), BF (player), GF
- **Stage**: Minecraft Forest + Dynamic Matrix animation (1:33-2:35)
- **Timer**: On-screen song timer

## 📚 Documentation

**Start here:** [`docs/FNF_CUSTOM_CONTENT_GUIDE.md`](docs/FNF_CUSTOM_CONTENT_GUIDE.md)

| Document | Description |
|----------|-------------|
| [FNF_CUSTOM_CONTENT_GUIDE.md](docs/FNF_CUSTOM_CONTENT_GUIDE.md) | Complete guide: characters, stages, weeks, songs |
| [ARROW_SYNC_METHODOLOGY.md](docs/ARROW_SYNC_METHODOLOGY.md) | Audio analysis algorithm for note synchronization |

### Quick Links

- **Characters**: How to create custom characters from images
- **Stages**: Background setup, parallax, dynamic switching
- **Songs**: Audio files, meta.json, chart format
- **Arrows/Notes**: librosa-based onset detection and quantization

## Installation

1. Download [Codename Engine](https://github.com/CodenameCrew/CodenameEngine/releases) for your platform
2. Copy contents of `assets/` folder to game's `assets/` folder
3. Add `daniel` to `data/config/freeplaySonglist.txt`
4. Play **WEEK D** in Story Mode or **DANIEL** in Freeplay

## Project Structure

```
fnf/
├── docs/                          # 📚 Documentation
│   ├── FNF_CUSTOM_CONTENT_GUIDE.md   # Complete guide
│   └── ARROW_SYNC_METHODOLOGY.md     # Arrow sync algorithm
├── assets/                        # 🎮 Game assets
│   ├── songs/daniel/                 # Song files
│   │   ├── song/Inst.ogg
│   │   ├── meta.json
│   │   ├── charts/normal.json
│   │   └── scripts/background_switch.hx
│   ├── data/
│   │   ├── stages/daniel.xml
│   │   └── weeks/weeks/daniel.xml
│   └── images/
│       ├── stages/daniel/            # Backgrounds
│       ├── characters/               # Character sprites
│       └── icons/                    # Health bar icons
├── tools/                         # 🔧 Python tools
│   ├── create_character.py          # Character generator
│   └── generate_chart.py            # Chart generator
└── audio_analysis.*               # 📊 Audio analysis results
```

## Tools

### Create Character from Image

```bash
python tools/create_character.py image.png character_name --output assets
```

### Generate Chart from Audio

```bash
python tools/generate_chart.py audio.ogg chart.json --bpm 130 --grid 1/8
```

## Audio Sync Algorithm

Uses librosa for precise note synchronization:

1. **HPSS** - Harmonic-Percussive separation
2. **BPM Detection** - 3 methods, median selection
3. **Onset Detection** - Musical event detection
4. **Quantization** - Snap to rhythmic grid
5. **Pattern Generation** - Direction patterns

See [ARROW_SYNC_METHODOLOGY.md](docs/ARROW_SYNC_METHODOLOGY.md) for details.

## Credits

- **Codename Engine** by CodenameCrew
- **Audio Analysis**: librosa library
- **Song**: DANIEL from YouTube
