from ImageTreatment.image_handler import ImageHandler
from color_viewer import visualize_colors


def main():
    handler = ImageHandler(with_benchmarking=True)
    handler.handle('Images/test.png')

    visualize_colors(handler.colors)


if __name__ == '__main__':
    main()
