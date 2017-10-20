import re
import config

class Regex:

    def __init__(self, pattern):
        self.orig_pattern = pattern
        self.pattern = self.modify_pattern(pattern)
        self.tiles = []
        self.backref_paths = []

    def add_tile(self, tile):
        self.tiles.append(tile)

    def modify_pattern(self, pattern):
        pattern = re.sub(r"(\[[A-Z]+)", r"\1" + config.univ_char, pattern)
        pattern = re.sub(r"([A-Z](?![^\[]*\]))", r"[\1" + config.univ_char + "]", pattern)
        pattern = "^" + pattern + "$"

        return pattern

    def process_backref_paths(self, paths):
        for path in paths:
            self.process_backref_units(path)

    def process_backref_units(self, path):
        units = [[self.tiles[int(tile_nr) - 1] for tile_nr in unit.strip().split("-")] for unit in path.strip().split(";")]

        for i in xrange(0, len(units)):
            unit = units[i]
            companion_units = units[:i] + units[i+1:]
            self.process_backref_companions(unit, companion_units)

        tiles_in_units = [tile for unit in units for tile in unit]
        for tile in self.tiles:
            if tile not in tiles_in_units:
                self.process_backref_companions([tile], units)

    def process_backref_companions(self, unit, companion_units):
        for i in xrange(0, len(unit)):
            tile = unit[i]
            companion_tiles = unit[:i] + unit[i+1:]
            tile.add_backref_companions(self, companion_tiles, companion_units)

    def is_match(self, regex_string):
        is_match = bool(re.match(self.pattern, regex_string))

        return is_match

    def regex_string(self, units, letter, conditions = None):
        tile_letter = {tile: (letter if tile.is_universal_value() else tile.get_value()) for tile in units[0]}
        if conditions != None:
            for tile, letter in conditions.items():
                tile_letter[tile] = letter

        for unit in units[1]:
            for unit_tile in unit:
                unit_letter = unit_tile.get_value()
                if unit_letter != config.univ_char:
                    for tile in unit:
                        if tile.get_value() == config.univ_char and tile not in tile_letter:
                            tile_letter[tile] = unit_letter
                    break

        regex_string = "".join([tile_letter[tile] if tile in tile_letter else tile.get_value() for tile in self.tiles])

        return regex_string

    def match_letters_in_tile(self, letters, tile, conditions = None):
        backref_companions = tile.get_backref_companions(self)
        backref_units = [([tile], [])] if len(backref_companions) <= 0 else [(companion["companion_tiles"] + [tile], companion["companion_units"]) for companion in backref_companions]

        matched_letters = []
        for letter in letters:
            for units in backref_units:
                regex_string = self.regex_string(units, letter, conditions)
                if self.is_match(regex_string):
                    matched_letters.append(letter)
                    break

        return matched_letters

    def match_combinations(self, combinations, tile_to_match, tiles):
        matched_combinations = []

        for combination in combinations:
            conditions = {}
            letter_to_match = config.univ_char

            for letter, tile in zip(combination, tiles):
                if tile == tile_to_match:
                    letter_to_match = letter
                else:
                    conditions[tile] = letter

            matched_letter = self.match_letters_in_tile(letter_to_match, tile_to_match, conditions)
            if len(matched_letter) != 0:
                matched_combinations.append(combination)

        return matched_combinations

    def __str__(self):
        return self.pattern
