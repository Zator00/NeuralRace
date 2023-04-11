import pyglet
import os

width = 1280
height = 720

window = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_DEFAULT, caption='Neural Race')
window.set_size(width, height)

label = pyglet.text.Label('Start Neural Race',
                          font_name ='Times New Roman',
                          font_size = 24,
                          x = 10, y = 10,
                          anchor_x ='left', anchor_y ='bottom')

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()
