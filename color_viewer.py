import matplotlib.pyplot as plt


def visualize_colors(color_list):
    """
    Visualize a list of RGBA colors in a 3D scatter plot.

    :param color_list: NumPy array of shape (N, 4) where N is the number of colors
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Extract color components
    r, g, b, a = color_list[:, 0], color_list[:, 1], color_list[:, 2], color_list[:, 3] / 255.0  # Normalize alpha

    # Plot the colored points
    ax.scatter(r, g, b, c=color_list[:, :3] / 255.0, alpha=a, s=10)

    # Axes definition
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 255)

    # Labels
    ax.set_xlabel('Red (R)')
    ax.set_ylabel('Green (G)')
    ax.set_zlabel('Blue (B)')
    ax.set_title('3D Color Scatter Plot')

    # Add legend with number of unique colors
    unique_colors_count = len(color_list)
    legend_text = f"Unique Colors: {unique_colors_count}"

    # Display legend outside the plot to avoid cluttering
    ax.text2D(0.05, 0.05, legend_text, transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.6))

    plt.show()
