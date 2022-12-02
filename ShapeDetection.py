import cv2


def convert(image_path, width, height):
    # reading image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (width, height))

    # converting image into grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        shape = []
        for point in approx:
            shape.append(point.flatten().tolist())
        color = (255, 255, 255)
        rects.append((shape, color))

    rects = [rect for rect in rects if len(rect[0]) > 2]
    rects = rects[1:]  # omit full screen rect

    return rects


if __name__ == "__main__":
    convert("images/shapes.png")
