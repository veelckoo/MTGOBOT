img = Pattern("../Images/trade/confirm_button.png")

match = find(img)
loc = Location(match.x, match.y)

hover(loc)