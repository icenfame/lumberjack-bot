from PIL import ImageGrab, Image
import pyautogui
import keyboard
import numpy as np
from time import sleep

def detectGame():
	screen = pyautogui.screenshot()
	button = pyautogui.locateOnScreen('regions/buttons/play.png') or \
				pyautogui.locateOnScreen('regions/buttons/replay.png') or \
				pyautogui.locateOnScreen('regions/buttons/left.png')

	canvasWidth = 600

	# Left
	for left in range(button.left.item(), 0, -1):
		if screen.getpixel((left - 1, button.top.item())) != (255, 255, 255):
			gameX = left
			break;

	# Right
	if screen.getpixel((gameX + canvasWidth - 1, button.top.item())) == (255, 255, 255):
		gameW = canvasWidth

	# Top
	for top in range(button.top.item(), 0, -1):
		if screen.getpixel((gameX - 1, top - 1)) != (51, 51, 51) and screen.getpixel((gameX, top + 1)) == (211, 247, 255):
			gameY = top;
			break;

	# Bottom
	for bottom in range(button.top.item(), screen.height, 1):
		if screen.getpixel((gameX, bottom)) != (255, 255, 255):
			gameH = bottom - gameY
			break;

	return (gameX, gameY, gameW, gameH)

def screenshot(region):
	img = pyautogui.screenshot(region=region)
	# img.save("screen.png")
	return img

def checkPlayer(region, img):
	headX = 240
	headY = 388
	headColor = (51, 93, 101)

	if img.getpixel((headX, region[3] - headY)) == headColor:
		return "left"
	elif img.getpixel((region[2] - headX, region[3] - headY)) == headColor:
		return "right"
	else:
		exit("Player not found")

def checkWood(region, img, player):
	woodY = region[3] - 498 # +100 to +2up
	woodW = 32
	woodH = 100

	if player == "left":
		woodX = 230
	elif player == "right":
		woodX = region[2] - 230 - woodW

	img = img.crop((woodX, woodY, woodX + woodW, woodY + woodH))
	arr = np.array(img)
	arr = arr.reshape((-1, 3))

	if [126, 173, 79] in arr:
		return player

def main():
	region = detectGame()

	while True:
		if keyboard.is_pressed('esc'):
			break;

		img = screenshot(region)
		player = checkPlayer(region, img)
		wood = checkWood(region, img, player)

		if player == "left" and wood == "left":
			pyautogui.press("right")
			pyautogui.press("right")
		elif player == "right" and wood == "right":
			pyautogui.press("left")
			pyautogui.press("left")
		else:
			pyautogui.press(player)
			pyautogui.press(player)

if __name__ == "__main__":
	main()