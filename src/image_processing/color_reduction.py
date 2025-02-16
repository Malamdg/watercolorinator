import numpy as np
from sklearn.cluster import KMeans
from src.core.logger import Logger
from src.core.config import config

# Initialize logger
logger = Logger.get_logger(__name__)

class ColorReductionStrategy:
    """
    Abstract base class for color reduction strategies.
    """

    def reduce(self, colors):
        """
        Reduce the number of colors in the given color array.

        :param colors: Numpy array of shape (N, 4) containing RGBA values.
        :return: Tuple (reduced_colors, color_map)
        """
        raise NotImplementedError("Color reduction strategy must implement the `reduce` method.")

class KMeansColorReducerAlphaLayering(ColorReductionStrategy):
    """
    Color reducer using K-Means clustering in 3D (RGB), applied per alpha layer.
    """

    def __init__(self, k=16):
        """
        Initialize the K-Means reducer with a specified number of clusters.

        :param k: Number of color clusters per alpha layer.
        """
        self.k = k

    def reduce(self, colors):
        """
        Apply K-Means clustering to reduce the number of colors.

        :param colors: Numpy array of shape (N, 4) containing RGBA values.
        :return: Tuple (reduced_colors, color_map)
        """
        unique_alphas = np.unique(colors[:, 3])  # Extract unique alpha values
        reduced_colors = []
        color_map = {}

        logger.info(f"Unique alphas : {unique_alphas}")

        for alpha in unique_alphas:
            mask = (colors[:, 3] == alpha)
            rgba_values = colors[mask]  # Extract full RGBA values for this alpha layer

            if len(rgba_values) == 0:
                continue  # Skip empty layers

            logger.info(f"Applying K-Means on alpha={alpha} layer with {len(rgba_values)} colors.")

            # Apply K-Means clustering on RGB values only (not alpha)
            kmeans = KMeans(n_clusters=min(self.k, len(rgba_values)), random_state=42, n_init=10)
            labels = kmeans.fit_predict(rgba_values[:, :3])  # Use only RGB for clustering
            cluster_centers = kmeans.cluster_centers_.astype(np.uint8)

            # Append the alpha channel back to cluster centers
            cluster_centers = np.hstack((cluster_centers, np.full((cluster_centers.shape[0], 1), alpha, dtype=np.uint8)))

            # Build the color map: original color -> closest cluster center (preserving alpha)
            for original, label in zip(rgba_values, labels):
                cluster_color = tuple(cluster_centers[label])
                color_map[tuple(original)] = cluster_color  # Mapping original -> reduced color

            # Store reduced colors with alpha
            reduced_colors.extend(cluster_centers)

        return np.array(reduced_colors, dtype=np.uint8), color_map

class ColorReducer:
    """
    Facade for managing color reduction strategies.
    """

    def __init__(self):
        """
        Load the configured strategy for color reduction.
        """
        strategy_name = config.get("app.color_reduction.strategy", "kmeans")

        if strategy_name == "kmeans_alpha":
            k = config.get(f"app.color_reduction.strategies.{strategy_name}.k", 16)
            self.strategy = KMeansColorReducerAlphaLayering(k)
        else:
            raise ValueError(f"Unknown color reduction strategy: {strategy_name}")

        logger.info(f"Loaded color reduction strategy: {strategy_name}")

    def reduce(self, colors):
        """
        Apply the configured reduction strategy.

        :param colors: Numpy array of shape (N, 4) containing RGBA values.
        :return: Tuple (reduced_colors, color_reduction_map)
        """
        return self.strategy.reduce(colors)
