xy = "1096 227"
reg = Region(1096, 227, 61, 16)
img = "../Images/trade/confirm_window/Mythic.png"
buffer = 0

for i in range(9):
	hover(Location(reg.x, reg.y))
	confirm_button = reg.find(img)
	if confirm_button:
		print("Found one at " + str(reg.x) + ", " + str(reg.y))
	if buffer != 17:
		buffer = 17
	else:
		buffer = 18
	reg.y += buffer