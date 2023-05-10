import pygame as pg
import math

width = 900
height = 900

screen = pg.display.set_mode((width, height))
track_texture = pg.image.load("race_track_v2.png")

class Car(pg.sprite.Sprite):
    
    def __init__(self, maxVel, rotationVel):
        super().__init__()
        self.START_POS = (400,400)
        
        #Car init values
        self.maxVel = maxVel
        self.vel = 0
        self.rotationVel = rotationVel
        self.angle = 0
        self.acceleration = 0.1
        self.x, self.y = self.START_POS
        
        self.originalImage = pg.image.load('car.png')
        self.image = self.originalImage
        self.size = self.image.get_size()
        self.rect = self.image.get_rect(center=self.START_POS)
        self.angle = 0
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotationVel
        elif right:
            self.angle -= self.rotationVel
            
    def moveForward(self):
        self.vel = min(self.vel + self.acceleration, self.maxVel)
        self.move()
        
    def moveBack(self):
        self.vel = max(self.vel - self.acceleration, -self.maxVel)
        self.move()
        
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
        
    def reduceSpeed(self):
        self.vel = max(self.vel - self.acceleration/2,0)
        self.move()
        
    def update(self):
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x,self.y))
        for sensor_placement in (130, 150, 180, -150, -130):
            self.sensors(sensor_placement)
        self.collision()
            
    def collision(self):
        pass
        
    def sensors(self, sensorPlacement):
        length = 0
        y = int(self.rect.center[1])
        x = int(self.rect.center[0])
        
        while not screen.get_at((x,y)) == pg.Color(0,0,0) and length < 200:
            length += 1
            x = int(self.rect.center[0] + math.sin(math.radians(self.angle + sensorPlacement)) * length)
            y = int(self.rect.center[1] + math.cos(math.radians(self.angle + sensorPlacement)) * length)
            #print(sensorPlacement," ",length)
            if screen.get_at((x,y)) == pg.Color(0,255,0):
                self.moveToStart()
            if x >= screen.get_width() - 1 or x <= 1 or y <= 1  or y >= screen.get_height() - 1:
                x = x - 1
                y = y - 1
                break
            
        pg.draw.line(screen, (255,255,255,255), self.rect.center, (x,y), 1)
        pg.draw.circle(screen, (255,0,255,0), (x,y),3)
        
    def moveToStart(self):
        self.x, self.y = self.START_POS
        self.vel = 0

def game():
    run = True
    car = pg.sprite.GroupSingle(Car(2,2))
    FPS = 60
    clock = pg.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                    
        screen.blit(track_texture, (0,0))

        keys = pg.key.get_pressed()
        moved = False

        if keys[pg.K_LEFT]:
            car.sprite.rotate(left=True)
                
        elif keys[pg.K_RIGHT]:
            car.sprite.rotate(right=True)
            
        if keys[pg.K_UP]:
            moved = True
            car.sprite.moveForward()
            
        elif keys[pg.K_DOWN]:
            moved = True
            car.sprite.moveBack()
            
        if not moved:
            car.sprite.reduceSpeed()
        
        car.draw(screen)
        car.update()
        pg.display.update()
    pg.quit()

game()