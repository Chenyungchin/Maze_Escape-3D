#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
#from player import Player
#from enemies import *
import tkinter
from tkinter import messagebox
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None,40)
        self.about = False
        self.game_over = True
        self.setting = False
        self.chosenalgorithm = 0
        self.chosensize = 0
        # Create the variable for the score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None,35)
        # Create the menu of the game
        self.menu = Menu(("Start","Setting","Guide","Exit"),font_color = WHITE,font_size=50)
        self.set = Setting(("Algorothm1","Algorithm2","Size1","Size2","Size3","Setting","Algorothm : ","Size of Maze : "),font_color = WHITE,font_size=30)
##        # Create the player
##        self.player = Player(32,128,"player.png")
##        # Create the blocks that will set the paths where the player can go
##        self.horizontal_blocks = pygame.sprite.Group()
##        self.vertical_blocks = pygame.sprite.Group()
##        # Create a group for the dots on the screen
##        self.dots_group = pygame.sprite.Group()
##        # Set the enviroment:
##        for i,row in enumerate(enviroment()):
##            for j,item in enumerate(row):
##                if item == 1:
##                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
##                elif item == 2:
##                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
##        # Create the enemies
##        self.enemies = pygame.sprite.Group()
##        self.enemies.add(Slime(288,96,0,2))
##        self.enemies.add(Slime(288,320,0,-2))
##        self.enemies.add(Slime(544,128,0,2))
##        self.enemies.add(Slime(32,224,0,2))
##        self.enemies.add(Slime(160,64,2,0))
##        self.enemies.add(Slime(448,64,-2,0))
##        self.enemies.add(Slime(640,448,2,0))
##        self.enemies.add(Slime(448,320,2,0))
##        # Add the dots inside the game
##        for i, row in enumerate(enviroment()):
##            for j, item in enumerate(row):
##                if item != 0:
##                    self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))
##
##        # Load the sound effects
##        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
##        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")
##

    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            if not self.setting :
                self.menu.event_handler(event)
            else:
                self.set.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about and not self.setting:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__()
                            self.chosenalgorithm,self.chosensize = self.set.chosen[0],self.set.chosen[1]-2
                            self.game_over = False
                            
                        elif self.menu.state == 1:
                            # --- Setting ------
                            self.setting = True
                            
                        elif self.menu.state == 2:
                            # --- About -------
                            self.about = True
                        elif self.menu.state == 3:
                            # --- EXIT -------
                            # User clicked exit
                            return True
                    #elif self.setting:
                        
##                elif event.key == pygame.K_RIGHT:
##                    self.player.move_right()
##
##                elif event.key == pygame.K_LEFT:
##                    self.player.move_left()
##
##                elif event.key == pygame.K_UP:
##                    self.player.move_up()
##
##                elif event.key == pygame.K_DOWN:
##                    self.player.move_down()
##                
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False
                    self.setting = False

##            elif event.type == pygame.KEYUP:
##                if event.key == pygame.K_RIGHT:
##                    self.player.stop_move_right()
##                elif event.key == pygame.K_LEFT:
##                    self.player.stop_move_left()
##                elif event.key == pygame.K_UP:
##                    self.player.stop_move_up()
##                elif event.key == pygame.K_DOWN:
##                    self.player.stop_move_down()
##
##            elif event.type == pygame.MOUSEBUTTONDOWN:
##                self.player.explosion = True
##                    
        return False
    
##    def run_logic(self):
##        if not self.game_over:
##            self.player.update(self.horizontal_blocks,self.vertical_blocks)
##            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
##            # When the block_hit_list contains one sprite that means that player hit a dot
##            if len(block_hit_list) > 0:
##                # Here will be the sound effect
##                self.pacman_sound.play()
##                self.score += 1
##            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
##            if len(block_hit_list) > 0:
##                self.player.explosion = True
##                self.game_over_sound.play()
##            self.game_over = self.player.game_over
##            self.enemies.update(self.horizontal_blocks,self.vertical_blocks)
##           # tkMessageBox.showinfo("GAME OVER!","Final Score = "+(str)(GAME.score))    
##
    
    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands
        #screen.fill(BLACK)
        image = pygame.image.load("./among_us_9.jpg")
        image.convert()
        image = pygame.transform.scale(image, (1024, 576))
        screen.blit(image, (0,0))
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                 image = pygame.image.load("./among_us_11.jpg")
                 image.convert()
                 image = pygame.transform.scale(image, (1024, 576))
                 screen.blit(image, (0,0))
                 self.display_message(screen,["Find the Way to Escape from the MAZE!","Use Up,Down,Left,Right in Keyboard and Mouse to control","Have Fun!"])
                #print(bool(self.setting))
                #self.display_message(screen,"QAQ",2)
                #"a maze containing various dots,\n"
                #known as Pac-Dots, and four ghosts.\n"
                #"The four ghosts roam the maze, trying to kill Pac-Man.\n"
                #"If any of the ghosts hit Pac-Man, he loses a life;\n"
                #"the game is over.\n")
            elif self.setting:
                image = pygame.image.load("./among_us_11.jpg")
                image.convert()
                image = pygame.transform.scale(image, (1024, 576))
                screen.blit(image, (0,0))
                self.set.display_frame(screen)
                
            else:
                self.menu.display_frame(screen)
                #self.display_message(screen,["Find the Way to Escape from the MAZE!","Use Up,Down,Left,Right in Keyboard and Mouse to control","Have Fun!"])
        else:
            screen.fill(BLACK)
            #self.display_message(screen,["You have chosen Algorithm %d and Size %d."%(self.set.chosen[0]+1,self.set.chosen[1]-1)])
            self.display_message(screen,["You have chosen Algorithm %d and Size %d."%(self.chosenalgorithm+1,self.chosensize+1)])
            # --- Draw the game here ---
##            self.horizontal_blocks.draw(screen)
##            self.vertical_blocks.draw(screen)
##            draw_enviroment(screen)
##            self.dots_group.draw(screen)
##            self.enemies.draw(screen)
##            screen.blit(self.player.image,self.player.rect)
##            #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
##            #screen.blit(text, (30, 650))
##            # Render the text for the score
##            text = self.font.render("Score: " + str(self.score),True,GREEN)
##            # Put the text on the screen
##            screen.blit(text,[120,20])
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def display_message(self,screen,message,color=(255,255,255)):
        #label = self.font.render(message,True,color)
        #font = pygame.font.Font("Arial", 24)
        # Get the width and height of the label
        #width = label.get_width()
        #height = label.get_height()
        # Determine the position of the label
        #posX = (SCREEN_WIDTH /2) - (width /2) 
        #posY = (SCREEN_HEIGHT /2) - (height /2) + (line-1)*50
        # Draw the label onto the screen
        #screen.blit(label,(posX,posY))
        for index,line in enumerate(message):    
            label = self.font.render(line,True,color)
        
            width = label.get_width()
            height = label.get_height()*2
            
            posX = (SCREEN_WIDTH /2) - (width)/2
##          # t_h: total height of text block
            t_h = len(message) * height 
            posY = (SCREEN_HEIGHT /2 - (t_h /2) + (index * height))
            screen.blit(label,(posX,posY))


class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font="./times.ttf",font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                
                label = self.font.render(item,True,self.select_color)
            else:
               
                label = self.font.render(item,True,self.font_color)
            
##            width = label.get_width()
##            height = label.get_height()
##            
##            posX = (SCREEN_WIDTH /2) - (width)/2
##            # t_h: total height of text block
##            t_h = len(self.items) * height 
##            posY = (SCREEN_HEIGHT *(2/3) - (t_h /2) + (index * height))
            if index ==0:
                posX,posY = 395,390
            elif index ==1:
                posX,posY = 537,390
            elif index ==2:
                posX,posY = 385,490
            elif index ==3:
                posX,posY = 565,490
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 1:
                    self.state -= 2
            elif event.key == pygame.K_DOWN:
                if self.state < 2:
                    self.state += 2
            elif event.key == pygame.K_RIGHT:
                if self.state %2 ==0:
                    self.state += 1
            elif event.key == pygame.K_LEFT:
                if self.state %2 ==1:
                    self.state -= 1
class Setting(object):
    state = 0
    chosen=[0,2]
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),chosen_color=(0,0,255),ttf_font="./times.ttf",font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        self.chosen_color = chosen_color
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                if index in self.chosen :
                    label = self.font.render(item,True,self.chosen_color)
                else:
                    label = self.font.render(item,True,self.font_color)
           
            width = label.get_width()
            height = label.get_height()
           
##            posX = (SCREEN_WIDTH /2) - (width)/2
##            # t_h: total height of text block
##            t_h = len(self.items) * height 
##            posY = (SCREEN_HEIGHT *(2/3) - (t_h /2) + (index * height))
            if index ==0:
                posX,posY = 425,390
            elif index ==1:
                posX,posY = 630,390
            elif index ==2:
                posX,posY = 385,490
            elif index ==3:
                posX,posY = 565,490
            elif index ==4:
                posX,posY = 800,490
            elif index ==5:
                posX,posY = (SCREEN_WIDTH /2) - (width)/2 , SCREEN_HEIGHT / 5
            elif index ==6:
                posX,posY = 200,390
            elif index ==7:
                posX,posY = 172,490
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 1:
                    self.state = 0
            elif event.key == pygame.K_DOWN:
                if self.state < 2:
                    self.state = 2
            elif event.key == pygame.K_RIGHT:
                if self.state %3 != 1:
                    self.state +=1
            elif event.key == pygame.K_LEFT:
                if self.state != 0 and self.state != 2:
                    self.state -=1
            elif event.key == pygame.K_RETURN:
                if self.state >1 :
                    self.chosen.pop()
                    self.chosen.append(self.state)
                else:
                    self.chosen.pop(0)
                    self.chosen.insert(0,self.state)
                    


                    
            
