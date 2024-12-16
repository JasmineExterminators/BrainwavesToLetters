README:

Touchless Solitaire:
I will be coding a slightly modified solitaire game where the user can move around cards with eyes only. In the solitaire game, the game will use backtracking to be able to check if the initial setup is solvable. The user then is able to choose cards to move to another pile (as per the rules of solitaire), flip a card from the deck, build up the A → K piles and wins when all four of the A → K piles are complete. 

Run Instructions
Run solidtaire.py
Install openCV: pip install opencv-python
Set up haarcascades folder (with datasets inside) in the folder you are running your program, as well as cmu_graphics folder and the cardGraphicsPNG folder

Shortcut Commands
Just take out the reset after the last backtracking that returns true, then you will have a completed game
Pressing 'h' will turn on hint mode - just follow the hints