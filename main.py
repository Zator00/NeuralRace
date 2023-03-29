import pygame as pg
import sys

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
    
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
    
    def process(self):
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False



pg.init()

font = pg.font.SysFont('Arial', 40)

res = (720,720)
(width, height) = (720, 720)
screen = pg.display.set_mode(res)

color = (255,255,255) 
color_light = (170,170,170) 
color_dark = (100,100,100) 
width = screen.get_width() 
height = screen.get_height()
smallfont = pg.font.SysFont('Corbel',35) 

text = smallfont.render('quit' , True , color)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                running = False

    screen.fill((60,25,60)) #error after clicking the button
    mouse = pg.mouse.get_pos()

    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pg.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
          
    else: 
        pg.draw.rect(screen,color_dark,[width/2,height/2,140,40])

    screen.blit(text , (width/2+50,height/2)) 
    pg.display.update()
pg.quit()