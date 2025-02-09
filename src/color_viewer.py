import matplotlib.pyplot as plt
from image_handler import ImageHandler
from core.logger import Logger

# Initialize logger
logger = Logger.get_logger(__name__)

def visualize_colors(color_list):
    """
    Plot a 3D scatter plot of RGB colors extracted from an image.

    :param color_list: Numpy array of shape (N, 4) containing RGBA colors.
    """
    if color_list.size == 0:
        logger.warning("No colors available for visualization.")
        return

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Extract RGB components
    r, g, b, a = color_list[:, 0], color_list[:, 1], color_list[:, 2], color_list[:, 3] / 255.0  # Normalize alpha

    # Scatter plot of colors
    ax.scatter(r, g, b, c=color_list[:, :3] / 255.0, alpha=a, s=10)

    # Set axes limits
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)

    # Labels
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title(f'3D Color Scatter Plot ({len(color_list)} unique colors)')

    logger.info(f"Displaying color scatter plot with {len(color_list)} unique colors.")
    plt.show()

if __name__ == "__main__":
    # Example usage
    img_handler = ImageHandler(with_benchmarking=True)
    img_handler.handle("example.png")  # Replace with your image file

    visualize_colors(img_handler.colors)
