# Regex crossword solver

An algorithm that solves the [regular expression crossword](http://www.i-programmer.info/news/144-graphics-and-games/5450-can-you-do-the-regular-expression-crossword.html) in less than 1 second.

### Solving the crossword

The idea is to always keep the crossword in a true state such that every pattern evaluates true against their respective regular expressions at all times. First, we try to find a unique character to each tile in isolation such that maintains the true state. If not possible, we look at 2, 3, ... tiles at a time until we find a unique combination of matching characters. Then we continue by looking at each tile independently again.

### Pre-processing regular expressions

Keeping the true state at all times requires some initial pre-processing of the regular expressions. For this, define a "universal character" "-" that does not belong to the alphabet. At first, every tile in the crossword gets the value "-" and every regex is modified such that all the patterns evaluate true:
* In a normal (not negated) character class, "-" is added, e.g. [CR] would become [CR-].
* Every character not in a class is put in one alongside "-", e.g. H would become [H-] and (C|HH) would become ([C-]|[H-][H-]).

### Backreferences

Backreferences make things slightly more tricky. Every regular expression with backreferencing can have multiple "backreferencing paths" - lists of tiles that are involved in backreferencing. Every such "path" consists of units of characters that have be the same. For example, (...?)\1* in the 8-th row of the crossword has 2 paths with 2 and 3 units respectively:
* Units [(8, 1, 12), (8, 3, 10), (8, 5, 8), (8, 7, 6), (8, 9, 4), (8, 11, 2)] and [(8, 2, 11), (8, 4, 9), (8, 6, 7), (8, 8, 5), (8, 10, 3), (8, 12, 1)] constitute one path.
* Units [(8, 1, 12), (8, 4, 9), (8, 7, 6), (8, 10, 3)], [(8, 2, 11), (8, 5, 8), (8, 8, 5), (8, 11, 2)] and [(8, 3, 10), (8, 6, 7), (8, 9, 4), (8, 12, 1)] constitute the other path.

If a tile belongs to any of the units of the backreferencing path currently under observation, its' value would be expanded to all of the tiles within the unit that still have "-" as value. Similarly, if any tile within a pattern of a regex with backreferencing belonged to any unit of a path currently under observation and had a different value to "-", this value would be expanded to other tiles within the same unit. Matching a character into a tile requires the examination of all possible paths until there is a unique character that maintains the true state of the crossword.

### Complexity

If we assumed the crossword could be solved one step at a time and there were no backreferences then the worst case complexity of the above algorithm would be O(3sn^2) where s is the alphabet size and n is the number of tiles. In reality, these are small, i.e. an English alphabet has 26 characters and the crossword has 127 tiles. This particular crossword has four regexes with backreferencing and it can not be solved by looking only at one tile at a time, and the algorithm solves it in less than 1 second.
