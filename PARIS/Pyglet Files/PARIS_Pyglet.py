import pyglet,os
from PARIS_Pyglet_Objs import *

window = pyglet.window.Window()
event_loop = pyglet.app.EventLoop()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')



@window.event
def on_key_press(symbol, modifiers):
    for dog in mainPool:
        dog.posUpdate(symbol)

@window.event
def on_draw():
    window.clear()
    for dog in mainPool:
        dog.draw()
    label.draw()

@window.event
def on_window_close(window):
    event_loop.exit()

def initMainPool():
        for path, dirs, files in os.walk("FakePool"):
            for file in files:
                if file == '.DS_Store': pass
                else:
                    mainPool.add(Stimulus(file,os.path.join(path,file)))

mainPoolPaths = set()
mainPool = set()


initMainPool()
pyglet.app.run()

def main():
    game = InfantAttentionApp()
    game.run()

if __name__ == '__main__':
    main()






