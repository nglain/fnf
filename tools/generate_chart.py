#!/usr/bin/env python3
"""
🎵 FNF Chart Auto-Generator
Автоматическая генерация чарта из аудио файла

Использование:
    python generate_chart.py audio.ogg output_chart.json [--bpm 130] [--notes-per-turn 16]

Зависимости:
    pip install librosa numpy
"""

import argparse
import json
import sys

try:
    import librosa
    import numpy as np
except ImportError:
    print("❌ Установите зависимости: pip install librosa numpy")
    sys.exit(1)


def generate_chart(
    audio_path: str,
    output_path: str,
    manual_bpm: float = None,
    notes_per_turn: int = 16,
    quantize_grid: str = "1/8",
    opponent: str = "dad",
    player: str = "bf",
    gf: str = "gf",
    stage: str = "stage",
    scroll_speed: float = 1.6
):
    """
    Генерирует FNF чарт из аудио файла.

    Args:
        audio_path: Путь к аудио файлу (ogg, mp3, wav)
        output_path: Путь для сохранения чарта (json)
        manual_bpm: Ручное указание BPM (если None - автоопределение)
        notes_per_turn: Количество нот до переключения между противником и игроком
        quantize_grid: Сетка квантизации ("1/4", "1/8", "1/16")
        opponent: Имя персонажа-противника
        player: Имя персонажа-игрока
        gf: Имя girlfriend персонажа
        stage: Имя сцены
        scroll_speed: Скорость прокрутки нот
    """

    print("=" * 60)
    print("🎵 FNF CHART AUTO-GENERATOR")
    print("=" * 60)

    # ============ ЗАГРУЗКА АУДИО ============
    print(f"\n📁 Загрузка: {audio_path}")
    y, sr = librosa.load(audio_path)
    duration = len(y) / sr
    print(f"   Длительность: {duration:.1f} сек")
    print(f"   Sample rate: {sr} Hz")

    # ============ РАЗДЕЛЕНИЕ HPSS ============
    print("\n🔊 Спектральное разделение (HPSS)...")
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # ============ ОПРЕДЕЛЕНИЕ ТЕМПА ============
    print("\n⏱️ Определение темпа...")
    onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)

    if manual_bpm:
        tempo_val = manual_bpm
        print(f"   Ручной BPM: {tempo_val}")
    else:
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        tempo_val = float(tempo) if hasattr(tempo, '__float__') else float(tempo[0]) if hasattr(tempo, '__getitem__') else 120.0
        print(f"   Автоопределённый BPM: {tempo_val:.1f}")

    # Расчёт длительностей нот
    beat_ms = 60000 / tempo_val
    grid_divisors = {"1/4": 1, "1/8": 2, "1/16": 4}
    divisor = grid_divisors.get(quantize_grid, 2)
    grid_ms = beat_ms / divisor
    print(f"   Сетка квантизации: {quantize_grid} = {grid_ms:.1f} мс")

    # ============ ДЕТЕКЦИЯ ONSET'ОВ ============
    print("\n🎯 Детекция onset'ов...")

    # На перкуссии
    onset_perc = librosa.onset.onset_detect(
        y=y_percussive, sr=sr,
        wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1,
        units='time'
    )
    print(f"   Перкуссия: {len(onset_perc)} onset'ов")

    # На полном сигнале
    onset_full = librosa.onset.onset_detect(
        y=y, sr=sr,
        wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1,
        units='time'
    )
    print(f"   Полный сигнал: {len(onset_full)} onset'ов")

    # Объединение
    all_onsets = np.unique(np.concatenate([onset_perc, onset_full]))
    all_onsets_ms = all_onsets * 1000
    print(f"   Уникальных: {len(all_onsets_ms)}")

    # ============ КВАНТИЗАЦИЯ ============
    print("\n📐 Квантизация к ритмической сетке...")

    def quantize(time_ms, grid):
        return round(time_ms / grid) * grid

    quantized = []
    for onset_ms in all_onsets_ms:
        q_time = quantize(onset_ms, grid_ms)
        if 0 < q_time < (duration * 1000 - 500):
            quantized.append(q_time)

    quantized = sorted(set(quantized))
    print(f"   После квантизации: {len(quantized)}")

    # ============ ФИЛЬТРАЦИЯ ============
    print("\n🧹 Фильтрация близких нот...")

    min_gap = grid_ms * 0.8
    filtered = [quantized[0]] if quantized else []
    for t in quantized[1:]:
        if t - filtered[-1] >= min_gap:
            filtered.append(t)

    print(f"   После фильтрации: {len(filtered)}")

    # ============ ГЕНЕРАЦИЯ НОТ ============
    print("\n🎮 Генерация нот...")

    patterns = [
        [0, 1, 2, 3],  # L D U R
        [3, 2, 1, 0],  # R U D L
        [0, 2, 1, 3],  # L U D R
        [1, 3, 0, 2],  # D R L U
        [2, 0, 3, 1],  # U L R D
    ]

    notes_opponent = []
    notes_player = []

    current_pattern = 0
    pattern_idx = 0

    for i, time_ms in enumerate(filtered):
        # Смена паттерна каждые 8 нот
        if i % 8 == 0 and i > 0:
            current_pattern = (current_pattern + 1) % len(patterns)
            pattern_idx = 0

        direction = patterns[current_pattern][pattern_idx % 4]
        pattern_idx += 1

        note = {"id": direction, "sLen": 0, "time": int(time_ms), "type": 0}

        # Распределение по notes_per_turn
        if (i // notes_per_turn) % 2 == 0:
            notes_opponent.append(note)
        else:
            notes_player.append(note)

    print(f"   Противник: {len(notes_opponent)} нот")
    print(f"   Игрок: {len(notes_player)} нот")

    # ============ СБОРКА ЧАРТА ============
    print("\n💾 Сохранение чарта...")

    chart = {
        "events": [],
        "strumLines": [
            {
                "visible": True,
                "keyCount": 4,
                "notes": notes_opponent,
                "position": "dad",
                "type": 0,
                "characters": [opponent]
            },
            {
                "visible": True,
                "keyCount": 4,
                "notes": notes_player,
                "position": "boyfriend",
                "type": 1,
                "characters": [player]
            },
            {
                "keyCount": 4,
                "notes": [],
                "visible": False,
                "position": "girlfriend",
                "type": 2,
                "characters": [gf]
            }
        ],
        "scrollSpeed": scroll_speed,
        "chartVersion": "1.6.0",
        "stage": stage,
        "codenameChart": True,
        "noteTypes": []
    }

    with open(output_path, 'w') as f:
        json.dump(chart, f, indent=2)

    print(f"\n✅ Чарт сохранён: {output_path}")
    print(f"   BPM: {tempo_val:.1f}")
    print(f"   Всего нот: {len(notes_opponent) + len(notes_player)}")
    print(f"   Нот за ход: {notes_per_turn}")
    print("=" * 60)

    # Также выводим meta.json
    meta = {
        "displayName": "Generated Song",
        "bpm": round(tempo_val, 1),
        "icon": opponent,
        "color": "#00FF00",
        "coopAllowed": True,
        "opponentModeAllowed": True
    }

    print("\n📋 meta.json (скопируйте):")
    print(json.dumps(meta, indent=2))

    return tempo_val


def main():
    parser = argparse.ArgumentParser(
        description="🎵 FNF Chart Auto-Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s song.ogg chart.json
  %(prog)s song.ogg chart.json --bpm 140
  %(prog)s song.ogg chart.json --notes-per-turn 8 --grid 1/16
  %(prog)s song.ogg chart.json --opponent pico --player bf
        """
    )

    parser.add_argument("audio", help="Путь к аудио файлу (ogg, mp3, wav)")
    parser.add_argument("output", help="Путь для сохранения чарта (json)")
    parser.add_argument("--bpm", type=float, help="Ручное указание BPM")
    parser.add_argument("--notes-per-turn", type=int, default=16, help="Нот до переключения (default: 16)")
    parser.add_argument("--grid", default="1/8", choices=["1/4", "1/8", "1/16"], help="Сетка квантизации")
    parser.add_argument("--opponent", default="dad", help="Персонаж-противник")
    parser.add_argument("--player", default="bf", help="Персонаж-игрок")
    parser.add_argument("--gf", default="gf", help="Girlfriend персонаж")
    parser.add_argument("--stage", default="stage", help="Имя сцены")
    parser.add_argument("--scroll-speed", type=float, default=1.6, help="Скорость прокрутки")

    args = parser.parse_args()

    generate_chart(
        audio_path=args.audio,
        output_path=args.output,
        manual_bpm=args.bpm,
        notes_per_turn=args.notes_per_turn,
        quantize_grid=args.grid,
        opponent=args.opponent,
        player=args.player,
        gf=args.gf,
        stage=args.stage,
        scroll_speed=args.scroll_speed
    )


if __name__ == "__main__":
    main()
