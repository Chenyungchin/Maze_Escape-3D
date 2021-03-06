
import pygame, time
import maze_3D
from maze_2D import build_grid, generate_maze, shortest_path_bfs, maze_drawing2D, remove_horizontal, remove_vertical, highlight_coloring, define_locations, auxiliary_map
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
#WHITE = (255,255,255)
WHITE = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
CYAN = (0, 255, 255)
LIGHTCORAL = (240, 128, 128)

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
        self.maze2D = False
        self.maze3D = False
        self.maze_matrix = []
        self.width = 0
        self.height = 0
        self.show_result = False
        self.display_result = False
        self.game_time = [0, 0]
        self.win = True
        self.path = []
        self.locations = ((0, 0), (0, 0), (0, 0))
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None,35)
        self.font_small = pygame.font.Font(None, 20)
        # Create the menu of the game
        self.menu = Menu(("Start","Setting","Guide","Exit"),font_color = WHITE,font_size=50)
        self.set = Setting(("DFS","Kruskal","Prim's","Small","Normal","Big","Setting","Algorothm  : ","Size of Maze  : "),font_color = WHITE,font_size=35)

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
                            self.chosenalgorithm,self.chosensize = self.set.chosen[0],self.set.chosen[1]-3
                            self.game_over = False
                            self.maze2D = True
                            
                            self.maze3D = False
                            self.maze_matrix = []
                            self.width = 0
                            self.height = 0
                            self.show_result = False
                            self.display_result = False
                            self.draw_maze = True
                            
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
                    elif not self.maze2D and not self.maze3D:
                        self.maze3D = True
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.maze3D = False
                    self.about = False
                    self.setting = False

        return False
    
    
    def display_frame(self,screen):
        #screen.fill(seBLACK)
        image = pygame.image.load("./resources/bg.png")
        #image = pygame.image.load("./resources/bg_.jpg")
        image.convert()
        image = pygame.transform.scale(image, (1024, 576))
        screen.blit(image, (0,0))
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                image = pygame.image.load("./resources/bg_.jpg")
                image.convert()
                image = pygame.transform.scale(image, (1024, 576))
                screen.blit(image, (0,0))
                self.display_message(screen,["Please select the maze-generating algorithm and map size in Setting.", "Press LEFT and RIGHT on your keyboard to adjust your vision.", "Press UP to proceed and SPACE to jump.","There are two pipes working as a transport portal in the maze.","Also there's a ghost that will kill you immediately when it touches you.","Find the way to escape from the MAZE! Enjoy the 3D world!"])
                label = self.font.render("Press ESC to return",True, WHITE)
                screen.blit(label, (700, 520))
                
            elif self.setting:
                image = pygame.image.load("./resources/bg_.jpg")
                image.convert()
                image = pygame.transform.scale(image, (1024, 576))
                screen.blit(image, (0,0))
                self.set.display_frame(screen)
                
            else:
                self.menu.display_frame(screen)
                caption = pygame.image.load("./resources/caption.png").convert_alpha()
                screen.blit(caption, (60, 70))
                pygame.display.update()

        else:
            if self.maze2D:
                screen.fill(LIGHTCORAL)

                mapsize = self.chosensize

                if mapsize == 0:
                    w = 720 // 12
                    width = 12
                    height = 9
                elif mapsize == 1:
                    w = 720 // 16
                    width = 16
                    height = 12
                elif mapsize == 2:
                    w = 720 // 20
                    width = 20
                    height = 15

                test = False
                if test:
                    w = 720 // 4
                    width = 4
                    height = 3
                
                build_grid(width, height, w)
                
                alg_dic = {0:"dfs_backtrack", 1:"randomized_kruskal", 2:"randomized_prims"} 
                algorithm = alg_dic[self.chosenalgorithm]

                note = pygame.image.load("./resources/note_" + algorithm + ".png").convert_alpha()
                note = pygame.transform.scale(note, (250, 450))
                screen.blit(note, (760, 20))

                self.maze_matrix, draw_step = generate_maze(algorithm, width, height, w)

                for i in range(2*height-1):
                    self.maze_matrix[i].insert(0, 1)
                    self.maze_matrix[i].append(1)
                self.maze_matrix.insert(0, [1]*(2*width+1))
                self.maze_matrix.append([1]*(2*width+1))
                #define starting point
                self.maze_matrix[1][0] = 0
                self.maze_matrix[-1][-2] = 0

                self.width = width 
                self.height = height 
                self.w = w

                self.locations = define_locations(self.maze_matrix, 2*self.width+1, 2*self.height+1)
                
                print(self.locations)
                # print(maze_matrix)
                # print(draw_step)

                maze_drawing2D(draw_step, algorithm, self.locations, 2*self.width+1, 2*self.height+1)
                # pygame.image.save(screen, "./resources/maze2D.jpg")
                self.maze2D = False
            else:
                if not self.maze3D:
                    # image = pygame.image.load("./resources/maze2D.jpg")
                    # image.convert()
                    # screen.blit(image, (0,0))
                    
                    self.maze_reconstruction(screen, self.maze_matrix, self.width, self.height, self.w)
                    self.display_message_picked_position(screen,"Press ENTER to start", (760, 500))
                    pygame.display.update()
                elif not self.show_result:
                    self.game_time[0] = time.time()
                    screen.fill(CYAN)
                    self.display_message(screen,["3D map is coming!"])
                    # auxiliary_map(???????????????, ????????????, self.locations[1], self.locations[2], 2*self.width+1, 2*self.height+1)
                    # print(self.maze_matrix)
                    # Thomas ??????:???Maze3D?????????
                    self.win, self.path = maze_3D.main(self.maze_matrix, self.locations, display=(SCREEN_WIDTH, SCREEN_HEIGHT))
                    self.show_result = True
                    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
                    self.game_time[1] = time.time()
                elif not self.display_result:
                    if self.win == True:
                        img = pygame.image.load("./resources/win.jpg").convert_alpha()
                    else:
                        img = pygame.image.load("./resources/lose.jpg").convert_alpha()
                    img = pygame.transform.scale(img, (1024, 576))
                    screen.blit(img, (0, 0))
                    pygame.display.update()
                    time.sleep(3)
                    self.maze_reconstruction(screen, self.maze_matrix, self.width, self.height, self.w, display_note=False)
                    # path = shortest_path_bfs(self.maze_matrix, (0, 1), (2*self.width-1, 2*self.height), 2*self.width+1, 2*self.height+1)
                    
                    self.carve_player_movements(screen, self.w, self.path)
                    self.display_result = True
                else:
                    self.maze_reconstruction(screen, self.maze_matrix, self.width, self.height, self.w, display_note=False)
                    # path = shortest_path_bfs(self.maze_matrix, (0, 1), (2*self.width-1, 2*self.height), 2*self.width+1, 2*self.height+1)
                    self.rewind(screen, self.game_time[1]-self.game_time[0])
                    self.carve_player_movements(screen, self.w, self.path, animation=False)



            
        pygame.display.flip()

    def maze_reconstruction(self, screen, maze_matrix, width, height, w, display_note = True):
        bias_x = 24
        bias_y = 18
        blue_violet = (138, 43, 226)
        lightcoral = (240, 128, 128)
        screen.fill(lightcoral)
        pygame.draw.rect(screen, blue_violet,(bias_x, bias_y, 720, 540))
        build_grid(width, height, w)
        alg_dic = {0:"dfs_backtrack", 1:"randomized_kruskal", 2:"randomized_prims"} 
        algorithm = alg_dic[self.chosenalgorithm]

        for j in range(2*height+1):
            for i in range(2*width+1):
                if i != 0 and i != 2*width and j != 0 and j != 2*height:
                    if (i+j)%2 == 1 and maze_matrix[j][i]%2 == 0:
                        if j % 2 == 1:
                            remove_vertical(bias_x+(i//2)*w, bias_y+((j-1)//2)*w, w)
                        else:
                            remove_horizontal(bias_x+((i-1)//2)*w, bias_y+(j//2)*w, w)
        if display_note:
            note = pygame.image.load("./resources/note_" + algorithm + ".png").convert_alpha()
            note = pygame.transform.scale(note, (250, 450))
            screen.blit(note, (760, 20))
        
        icons = ["./resources/start.png", "./resources/ghost.png", "./resources/pipe.png", "./resources/pipe.png", "./resources/trophy.png"]
        locations_all = [(1, 1), self.locations[0], self.locations[1], self.locations[2], (2*width-1, 2*height-1)]
        for index, url in enumerate(icons):
            icon = pygame.image.load(url).convert_alpha()
            icon = pygame.transform.scale(icon, (w, w))
            col, row = locations_all[index]
            x, y = bias_x+((col-1)//2)*w, bias_y+((row-1)//2)*w
            screen.blit(icon, (x, y))

    def carve_player_movements(self, screen, w, movements, animation=True):
        bias_x = 24
        bias_y = 18

        footprint = pygame.image.load("./resources/footprint.png").convert_alpha()
        footprint = pygame.transform.scale(footprint, (w-1, w-1))

        left =  pygame.image.load("./resources/left.png").convert_alpha()
        left = pygame.transform.scale(left, (w, w))

        right =  pygame.image.load("./resources/right.png").convert_alpha()
        right = pygame.transform.scale(right, (w, w))

        up =  pygame.image.load("./resources/up.png").convert_alpha()
        up = pygame.transform.scale(up, (w, w))

        down =  pygame.image.load("./resources/down.png").convert_alpha()
        down = pygame.transform.scale(down, (w, w))

        best_path = shortest_path_bfs(self.maze_matrix, (0, 1), (2*self.width-1, 2*self.height), 2*self.width+1, 2*self.height+1)
        print(best_path)
        last_col, last_row  = -1, 1
        
        for i in range(max(len(movements), len(best_path))):
            if animation == True:
                time.sleep(0.1)
            
            if i < len(best_path):

                col, row = best_path[i]
                if col > last_col:
                    direct = right
                elif col < last_col:
                    direct = left
                elif row > last_row:
                    direct = down
                else:
                    direct = up
                last_col, last_row = col, row

                if col%2 == 1 and row%2 == 1:
                    x = bias_x+((col-1)//2)*w
                    y = bias_y+((row-1)//2)*w
                    # highlight_coloring(x, y, w)
                    screen.blit(direct, (x+1, y+1))
                    if animation == True:
                        pygame.display.update() 
            if i < len(movements):
                col, row = movements[i]
                if col%2 == 1 and row%2 == 1:
                    x = bias_x+((col-1)//2)*w
                    y = bias_y+((row-1)//2)*w
                    # highlight_coloring(x, y, w)
                    screen.blit(footprint, (x+1, y+1))
                    if animation == True:
                        pygame.display.update()
        pygame.display.update()
    
    def rewind(self, screen, time):
        posx = 760
        font = pygame.font.Font(None,50)
        label = font.render("REWIND:", True, WHITE)
        screen.blit(label, (770, 25))
        
        if self.win:
            result = "Win"
        else:
            result = "Lose"
        self.display_message_picked_position(screen, "Result : "+result, (posx, 100))
        sec = self.game_time[1]-self.game_time[0]
        sec = round(sec)
        time = str(sec//60), str(sec%60)
        self.display_message_picked_position(screen, "Time : "+time[0]+" min "+time[1]+" sec", (posx, 150))
        best_path_len = len(shortest_path_bfs(self.maze_matrix, (0, 1), (2*self.width-1, 2*self.height), 2*self.width+1, 2*self.height+1))
        self.display_message_picked_position(screen, "Best Route : "+ str(best_path_len) +" steps", (posx, 200))
        if self.win:
            self.display_message_picked_position(screen, "Your Route : "+ str(len(self.path)) +" steps", (posx, 250))
        self.display_message_picked_position(screen,"Press ESC to return", (760, 500))



            



        

    def display_message_picked_position(self, screen, message, pos, color=WHITE):
        label = self.font.render(message,True,color)
        screen.blit(label, pos)


    def display_message(self,screen,message,color=(0,0,0)):
        
        for index,line in enumerate(message):    
            label = self.font.render(line,True,color)
        
            width = label.get_width()
            height = label.get_height()*2
            
            posX = (SCREEN_WIDTH /2) - (width)/2
            #t_h: total height of text block
            t_h = len(message) * height 
            posY = (SCREEN_HEIGHT /2 - (t_h /2) + (index * height))
            posX = 120
            screen.blit(label,(posX,posY))


class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font="./resources/times.ttf",font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                url = "frame_selected.png"
                label = self.font.render(item,True,self.select_color)
            else:
                url = "frame.png"
                label = self.font.render(item,True,self.font_color)
            
            
            if index ==0:
                posX,posY = 395,340
                frame_x, frame_y = 370, 330
            elif index ==1:
                posX,posY = 537,340
                frame_x, frame_y = 535, 330
            elif index ==2:
                posX,posY = 385,440
                frame_x, frame_y = 370, 430
            elif index ==3:
                posX,posY = 565,440
                frame_x, frame_y = 535, 430
            self.image_blitter(url, screen, (150, 80), (frame_x, frame_y))
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

    def image_blitter(self, url, screen, scale, pos):
        image = pygame.image.load("./resources/" + url)
        image.convert()
        image = pygame.transform.scale(image, scale)
        screen.blit(image, pos)
class Setting(object):
    state = 0
    chosen=[0,3]
    def __init__(self,items,font_color=(0,0,0),select_color=RED,chosen_color=BLUE,ttf_font="./resources/times.ttf",font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        self.font_title = pygame.font.Font(ttf_font, 2*font_size)
        self.chosen_color = chosen_color
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                url = "frame_selected.png"
                label = self.font.render(item,True,self.select_color)
            else:
                if index in self.chosen :
                    url = "frame_chosen.png"
                    label = self.font.render(item,True,self.chosen_color)
                else:
                    url = "frame.png"
                    label = self.font.render(item,True,self.font_color)
           
            width = label.get_width()
            height = label.get_height()

            
           
            if index ==0:
                posX,posY = 325,340
            elif index ==1:
                posX,posY = 530,340
            elif index ==2:
                posX,posY = 740,340
            elif index ==3:
                posX,posY = 325,440
            elif index ==4:
                posX,posY = 530,440
            elif index ==5:
                posX,posY = 740,440
            elif index ==6:
                posX,posY = (SCREEN_WIDTH /2) - (width)/2 , SCREEN_HEIGHT / 5
                label = self.font_title.render(item,True,self.font_color)
            elif index ==7:
                posX,posY = 100,340
            elif index ==8:
                posX,posY = 72,440
            
            if index < 6:
                self.image_blitter(url, screen, (150, 80), (posX-20, posY-20))

            screen.blit(label,(posX,posY))
        
        label = self.font.render("Press ESC to return",True,self.font_color)
        screen.blit(label, (700, 520))
    
    def image_blitter(self, url, screen, scale, pos):
        image = pygame.image.load("./resources/" + url)
        image.convert()
        image = pygame.transform.scale(image, scale)
        screen.blit(image, pos)
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 2:
                    self.state = 0
            elif event.key == pygame.K_DOWN:
                if self.state < 3:
                    self.state = 3
            elif event.key == pygame.K_RIGHT:
                if self.state %3 != 2:
                    self.state +=1
            elif event.key == pygame.K_LEFT:
                if self.state %3 != 0:
                    self.state -=1
            elif event.key == pygame.K_RETURN:
                if self.state >2 :
                    self.chosen.pop()
                    self.chosen.append(self.state)
                else:
                    self.chosen.pop(0)
                    self.chosen.insert(0,self.state)
                    


                    
            
