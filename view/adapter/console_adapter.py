import tdl


class ConsoleAdapter:
    def __init__(self, width, height):
        self.console = tdl.Console(width, height)

    @property
    def width(self):
        return self.console.width

    @property
    def height(self):
        return self.console.height

    def draw_str(self, x, y, string, fg=Ellipsis, bg=None):
        self.console.draw_str(x, y, string, fg, bg)

    def clear(self, fg, bg):
        self.console.clear(fg, bg)

    def draw_rect(self, x, y, width, height, string, fg=Ellipsis, bg=None):
        self.console.draw_rect(x, y, width, height, string, fg, bg)
