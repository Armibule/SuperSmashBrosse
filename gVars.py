class GVars:
    def __init__(self, screen, mouseManager):
        self.running = True
        self.keyPressed = {}
        self.clickedPos = None
        self.menu = "menu"
        self.popup = ""
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.SCREEN_CENTER = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.mouseManager = mouseManager
        self.popupCanvasScale = 0.3

    def setMenu(self, menu):
        self.menu = menu

    def setPopup(self, name):
        if self.popup != name:
            self.popupCanvasScale = 0.3
            self.popup = name
