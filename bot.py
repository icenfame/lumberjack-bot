"""Bot for Telegram game LumberJack"""
import sys
from time import sleep
import pyautogui
import keyboard


def detect_game():
    """Detect game on a screen"""

    screen = pyautogui.screenshot()
    button = (
        pyautogui.locateOnScreen('regions/buttons/play.png') or
        pyautogui.locateOnScreen('regions/buttons/replay.png') or
        pyautogui.locateOnScreen('regions/buttons/left.png')
    )

    if not button:
        sys.exit(
            "[ERROR]: Cannot find game. Make sure you have opened game on your screen")

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
    """Take a screenshot of a specific region"""

    return pyautogui.screenshot(region=region)


def check_player(region, img):
    """Check player position by the head"""

    head_x = 240
    head_y = 388
    head_color = (51, 93, 101)

    if img.getpixel((head_x, region[3] - head_y)) == head_color:
        return "left"

    if img.getpixel((region[2] - head_x, region[3] - head_y)) == head_color:
        return "right"

    return None


def check_branch(region, img, player, offset_y):
    """Check a branch on a screen"""

    branch_y = region[3] - 399
    branch_color = (136, 99, 50)

    if player == "left":
        branch_x = 240
    elif player == "right":
        branch_x = region[2] - 240

    return img.getpixel((branch_x, branch_y - (100 * offset_y))) == branch_color


def play(region):
    """Auto-play game"""

    play_button = (
        pyautogui.locateOnScreen('regions/buttons/play.png') or
        pyautogui.locateOnScreen('regions/buttons/replay.png')
    )

    if play_button:
        pyautogui.click(play_button)

    pyautogui.click(region)
    sleep(1)


def main():
    """Main function"""

    pyautogui.PAUSE = 1 / 60

    region = detect_game()
    score = 0

    play(region)

    while True:
        sleep(0.2)

        if keyboard.is_pressed('esc'):
            sys.exit("[INFO]: User ESC exit")

        img = screenshot(region)
        player = check_player(region, img)

        if not player:
            if score > 0:
                print(f"[INFO]: Score {score}")

            break

        for offset_y in range(6):
            if check_branch(region, img, player, offset_y):
                if player == "left":
                    pyautogui.press("right")
                    pyautogui.press("right")
                elif player == "right":
                    pyautogui.press("left")
                    pyautogui.press("left")
            else:
                pyautogui.press(player)
                pyautogui.press(player)

        score += 12


if __name__ == "__main__":
    main()
