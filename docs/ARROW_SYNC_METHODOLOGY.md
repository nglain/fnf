# 🎯 Методология синхронизации стрелок с музыкой

## Обзор

Данная методология позволяет автоматически генерировать ноты (стрелки) для FNF, которые точно синхронизированы с музыкой. Основана на аудио-анализе с использованием библиотеки librosa.

## Принцип работы

```
Аудио файл → HPSS разделение → Onset Detection → Квантизация → Ноты
```

### 1. HPSS (Harmonic-Percussive Source Separation)

Разделяем аудио на гармоническую (мелодия) и перкуссивную (ритм) части:

```python
import librosa

y, sr = librosa.load('Inst.ogg')
y_harmonic, y_percussive = librosa.effects.hpss(y)
```

**Зачем:** Перкуссия даёт более чёткие onset'ы для ритм-игры.

### 2. Определение BPM (3 метода)

```python
# Метод 1: По перкуссии
onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
tempo1, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

# Метод 2: По полному сигналу
tempo2, _ = librosa.beat.beat_track(y=y, sr=sr)

# Метод 3: Темпограмма
tempo3 = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)[0]

# Берём медиану для надёжности
BPM = np.median([tempo1, tempo2, tempo3])
```

**Зачем:** Разные методы могут давать разные результаты. Медиана отсекает выбросы.

### 3. Расчёт ритмической сетки

```python
beat_ms = 60000 / BPM  # Длительность четверти в мс

grid = {
    "1/4": beat_ms,           # Четверть нота (easy)
    "1/8": beat_ms / 2,       # Восьмая нота (normal)
    "1/16": beat_ms / 4       # Шестнадцатая (hard)
}
```

| Сложность | Сетка | Пример (130 BPM) |
|-----------|-------|------------------|
| Easy | 1/4 | 461 ms |
| Normal | 1/8 | 231 ms |
| Hard | 1/16 | 115 ms |

### 4. Onset Detection

```python
onsets = librosa.onset.onset_detect(
    y=y_percussive, sr=sr,
    wait=1,        # Минимум 1 фрейм между onset'ами
    pre_avg=1,     # Усреднение до
    post_avg=1,    # Усреднение после
    pre_max=1,     # Локальный максимум до
    post_max=1,    # Локальный максимум после
    units='time'   # Результат в секундах
)

onsets_ms = onsets * 1000  # Конвертируем в миллисекунды
```

**Типы чувствительности:**

| Тип | Параметры | Результат |
|-----|-----------|-----------|
| Strict | wait=2, delta=0.07 | Меньше нот, только чёткие удары |
| Default | wait=1 | Баланс |
| Sensitive | delta=0.03, full signal | Больше нот |

### 5. Определение Offset

```python
# Первый onset = начало музыки
OFFSET_MS = onsets_ms[0] if len(onsets_ms) > 0 else 0
```

**Зачем:** Смещение компенсирует тишину в начале трека.

### 6. Квантизация к сетке

```python
def quantize(time_ms, grid, offset):
    adjusted = time_ms - offset
    quantized = round(adjusted / grid) * grid
    return quantized + offset

quantized_notes = [quantize(t, grid["1/8"], OFFSET_MS) for t in onsets_ms]
```

**Зачем:** Привязывает ноты к ритмической сетке, убирает "плавающие" ноты.

### 7. Фильтрация близких нот

```python
min_gap = grid["1/8"] * 0.9  # 90% от сетки

filtered = [quantized_notes[0]]
for t in quantized_notes[1:]:
    if t - filtered[-1] >= min_gap:
        filtered.append(t)
```

### 8. Генерация паттернов

```python
# Направления: 0=LEFT, 1=DOWN, 2=UP, 3=RIGHT
patterns = [
    [0, 1, 2, 3],  # L D U R
    [3, 2, 1, 0],  # R U D L
    [0, 2, 1, 3],  # L U D R
    [1, 3, 0, 2],  # D R L U
]

notes = []
pattern_idx = 0
for i, time_ms in enumerate(filtered):
    if i % 8 == 0 and i > 0:
        pattern_idx = (pattern_idx + 1) % len(patterns)
    
    direction = patterns[pattern_idx][i % 4]
    notes.append({
        "id": direction,
        "sLen": 0,
        "time": int(time_ms),
        "type": 0
    })
```

### 9. Распределение между игроками

```python
NOTES_PER_TURN = 16  # Нот до смены

notes_opponent = []
notes_player = []

for i, note in enumerate(notes):
    if (i // NOTES_PER_TURN) % 2 == 0:
        notes_opponent.append(note)
    else:
        notes_player.append(note)
```

## Полный пример

```python
#!/usr/bin/env python3
import librosa
import numpy as np
import json

def generate_chart(audio_path, output_path, manual_bpm=None):
    # Загрузка
    y, sr = librosa.load(audio_path)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    # BPM
    onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
    if manual_bpm:
        BPM = manual_bpm
    else:
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        BPM = float(tempo)
    
    grid = 60000 / BPM / 2  # 1/8 нота
    
    # Onset detection
    onsets = librosa.onset.onset_detect(
        y=y_percussive, sr=sr,
        wait=1, pre_avg=1, post_avg=1,
        pre_max=1, post_max=1,
        units='time'
    )
    onsets_ms = onsets * 1000
    
    # Offset и квантизация
    offset = onsets_ms[0] if len(onsets_ms) > 0 else 0
    
    def quantize(t):
        adj = t - offset
        return round(adj / grid) * grid + offset
    
    quantized = sorted(set([quantize(t) for t in onsets_ms]))
    
    # Фильтрация
    min_gap = grid * 0.9
    filtered = [quantized[0]]
    for t in quantized[1:]:
        if t - filtered[-1] >= min_gap:
            filtered.append(t)
    
    # Генерация нот
    patterns = [[0,1,2,3], [3,2,1,0], [0,2,1,3], [1,3,0,2]]
    notes_opp, notes_plr = [], []
    
    for i, t in enumerate(filtered):
        direction = patterns[(i//8) % len(patterns)][i % 4]
        note = {"id": direction, "sLen": 0, "time": int(t), "type": 0}
        
        if (i // 16) % 2 == 0:
            notes_opp.append(note)
        else:
            notes_plr.append(note)
    
    # Сохранение
    chart = {
        "strumLines": [
            {"notes": notes_opp, "position": "dad", "characters": ["opponent"]},
            {"notes": notes_plr, "position": "boyfriend", "characters": ["bf"]},
            {"notes": [], "position": "girlfriend", "characters": ["gf"]}
        ],
        "scrollSpeed": 1.8,
        "stage": "stage"
    }
    
    with open(output_path, 'w') as f:
        json.dump(chart, f, indent=2)
    
    print(f"✅ Создано {len(filtered)} нот, BPM: {BPM}")

if __name__ == "__main__":
    generate_chart("Inst.ogg", "chart.json")
```

## Рекомендации

| Параметр | Easy | Normal | Hard |
|----------|------|--------|------|
| Сетка | 1/4 | 1/8 | 1/16 |
| Onset чувствительность | Strict | Default | Sensitive |
| Нот за ход | 8 | 16 | 32 |
| Scroll Speed | 1.2 | 1.6-1.8 | 2.0-2.5 |

## Инструмент

Готовый скрипт: `tools/generate_chart.py`

```bash
python tools/generate_chart.py audio.ogg chart.json --bpm 130 --grid 1/8
```
