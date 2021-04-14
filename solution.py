from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
main_diagonal_units = [rows[index]+cols[index] for index,s in enumerate(rows)]
#print("Main Diagonal :",main_diagonal_units)
counter_diagonal_units = [rows[index]+cols[8-index] for index,s in enumerate(rows)]
#print("Counter Diagonal :",counter_diagonal_units )
#diagonal_units = list(set(cross_diag(rows, cols)+cross_diag(rows[::-1], cols)))
#unitlist = row_units + column_units + square_units + main_diagonal_units + counter_diagonal_units
unitlist = row_units + column_units + square_units
unitlist.append(main_diagonal_units)
unitlist.append(counter_diagonal_units)


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins_old(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # raise NotImplementedError
    # find all boxes with 2 digits only and add their box to a list
    # go through that list to identify naked twin pairs i.e. in same unit and same digits
    naked_twins_sudoku = values.copy()
    #print(unitlist)
    for unit in unitlist:
        #print("*GOING THROUGH UNIT: ",unit)
        for box in unit:
            #print("FOR BOX: ", box)
            #print("VALUE OF BOX: ", values[box])
             
            if len(values[box]) == 2:
               for peer in unit:
                    #print("FOR PEER: ",peer)
                    if peer != box:
                        if values[box] == values[peer]:
                            # check against all other boxes in this unit
                            # delete each digit in this string in all the peers
                            #print("***Found equal values***")
                            naked_peer = peer
                            for digit in values[box]:
                                for peer in unit:
                                    if peer !=box and peer != naked_peer:
                                        #print("Replacing in ",peer, "digit", digit)
                                        naked_twins_sudoku[peer] = naked_twins_sudoku[peer].replace(digit,'')
    return naked_twins_sudoku

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # raise NotImplementedError
    # find all boxes with 2 digits only and add their box to a list
    # go through that list to identify naked twin pairs i.e. in same unit and same digits
    naked_twins_sudoku = values.copy()

    for box in values:
        for peer in peers[box]:
            if len(values[box]) == 2:
                if values[box] == values[peer]:
                    for intersection_box in peers[box].intersection(peers[peer]):
                        for digit in values[box]:
                            naked_twins_sudoku[intersection_box] = naked_twins_sudoku[intersection_box].replace(digit,'')
    return naked_twins_sudoku

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    #eliminate_values = values.copy()
    #print("Starting Elimination ...")
    #print("========================")
    for key in values:
        value = values[key]
        if len(value) == 1:
            #print("==========================================================================")
            #print("Found box ", key, "with value ", value, "eliminating ", value," in peers ")
            #print("==========================================================================")
            #print("Its peers are :", peers[key])
            #print("Found value ", value, "in box ", key)
            for peer in peers[key]:
                if len(values[peer]) > 1:
                    #eliminate_values[peer] = values[peer].replace(value,'')
                    #print("===============================================")
                    #print("Eliminate Input Sudoku :\n")
                    #print("===============================================")
                    #display(values)
                    #print("Eliminating for ",value, " in box ",peer)
                    values[peer] = values[peer].replace(value,'')
                    #print("===============================================")
                    #print("Eliminate Output Sudoku after eliminating for ",value, " in box ",peer)
                    #print("===============================================")
                    #display(values)
                    
            #print("Replaced ",value," in ",values[peer]," of box ",peer,"Resulting value in ", peer, " is ",eliminate_values[peer])
            #display(values)
    #return eliminate_values
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in ('123456789'):
            digit_boxes = [box for box in unit if digit in values[box]]
            if(len(digit_boxes) == 1):
                values[digit_boxes[0]] = digit
                #print("======================================================")
                #print(" Only Choice: Assigned ",digit," to box ", digit_boxes )
                #print("======================================================")
                #display(values)
    return values

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy 
        values = eliminate(values)
        #print("After eliminate :")
        #display(values)
    
        # Use the Only Choice Strategy
        values = only_choice(values)
        #print("After only_choice :")
        #display(values)

        # Use the Naked Twins strategy
        values = naked_twins(values)
        #print("After naked_twins :")
        #display(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
   
    #print("values before reduction :")
    #display(values)
    values = reduce_puzzle(values)
    #print("values after reduction :")
    #display(values)
    
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)   
    for digit in values[s]:
        sudoku_copy = values.copy()
        sudoku_copy[s] = digit
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        ret_val = search(sudoku_copy)
        if ret_val:
            return ret_val


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
