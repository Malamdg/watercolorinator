from ImageTreatment.image_handler import ImageHandler


def main():
    handler = ImageHandler(with_benchmarking=True)
    handler.handle('Images/test.png')

    print(f"COLOR COUNT: {len(handler.colors)}")


if __name__ == '__main__':
    main()
