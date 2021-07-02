# Maze_Escape-3D
NTUEE Data Structures Final Project

## Required Software and Modules
* Software : Python3
* Module：Pygame and OpenGL
(execute "pip install pygame" and "pip install PYOpenGL" to download the modules)


## How to Execute
* Environment : Available for Windows10 and Linux
* Executing Command: Run "python ./main.py" to begin the game. 

## How to Play
Select the maze-generating algorithm and map size in Setting.

Press LEFT and RIGHT on your keyboard to adjust your vision and press UP to proceed.

Find the way to escape from the MAZE!

Enjoy the 3D world!


## Code Introduction:

1.main.py

  (a)main()：Main function of the program. Control the FPS, processing events and displaying screen.
  
2.game.py

  (a)class Game()：Main initial class that contains functions about keyboard settings and frames.
  
  (b)class Menu()：The initial menu with "Start", "Setting", "Guide" and "Exit".
  
  (c)class Setting()：The setting menu to choose algorithms and size of maze.
  
3.disjoint_set.py

  (a)find & merge：Implement disjoint-set operation including makeset(), union() and find().
  
4.maze2D.py

  Build the 2D maze model, design drawing animation and implement three maze-construction algorithms.(BFS, Kruskal and Prim's)
  
5.maze.py

  Construct the exteriority and shape of the 3D-maze and set the keyboard operation in vision.
  
6.maze3D.py

  Use OpenGL to draw the maze and specific items, set the keyboard operation in movement, control the ghost and handle the winning and losing conditions.
  
7.objloader.py

  Load the objects that includes texture, material, color, shape, etc.
  
## Author
* 詹侑昕 B08901046
* 陳永縉 B08901061
* 李允恩 B08901102
