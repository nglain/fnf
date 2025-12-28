import flixel.FlxSprite;
import flixel.text.FlxText;

var minecraftBg:FlxSprite;
var matrixBg:FlxSprite;
var timerText:FlxText;
var matrixActive:Bool = false;

// Тайминги (в миллисекундах)
var MATRIX_START:Float = 93000;  // 1:33
var MATRIX_END:Float = 155000;   // 2:35

function onCreate() {
    // Получаем спрайты фонов
    minecraftBg = PlayState.instance.stage.getNamedProp("bg");
    matrixBg = PlayState.instance.stage.getNamedProp("matrixBg");
    
    // ПРИНУДИТЕЛЬНО скрываем матрицу в начале
    if (matrixBg != null) {
        matrixBg.visible = false;
        matrixBg.alpha = 0;
    }
    
    // Показываем Minecraft
    if (minecraftBg != null) {
        minecraftBg.visible = true;
        minecraftBg.alpha = 1;
    }
    
    // Создаём таймер
    timerText = new FlxText(10, 10, 200, "0:00");
    timerText.setFormat(null, 16, 0xFFFFFF, "left");
    timerText.scrollFactor.set(0, 0);
    timerText.alpha = 0.7;
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
    if (songPos >= MATRIX_START && songPos < MATRIX_END) {
        if (!matrixActive && matrixBg != null) {
            // Включаем Matrix
            minecraftBg.visible = false;
            minecraftBg.alpha = 0;
            matrixBg.visible = true;
            matrixBg.alpha = 1;
            matrixBg.animation.play("idle");
            matrixActive = true;
        }
    } else {
        if (matrixActive && minecraftBg != null) {
            // Возвращаем Minecraft
            matrixBg.visible = false;
            matrixBg.alpha = 0;
            minecraftBg.visible = true;
            minecraftBg.alpha = 1;
            matrixActive = false;
        }
    }
}
