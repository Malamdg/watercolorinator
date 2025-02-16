from collections import defaultdict

import numpy as np
import os
import time

from src.core.logger import Logger
from src.image_processing.color_reduction import ColorReducer
from src.image_processing.utils import read_image, get_color_array, array_to_matrix

# Initialize logger
logger = Logger.get_logger(__name__)


class ImageHandler:
    """
    Handles image loading, processing, and color extraction.
    """

    def __init__(self, with_benchmarking=False):
        """
        Initialize the ImageHandler class.

        :param with_benchmarking: Enable benchmarking for performance measurement.
        """
        self.benchmark = with_benchmarking
        self.color_map = {}  # Stores color (RGBA) to pixel coordinates
        self.colors = np.array([])  # List of unique colors in the image
        self.pixels = np.array([])  # Pixel matrix of the image
        self.reducer = ColorReducer()

    def handle(self, file_path):
        """
        Process the image: read it, map colors, and reduce the color count.

        :param file_path: Path to the image file.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File {file_path} does not exist.")

        if self.benchmark:
            logger.notice("Start handling image...")

        start_time = time.time()
        self.read_img(file_path)
        elapsed = time.time() - start_time
        logger.info(f"Image {file_path} successfully loaded in {elapsed:.4f} seconds.")

        start_time = time.time()
        self.build_map()
        elapsed = time.time() - start_time
        logger.info(f"Color map built in {elapsed:.4f} seconds.")

        start_time = time.time()
        self.reduce_color_count()
        elapsed = time.time() - start_time
        logger.info(f"Color reduction applied in {elapsed:.4f} seconds.")

    def read_img(self, file_path):
        """
        Read an image file and convert it to a pixel matrix.

        :param file_path: Path to the image file.
        """
        try:
            width, height, rgba_values, metadata = read_image(file_path)
            color_array = get_color_array(rgba_values)

            # Store the pixels as a matrix (height x width)
            self.pixels = array_to_matrix(color_array, height, width)
            self.colors = np.unique(self.pixels.reshape(-1, self.pixels.shape[-1]), axis=0)  # Unique colors

            logger.debug(f"Image {file_path} read with dimensions {width}x{height}.")

        except Exception as e:
            logger.error(f"Error reading image {file_path}: {e}")
            raise

    def build_map(self):
        """
        Build a color map linking each unique color to its pixel coordinates.
        """
        self.color_map = {}
        for y in range(self.pixels.shape[0]):  # Height
            for x in range(self.pixels.shape[1]):  # Width
                color = tuple(self.pixels[y, x])
                if color not in self.color_map:
                    self.color_map[color] = []
                self.color_map[color].append((x, y))

        logger.debug("Color map constructed.")

    def reduce_color_count(self):
        """
        Reduce the number of colors in the image and update the color map.
        """
        self.colors, color_reduction_map = self.reducer.reduce(self.colors)

        reduced_color_map = defaultdict(list)

        # Apply color reduction on the color map
        for original_color, reduced_color in color_reduction_map.items():
            if original_color in self.color_map:  # Ensure the original color exists
                reduced_color_map[tuple(reduced_color)].extend(self.color_map[original_color])

        self.color_map = dict(reduced_color_map)
        # Apply reduced colors efficiently using `color_map`
        for reduced_color, pixel_positions in self.color_map.items():
            for x, y in pixel_positions:
                self.pixels[y, x] = reduced_color  # Direct assignment

        logger.debug("Colors reduced successfully.")