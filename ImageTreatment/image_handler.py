import time
import png
import numpy as np


class ImageHandler:
    def __init__(self, with_benchmarking=False):
        self.benchmark = with_benchmarking
        self.color_map = dict()  # maps a color (rgba) to a list of coordinates
        self.colors = []  # lists the colors of the image
        self.pixels = []  # pixel matrix of the image

    def handle(self, fp):
        start_time = 0

        self.benchmark and print(f"Start Handling image".center(80, "-"))

        if self.benchmark:
            start_time = time.time()

        self.read_img(fp)
        self.benchmark and print(f'Image read in {time.time() - start_time}s')

        if self.benchmark:
            start_time = time.time()

        self.build_map()
        self.benchmark and print(f"Color map built in {time.time() - start_time}s")

        if self.benchmark:
            start_time = time.time()

        self.reduce_color_count()
        self.benchmark and print(f"Colors reduced in {time.time() - start_time}s")

    def read_img(self, fp):
        """
        Read an image and build the corresponding attributes.

        :param fp:
        :return:
        """
        image = open(fp, 'rb') # open file read + binary mode
        reader = png.Reader(file=image) # load image file content in the reader object
        width, height, rgba_values, metadata = reader.read_flat() # get treatment useful values from the reader
        image.close() # close the file


        rgba_list = rgba_values.tolist() # flat RGBA values are disposed in a list
        color_count = int(len(rgba_list) / 4) # color count is the number of items / 4 (R, B, G, A = 4 values)

        # Convert the rgba list to a RGBAColor list
        color_list = [
            np.array([rgba_list[4 * i], rgba_list[4 * i + 1], rgba_list[4 * i + 2], rgba_list[4 * i + 3]]) for i in
            range(color_count)
        ]

        # store the colors from the image to a list with only unique values

        self.pixels = [color_list[i * width: (i + 1) * width] for i in range(height)] # convert the color list to a matrix in order to display an image


    def build_map(self):
        pass

    def reduce_color_count(self):
        pass
