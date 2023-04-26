import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import *
from pyglet.gl import *
import math

key = pyglet.window.key

class main(pyglet.window.Window):
    def __init__ (self, width=900, height=900, fps=False, *args, **kwargs):
        super(main, self).__init__(width, height, *args, **kwargs)

        self.mouse = [0,0]
        self.keys = {}
        self.alive = 1

        self.max_speed = 2
        self.carSpeedX = 0
        self.carSpeedY = 0

        car_image = pyglet.image.load('car.png')
        car_image.anchor_x = car_image.width // 2
        car_image.anchor_y = car_image.height // 2
        car_imageX, car_imageY = width/2 - 40, height/2 + 70
        self.car = pyglet.sprite.Sprite(car_image, x=car_imageX, y=car_imageY)
        self.car.scale = 2

        self.track_texture = pyglet.image.load('race_track.png')
        self.background = pyglet.sprite.Sprite(self.track_texture)

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
        self.background.draw()
        self.car.draw()
        self.flip()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse[0] += dx
        self.mouse[1] += dy
        print(x," ",y)
        pass

    def run(self):
        
        
        while self.alive == 1:
            event = self.dispatch_events()

            if key.LEFT in self.keys:
                self.car.rotation -= 1
                
            elif key.RIGHT in self.keys:
                self.car.rotation += 1
                
            if key.UP in self.keys:
                self.carSpeedX = self.max_speed * math.sin(math.radians(self.car.rotation))
                self.carSpeedY = self.max_speed * math.cos(math.radians(self.car.rotation))
                print(self.car.rotation)
            elif key.DOWN in self.keys:
                self.carSpeedX = -self.max_speed * math.sin(math.radians(self.car.rotation))
                self.carSpeedY = -self.max_speed * math.cos(math.radians(self.car.rotation))
            elif mouse.LEFT in self.keys:
                print('COORDINATES: x=')
            
            self.car.x += self.carSpeedX
            self.car.y += self.carSpeedY
            
            region = self.track_texture.get_region(int(self.car.x), int(self.car.y), 1, 1)
            image_data = region.get_image_data()
            pixel_data = image_data.get_data('RGBA', image_data.width * 4)
            if pixel_data == b'\x00\xff\x00\xff':
                self.car.x, self.car.y = self.width/2 - 40, self.height/2 + 70
                self.carSpeedX, self.carSpeedY = 0, 0
            
            self.carSpeedX *= 0.97
            self.carSpeedY *= 0.97
            
            self.render()

if __name__ == '__main__':
    x = main()
    x.run()