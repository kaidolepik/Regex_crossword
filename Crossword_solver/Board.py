import config
import cv2
import numpy as np
from Regex import Regex
from Tile import Tile

class Board:

    def __init__(self):
        self.tiles = {}
        self.create_tiles()
        self.board_image = np.copy(cv2.imread(config.grid_file))
        self.video = cv2.VideoWriter(config.crossword_out_video_file, cv2.cv.CV_FOURCC(*"avc1"), config.cv2_fps, (self.board_image.shape[1], self.board_image.shape[0]))
        self.video.write(self.board_image)

    def destroy(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_tiles(self):
        return self.tiles

    def row_first_coordinates(self, pos):
        max_right = (6 + pos) if pos < 7 else (20 - pos)
        row = pos

        return row, max_right

    def row_tile_coordinates(self, max_right, left):
        return max_right + 1 - left

    def left_first_coordinates(self, pos):
        if pos < 7:
            start_row = 13
            end_row = 8 - pos
        else:
            start_row = 20 - pos
            end_row = 1
        start_left = pos

        return (start_row, end_row, start_left)

    def left_tile_coordinates(self, row, start_left):
        if row < 7:
            left = start_left + row - 7
            right = 7 + row - left
        else:
            left = start_left
            right = 21 - row - left

        return (left, right)

    def right_first_coordinates(self, pos):
        if pos < 7:
            start_row = 8 - pos
            end_row = 13
            start_right = 1
        else:
            start_row = 1
            end_row = 20 - pos
            start_right = pos - 6

        return (start_row, end_row, start_right)

    def right_tile_coordinates(self, row, start_row, start_right):
        if row < 7:
            right = start_right + row - start_row
            left = 7 + row - right
        else:
            right = 7 + start_right - start_row
            left = 21 - row - right

        return (left, right)

    def calc_xy_coords(self, row, left):
        height = config.height_start + config.height_step * (row - 1)
        width = config.width_start - config.width_step * (6 - abs(7 - row)) / 2 + config.width_step * (left - 1)

        return (width, height)

    def draw_tile(self, tiles):
        for tile in tiles:
            cv2.putText(img = self.board_image, text = tile.get_value(), org = tile.get_xy_coords(), fontFace = config.font_face,
                        fontScale = config.font_scale, color = config.font_color, thickness = config.font_thickness)
        self.video.write(self.board_image)
        cv2.imshow("Crossword", self.board_image)
        cv2.waitKey(config.cv2_waitKey)

    def process_tile(self, pos_coords, regex):
        if pos_coords not in self.tiles:
            xy_coords = self.calc_xy_coords(row = pos_coords[0], left = pos_coords[1])
            tile = Tile(pos_coords, xy_coords)
            self.tiles[pos_coords] = tile
        else:
            tile = self.tiles[pos_coords]

        tile.add_regex(regex)
        regex.add_tile(tile)

    def create_row_regex_tiles(self, regex, pos):
        row, max_right = self.row_first_coordinates(pos)
        for left in xrange(1, max_right + 1):
            right = self.row_tile_coordinates(max_right, left)

            self.process_tile((row, left, right), regex)

    def create_left_regex_tiles(self, regex, pos):
        start_row, end_row, start_left = self.left_first_coordinates(pos)
        for row in xrange(start_row, end_row - 1, -1):
            left, right = self.left_tile_coordinates(row, start_left)

            self.process_tile((row, left, right), regex)

    def create_right_regex_tiles(self, regex, pos):
        start_row, end_row, start_right = self.right_first_coordinates(pos)
        for row in xrange(start_row, end_row + 1):
            left, right = self.right_tile_coordinates(row, start_row, start_right)

            self.process_tile((row, left, right), regex)

    def create_tiles(self):
        with open(config.crossword_file, "r") as fin:
            fin.readline()

            for line in fin:
                regex_info = line.strip().split(" ")
                pattern, type = regex_info[:2]
                pos = int(regex_info[2])
                regex = Regex(pattern)

                if type == "row":
                    self.create_row_regex_tiles(regex, pos)
                elif type == "left":
                    self.create_left_regex_tiles(regex, pos)
                elif type == "right":
                    self.create_right_regex_tiles(regex, pos)

                if len(regex_info) > 3:
                    regex.process_backref_paths(regex_info[3:])
