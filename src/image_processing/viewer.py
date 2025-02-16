import matplotlib.pyplot as plt
import numpy as np

from src.core.logger import Logger
from src.image_processing.image_handler import ImageHandler
from src.image_processing.utils import get_color_matrix

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

def compare_images(source, target):
    """
    Compare two images and visualize the differences.

    :param source: Path to the original image or numpy array of shape (H, W, 4).
    :param target: Numpy array of shape (H, W, 4) containing the reduced image.
    """
    # Load the source image if it's a file path
    if isinstance(source, str):
        source = get_color_matrix(source)

    if source.shape != target.shape:
        logger.warning(f"Image dimensions do not match: {source.shape} vs {target.shape}")
        return

    # Compute absolute differences in RGB channels
    diff = np.abs(source[:, :, :3] - target[:, :, :3])  # Ignore alpha for comparison
    diff_sum = np.sum(diff, axis=2)  # Sum differences across R, G, B

    # Normalize difference map for visualization
    diff_normalized = (diff_sum / diff_sum.max()) if diff_sum.max() > 0 else diff_sum

    # Visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(source.astype(np.uint8))
    axes[0].set_title("Original Image")
    axes[0].axis("off")

    axes[1].imshow(target.astype(np.uint8))
    axes[1].set_title("Reduced Image")
    axes[1].axis("off")

    heatmap = axes[2].imshow(diff_normalized, cmap="hot", interpolation="nearest")
    axes[2].set_title("Difference Heatmap")
    axes[2].axis("off")
    fig.colorbar(heatmap, ax=axes[2], fraction=0.046, pad=0.04)

    logger.info("Displaying image comparison.")
    plt.show()

if __name__ == "__main__":
    # Example usage
    img_handler = ImageHandler(with_benchmarking=True)
    img_handler.handle("../../Images/test.png")  # Replace with your image file

    visualize_colors(img_handler.colors)
