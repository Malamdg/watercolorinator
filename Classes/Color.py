
class RGBColor:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

class RGBAColor(RGBColor):
    def __init__(self, r: int, g: int, b: int, a: int):
        super().__init__(r, g, b)
        self.a = a

    def get_rgb(self):
        return RGBColor(self.r, self.g, self.b)