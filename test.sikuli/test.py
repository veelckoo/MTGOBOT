img = Pattern("../Images/trade/set/scroll_down.png")

match = find(img)
loc = Location(match.x, match.y)

hover(loc)