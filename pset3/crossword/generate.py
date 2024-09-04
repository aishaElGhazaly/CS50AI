import sys
import copy
from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        removed_words = []

        for key, value in self.domains.items():
            for word in value:
                if len(word) != key.length:
                    removed_words.append((key, word))

        if removed_words:
            for key, word in removed_words:
                self.domains[key].remove(word)

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        if overlap:
            removed_words = set()

            for word_x in self.domains[x]:
                matches = False

                for word_y in self.domains[y]:
                    if word_x[overlap[0]] == word_y[overlap[1]]:
                        matches = True
                        break

                if not matches:
                    removed_words.add(word_x)

            if removed_words:
                self.domains[x] -= removed_words
                revised = True

        return revised

        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []

            for var_x in self.domains:
                for var_y in self.domains:
                    if var_x != var_y:
                        arcs.append((var_x, var_y))

        while arcs:
            var_x, var_y = arcs.pop(0)

            if self.revise(var_x, var_y):
                if not self.domains[var_x]:
                    return False
                else:
                    for var_z in self.crossword.neighbors(var_x) - {var_y}:
                        arcs.append((var_z, var_x))

        return True

        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False

        return True
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = []

        for var in assignment:
            value = assignment[var]

            if value in values:
                return False
            else:
                values.append(value)

            if len(value) != var.length:
                return False

            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    (i, j) = self.crossword.overlaps[var, neighbor]

                    neighbor_value = assignment[neighbor]

                    if value[i] != neighbor_value[j]:
                        return False

        return True
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = {}

        for value in self.domains[var]:
            count = 0

            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    for neighbor_value in self.domains[neighbor]:
                        overlap = self.crossword.overlaps[var, neighbor]

                        if overlap and value[overlap[0]] != neighbor_value[overlap[1]]:
                            count += 1

            values[value] = count

        return sorted(values, key=lambda v: values[v])

        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = []

        for var in self.domains:
            if var not in assignment:
                unassigned.append(var)

        variable = sorted(
            unassigned,
            key=lambda var: (
                len(self.domains[var]),
                -len(self.crossword.neighbors(var)),
            ),
        )[0]

        return variable
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        values = self.order_domain_values(var, assignment)

        for value in values:
            pre_assignment = copy.deepcopy(assignment)
            assignment[var] = value

            if self.consistent(assignment):
                result = self.backtrack(assignment)

                if result:
                    return result
                else:
                    assignment = pre_assignment

        return None
        # raise NotImplementedError


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
