import time
import numpy as np
import imageio.v3 as iio
import psutil
from logger import Logger  # Import our custom logger


class ImageHandler:
    def __init__(self, with_benchmarking: bool = False):
        """Initialize the ImageHandler with structured logging and benchmarking."""
        self.benchmark = with_benchmarking
        self.pixels = None
        self.colors = None
        self.logger = Logger.get_logger(self.__class__.__name__)  # Dedicated logger

    def handle(self, file_path: str):
        """Main processing function: load, analyze, and monitor image data."""
        self.logger.info(f"Processing image: {file_path}")

        self._benchmark_step("Image Loading", self.read_img, file_path)
        self._benchmark_step("Unique Colors Extraction", self.extract_unique_colors)

        self.logger.info("Processing completed successfully.")

    def read_img(self, file_path: str):
        """Read an image file and store it as a NumPy array."""
        try:
            image = iio.imread(file_path)  # Load image as NumPy array
            if image.shape[-1] != 4:
                raise ValueError("Expected an RGBA image (4 channels).")

            self.pixels = image.astype(np.uint8)  # Ensure uint8 type (0-255)
        except Exception as e:
            self.logger.error(f"Failed to load image: {e}")
            self.pixels = None

    def extract_unique_colors(self):
        """Extract unique RGBA colors from the image."""
        if self.pixels is None:
            self.logger.warning("No image data found. Skipping color extraction.")
            return

        self.colors = np.unique(self.pixels.reshape(-1, 4), axis=0)
        self.logger.info(f"Unique colors found: {len(self.colors)}")

    def _benchmark_step(self, step_name: str, func, *args):
        """Benchmark a specific function and log execution time and memory usage."""
        if self.benchmark:
            self.logger.info(f"--- {step_name} ---")
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # MB

            func(*args)  # Execute function

            elapsed_time = time.time() - start_time
            end_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
            memory_usage = end_memory - start_memory

            self.logger.info(f"{step_name} completed in {elapsed_time:.4f}s | Memory Used: {memory_usage:.2f} MB")


# Example Usage
if __name__ == "__main__":
    handler = ImageHandler(with_benchmarking=True)
    handler.handle("example.png")  # Replace with your image file
