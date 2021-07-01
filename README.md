# Maze_Escape-3D
NTUEE Data Structures Final Project

How to start：Run main.py to begin the game. Use keyboard and mouse to control and follow the instruction in the program.

Module：Pygame and OpenGL.

Introduction:

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
  



執行環境、執行指令(？
