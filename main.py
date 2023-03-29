import pygame as pg
import sys


pg.init()

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
                pg.quit()

    screen.fill((60,25,60)) #error after clicking the button
    mouse = pg.mouse.get_pos()

    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pg.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
          
    else: 
        pg.draw.rect(screen,color_dark,[width/2,height/2,140,40])

    screen.blit(text , (width/2+50,height/2)) 
    pg.display.update()
pg.quit()