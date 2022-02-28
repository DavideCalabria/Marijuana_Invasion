# marijuana_invasion
Marijuana invasion is a python game created using pygame library, Most of the code here is from "Alien Invasion" Eric Matthes' "Python Crash Course" book, though I have added some gameplay  changes.

![Screenshot from 2022-02-28 16-00-00](/images/marijuana_invasion.png)

#### Major changes include:

  * Changed background color with an image background
  * Changed ship image with joint image and alien image with leaf image.
  * Added 'Enter' key to start the game
  * Added a feature that saves the high score so it isn't reset each time you start the game
  * Added different levels to start the game
  * Added sound effects
    * reggae background music
    * joint crash sound
    * shooting sound
    * game over sound

## game description

In Marijauna Invasion, the player controls a ship that appears at the bottom center of the screen. \
The player can move the ship right, left using the arrow keys and shoot bullets using the spacebar. \
When the game begins, a fleet of marijuana leaf fills the skyand moves across and down the screen. \
The player shoots and destroys the leafs. If the player shoots all the leafs, a new fleet appears that moves faster than the previous fleet.
If any leaf hits the player’s joint or reaches the bottom of the screen, the player loses a joint. If the player loses three joints, the game ends.

## requirements
* python3
* pygame

To run:
```
python marijauna_invasion.py
