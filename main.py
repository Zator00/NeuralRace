
import pyglet
import os

width = 1280
height = 720

window = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_DEFAULT, caption='Neural Race')
window.set_size(width, height)

start = pyglet.text.Label('Start Neural Race',
                          font_name ='Times New Roman',
                          font_size = 24,
                          x = width/2, y = height/2 + 80,
                          anchor_x ='center', anchor_y ='center')

settings = pyglet.text.Label('Settings',
                          font_name ='Times New Roman',
                          font_size = 24,
                          x = width/2, y = height/2,
                          anchor_x ='center', anchor_y ='center')

exitText = pyglet.text.Label('Exit game',
                          font_name ='Times New Roman',
                          font_size = 24,
                          x = width/2, y = height/2 - 80,
                          anchor_x ='center', anchor_y ='center')

@window.event
def on_draw():
    window.clear()
    start.draw()
    settings.draw()
    exitText.draw()


pyglet.app.run()
