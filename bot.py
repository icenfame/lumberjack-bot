from PIL import ImageGrab, ImageOps, Image
import pyautogui
import keyboard
import numpy as np
from time import sleep

# Full window
xBase = 660
yBase = 71
hBase = 969 # div
# Half window
xBase = 180
yBase = 80
hBase = 959 # div
# hBase = 731 # canvas

# Both
wBase = 600

def screenshot(i = 0):
	img = ImageGrab.grab(bbox=(xBase, yBase, xBase + wBase, yBase + hBase))
	# img.save(f"game/screen_{i}.png")
	# img.save("screen.png")

	return img

def checkPlayerPosition(img):
	if img.getpixel((240, 570)) == (51, 93, 101): # red shirt (207, 70, 59)
		return "left"
	elif img.getpixel((wBase - 240, 570)) == (51, 93, 101):
		return "right"
	else:
		exit("Player not found")

def checkWood(img, player):
	y = 461
	w = 60
	h = 100

	# 0 up
	# y = 461
	# 2 up
	# y = 360

	if player == "left":
		x = 200
	elif player == "right":
		x = wBase - 200 - w

	img = img.crop((x, y, x + w, y + h))

	arr = np.array(img)
	arr = arr.reshape((-1, 3))

	if [126, 173, 79] in arr:
		return player

# Start play
# TODO

# def checkButton():
# 	x = xBase + 242
# 	y = 866
# 	w = 120
# 	h = 120

# 	img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
	# img.save("screen.png")

# def captureGame():
# 	img = ImageGrab.grab(bbox=(xBase, yBase, xBase + wBase, yBase + hBase))
# 	img.save("screen.png")


# print(captureWoodBlock())

# checkButton()
# captureGame()
# exit()
# i = 0

pyautogui.PAUSE = 0.3

# Playing
while True:
	# sleep(0.01)

	img = screenshot();
	player = checkPlayerPosition(img)
	wood = checkWood(img, player)

	# print("Player:", player, "\tWood:", wood)

	# exit()

	# i += 1

	if player == "left" and wood == "left":
		pyautogui.press("right")
		pyautogui.press("right")

		# pyautogui.click(x=560, y=920)
		# pyautogui.click(x=560, y=920)
	elif player == "right" and wood == "right":
		pyautogui.press("left")
		pyautogui.press("left")

		# pyautogui.click(x=400, y=920)
		# pyautogui.click(x=400, y=920)

	# elif player == "left" and wood2 == "left":
	# 	pyautogui.press("left")
	# 	pyautogui.press("left")
	# 	pyautogui.press("right")
	# 	pyautogui.press("right")

	# 	# print("2L 2R")
	# elif player == "right" and wood2 == "right":
	# 	pyautogui.press("right")
	# 	pyautogui.press("right")
	# 	pyautogui.press("left")
	# 	pyautogui.press("left")

		# print("2R 2L")
	else:
		pyautogui.press(player)
		pyautogui.press(player)

		# if player == "left":
		# 	pyautogui.click(x=400, y=920)
		# 	pyautogui.click(x=400, y=920)
		# else:
		# 	pyautogui.click(x=560, y=920)
		# 	pyautogui.click(x=560, y=920)


		# print(f"2{player[0].upper()}")

	if keyboard.is_pressed('esc'):
		break;