import numpy as np
import png
import os
import time

from src.color_viewer import visualize_colors
from src.core.logger import Logger
from src.image_processing.color_reduction import ColorReducer

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
            with open(file_path, 'rb') as img_file:
                reader = png.Reader(file=img_file)
                width, height, rgba_values, metadata = reader.read_flat()

            rgba_list = rgba_values.tolist()
            color_count = len(rgba_list) // 4  # 4 values per pixel (RGBA)

            # Convert list to an array of RGBA colors
            color_array = np.array([
                [rgba_list[4 * i], rgba_list[4 * i + 1], rgba_list[4 * i + 2], rgba_list[4 * i + 3]]
                for i in range(color_count)
            ])

            # Store the pixels as a matrix (height x width)
            self.pixels = color_array.reshape((height, width, 4))
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
        Reduce the number of colors in the image (simple implementation for now).
        """
        self.colors, color_map = self.reducer.reduce(self.colors)