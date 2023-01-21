import cv2
import pyautogui
import numpy as np
from imutils.object_detection import non_max_suppression
import keyboard

def screen_capture():
    # first we grab our web browser window
    # the game should be the only tab open
    # we will first configure our viewing screen, later we will
    # define our more specific roi to avoid re-clicking an already dealt with enemy
    window = pyautogui.getWindowsWithTitle("Defend Your Castle")[0]
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    # pyautogui returns a PIL (pillow) image object
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    # next we convert the image object to a numpy array that opencv can use
    game_screen = np.array(screenshot)
    # convert the colors since PIL is default rgb instead of bgr
    game_screen = cv2.cvtColor(game_screen, cv2.COLOR_RGB2BGR)
    # lets the user select the game window more specifically and press 'enter'
    # the user should select the whole game screen
    roi_game_screen = cv2.selectROI("select the game screen", game_screen)
    cv2.destroyAllWindows()
    # next we will get the roi to search for enemies
    # it is important that we avoid re-clicking falling enemies so
    # this roi should leave a gap from the left so that we can
    # drag the enemy to the upper left portion of the game and release
    # the enemy and have it fall straight down without it being detected again
    roi_search = cv2.selectROI("select the search roi", game_screen)
    cv2.destroyAllWindows()
    # load our enemy template
    enemy1 = cv2.imread("resources/enemies/enemy_1.png")
    enemy1 = cv2.cvtColor(enemy1, cv2.COLOR_RGB2GRAY)
    (tH, tW) = enemy1.shape[:2]
    while(True):
        # for viewing convienice we will have our view window being shown
        # and we will draw rectangles around enemies in the window
        # but the actual matching of the template will be done in our roi_search screen
        game_screen = pyautogui.screenshot(region=roi_game_screen)
        game_screen = np.array(game_screen)
        game_screen = cv2.cvtColor(game_screen, cv2.COLOR_RGB2BGR)
        # get the search screen and convert it for opencv
        search_screen = pyautogui.screenshot(region=roi_search)
        search_screen = np.array(search_screen)
        search_screen = cv2.cvtColor(search_screen, cv2.COLOR_RGB2GRAY)
        # draw our selected region on the game window to show roi_search
        cv2.rectangle(game_screen, pt1=(roi_search[0]-roi_game_screen[0], roi_search[1]-roi_game_screen[1]), pt2=(roi_search[0]+roi_search[2]-roi_game_screen[0], (roi_search[1]+roi_search[3])-roi_game_screen[1]),color=(0,0,255),thickness=2)
        # find our template in the region
        result = cv2.matchTemplate(search_screen, enemy1, cv2.TM_CCOEFF_NORMED)
        # set our match threshold
        (yCoords, xCoords) = np.where(result >= .5)
        rects = []
        for (x, y) in zip(xCoords, yCoords):
            rects.append((x, y, x + tW, y + tH))
        # rects array now has the location of all matches found, the problem is that multiple matches can arise
        # around a particular template so in order to clean up the noise we use non_max_suppression
        # which, in layman terms, we select the predictions with the maximum confidence and suppress all the other 
        # predictions having overlap with the selected predictions greater than a threshold.
        pick = non_max_suppression(np.array(rects))
        for (startX, startY, endX, endY) in pick:
            # visually display the detection
            cv2.rectangle(game_screen, (startX + roi_search[0]-roi_game_screen[0], roi_search[1]-roi_game_screen[1]+startY), (endX+roi_search[0]-roi_game_screen[0], endY+roi_search[1]-roi_game_screen[1]),(255, 0, 0), 3)
            cv2.rectangle(search_screen, (startX, startY), (endX, endY),(255, 0, 0), 3)
            # while we hold the spacebar our app will move to the enemy and click and drag it
            if keyboard.is_pressed("space"):
                pyautogui.moveTo(endX+roi_search[0], int((endY + startY)/2) + roi_search[1])
                pyautogui.dragTo(x=roi_game_screen[0], y=roi_game_screen[1], button='left')
        # show what is happening
        # cv2.imshow("search region", search_screen)
        cv2.imshow("Game Screen", game_screen)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

def main():
    screen_capture()

if __name__ == "__main__":
    main()