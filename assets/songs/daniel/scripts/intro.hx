import flixel.FlxSprite;
import flixel.FlxG;
import flixel.util.FlxTimer;

function onCreate() {
    // Создаём анимированный спрайт для интро
    var intro = new FlxSprite(-200, -100);
    intro.frames = Paths.getSparrowAtlas('stages/daniel/intro_anim');
    
    // Добавляем анимацию из всех кадров
    intro.animation.addByPrefix('play', 'intro', 10, false);
    intro.scale.set(1.2, 1.2);
    intro.updateHitbox();
    intro.scrollFactor.set(0, 0); // Фиксированная позиция
    
    PlayState.instance.add(intro);
    intro.animation.play('play');
    
    // Удаляем после проигрывания
    new FlxTimer().start(2.0, function(timer) {
        intro.destroy();
    });
}
