from io_helper import IOHelper, cell_to_coordinate, coordinate_to_cell


def query_player(game, state):
    """Make a move by querying standard input."""
    available_moves = game.actions(state)
    available_moves = [coordinate_to_cell(move) for move in available_moves]

    print("current state:")
    game.display(state)
    io_helper = IOHelper(available_moves)
    io_helper.display_menu(max_per_line=3)
    move = None
    if game.actions(state):
        move_string = str(cell_to_coordinate(io_helper.read_user_input()))
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move
