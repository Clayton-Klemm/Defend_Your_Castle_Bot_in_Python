# Defend_Your_Castle_Bot_in_Python
setting it up:

step 1: When starting this you will want the game already open in its own window (no other tabs)

step 2: begin playing the game and as soon as you can see your castle start the python code

step 3: first select the region of the game inside the window then select the search roi (in the image it is the red rectangle). Make sure to leave a gap to the
left so that it will avoid re-detecting the falling enemies

it should look something like this:

![setting up the bot](https://user-images.githubusercontent.com/36232582/213885263-38d0e604-c3e8-4352-8889-694f9191804d.png)



Then when you want it to click for you just hold the spacebar. Have fun! :D


If you play this game smartly you can have it play itself, see https://youtu.be/ds2L64gGm7w for details

some improvements could include:

*Maybe calling the windows api for screenshots rather than pyautogui

*using an object detection model such as YOLO or something other than template matching

*rather than drawing the search roi separately you could probably auto calculate the search roi by doing percentages of
the game screen window

*instead of leaving a gap to the left could have pyautogui sling the enemies all the way right instead which would allow for a 
longer search roi giving more time to detect

*give the script some logic to detect game states so that it can auto go on to the next stage, save the game, buy upgrades, etc. 
