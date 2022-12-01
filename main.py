from Game import Game
from MapMode import MapMode
import sys
import os

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        raise Exception("Usage: python main.py [input_image_path] [quadtree | opencv]")

    image_path = os.path.join(os.getcwd(), args[0])
    if not os.path.exists(image_path):
        raise Exception("Invalid image path.")

    mode = args[1].upper()
    if mode in MapMode.__members__:
        mode = MapMode[mode]
    else:
        raise Exception("Invalid mode. Must be 'quadtree' or 'opencv'.")

    Game(mode, image_path).run()
