# 🎮 Friday Night Funkin' - Руководство по созданию кастомного контента

## Codename Engine для macOS

**Версия движка:** 1.0.1
**Путь установки:** `/Users/larry/t/game/fnf/CodenameEngine-Build/CodenameEngine.app`
**Ресурсы:** `Contents/Resources/assets/`

---

## 📁 Структура проекта

```
assets/
├── data/
│   ├── characters/          # XML конфигурации персонажей
│   ├── stages/              # XML конфигурации сцен
│   └── weeks/
│       ├── weeks/           # XML файлы недель
│       ├── characters/      # XML персонажей для меню
│       └── weeks.txt        # Порядок недель
├── images/
│   ├── characters/          # Спрайт-листы персонажей
│   ├── icons/               # Иконки для health bar
│   ├── stages/              # Фоны и элементы сцен
│   └── menus/storymenu/
│       ├── weeks/           # Картинки названий недель
│       └── characters/      # Персонажи для меню выбора
└── songs/
    └── [song_name]/
        ├── song/            # Аудио файлы
        │   ├── Inst.ogg     # Инструментал
        │   └── Voices.ogg   # Голоса (опционально)
        ├── charts/          # Чарты (ноты)
        │   ├── easy.json
        │   ├── normal.json
        │   └── hard.json
        └── meta.json        # Метаданные песни
```

---

## 👤 Создание персонажей

### 1. Подготовка изображения

**Требования:**
- Формат: PNG с прозрачным фоном
- Рекомендуемый размер: 300-500px по высоте
- Желательно: отдельные позы или одна картинка для генерации

### 2. Генерация спрайт-листа из одной картинки

```python
from PIL import Image
import numpy as np

# Загрузка и очистка фона
img = Image.open("character.png").convert('RGBA')
data = np.array(img)

# Удаление белого фона
white_mask = (data[:,:,0] > 240) & (data[:,:,1] > 240) & (data[:,:,2] > 240)
data[white_mask, 3] = 0
img_clean = Image.fromarray(data)

# Resize до нужного размера
scale = 400 / img_clean.height
img_resized = img_clean.resize((int(img_clean.width * scale), 400))

# Генерация анимаций
def tilt(img, angle):
    return img.rotate(angle, expand=True, fillcolor=(0,0,0,0))

frames = {
    'idle': [img_resized, img_resized.resize((img_resized.width, int(img_resized.height * 0.97)))],
    'singLEFT': [tilt(img_resized, 10)],
    'singDOWN': [img_resized.resize((int(img_resized.width * 1.08), int(img_resized.height * 0.90)))],
    'singUP': [img_resized.resize((int(img_resized.width * 0.92), int(img_resized.height * 1.08)))],
    'singRIGHT': [tilt(img_resized, -10)],
}

# Сборка спрайт-листа (3x2 сетка)
# ... сохранение в PNG
```

### 3. XML файл анимаций (images/characters/[name].xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<TextureAtlas imagePath="mychar.png">
    <SubTexture name="mychar idle0000" x="0" y="0" width="400" height="450"/>
    <SubTexture name="mychar idle0001" x="400" y="0" width="400" height="450"/>
    <SubTexture name="mychar singLEFT0000" x="800" y="0" width="400" height="450"/>
    <SubTexture name="mychar singDOWN0000" x="0" y="450" width="400" height="450"/>
    <SubTexture name="mychar singUP0000" x="400" y="450" width="400" height="450"/>
    <SubTexture name="mychar singRIGHT0000" x="800" y="450" width="400" height="450"/>
</TextureAtlas>
```

### 4. XML конфигурация персонажа (data/characters/[name].xml)

```xml
<!DOCTYPE codename-engine-character>
<character
    y="350"                    <!-- Вертикальная позиция -->
    sprite="mychar"            <!-- Имя спрайт-листа -->
    flipX="false"              <!-- Отзеркалить по X -->
    isPlayer="false"           <!-- true для игрока, false для противника -->
    isGF="false"               <!-- true для girlfriend позиции -->
    icon="mychar"              <!-- Имя иконки -->
    color="#FF6B00"            <!-- Цвет темы -->
    scrollFactor="0.95">       <!-- Для GF: параллакс -->

    <anim name="idle" anim="mychar idle" fps="12" loop="true"/>
    <anim name="singUP" anim="mychar singUP" fps="24" loop="false"/>
    <anim name="singLEFT" anim="mychar singLEFT" fps="24" loop="false"/>
    <anim name="singRIGHT" anim="mychar singRIGHT" fps="24" loop="false"/>
    <anim name="singDOWN" anim="mychar singDOWN" fps="24" loop="false"/>
</character>
```

### 5. Иконка для Health Bar (images/icons/icon-[name].png)

**Формат:** 300x150 PNG (два кадра по 150x150)
- Левая половина: нормальное состояние
- Правая половина: проигрышное состояние (красноватый оттенок)

### 6. Типы персонажей

| Тип | isPlayer | isGF | Позиция | Анимации |
|-----|----------|------|---------|----------|
| Противник | false | false | Слева | idle, sing* |
| Игрок | true | false | Справа | idle, sing* |
| GF | false | true | Центр/фон | danceLeft, danceRight |

---

## 🎵 Создание песни

### 1. Подготовка аудио

```bash
# Скачивание с YouTube
yt-dlp -x --audio-format vorbis -o "Inst.ogg" "URL"

# Или конвертация существующего файла
ffmpeg -i input.mp3 -c:a libvorbis -q:a 5 Inst.ogg
```

### 2. Структура папки песни

```
songs/mysong/
├── song/
│   └── Inst.ogg          # Обязательно
├── charts/
│   └── normal.json       # Минимум одна сложность
└── meta.json
```

### 3. meta.json

```json
{
    "displayName": "My Song",
    "bpm": 130.0,
    "icon": "opponent-name",
    "color": "#FF6B00",
    "coopAllowed": true,
    "opponentModeAllowed": true
}
```

### 4. Формат чарта (charts/normal.json)

```json
{
    "events": [],
    "strumLines": [
        {
            "visible": true,
            "keyCount": 4,
            "notes": [
                {"id": 0, "sLen": 0, "time": 1000, "type": 0},
                {"id": 1, "sLen": 0, "time": 1500, "type": 0}
            ],
            "position": "dad",
            "type": 0,
            "characters": ["opponent-name"]
        },
        {
            "visible": true,
            "keyCount": 4,
            "notes": [...],
            "position": "boyfriend",
            "type": 1,
            "characters": ["player-name"]
        },
        {
            "keyCount": 4,
            "notes": [],
            "visible": false,
            "position": "girlfriend",
            "type": 2,
            "characters": ["gf-name"]
        }
    ],
    "scrollSpeed": 1.5,
    "chartVersion": "1.6.0",
    "stage": "stage",
    "codenameChart": true,
    "noteTypes": []
}
```

**Направления нот (id):**
- 0 = LEFT
- 1 = DOWN
- 2 = UP
- 3 = RIGHT

**sLen** = длина удержания (в мс), 0 для обычных нот

---

## 🤖 Автогенерация нот

### Установка зависимостей

```bash
pip install librosa numpy
```

### Алгоритм автогенерации

```python
import librosa
import numpy as np
import json

# 1. Загрузка аудио
y, sr = librosa.load("Inst.ogg")

# 2. Разделение на перкуссию и гармонику (ВАЖНО!)
y_harmonic, y_percussive = librosa.effects.hpss(y)

# 3. Определение темпа по перкуссии
onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

# 4. Детекция onset'ов с оптимальными параметрами
onset_times = librosa.onset.onset_detect(
    y=y_percussive,
    sr=sr,
    wait=1,        # Мин. ожидание между onset'ами
    pre_avg=1,     # Усреднение до
    post_avg=1,    # Усреднение после
    pre_max=1,     # Pre-max для peak picking
    post_max=1,    # Post-max для peak picking
    units='time'   # Результат в секундах
)

# 5. Квантизация к ритмической сетке
beat_ms = 60000 / tempo  # Длительность бита в мс
eighth_note_ms = beat_ms / 2  # 1/8 нота

def quantize(time_ms, grid_ms):
    return round(time_ms / grid_ms) * grid_ms

quantized = [quantize(t * 1000, eighth_note_ms) for t in onset_times]
quantized = sorted(set(quantized))

# 6. Фильтрация слишком близких нот
min_gap = eighth_note_ms * 0.8
filtered = [quantized[0]]
for t in quantized[1:]:
    if t - filtered[-1] >= min_gap:
        filtered.append(t)

# 7. Генерация нот с паттернами
notes = []
patterns = [[0,1,2,3], [3,2,1,0], [0,2,1,3], [1,3,0,2]]
for i, time_ms in enumerate(filtered):
    pattern = patterns[(i // 8) % len(patterns)]
    direction = pattern[i % 4]
    notes.append({"id": direction, "sLen": 0, "time": int(time_ms), "type": 0})
```

### Параметры для настройки

| Параметр | Описание | Рекомендация |
|----------|----------|--------------|
| `wait` | Мин. frames между onset'ами | 1-3 |
| `pre_avg, post_avg` | Усреднение для сглаживания | 1 |
| `pre_max, post_max` | Peak picking окно | 1 |
| Квантизация | Сетка для выравнивания | 1/8 или 1/16 ноты |
| `NOTES_PER_TURN` | Нот до переключения | 8-16 |

---

## 🎭 Создание сцены (Stage)

### XML конфигурация (data/stages/[name].xml)

```xml
<!DOCTYPE codename-engine-stage>
<stage
    zoom="0.9"              <!-- Масштаб камеры -->
    name="mystage"
    folder="stages/mystage/"   <!-- Папка с ресурсами -->
    startCamPosY="600"
    startCamPosX="1000">

    <!-- Фоновые элементы (scroll < 1 = параллакс) -->
    <sprite name="bg" x="-600" y="-200" sprite="background" scroll="0.9"/>
    <sprite name="floor" x="-600" y="600" sprite="floor" scroll="0.9"/>

    <!-- Дополнительные элементы -->
    <sprite name="speaker" x="300" y="500" sprite="speaker" scroll="0.95"/>

    <!-- Персонажи -->
    <girlfriend y="80"/>
    <dad/>
    <boyfriend/>

    <!-- Передний план (scroll > 1 = движется быстрее) -->
    <sprite name="curtains" x="-500" y="-300" sprite="curtains" scroll="1.3"/>
</stage>
```

### Атрибуты спрайтов

| Атрибут | Описание |
|---------|----------|
| `x, y` | Позиция |
| `sprite` | Имя файла (без расширения) |
| `scroll` | Параллакс (0.1 = медленно, 1.3 = быстро) |
| `scale` | Масштаб |
| `zoomfactor` | Влияние зума камеры |

---

## 📅 Регистрация недели

### 1. XML недели (data/weeks/weeks/[name].xml)

```xml
<!DOCTYPE codename-engine-week>
<week
    name="MY WEEK"           <!-- Отображаемое имя -->
    chars="opponent,player,gf"   <!-- Персонажи для превью -->
    sprite="myweek"          <!-- Картинка названия -->
    color="FF6B00">          <!-- Цвет темы (без #) -->

    <song>song1</song>
    <song>song2</song>
    <song hide="true">secret_song</song>  <!-- Скрытая песня -->
</week>
```

### 2. Добавление в weeks.txt

```
tutorial
week1
week2
...
myweek    <- добавить в конец
```

### 3. Картинка названия (images/menus/storymenu/weeks/[name].png)

- Размер: ~359x89 px
- Белый текст на прозрачном фоне
- Шрифт: Arial Black или Impact

---

## 🔧 Скрипты и инструменты

### Полный скрипт создания персонажа

```python
#!/usr/bin/env python3
"""
Создание FNF персонажа из одной картинки
Использование: python create_character.py image.png character_name
"""

import sys
from PIL import Image
import numpy as np
import os

def create_character(image_path, name, output_dir):
    # Загрузка и очистка
    img = Image.open(image_path).convert('RGBA')
    data = np.array(img)

    # Удаление белого/светлого фона
    light_mask = (data[:,:,0] > 240) & (data[:,:,1] > 240) & (data[:,:,2] > 240)
    data[light_mask, 3] = 0
    img = Image.fromarray(data)

    # Resize
    scale = 400 / img.height
    img = img.resize((int(img.width * scale), 400), Image.Resampling.LANCZOS)

    # Генерация фреймов
    def tilt(img, angle):
        return img.rotate(angle, expand=True, fillcolor=(0,0,0,0))

    frames = [
        img,  # idle0
        img.resize((img.width, int(img.height * 0.97))),  # idle1
        tilt(img, 10),   # singLEFT
        img.resize((int(img.width * 1.08), int(img.height * 0.90))),  # singDOWN
        img.resize((int(img.width * 0.92), int(img.height * 1.08))),  # singUP
        tilt(img, -10),  # singRIGHT
    ]

    # Спрайт-лист
    fw = max(f.width for f in frames) + 10
    fh = max(f.height for f in frames) + 10
    sheet = Image.new('RGBA', (fw * 3, fh * 2), (0, 0, 0, 0))

    for i, frame in enumerate(frames):
        x = (i % 3) * fw + (fw - frame.width) // 2
        y = (i // 3) * fh + (fh - frame.height) // 2
        sheet.paste(frame, (x, y), frame)

    # Сохранение
    chars_dir = os.path.join(output_dir, "images/characters")
    os.makedirs(chars_dir, exist_ok=True)
    sheet.save(os.path.join(chars_dir, f"{name}.png"))

    # XML анимаций
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
<TextureAtlas imagePath="{name}.png">
    <SubTexture name="{name} idle0000" x="0" y="0" width="{fw}" height="{fh}"/>
    <SubTexture name="{name} idle0001" x="{fw}" y="0" width="{fw}" height="{fh}"/>
    <SubTexture name="{name} singLEFT0000" x="{fw*2}" y="0" width="{fw}" height="{fh}"/>
    <SubTexture name="{name} singDOWN0000" x="0" y="{fh}" width="{fw}" height="{fh}"/>
    <SubTexture name="{name} singUP0000" x="{fw}" y="{fh}" width="{fw}" height="{fh}"/>
    <SubTexture name="{name} singRIGHT0000" x="{fw*2}" y="{fh}" width="{fw}" height="{fh}"/>
</TextureAtlas>'''

    with open(os.path.join(chars_dir, f"{name}.xml"), 'w') as f:
        f.write(xml)

    # Character XML
    data_dir = os.path.join(output_dir, "data/characters")
    os.makedirs(data_dir, exist_ok=True)

    char_xml = f'''<!DOCTYPE codename-engine-character>
<character y="350" sprite="{name}" flipX="false" isPlayer="false" icon="{name}" color="#00FF00">
    <anim name="idle" anim="{name} idle" fps="12" loop="true"/>
    <anim name="singUP" anim="{name} singUP" fps="24" loop="false"/>
    <anim name="singLEFT" anim="{name} singLEFT" fps="24" loop="false"/>
    <anim name="singRIGHT" anim="{name} singRIGHT" fps="24" loop="false"/>
    <anim name="singDOWN" anim="{name} singDOWN" fps="24" loop="false"/>
</character>'''

    with open(os.path.join(data_dir, f"{name}.xml"), 'w') as f:
        f.write(char_xml)

    # Иконка
    icons_dir = os.path.join(output_dir, "images/icons")
    os.makedirs(icons_dir, exist_ok=True)

    icon = img.resize((150, 150), Image.Resampling.LANCZOS)
    icon_sheet = Image.new('RGBA', (300, 150), (0, 0, 0, 0))
    icon_sheet.paste(icon, (0, 0), icon)

    # Losing state (red tint)
    losing_data = np.array(icon)
    mask = losing_data[:,:,3] > 0
    losing_data[mask, 0] = np.minimum(255, losing_data[mask, 0] + 50)
    losing_data[mask, 1] = np.maximum(0, losing_data[mask, 1] - 30)
    losing = Image.fromarray(losing_data)
    icon_sheet.paste(losing, (150, 0), losing)
    icon_sheet.save(os.path.join(icons_dir, f"icon-{name}.png"))

    print(f"✅ Персонаж '{name}' создан!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_character.py image.png character_name")
        sys.exit(1)

    create_character(sys.argv[1], sys.argv[2], "assets")
```

---

## 🎯 Синхронизация стрелок с музыкой (Audio Analysis)

### Теория

Для точной синхронизации нот с музыкой используется анализ аудио:

1. **BPM Detection** - определение темпа песни
2. **Onset Detection** - обнаружение музыкальных событий (удары, ноты)
3. **Quantization** - привязка к ритмической сетке
4. **Offset** - корректировка задержки

### Алгоритм синхронизации

```python
import librosa
import numpy as np

# 1. Загрузка аудио
y, sr = librosa.load('Inst.ogg')
duration = len(y) / sr

# 2. HPSS - разделение на гармонику и перкуссию
y_harmonic, y_percussive = librosa.effects.hpss(y)

# 3. Определение BPM (3 метода для надёжности)
onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
tempo1, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

tempo2, _ = librosa.beat.beat_track(y=y, sr=sr)

tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
tempo3 = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)[0]

BPM = np.median([tempo1, tempo2, tempo3])  # Усреднение

# 4. Расчёт ритмической сетки
beat_ms = 60000 / BPM
grid_1_4 = beat_ms           # Четверть ноты
grid_1_8 = beat_ms / 2       # Восьмая нота
grid_1_16 = beat_ms / 4      # Шестнадцатая нота

# 5. Onset Detection
onsets = librosa.onset.onset_detect(
    y=y_percussive, sr=sr,
    wait=1, pre_avg=1, post_avg=1,
    pre_max=1, post_max=1,
    units='time'
)
onsets_ms = onsets * 1000

# 6. Определение offset (первый onset)
OFFSET_MS = onsets_ms[0] if len(onsets_ms) > 0 else 0

# 7. Квантизация к сетке
def quantize(time_ms, grid, offset):
    adjusted = time_ms - offset
    quantized = round(adjusted / grid) * grid
    return quantized + offset

quantized_notes = [quantize(t, grid_1_8, OFFSET_MS) for t in onsets_ms]
```

### Параметры качества

| Параметр | Рекомендация |
|----------|--------------|
| **BPM** | Проверить 3 методами, взять медиану |
| **Grid** | 1/8 для нормальной сложности, 1/16 для hard |
| **Offset** | Первый onset или ручная подстройка |
| **Min gap** | grid * 0.8-0.9 (фильтрация близких нот) |

### Типы onset detection

```python
# Strict - только чёткие удары (меньше нот)
onsets_strict = librosa.onset.onset_detect(
    y=y_percussive, sr=sr,
    wait=2, pre_avg=2, post_avg=2,
    pre_max=2, post_max=2,
    delta=0.07
)

# Default - баланс
onsets_default = librosa.onset.onset_detect(
    y=y_percussive, sr=sr,
    wait=1, pre_avg=1, post_avg=1,
    pre_max=1, post_max=1
)

# Sensitive - больше нот (для hard)
onsets_sensitive = librosa.onset.onset_detect(
    y=y, sr=sr,  # Полный сигнал
    wait=1, pre_avg=1, post_avg=1,
    pre_max=1, post_max=1,
    delta=0.03
)
```

### Пример реального анализа (DANIEL)

```json
{
  "audio_file": "Inst.ogg",
  "duration_sec": 187.05,
  "tempo": {
    "method1_percussion": 129.2,
    "method2_full": 129.2,
    "method3_tempogram": 129.2,
    "selected": 129.2
  },
  "grid_ms": {
    "1/4": 464.4,
    "1/8": 232.2,
    "1/16": 116.1
  },
  "onsets": {
    "strict_count": 420,
    "default_count": 735,
    "sensitive_count": 808
  },
  "timing": {
    "first_onset_ms": 70.0,
    "recommended_offset_ms": 70.0
  }
}
```

### Генерация паттернов нот

```python
# Направления: 0=LEFT, 1=DOWN, 2=UP, 3=RIGHT
patterns = [
    [0, 1, 2, 3],  # L D U R
    [3, 2, 1, 0],  # R U D L
    [0, 2, 1, 3],  # L U D R
    [1, 3, 0, 2],  # D R L U
    [2, 0, 3, 1],  # U L R D
]

notes = []
pattern_idx = 0
for i, time_ms in enumerate(quantized_notes):
    if i % 8 == 0 and i > 0:
        pattern_idx = (pattern_idx + 1) % len(patterns)

    direction = patterns[pattern_idx][i % 4]
    notes.append({
        "id": direction,
        "sLen": 0,        # Длина удержания (0 = tap)
        "time": int(time_ms),
        "type": 0
    })
```

### Распределение между игроком и противником

```python
NOTES_PER_TURN = 16  # Нот до смены

notes_opponent = []
notes_player = []

for i, note in enumerate(all_notes):
    if (i // NOTES_PER_TURN) % 2 == 0:
        notes_opponent.append(note)
    else:
        notes_player.append(note)
```

### Freeplay Registration

Для добавления песни в Freeplay, добавьте имя песни в:
```
data/config/freeplaySonglist.txt
```

Пример:
```
tutorial
bopeebo
fresh
...
daniel    <- ваша песня
```

---

## 📚 Полезные ссылки

- [Codename Engine GitHub](https://github.com/CodenameCrew/CodenameEngine)
- [librosa Documentation](https://librosa.org/doc/latest/)
- [GameBanana FNF Mods](https://gamebanana.com/games/8694)
- [FNF Chart Visualizer](https://jsm925.github.io/FunkinChart/)

---

## ✅ Чеклист создания контента

### Новый персонаж
- [ ] Картинка с прозрачным фоном
- [ ] Спрайт-лист (`images/characters/name.png`)
- [ ] XML анимаций (`images/characters/name.xml`)
- [ ] Character XML (`data/characters/name.xml`)
- [ ] Иконка (`images/icons/icon-name.png`)
- [ ] Menu character (`images/menus/storymenu/characters/name.png`)
- [ ] Week character XML (`data/weeks/characters/name.xml`)

### Новая песня
- [ ] Аудио файл (`songs/name/song/Inst.ogg`)
- [ ] meta.json (`songs/name/meta.json`)
- [ ] Чарт (`songs/name/charts/normal.json`)
- [ ] Регистрация в неделе

### Новая неделя
- [ ] Week XML (`data/weeks/weeks/name.xml`)
- [ ] Картинка названия (`images/menus/storymenu/weeks/name.png`)
- [ ] Добавить в `weeks.txt`

---

*Документация создана на основе проекта WEEK D с персонажами Green Stick (opponent), BF (player), GF*
*Фон: Minecraft Forest | Audio: DANIEL (129.2 BPM, offset 70ms)*

---

## 🎬 Динамическая смена фонов по времени

### Stage с несколькими фонами

```xml
<!DOCTYPE codename-engine-stage>
<stage zoom="0.9" name="mystage" folder="stages/mystage/">
    <!-- Основной фон (видимый) -->
    <sprite name="bg1" x="0" y="0" sprite="background1" visible="true"/>
    
    <!-- Альтернативный фон (скрытый) -->
    <sprite name="bg2" x="0" y="0" sprite="background2" visible="false">
        <anim name="idle" anim="anim" fps="10" loop="true"/>
    </sprite>
    
    <girlfriend/>
    <dad/>
    <boyfriend/>
</stage>
```

### HScript для переключения (songs/[song]/scripts/background_switch.hx)

```haxe
import flixel.FlxSprite;
import flixel.text.FlxText;

var bg1:FlxSprite;
var bg2:FlxSprite;
var timerText:FlxText;
var bg2Active:Bool = false;

// Тайминги в миллисекундах
var BG2_START:Float = 93000;  // 1:33
var BG2_END:Float = 155000;   // 2:35

function onCreate() {
    bg1 = PlayState.instance.stage.getNamedProp("bg1");
    bg2 = PlayState.instance.stage.getNamedProp("bg2");
    
    // Таймер (опционально)
    timerText = new FlxText(10, 10, 200, "0:00");
    timerText.setFormat(null, 16, 0xFFFFFF, "left");
    timerText.scrollFactor.set(0, 0);
    PlayState.instance.add(timerText);
}

function onUpdate(elapsed:Float) {
    var songPos = Conductor.songPosition;
    
    // Обновляем таймер
    var seconds = Math.floor(songPos / 1000);
    var mins = Math.floor(seconds / 60);
    var secs = seconds % 60;
    timerText.text = mins + ":" + (secs < 10 ? "0" : "") + secs;
    
    // Переключение фонов
    if (songPos >= BG2_START && songPos < BG2_END) {
        if (!bg2Active) {
            bg1.visible = false;
            bg2.visible = true;
            bg2.animation.play("idle");
            bg2Active = true;
        }
    } else if (bg2Active) {
        bg2.visible = false;
        bg1.visible = true;
        bg2Active = false;
    }
}
```

### Конвертация времени

| Формат | Миллисекунды |
|--------|--------------|
| 0:30 | 30000 |
| 1:00 | 60000 |
| 1:33 | 93000 |
| 2:00 | 120000 |
| 2:35 | 155000 |
| 3:00 | 180000 |

**Формула:** `минуты * 60000 + секунды * 1000`
