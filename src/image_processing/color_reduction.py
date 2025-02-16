import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from src.core.logger import Logger
from src.core.config import config
from src.image_processing.utils import compute_luminance

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

class AlphaLayeringKMeansColorReducer(ColorReductionStrategy):
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

class LuminanceKMeansReducer(ColorReductionStrategy):
    """
    Color reducer using K-Means clustering based on color luminance.
    """

    def __init__(self, k_luminance=8, k_color=16):
        """
        Initialize the K-Means reducer with separate clusters for luminance and color.

        :param k_luminance: Number of luminance clusters.
        :param k_color: Number of color clusters per luminance group.
        """
        self.k_luminance = k_luminance
        self.k_color = k_color

    def reduce(self, colors):
        """
        Apply K-Means clustering based on luminance and then reduce colors.

        :param colors: Numpy array of shape (N, 4) containing RGBA values.
        :return: Tuple (reduced_colors, color_map)
        """
        # Extract RGB and Alpha channels
        rgb_values = colors[:, :3]
        alpha_values = colors[:, 3]

        # Compute luminance values
        luminance = compute_luminance(rgb_values).reshape(-1, 1)

        # Apply K-Means clustering on luminance
        kmeans_luminance = KMeans(n_clusters=min(self.k_luminance, len(luminance)), random_state=42, n_init=10)
        luminance_labels = kmeans_luminance.fit_predict(luminance)

        reduced_colors = []
        color_map = {}

        # Process each luminance cluster separately
        for luminance_group in range(self.k_luminance):
            mask = (luminance_labels == luminance_group)
            cluster_rgb = rgb_values[mask]
            cluster_alpha = alpha_values[mask]

            if len(cluster_rgb) == 0:
                continue

            logger.info(f"Applying K-Means on luminance group {luminance_group} with {len(cluster_rgb)} colors.")

            # Apply K-Means on RGB within each luminance group
            kmeans_rgb = KMeans(n_clusters=min(self.k_color, len(cluster_rgb)), random_state=42, n_init=10)
            rgb_labels = kmeans_rgb.fit_predict(cluster_rgb)
            cluster_centers = kmeans_rgb.cluster_centers_.astype(np.uint8)

            # Append the average alpha value for each cluster
            cluster_alpha_mean = np.array([np.mean(cluster_alpha[rgb_labels == i]) for i in range(len(cluster_centers))], dtype=np.uint8)
            cluster_centers = np.hstack((cluster_centers, cluster_alpha_mean.reshape(-1, 1)))

            # Build the color map
            for original, label in zip(cluster_rgb, rgb_labels):
                cluster_color = tuple(cluster_centers[label])
                color_map[tuple(original)] = cluster_color  # Mapping original -> reduced color

            reduced_colors.extend(cluster_centers)

        return np.array(reduced_colors, dtype=np.uint8), color_map

class AutoAdaptiveColorReducer:
    """
    Adaptive color reducer using K-Means clustering with dynamic determination of cluster count.
    """

    def __init__(self, max_clusters=32):
        """
        Initialize the adaptive reducer with a max number of clusters.

        :param max_clusters: Maximum number of clusters to consider.
        """
        self.max_clusters = max_clusters

    def determine_optimal_k(self, rgb_values):
        """
        Determine the optimal number of clusters using silhouette analysis.

        :param rgb_values: Numpy array of shape (N, 3) containing RGB values.
        :return: Optimal number of clusters.
        """
        if len(rgb_values) < 10:
            return min(3, len(rgb_values))  # If very few colors, no need for many clusters

        best_k = 2
        best_score = -1

        for k in range(2, min(self.max_clusters, len(rgb_values) - 1)):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(rgb_values)
            score = silhouette_score(rgb_values, labels)

            if score > best_score:
                best_k = k
                best_score = score

        logger.info(f"Optimal number of clusters determined: {best_k}")
        return best_k

    def reduce(self, colors):
        """
        Apply an adaptive K-Means clustering on luminance groups followed by RGB clustering.

        :param colors: Numpy array of shape (N, 4) containing RGBA values.
        :return: Tuple (reduced_colors, color_map)
        """
        # Extract RGB and Alpha channels
        rgb_values = colors[:, :3]
        alpha_values = colors[:, 3]

        # Compute luminance values
        luminance = compute_luminance(rgb_values).reshape(-1, 1)

        # Determine optimal number of luminance clusters
        k_luminance = self.determine_optimal_k(luminance)

        # Apply K-Means clustering on luminance
        kmeans_luminance = KMeans(n_clusters=k_luminance, random_state=42, n_init=10)
        luminance_labels = kmeans_luminance.fit_predict(luminance)

        reduced_colors = []
        color_map = {}

        # Process each luminance cluster separately
        for luminance_group in range(k_luminance):
            mask = (luminance_labels == luminance_group)
            cluster_rgb = rgb_values[mask]
            cluster_alpha = alpha_values[mask]

            if len(cluster_rgb) == 0:
                continue

            # Determine optimal K for this RGB group
            k_rgb = self.determine_optimal_k(cluster_rgb)

            logger.info(f"Applying K-Means on luminance group {luminance_group} with {k_rgb} clusters.")

            # Apply K-Means on RGB within each luminance group
            kmeans_rgb = KMeans(n_clusters=k_rgb, random_state=42, n_init=10)
            rgb_labels = kmeans_rgb.fit_predict(cluster_rgb)
            cluster_centers = kmeans_rgb.cluster_centers_.astype(np.uint8)

            # Append the average alpha value for each cluster
            cluster_alpha_mean = np.array([np.mean(cluster_alpha[rgb_labels == i]) for i in range(len(cluster_centers))], dtype=np.uint8)
            cluster_centers = np.hstack((cluster_centers, cluster_alpha_mean.reshape(-1, 1)))

            # Build the color map using RGBA values
            for original_rgb, original_alpha, label in zip(cluster_rgb, cluster_alpha, rgb_labels):
                original_rgba = (*original_rgb, original_alpha)  # Convert RGB to RGBA
                cluster_color = tuple(cluster_centers[label])  # Ensure the reduced color is also RGBA
                color_map[original_rgba] = cluster_color  # Mapping original RGBA -> reduced RGBA

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

        if strategy_name == "alpha_kmeans":
            k = config.get(f"app.color_reduction.strategies.{strategy_name}.k", 16)
            self.strategy = AlphaLayeringKMeansColorReducer(k)
        elif strategy_name == "luminance_kmeans":
            k_luminance = config.get(f"app.color_reduction.strategies.{strategy_name}.k_luminance", 16)
            k_color = config.get(f"app.color_reduction.strategies.{strategy_name}.k_color", 16)
            self.strategy = LuminanceKMeansReducer(k_luminance=k_luminance, k_color=k_color)
        elif strategy_name == "auto_adaptive":
            self.strategy = AutoAdaptiveColorReducer()
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
