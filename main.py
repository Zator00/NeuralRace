
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import *
from pyglet.gl import *

key = pyglet.window.key

class main(pyglet.window.Window):
    def __init__ (self, width=800, height=600, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)

        self.keys = {}
        self.alive = 1
        
        car_image = pyglet.image.load('car.png')
        car_image.anchor_x = car_image.width // 2
        car_image.anchor_y = car_image.height // 2
        car_imageX, car_imageY = width/2, height/2
        self.car = pyglet.sprite.Sprite(car_image, x=car_imageX, y=car_imageY)
        self.car.scale = 3

    def on_draw(self):
        self.render()

    def on_close(self):
        self.alive = 0

    def on_key_release(self, symbol, modifiers):
        try:
            del self.keys[symbol]
        except:
            pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            self.alive = 0
        if symbol == key.O:
            for i in self.keys:
                print(i)
        self.keys[symbol] = True

    def render(self):
        self.clear()
        self.car.draw()
        self.flip()

    def run(self):
        while self.alive == 1:
            event = self.dispatch_events()
            if key.A in self.keys and key.W in self.keys: #todo change from if to smth else to make controls work properly
                print('sdawd')
                self.car.position = [self.car.position[0] - 1, self.car.position[1] + 1, self.car.position[2]]
            if key.A in self.keys:
                self.car.position = [self.car.position[0] - 1, self.car.position[1], self.car.position[2]]
                self.car.rotation = 270
            elif key.W in self.keys:
                self.car.position = [self.car.position[0], self.car.position[1] + 1, self.car.position[2]]
                self.car.rotation = 0
            elif key.S in self.keys:
                self.car.position = [self.car.position[0], self.car.position[1] - 1, self.car.position[2]]
                self.car.rotation = 180
            elif key.D in self.keys:
                self.car.position = [self.car.position[0] + 1, self.car.position[1], self.car.position[2]]
                self.car.rotation = 90
            elif mouse.LEFT in self.keys:
                print('COORDINATES: x=')

            self.render()

if __name__ == '__main__':
    x = main()
    x.run()