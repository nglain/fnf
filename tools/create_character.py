#!/usr/bin/env python3
"""
👤 FNF Character Creator
Создание персонажа из одной картинки

Использование:
    python create_character.py image.png character_name [--player] [--gf] [--color "#FF0000"]

Зависимости:
    pip install pillow numpy
"""

import argparse
import os
import sys

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("❌ Установите зависимости: pip install pillow numpy")
    sys.exit(1)


def create_character(
    image_path: str,
    name: str,
    output_dir: str,
    is_player: bool = False,
    is_gf: bool = False,
    color: str = "#00FF00",
    height: int = 400
):
    """
    Создаёт FNF персонажа из одной картинки.

    Args:
        image_path: Путь к исходной картинке
        name: Имя персонажа (латиницей, без пробелов)
        output_dir: Папка assets игры
        is_player: True если это играбельный персонаж
        is_gf: True если это girlfriend (танцует на фоне)
        color: Цвет темы в формате #RRGGBB
        height: Высота персонажа в пикселях
    """

    print("=" * 60)
    print(f"👤 FNF CHARACTER CREATOR")
    print(f"   Персонаж: {name}")
    print(f"   Тип: {'Игрок' if is_player else 'GF' if is_gf else 'Противник'}")
    print("=" * 60)

    # ============ ЗАГРУЗКА ИЗОБРАЖЕНИЯ ============
    print(f"\n📁 Загрузка: {image_path}")
    img = Image.open(image_path).convert('RGBA')
    print(f"   Размер: {img.size}")

    # ============ УДАЛЕНИЕ ФОНА ============
    print("\n🧹 Удаление фона...")
    data = np.array(img)

    # Удаление белого/светлого фона
    light_mask = (data[:,:,0] > 240) & (data[:,:,1] > 240) & (data[:,:,2] > 240)
    removed_pixels = np.sum(light_mask)
    data[light_mask, 3] = 0
    img = Image.fromarray(data)
    print(f"   Удалено пикселей: {removed_pixels}")

    # ============ МАСШТАБИРОВАНИЕ ============
    print(f"\n📐 Масштабирование до высоты {height}px...")
    scale = height / img.height
    new_size = (int(img.width * scale), height)
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    print(f"   Новый размер: {img.size}")

    # ============ ГЕНЕРАЦИЯ АНИМАЦИЙ ============
    print("\n🎬 Генерация анимаций...")

    def tilt(img, angle):
        return img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(0,0,0,0))

    if is_gf:
        # GF: только танцевальные анимации
        frames = [
            tilt(img, 5),   # danceLeft
            tilt(img, -5),  # danceRight
        ]
        anim_names = ['dance0000', 'dance0001']
    else:
        # Обычный персонаж: idle + sing
        idle2 = img.resize((img.width, int(img.height * 0.97)), Image.Resampling.LANCZOS)
        idle2_padded = Image.new('RGBA', img.size, (0, 0, 0, 0))
        idle2_padded.paste(idle2, (0, int(img.height * 0.03)))

        frames = [
            img,                    # idle0
            idle2_padded,           # idle1
            tilt(img, 10),          # singLEFT
            img.resize((int(img.width * 1.08), int(img.height * 0.90)), Image.Resampling.LANCZOS),  # singDOWN
            img.resize((int(img.width * 0.92), int(img.height * 1.08)), Image.Resampling.LANCZOS),  # singUP
            tilt(img, -10),         # singRIGHT
        ]
        anim_names = ['idle0000', 'idle0001', 'singLEFT0000', 'singDOWN0000', 'singUP0000', 'singRIGHT0000']

    print(f"   Создано фреймов: {len(frames)}")

    # ============ СОЗДАНИЕ СПРАЙТ-ЛИСТА ============
    print("\n🖼️ Создание спрайт-листа...")

    fw = max(f.width for f in frames) + 10
    fh = max(f.height for f in frames) + 10
    cols = 3 if not is_gf else 2
    rows = 2 if not is_gf else 1

    sheet = Image.new('RGBA', (fw * cols, fh * rows), (0, 0, 0, 0))

    for i, frame in enumerate(frames):
        x = (i % cols) * fw + (fw - frame.width) // 2
        y = (i // cols) * fh + (fh - frame.height) // 2
        sheet.paste(frame, (x, y), frame)

    print(f"   Размер листа: {sheet.size}")

    # ============ СОХРАНЕНИЕ СПРАЙТ-ЛИСТА ============
    chars_dir = os.path.join(output_dir, "images/characters")
    os.makedirs(chars_dir, exist_ok=True)

    sheet_path = os.path.join(chars_dir, f"{name}.png")
    sheet.save(sheet_path)
    print(f"\n💾 Спрайт-лист: {sheet_path}")

    # ============ XML АНИМАЦИЙ ============
    xml_lines = ['<?xml version="1.0" encoding="utf-8"?>', f'<TextureAtlas imagePath="{name}.png">']
    for i, anim_name in enumerate(anim_names):
        x = (i % cols) * fw
        y = (i // cols) * fh
        xml_lines.append(f'    <SubTexture name="{name} {anim_name}" x="{x}" y="{y}" width="{fw}" height="{fh}"/>')
    xml_lines.append('</TextureAtlas>')

    xml_path = os.path.join(chars_dir, f"{name}.xml")
    with open(xml_path, 'w') as f:
        f.write('\n'.join(xml_lines))
    print(f"💾 XML анимаций: {xml_path}")

    # ============ CHARACTER XML ============
    data_dir = os.path.join(output_dir, "data/characters")
    os.makedirs(data_dir, exist_ok=True)

    if is_gf:
        char_xml = f'''<!DOCTYPE codename-engine-character>
<character y="0" sprite="{name}" flipX="false" isPlayer="false" isGF="true" icon="{name}" color="{color}" scrollFactor="0.95">
    <anim name="danceLeft" anim="{name} dance" indices="0" fps="12" loop="false"/>
    <anim name="danceRight" anim="{name} dance" indices="1" fps="12" loop="false"/>
</character>'''
    else:
        char_xml = f'''<!DOCTYPE codename-engine-character>
<character y="350" sprite="{name}" flipX="{'true' if is_player else 'false'}" isPlayer="{'true' if is_player else 'false'}" icon="{name}" color="{color}">
    <anim name="idle" anim="{name} idle" fps="12" loop="true"/>
    <anim name="singUP" anim="{name} singUP" fps="24" loop="false"/>
    <anim name="singLEFT" anim="{name} singLEFT" fps="24" loop="false"/>
    <anim name="singRIGHT" anim="{name} singRIGHT" fps="24" loop="false"/>
    <anim name="singDOWN" anim="{name} singDOWN" fps="24" loop="false"/>
</character>'''

    char_xml_path = os.path.join(data_dir, f"{name}.xml")
    with open(char_xml_path, 'w') as f:
        f.write(char_xml)
    print(f"💾 Character XML: {char_xml_path}")

    # ============ ИКОНКА ============
    icons_dir = os.path.join(output_dir, "images/icons")
    os.makedirs(icons_dir, exist_ok=True)

    icon_size = 150
    icon = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    icon_sheet = Image.new('RGBA', (icon_size * 2, icon_size), (0, 0, 0, 0))
    icon_sheet.paste(icon, (0, 0), icon)

    # Losing state
    losing_data = np.array(icon)
    mask = losing_data[:,:,3] > 0
    losing_data[mask, 0] = np.minimum(255, losing_data[mask, 0].astype(int) + 50).astype(np.uint8)
    losing_data[mask, 1] = np.maximum(0, losing_data[mask, 1].astype(int) - 30).astype(np.uint8)
    losing = Image.fromarray(losing_data)
    icon_sheet.paste(losing, (icon_size, 0), losing)

    icon_path = os.path.join(icons_dir, f"icon-{name}.png")
    icon_sheet.save(icon_path)
    print(f"💾 Иконка: {icon_path}")

    # ============ MENU CHARACTER ============
    menu_dir = os.path.join(output_dir, "images/menus/storymenu/characters")
    os.makedirs(menu_dir, exist_ok=True)

    menu_char = img.resize((200, int(200 * img.height / img.width)), Image.Resampling.LANCZOS)
    menu_path = os.path.join(menu_dir, f"{name}.png")
    menu_char.save(menu_path)

    menu_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<TextureAtlas imagePath="{name}.png">
    <SubTexture name="{name} {'dance' if is_gf else 'idle'}0000" x="0" y="0" width="{menu_char.width}" height="{menu_char.height}"/>
</TextureAtlas>'''

    with open(os.path.join(menu_dir, f"{name}.xml"), 'w') as f:
        f.write(menu_xml)
    print(f"💾 Menu character: {menu_path}")

    # ============ WEEK CHARACTER XML ============
    week_chars_dir = os.path.join(output_dir, "data/weeks/characters")
    os.makedirs(week_chars_dir, exist_ok=True)

    week_char_xml = f'''<!DOCTYPE codename-engine-week-character>
<character sprite="{name}" scale="0.6" flipX="false">
    <anim name="idle" anim="{name} {'dance' if is_gf else 'idle'}" fps="12" loop="true"/>
</character>'''

    with open(os.path.join(week_chars_dir, f"{name}.xml"), 'w') as f:
        f.write(week_char_xml)
    print(f"💾 Week character XML: {week_chars_dir}/{name}.xml")

    print("\n" + "=" * 60)
    print(f"✅ ПЕРСОНАЖ '{name}' СОЗДАН!")
    print("=" * 60)
    print(f"\nИспользование в чарте:")
    print(f'    "characters": ["{name}"]')
    print(f"\nИспользование в неделе:")
    print(f'    chars="{name},bf,gf"')


def main():
    parser = argparse.ArgumentParser(
        description="👤 FNF Character Creator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s character.png mychar
  %(prog)s player.png hero --player
  %(prog)s dancer.png dancer --gf
  %(prog)s enemy.png villain --color "#FF0000"
        """
    )

    parser.add_argument("image", help="Путь к картинке персонажа")
    parser.add_argument("name", help="Имя персонажа (латиницей)")
    parser.add_argument("-o", "--output", default="assets", help="Папка assets (default: assets)")
    parser.add_argument("--player", action="store_true", help="Создать как играбельного персонажа")
    parser.add_argument("--gf", action="store_true", help="Создать как girlfriend (танцует на фоне)")
    parser.add_argument("--color", default="#00FF00", help="Цвет темы (default: #00FF00)")
    parser.add_argument("--height", type=int, default=400, help="Высота персонажа в px (default: 400)")

    args = parser.parse_args()

    create_character(
        image_path=args.image,
        name=args.name,
        output_dir=args.output,
        is_player=args.player,
        is_gf=args.gf,
        color=args.color,
        height=args.height
    )


if __name__ == "__main__":
    main()
