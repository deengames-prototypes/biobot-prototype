from game import Game

def quit_event(event):
    Game.instance.save_manager.save()
    exit()


def mousemotion_event(event):
    Game.instance.auto_target = False
    Game.instance.mouse_coord = event.cell