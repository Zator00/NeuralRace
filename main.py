from typing import Any
import pygame
import math
import os
import sys

width = 900
height = 900

screen = pygame.display.set_mode((width, height))
track_texture = pygame.image.load("race_track.png")

class Car(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.original_car = pygame.image.load("car.png")
        self.image = self.original_car
        self.rect = self.image.get_rect(center=(400,400))
        self.angle = 0
        self.driving_status = False
        self.speed_vector = pygame.math.Vector2(0.1,0)
        self.rotation_speed = 0.01
        self.direction = 0
        self.alive = True

        
    def update(self):
        self.drive()
        self.rotation()
        for sensor_placment in (-60, -30, 0, 30, 60):
            self.sensors(sensor_placment)
        self.collision()

    def drive(self):
        if self.driving_status:
            self.rect.center += self.speed_vector * 2
            
    def rotation(self):
        if self.direction == 1:
            self.angle -= self.rotation_speed
            self.speed_vector.rotate_ip(self.rotation_speed)
        if self.direction == -1:
            self.angle += self.rotation_speed
            self.speed_vector.rotate_ip(-self.rotation_speed)
            
        self.image = pygame.transform.rotozoom(self.original_car, self.angle, 1.6)
        self.rect = self.image.get_rect(center=self.rect.center)

    def collision(self):
        length = 12
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle)) * length)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle)) * length)]
        
        if screen.get_at(collision_point_right) == pygame.Color(0, 255, 0, 255) \
                or screen.get_at(collision_point_left) == pygame.Color(0, 255, 0, 255):
            self.alive = False

        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_left, 4) 
        
    def sensors(self, sensor_placment):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        
        while not screen.get_at((x,y)) == pygame.Color(0,255,0,255) and length < 170:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + sensor_placment)) * length)
            y = int(self.rect.center[1] + math.sin(math.radians(self.angle + sensor_placment)) * length)
            
        pygame.draw.line(screen, (255,255,255,255), self.rect.center, (x,y), 1)
        pygame.draw.circle(screen, (255,0,255,0), (x,y),3)

car = pygame.sprite.GroupSingle(Car())

def game():
    racemode = True
    while racemode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
        screen.blit(track_texture, (0,0))

        keys = pygame.key.get_pressed()

        if pygame.key.get_pressed() == False:
            car.sprite.driving_status = False
            car.sprite.direction = 0
        
        if keys[pygame.K_UP]:
            car.sprite.driving_status = True
        
        if keys[pygame.K_LEFT]:
            car.sprite.direction = -1
        
        if keys[pygame.K_RIGHT]:
            car.sprite.direction = 1
            
        car.draw(screen)
        car.update()
        pygame.display.update()
            

game()