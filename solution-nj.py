assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
all_digits = '123456789'

# Placeholders
all_boxes = None
all_units = None
box_unit_mapping = None
box_peer_mapping = None

DEBUG_PRINT = False


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # All boxes with two values
    boxes_with_two_values = [box for box in values.keys() if len(values[box]) == 2]

    if DEBUG_PRINT:
        print("2 boxes: ", len(boxes_with_two_values), [values[box] for box in boxes_with_two_values])

    for box in boxes_with_two_values:
        # for each box check with each unit containing that box
        twin_value = values[box]
        units = box_unit_mapping[box]
        for unit in units:
            twins = [b for b in unit if values[b] == twin_value]
            if len(twins) == 2:
                if DEBUG_PRINT:
                    print("Found a twin: ", twin_value, twins, unit, [values[u] for u in unit])
                boxes_other_then_twins = set(unit) - set(twins)
                for reduce_twin_box in boxes_other_then_twins:
                    for digit in twin_value:
                        assign_value(values, reduce_twin_box, values[reduce_twin_box].replace(digit, ''))
                if DEBUG_PRINT:
                    print("After reduction of twin: ", twin_value, twins, unit, [values[u] for u in unit])
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    for c in grid:
        if c in all_digits:
            chars.append(c)
        if c == '.':
            chars.append(all_digits)
    assert (len(chars) == 81)
    result = dict(zip(all_boxes, chars))
    if DEBUG_PRINT:
        print("Grid:", solved_values_count(result), result)
    return result


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in all_boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in box_peer_mapping[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))

    if DEBUG_PRINT:
        print("Eliminate: ", solved_values_count(values), values)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in all_units:
        for digit in all_digits:
            boxes_with_digit = [box for box in unit if digit in values[box]]
            if len(boxes_with_digit) == 1:
                assign_value(values, boxes_with_digit[0], digit)
    if DEBUG_PRINT:
        print("Only Choice: ", solved_values_count(values), values)
    return values


def solved_values_count(values):
    return len([box for box in values.keys() if len(values[box]) == 1])


def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice(), naked_twins(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = solved_values_count(values)
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the naked twins strategy
        # values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = solved_values_count(values)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print("Exiting this reduction as sanity failed for: ",
                  [box for box in values.keys() if len(values[box]) == 0])
            return False
    if DEBUG_PRINT:
        print("Reduced: ", solved_values_count(values), values)
    return values


def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    First, reduce the puzzle using the previous function
    Choose one of the unfilled squares with the fewest possibilities
    Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    If you're stuck, see the solution.py tab!
    :param values: 
    :return: 
    """

    if DEBUG_PRINT:
        print("Starting reduction of: ", solved_values_count(values), values)
        print("\n")
        display(values)

    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier

    if all(len(values[s]) == 1 for s in values):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in values if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        print("ATTEMPT: ", n, s)
        assign_value(new_sudoku, s, value)
        # new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


# initialization sequence
all_boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# all_units = row_units + col_units + square_units

diag_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
all_units = row_units + col_units + square_units + diag_units

box_unit_mapping = dict((box, [unit for unit in all_units if box in unit]) for box in all_boxes)
box_peer_mapping = dict((box, set(sum(box_unit_mapping[box], [])) - set([box])) for box in all_boxes)

if __name__ == '__main__':
    # diag_sudoku_grid = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'

    final_res = solve(diag_sudoku_grid)
    if final_res != False:
        display(final_res)
    else:
        print("Suduko can not be solved")

    try:
        from visualize import visualize_assignments

        # visualize_assignments(assignments)

    except SystemExit:
        print(SystemExit.args)
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
