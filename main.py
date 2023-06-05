import pygame as pg
from pygame.math import Vector2
import math
import numpy as np

width = 900
height = 900

pygame_icon = pg.image.load('logo.png')
pg.display.set_icon(pygame_icon)

screen = pg.display.set_mode((width, height))
track_texture = pg.image.load("race_track_v3.png")

# Funkcja do rysowania linii na podstawie parametrów położenia
class Car(pg.sprite.Sprite):
    
    def __init__(self, maxVel, rotationVel):
        super().__init__()
        self.START_POS = (350,630)
        
        #Car init values
        self.maxVel = maxVel
        self.vel = 0
        self.rotationVel = rotationVel
        self.acceleration = 0.1
        self.x, self.y = self.START_POS
        self.moved = False
        
        self.originalImage = pg.image.load('car.png')
        self.rect = self.originalImage.get_rect()
        self.image = self.originalImage
        self.size = self.image.get_size()
        self.rect = self.image.get_rect(center=self.START_POS)
        self.angle = 40
        self.score = 0
        self.key = 0
        
        self.sensorsLengths = [0, 0, 0, 0, 0]
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotationVel
        elif right:
            self.angle -= self.rotationVel

        if screen.get_at((int(self.x-20), int(self.y-20))) == pg.Color(0, 0, 0): #chyba można usunąć ten warunek
            self.vel = 0
            
    def moveForward(self):
        self.moved = True
        if screen.get_at((int(self.x-20), int(self.y-20))) != pg.Color(230,215,150):
            self.vel = min(self.vel + self.acceleration, self.maxVel)
            self.move()
            self.checkCollision()
        else:
            self.vel = 0
        
    def moveBack(self):
        self.moved = True
        self.vel = min(self.vel - self.acceleration, -self.maxVel)
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
        
    def update(self, lines):
        self.moved = False
        self.checkCollision()
        self.checkIfCarIsMoving()
        self.image = pg.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x,self.y))
        offset = Vector2(40, 0)
        offset.rotate_ip(-self.angle-90)
        position = Vector2(self.x+5, self.y) + offset
        
        for i, sensor_placement in enumerate([130, 150, 180, -150, -130]):
            self.sensorsLengths[i] = self.sensors(sensor_placement)
        for line in lines:
            if self.rect.colliderect((line.start[0], line.start[1], line.end[0] - line.start[0], line.end[1] - line.start[1])):
                if line.key - 1 == self.key:
                    self.score += 10
                    self.key = line.key
                    print(self.score)
                    
                # Zatrzymaj samochód, jeśli uderzył w czarną krawędź toru
                elif screen.get_at((int(self.x), int(self.y))) == pg.Color(0, 0, 0):
                    self.vel = 0
        
            
    def checkIfCarIsMoving(self):
        if not self.moved:
            self.reduceSpeed()
        
    def sensors(self, sensorPlacement):
        length = 0
        y = int(self.rect.center[1])
        x = int(self.rect.center[0])
        
        while not screen.get_at((x,y)) == pg.Color(0,0,0) and length < 200:
            length += 1
            x = int(self.rect.center[0] + math.sin(math.radians(self.angle + sensorPlacement)) * length)
            y = int(self.rect.center[1] + math.cos(math.radians(self.angle + sensorPlacement)) * length)
            #print(sensorPlacement," ",length)
            if x >= screen.get_width() - 1 or x <= 1 or y <= 1  or y >= screen.get_height() - 1:
                x = x - 1
                y = y - 1
                break

        pg.draw.line(screen, (255,255,255,255), self.rect.center, (x,y), 1)
        pg.draw.circle(screen, (255,0,255,0), (x,y),3)
        return length
        
    def moveToStart(self):
        self.x, self.y = self.START_POS
        self.vel = 0
    
    def getSensorsLength(self):
        return self.sensorsLengths
    
    def checkCollision(self):
        if screen.get_at((int(self.rect.center[0]-20), int(self.rect.center[1]-20))) == pg.Color(0, 0, 0):
            self.vel = 0
    
class Line(pg.sprite.Sprite):
    def __init__(self, start, end, i):
        super().__init__()
        self.start = start
        self.end = end
        self.key = i

class NeuralRace:
    def __init__(self, w=900, h=900):
        self.w = w
        self.h = h
        self.icon = pg.image.load('logo.png')
        self.display = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.car = pg.sprite.GroupSingle(Car(2,2))
        self.FPS = 60
        self.line_positions = self.load_line_positions('lines.txt')
        self.lines = pg.sprite.Group()
        for i, pos in enumerate(self.line_positions):
            line = Line((pos[0], pos[1]), (pos[2], pos[3]), i)
            self.lines.add(line)
        
        self.score = 0
        
    def draw_lines(self, screen, lines):
     for line in lines:
        pg.draw.line(screen, (0,0,4), line.start, line.end, 2)
        
    def load_line_positions(self, filename):
        positions = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Rozdzielanie linii na poszczególne wartości
                x1, y1, x2, y2 = map(int, line.strip().split(','))
                positions.append((x1, y1, x2, y2))
        return positions
    
    def _update_ui(self):
        self.display.blit(track_texture, (0,0))
        self.draw_lines(self.display, self.lines)
        self.car.draw(self.display)
        self.car.update(self.lines)
        self.score = self.car.sprite.score
        pg.display.update()
        
    def get_state(self):
        return self.car.sprite.getSensorsLength()
    
    def play_step(self, action):
        self.clock.tick(self.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
                return game_over, self.score
        
        if action == -0.5:
            self.car.sprite.rotate(left=True)
                
        elif action == 0.5:
            self.car.sprite.rotate(right=True)
            
        if action == -1:        
            self.car.sprite.moveForward()

        elif action == 1:
            self.car.sprite.moveBack()

        if self.car.sprite.score == 310 or self.car.sprite.vel == 0:
            return True, self.score
            
        self._update_ui()
        return False, self.score

def choose_action(state, q_table):
    if np.random.uniform(0, 1) < 0.1:
        # Wybierz losową akcję
        action = np.random.choice([-1, -0.5, 0, 0.5, 1])
    else:
        # Wybierz akcję na podstawie Q-wartości
        state_index = np.argmax(state)  # Przekształć stan na indeks
        q_values = q_table[state_index]
        action_index = np.argmax(q_values)
        action = [-1, -0.5, 0, 0.5, 1][action_index]
    print(action)
    return action

if __name__ == '__main__':
    env = NeuralRace()
    for episode in range(10000):
        state = env.get_state()
        game_over = False
        score = 0
        q_table = np.zeros((5, 2))
        while not game_over:
            action = choose_action(state, q_table)
            game_over, score = env.play_step(action)
            score = score
        #print(f"Episode: {episode + 1}, Score: {score}")
    print("Training complete!")
    pg.quit()
