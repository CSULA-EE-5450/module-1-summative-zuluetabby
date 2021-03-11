# EE 5450 Module 1 Summative

## Battleship Game w/ KIVY

This is a Battleship game written in python using the [Kivy](https://kivy.org/#home) library.

## Rules of Battleship
1. Start the game with a friend and provide your usernames. After entering both names, click 'Start' and you will be 
   sent to a selection screen.
2. Both players will be given ships of four different sizes, ranging from 1 to 4 blocks in length. Select the ship in the 
   selection list and place them in the board/grid. You are allowed to change the orientation of the ship. Keep in 
   mind that the ships should not be placed adjacent to one another or overlapping.
4. Each player will take turns guessing where the other person has placed their ship on the grid. The person who sinks 
   all enemy ships first wins!
   
# The Code!
## Menu
The menu screen is created using Kivy to take care of the aesthetics and functions for each button. The files relating 
to the menu are found in **menu.kv** and **menu.py**. 

## Game
The file **battleship_game.py** covers most of the game functions and imports other files mentioned
in order to run. 

## Player
The player has to be initialized, bounded, and given moves to play the game. These functions can be found in the 
**player.py**, **player_moves.py**, and **playerscreen.kv** files. 

## Multiplayer
The game should be played with a friend! It's not fun to play alone, so multiplayer functions were implemented 
in order to play with a friend. The file **multiplayer_client.py**, **multiplayer_scenes.py**, and 
**multiplayerscreen.kv** go over the GUI and functions for multiplayer. Kivy is used to set up the buttons  and
visuals for each player.

## Ships
The game is called BattleSHIP, and it needs ships with character to them! The characteristics of the ship need to 
be defined, and the players should be able to place them on the grid. When playing the game, the ships need to 
recognize when they've been hit or sunk completely. The files relating to the ship are **ship_selection.py**, 
**ship_status**, and **selections.kv**. 

# KIVY - A WIP learning
Research was done on kivy and sample codes from other games like 'Connect 4', 'Pong', and 'Chess' were used to help 
as guidelines. The [API References](https://kivy.org/doc/stable/api-index.html) are researched and tested. Most of
the kv files are found in a folder called **kivy_screen** holding all the files related to the GUI of the game. 
