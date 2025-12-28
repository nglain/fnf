import flixel.FlxSprite;
import flixel.FlxG;

var purpleStick:FlxSprite;

function onCreate() {
    trace("Creating purple stickman...");

    purpleStick = new FlxSprite(150, 180);
    purpleStick.frames = Paths.getSparrowAtlas("characters/purplestick");

    if (purpleStick.frames != null) {
        purpleStick.animation.addByPrefix("idle", "purplestick idle", 12, true);
        purpleStick.animation.addByPrefix("singLEFT", "purplestick singLEFT", 24, false);
        purpleStick.animation.addByPrefix("singDOWN", "purplestick singDOWN", 24, false);
        purpleStick.animation.addByPrefix("singUP", "purplestick singUP", 24, false);
        purpleStick.animation.addByPrefix("singRIGHT", "purplestick singRIGHT", 24, false);
        purpleStick.animation.play("idle");
        purpleStick.scrollFactor.set(1, 1);
        purpleStick.antialiasing = true;
        purpleStick.scale.set(0.9, 0.9);
        purpleStick.updateHitbox();

        // Add behind boyfriend but in front of stage
        PlayState.instance.insert(PlayState.instance.members.indexOf(PlayState.instance.boyfriendGroup), purpleStick);
        trace("Purple stickman created at x=150!");
    } else {
        trace("ERROR: Could not load purplestick frames!");
    }
}

function opponentNoteHit(note) {
    if (purpleStick != null && purpleStick.animation != null) {
        switch(note.noteData) {
            case 0: purpleStick.animation.play("singLEFT", true);
            case 1: purpleStick.animation.play("singDOWN", true);
            case 2: purpleStick.animation.play("singUP", true);
            case 3: purpleStick.animation.play("singRIGHT", true);
        }
    }
}

function onBeatHit() {
    if (purpleStick != null && purpleStick.animation != null && purpleStick.animation.curAnim != null) {
        if (purpleStick.animation.curAnim.finished) {
            purpleStick.animation.play("idle", true);
        }
    }
}
