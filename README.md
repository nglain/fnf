# 🎮 FNF Custom Content - WEEK D (DANIEL)

Custom content for Friday Night Funkin' (Codename Engine)

## Features

- **Song**: DANIEL (129.2 BPM, 3:07 duration)
- **Characters**: Green Stick (opponent), BF (player), GF
- **Stage**: Minecraft Forest background
- **Intro**: Animated Matrix-style intro

## Installation

1. Download [Codename Engine](https://github.com/CodenameCrew/CodenameEngine/releases)
2. Copy `assets/` folder contents to game's `assets/` folder
3. Play WEEK D in Story Mode or DANIEL in Freeplay

## Files Structure

```
assets/
├── songs/daniel/          # Song files
├── data/stages/daniel.xml # Stage config
├── data/weeks/weeks/daniel.xml
├── images/stages/daniel/  # Backgrounds & animations
└── images/characters/     # Character sprites
```

## Tools

- `tools/create_character.py` - Create character from single image
- `tools/generate_chart.py` - Auto-generate chart from audio

## Audio Sync Algorithm

Uses librosa for precise note synchronization:
- HPSS (Harmonic-Percussive Separation)
- Onset detection with quantization
- BPM detection (3 methods)

See `FNF_CUSTOM_CONTENT_GUIDE.md` for full documentation.

## Credits

- Codename Engine by CodenameCrew
- Audio analysis: librosa
