import flixel.FlxSprite;
import flixel.FlxG;
import flixel.text.FlxText;

var minecraftBg:FlxSprite;
var matrixBg:FlxSprite;
var timerText:FlxText;
var matrixActive:Bool = false;
var matrixCreated:Bool = false;

// Тайминги (в миллисекундах)
var MATRIX_START:Float = 93000;  // 1:33
var MATRIX_END:Float = 155000;   // 2:35

function onCreate() {
    // Получаем Minecraft фон
    minecraftBg = PlayState.instance.stage.getNamedProp("bg");
    
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
        if (!matrixActive) {
            // Создаём матрицу если ещё не создана
            if (!matrixCreated) {
                matrixBg = new FlxSprite(-300, -200);
                matrixBg.frames = Paths.getSparrowAtlas("stages/daniel/intro_anim");
                matrixBg.animation.addByPrefix("idle", "intro", 10, true);
                matrixBg.scrollFactor.set(0.8, 0.8);
                matrixBg.scale.set(1.0, 1.0);
                PlayState.instance.insert(0, matrixBg);
                matrixCreated = true;
            }
            
            // Включаем Matrix
            minecraftBg.visible = false;
            matrixBg.visible = true;
            matrixBg.animation.play("idle");
            matrixActive = true;
        }
    } else {
        if (matrixActive) {
            // Возвращаем Minecraft
            if (matrixBg != null) {
                matrixBg.visible = false;
            }
            minecraftBg.visible = true;
            matrixActive = false;
        }
    }
}
