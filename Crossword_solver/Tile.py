from collections import defaultdict
import config
import string

class Tile:

    def __init__(self, pos_coords, xy_coords):
        self.pos_coords = pos_coords
        self.xy_coords = xy_coords
        self.regexes = []
        self.backref_companions = defaultdict(list)
        self.value = config.univ_char
        self.matching_letters = string.ascii_uppercase

    def add_regex(self, regex):
        self.regexes.append(regex)

    def add_backref_companions(self, regex, companion_tiles, companion_units):
        self.backref_companions[regex].append({"companion_tiles": companion_tiles, "companion_units": companion_units})

    def get_regexes(self):
        return self.regexes

    def get_backref_companions(self, regex):
        return self.backref_companions[regex]

    def get_value(self):
        return self.value

    def get_pos_coords(self):
        return self.pos_coords

    def get_xy_coords(self):
        return self.xy_coords

    def get_matching_letters(self):
        return self.matching_letters

    def set_value(self, value):
        self.value = value

    def set_universal_value(self):
        self.set_value(config.univ_char)

    def set_matching_letters(self, matching_letters):
        self.matching_letters = matching_letters

    def is_universal_value(self):
        return self.value == config.univ_char

    def __str__(self):
        return str(self.get_pos_coords()) + ", " + self.get_value() + ", " + " ".join(str(regex) for regex in self.regexes)
