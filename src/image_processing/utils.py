import numpy as np
import png


def read_image(fp: str):
    """
    Reads an image file and extracts its metadata and pixel values.

    :param fp: Path to the image file.
    :return: Tuple (width, height, rgba_values, metadata)
    """
    try:
        with open(fp, 'rb') as img_file:
            reader = png.Reader(file=img_file)
            width, height, rgba_values, metadata = reader.read_flat()

        return width, height, np.array(rgba_values, dtype=np.uint8), metadata

    except Exception as e:
        raise IOError(f"Error reading image {fp}: {e}")


def get_color_array(rgba_values: np.ndarray):
    """
    Converts a flat RGBA pixel array into a structured 2D color array.

    :param rgba_values: Numpy array containing RGBA values in a flat format.
    :return: Numpy array of shape (N, 4) with RGBA color values.
    """
    color_count = len(rgba_values) // 4  # 4 values per pixel (R, G, B, A)

    # Reshape the flat array into (N, 4) where N is the number of pixels
    return rgba_values.reshape((color_count, 4))


def array_to_matrix(color_array: np.ndarray, height: int, width: int):
    """
    Converts a flat color array into an image matrix.

    :param color_array: Numpy array of shape (N, 4) with RGBA values.
    :param height: Image height.
    :param width: Image width.
    :return: Numpy array of shape (H, W, 4) representing the image.
    """
    return color_array.reshape((height, width, 4))


def get_color_matrix(fp: str):
    """
    Reads an image and returns its pixel matrix.

    :param fp: Path to the image file.
    :return: Numpy array of shape (H, W, 4) containing the image pixels.
    """
    width, height, rgba_values, metadata = read_image(fp)
    color_array = get_color_array(rgba_values)
    return array_to_matrix(color_array, height, width)

def compute_luminance(rgb_values):
    """
    Compute luminance based on human perception.

    :param rgb_values: Numpy array of shape (N, 3) containing RGB values.
    :return: Numpy array of shape (N, 1) with luminance values.
    """
    return 0.2126 * rgb_values[:, 0] + 0.7152 * rgb_values[:, 1] + 0.0722 * rgb_values[:, 2]