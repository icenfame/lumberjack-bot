"""Automation module"""
import pyautogui
import numpy as np
import keyboard


def detect_game():
    """Detect game on screen"""

    screen = pyautogui.screenshot()
    button = (
        pyautogui.locateOnScreen('regions/buttons/play.png') or
        pyautogui.locateOnScreen('regions/buttons/replay.png') or
        pyautogui.locateOnScreen('regions/buttons/left.png')
    )

    canvas_width = 600
    white = (255, 255, 255)
    background = (51, 51, 51)
    blue = (211, 247, 255)

    # Left
    for left in range(button.left.item(), 0, -1):
        if screen.getpixel((left - 1, button.top.item())) != white:
            game_x = left
            break

    # Right
    if screen.getpixel((game_x + canvas_width - 1, button.top.item())) == white:
        game_w = canvas_width

    # Top
    for top in range(button.top.item(), 0, -1):
        if (screen.getpixel((game_x - 1, top - 1)) != background and
                screen.getpixel((game_x, top + 1)) == blue):
            game_y = top
            break

    # Bottom
    for bottom in range(button.top.item(), screen.height, 1):
        if screen.getpixel((game_x, bottom)) != white:
            game_h = bottom - game_y
            break

    return (game_x, game_y, game_w, game_h)


def screenshot(region):
    """Make screenshot of specific region"""

    img = pyautogui.screenshot(region=region)
    return img


def check_player(region, img):
    """Check player position by the head"""

    head_x = 240
    head_y = 388
    head_color = (51, 93, 101)

    if img.getpixel((head_x, region[3] - head_y)) == head_color:
        return "left"
    elif img.getpixel((region[2] - head_x, region[3] - head_y)) == head_color:
        return "right"
    else:
        exit("Player not found")


def check_wood(region, img, player):
    """Check wood over the player head"""

    wood_y = region[3] - 498
    wood_w = 32
    wood_h = 100

    if player == "left":
        wood_x = 230
    elif player == "right":
        wood_x = region[2] - 230 - wood_w

    # TODO find all woods by pixel

    img = img.crop((wood_x, wood_y, wood_x + wood_w, wood_y + wood_h))
    arr = np.array(img)
    arr = arr.reshape((-1, 3))

    if [126, 173, 79] in arr:
        return player


def main():
    """Main function"""
    region = detect_game()

    # TODO auto start game & end if lost

    while True:
        if keyboard.is_pressed('esc'):
            break

        img = screenshot(region)
        player = check_player(region, img)
        wood = check_wood(region, img, player)

        if player == wood == "left":
            pyautogui.press("right")
            pyautogui.press("right")
        elif player == wood == "right":
            pyautogui.press("left")
            pyautogui.press("left")
        else:
            pyautogui.press(player)
            pyautogui.press(player)


if __name__ == "__main__":
    main()
