from ImageTreatment.image_handler import ImageHandler


def main():
    image = open('./Images/test.png', 'rb')
    handler = ImageHandler()
    handler.handle(image)
    i = 0
    for color in handler.colors:
        i += 1
        print(f"Color #{i} :  {color}")
    return


if __name__ == '__main__':
    main()
