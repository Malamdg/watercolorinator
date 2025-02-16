from src.image_processing.viewer import visualize_colors, compare_images
from src.core.logger import Logger
from src.image_processing.image_handler import ImageHandler

TEST_FP = '../Images/test.png'

def initialize():
    """App initialization"""
    logger = Logger.get_logger("Watercolorinator")
    logger.info("Initializing application...")
    return logger

def run(logger):
    """Main application logic."""
    logger.info("Starting Watercolorinator...")
    handler = ImageHandler(with_benchmarking=True)
    handler.handle(TEST_FP)

    visualize_colors(handler.colors)
    compare_images(TEST_FP, handler.pixels)
    logger.info("Application finished.")

