from src.core.logger import Logger
from src.image_handler import ImageHandler
from src.color_viewer import visualize_colors

def initialize():
    """App initialization"""
    logger = Logger.get_logger("Watercolorinator")
    logger.info("Application en cours d'initialisation...")
    return logger

def run(logger):
    """Main application logic."""
    logger.info("Starting Watercolorinator...")
    handler = ImageHandler(with_benchmarking=True)
    handler.handle('../Images/test.png')

    visualize_colors(handler.colors)
    logger.info("Application finished.")

