
import graphics

class Plotter(object):
    
    def __init__(self, label, data):
        
        win = graphics.GraphWin(label, 256, 256)
        win.setBackground("white")

        for i in range(0, len(data)):
            color = self.get_color(data[i])
            x = i % 16
            y = int(i / 16)

            p1 = graphics.Point(x * 16, y * 16)
            p2 = graphics.Point((x + 1) * 16 - 1, (y + 1) * 16 - 1)
            
            rectangle = graphics.Rectangle(p1, p2)
            rectangle.setFill(color)
            rectangle.setOutline(color)
            rectangle.draw(win)

        win.getMouse()
        win.close()

    def get_color(self, data):
        gray = int((1 - data) * 255 / 2)
        return graphics.color_rgb(gray, gray, gray)
