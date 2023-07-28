import png
from Classes.Color import RGBAColor
def extractColors(pixel_map):
    pixels = []
    for row in pixel_map:
        for pixel in row:
            if not(pixel in pixels):
                pixels.append(pixel)
    pixels.sort()
    return pixels


def createPixelList(rgba_values):
    pixels = []
    rgba_values_list = rgba_values.tolist()
    for i in range(0, len(rgba_values), 4):
        pixel = RGBAColor(rgba_values_list[i], rgba_values_list[i+1], rgba_values_list[i+2], rgba_values_list[i+3])
        pixels.append(pixel)
    return pixels


def convertListToMap(pixel_list, width, height):
    pixel_map = []
    for i in range(height):
        row_i = pixel_list[i*width: i*width + width]
        pixel_map.append(row_i)
    return pixel_map


def buildPixelMap(rgba_values, width, height):
    pixel_list = createPixelList(rgba_values)
    return convertListToMap(pixel_list, width, height)


def getAllOccurrences(color, pixel_map):
    occurrences = []
    height = len(pixel_map)
    width = len(pixel_map[height - 1])
    for i in range(height):
        for j in range(width):
            pixel = pixel_map[i][j]
            if pixel == color:
                occurrences.append((i, j))
    return occurrences


def determineColorLayers(pixel_map, colors):
    layers = []
    for i in range(len(colors)):
        color = colors[i]
        layer = getAllOccurrences(color, pixel_map)
        layers.append(layer)
    return layers


class ImageHandler:
    def __init__(self):
        self.size = ()
        self.pixel_map = []  # pixel list, list
        self.colors = []  # RGBAColor
        self.layers = []  # RGBAColor indexes => Coordinates list [(x, y), ...]

    def handle(self, image):
        reader = png.Reader(file=image)
        width, height, rgba_values, metadata = reader.read_flat()
        image.close()

        self.size = (width, height)
        self.pixel_map = buildPixelMap(rgba_values, int(width), int(height))
        self.colors = extractColors(self.pixel_map)
        self.layers = determineColorLayers(self.pixel_map, self.colors)
        return self
