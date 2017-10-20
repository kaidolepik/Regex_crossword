from Board import Board
import itertools

class Solver:

    def __init__(self, board):
        self.board = board

    def solve_k_tiles_simultaneously(self, tiles, k):
        solved_tiles = []

        for k_tiles_tuple in itertools.combinations(tiles, k):
            matching_combinations = [combination for combination in itertools.product(*[tile.get_matching_letters() for tile in k_tiles_tuple])]
            matched_regexes = set()

            for tile_to_match in k_tiles_tuple:
                regexes = set(tile_to_match.get_regexes()) - matched_regexes
                for regex in regexes:
                    matching_combinations = regex.match_combinations(matching_combinations, tile_to_match, k_tiles_tuple)
                    matched_regexes.add(regex)

            if len(matching_combinations) == 1:
                for letter, tile in zip(matching_combinations[0], k_tiles_tuple):
                    tile.set_value(letter)

                solved_tiles = [tile for tile in k_tiles_tuple]
                break

        if len(solved_tiles) > 0:
            self.board.draw_tile(solved_tiles)

        return solved_tiles

    def solve_single_tiles(self, unsolved_tiles):
        solved_tiles = []

        for tile in unsolved_tiles:
            matching_letters = tile.get_matching_letters()

            for regex in tile.get_regexes():
                matching_letters = regex.match_letters_in_tile(matching_letters, tile)
            tile.set_matching_letters(matching_letters)

            if len(matching_letters) == 1:
                tile.set_value(matching_letters[0])
                solved_tiles.append(tile)
                self.board.draw_tile([tile])

        return solved_tiles

    def solve_crossword(self):
        unsolved_tiles = [self.board.get_tiles()[pos_coords] for pos_coords in sorted(self.board.get_tiles().keys())]

        while len(unsolved_tiles) != 0:
            solved_tiles = self.solve_single_tiles(unsolved_tiles)

            if len(solved_tiles) == 0:
                k = 2
                while len(solved_tiles) == 0 and k <= len(unsolved_tiles):
                    solved_tiles = self.solve_k_tiles_simultaneously(unsolved_tiles, k)
                    k += 1

                if len(solved_tiles) == 0:
                    break # There is no unique solution to the crossword
                self.board.draw_tile(solved_tiles)

            unsolved_tiles = [tile for tile in unsolved_tiles if tile not in solved_tiles]


if __name__ == "__main__":
    board = Board()
    solver = Solver(board)
    solver.solve_crossword()
    board.destroy()
