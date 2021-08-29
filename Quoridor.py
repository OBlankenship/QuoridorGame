class QuoridorGame:
    """Contains functions for setting up and playing a game of Quoridor
    Includes functions for pawn movement, fence placement, turn handling, and game completion
    Needs to communicate with player objects and pawn objects for both players/pawns
    """
    def __init__(self):
        """Initializes a QuoridorGame
        Parameters: None
        Returns: None
        """
        # Creates a 9x9 matrix of all 0's for pawn management
        self._board = [[0 for j in range(9)] for i in range(9)]
        # Creates a 10x10 matrix of all 0's for fence management
        self._fence_board = [[0 for j in range(10)] for i in range(10)]
        self.generate_edges()
        # Places the pawns to their starting positions
        self._board[0][4] = "P1"
        self._board[8][4] = "P2"
        self._pawn1 = Pawn((0, 4))
        self._pawn2 = Pawn((8, 4))
        # Configures the Player objects
        self._player1 = Player(self._pawn1, "P1")
        self._player2 = Player(self._pawn2, "P2")
        # Initializes variables for handling current player and game winner
        self._current_player = self._player1
        self._game_won = False
        self._winner = None

    def generate_edges(self):
        """Adds fences to the edges of the board
        Parameters: None
        Returns: None
        Note: Part of the initialization of a QuoridorGame
        """
        for entry in range(0, 9):
            self._fence_board[0][entry] = "h"
        for entry in range(0, 9):
            self._fence_board[entry][0] = "v"
        for entry in range(0, 9):
            self._fence_board[9][entry] = "h"
        for entry in range(0, 9):
            self._fence_board[entry][9] = "v"
        self._fence_board[0][0] = "vh"
        self._fence_board[9][9] = "vh"

    def lookup_player(self, player_number):
        """Takes a player number and returns the object associated with that player
        Parameters: The integer number representing a player (1 or 2)
        Returns: The player object associated with that number
        """
        if player_number == 1:
            return self._player1
        else:
            return self._player2

    def check_jump(self, pos, current_pos):
        """Checks if a pawn jump is a valid move
        Parameters: Target position, current position
        Returns: True if the jump is valid / False if the jump is blocked
        """
        # Handles a jump upwards
        if current_pos[0] - pos[0] == 2 and self._board[current_pos[0]-1][current_pos[1]] != 0:
            # Ensures a fence won't obstruct the jump
            if self._fence_board[current_pos[0]-1][current_pos[1]] == "h" or\
                    self._fence_board[current_pos[0]-1][current_pos[1]] == "vh":
                print("Jump blocked by fence!")
                return False
            else:
                return True
        # Handles a jump downwards
        if current_pos[0] - pos[0] == -2 and self._board[current_pos[0]+1][current_pos[1]] != 0:
            # Ensures a fence won't obstruct the jump
            if self._fence_board[current_pos[0]+2][current_pos[1]] == "h" or\
                    self._fence_board[current_pos[0]+2][current_pos[1]] == "vh":
                print("Jump blocked by fence!")
                return False
            else:
                return True
        # Handles a jump to the left
        if current_pos[1] - pos[1] == 2 and self._board[current_pos[0]][current_pos[1]-1] != 0:
            # Ensures a fence won't obstruct the jump
            if self._fence_board[current_pos[0]][current_pos[1]-1] == "v" or\
                    self._fence_board[pos[0]][pos[1]-1] == "vh":
                print("Jump blocked by fence!")
                return False
            else:
                return True
        # Handles a jump to the right
        if current_pos[1] - pos[1] == -2 and self._board[current_pos[0]][current_pos[1]+1] != 0:
            # Ensures a fence won't obstruct the jump
            if self._fence_board[current_pos[0]][current_pos[1]+2] == "v" or\
                    self._fence_board[current_pos[0]][current_pos[1]+2] == "vh":
                print("Jump blocked by fence!")
                return False
            else:
                return True
        # If none of the above is true, the move is 2 spaces, but invalid. Returns False
        print("Invalid number of spaces!")
        return False

    def check_diag(self, current_pos, dir):
        """If a player attempts a diagonal move, checks if that move is valid per the rules
        Parameters: current position, movement direction
        Returns: False if the move is invalid / True if the move is valid
        """
        # Checks moves upwards
        if dir == "nw" or dir == "ne":
            # Checks for opponent pawn
            if self._board[current_pos[0]-1][current_pos[1]] != 0:
                # Ensures the opponent pawn has a fence behind it
                if self._fence_board[current_pos[0]-1][current_pos[1]] == "h" \
                        or self._fence_board[current_pos[0]-1][current_pos[1]] == "vh":
                    return True
        # Checks moves to the right
        if dir == "ne" or dir == "se":
            # Checks for opponent pawn
            if self._board[current_pos[0]][current_pos[1]+1] != 0:
                # Ensures the opponent pawn has a fence behind it
                if self._fence_board[current_pos[0]][current_pos[1]+2] == "v" \
                        or self._fence_board[current_pos[0]][current_pos[1]+2] == "vh":
                    return True
        # Checks moves downwards
        if dir == "sw" or dir == "se":
            # Checks for opponent pawn
            if self._board[current_pos[0]+1][current_pos[1]] != 0:
                # Ensures the opponent pawn has a fence behind it
                if self._fence_board[current_pos[0]+2][current_pos[1]] == "h" \
                        or self._fence_board[current_pos[0]+2][current_pos[1]] == "vh":
                    return True
        # Checks moves to the left
        if dir == "nw" or dir == "sw":
            # Checks for opponent pawn
            if self._board[current_pos[0]][current_pos[1]-1] != 0:
                # Ensures the opponent pawn has a fence behind it
                if self._fence_board[current_pos[0]][current_pos[1]-1] == "v" \
                        or self._fence_board[current_pos[0]][current_pos[1]-1] == "vh":
                    return True
        return False

    def validate_movement(self, pos, current_pos):
        """Ensures the player movement is valid
        Parameters: Pawn target position and current position
        Returns: True if move is valid / False if move is invalid
        """
        dir = self.determine_dir(pos, current_pos)
        # Handles attempts to move outside the board
        if pos[0] > 8 or pos[0] < 0 or pos[1] > 8 or pos[1] < 0:
            print("Move blocked by a fence!")
            return False
        # Handles pawn overlap
        if self._board[pos[0]][pos[1]] != 0:
            print("Move blocked by a pawn!")
            return False
        # Handles player trying to move diagonally
        if current_pos[0] - pos[0] != 0 and current_pos[1] - pos[1] != 0:
            # Checks to see if it is a valid diagonal move
            if self.check_diag(current_pos, dir):
                # Shortcuts the check on number of spaces since that is already checked
                return True
            else:
                print("Can't move diagonally!")
                return False
        # Handles player attempting to move an invalid number of spaces
        if (current_pos[0] - pos[0] == 2 or current_pos[0] - pos[0] == -2
                or current_pos[1] - pos[1] == 2 or current_pos[1] - pos[1] == -2):
            # If the player tries to move 2 spaces, check if it is a pawn jump
            if self.check_jump(pos, current_pos):
                return True
            else:
                return False
        if current_pos[0] - pos[0] > 1 or current_pos[0] - pos[0] < -1:
            print("Invalid number of spaces!")
            return False
        if current_pos[1] - pos[1] > 1 or current_pos[1] - pos[1] < -1:
            print("Invalid number of spaces!")
            return False
        return True

    def determine_dir(self, pos, current_pos):
        """Determines the direction the player is attempting to move
        Parameters: Pawn target position and current position
        Returns: The direction that the pawn is moving
        """
        dir = ""
        if current_pos[1] - pos[1] == 1 and current_pos[0] - pos[0] == 1:
            dir = "nw"
            return dir
        if current_pos[1] - pos[1] == 1 and current_pos[0] - pos[0] == -1:
            dir = "sw"
            return dir
        if current_pos[1] - pos[1] == -1 and current_pos[0] - pos[0] == 1:
            dir = "ne"
            return dir
        if current_pos[1] - pos[1] == -1 and current_pos[0] - pos[0] == -1:
            dir = "se"
            return dir
        if current_pos[1] - pos[1] >= 1:
            dir = "left"
            return dir
        if current_pos[1] - pos[1] <= -1:
            dir = "right"
            return dir
        if current_pos[0] - pos[0] >= 1:
            dir = "up"
            return dir
        if current_pos[0] - pos[0] <= -1:
            dir = "down"
            return dir

    def collision_check(self, pos, current_pos):
        """Checks for collision with fences
        Parameters: Pawn target position and current position
        Returns: True if the move is valid / False if the move in invalid
        """
        # Determines the direction the player is attempting to move
        dir = self.determine_dir(pos, current_pos)
        # Handles fences when moving left
        if dir == "left" and \
                (self._fence_board[current_pos[0]][current_pos[1]] == "v"
                 or self._fence_board[current_pos[0]][current_pos[1]] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles fences when moving right
        if dir == "right" and \
                (self._fence_board[current_pos[0]][current_pos[1]+1] == "v"
                 or self._fence_board[current_pos[0]][current_pos[1]+1] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles fences when moving up
        if dir == "up" and \
                (self._fence_board[current_pos[0]][current_pos[1]] == "h"
                 or self._fence_board[current_pos[0]][current_pos[1]] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles fences when moving down
        if dir == "down" \
                and (self._fence_board[current_pos[0]+1][current_pos[1]] == "h"
                     or self._fence_board[current_pos[0]+1][current_pos[1]] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles NW movement when the opposing pawn is above
        if dir == "nw" and self._board[current_pos[0]-1][current_pos[1]] != 0 \
                and (self._fence_board[current_pos[0]-1][current_pos[1]] == "v"
                     or self._fence_board[current_pos[0]-1][current_pos[1]] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles NW movement when the opposing pawn is to the left
        if dir == "nw" and self._board[current_pos[0]][current_pos[1]-1] != 0 \
                and (self._fence_board[current_pos[0]][current_pos[1]-1] == "h"
                     or self._fence_board[current_pos[0]][current_pos[1]-1] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles NE movement when the opposing pawn is above
        if dir == "ne" and self._board[current_pos[0]-1][current_pos[1]] != 0 \
                and (self._fence_board[current_pos[0]-1][current_pos[1]+1] == "v"
                     or self._fence_board[current_pos[0]-1][current_pos[1]+1] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles NE movement when the opposing pawn is to the right
        if dir == "ne" and self._board[current_pos[0]][current_pos[1]+1] != 0 \
                and (self._fence_board[current_pos[0]][current_pos[1]+1] == "h"
                     or self._fence_board[current_pos[0]][current_pos[1]+1] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles SE movement when the opposing pawn is to the below
        if dir == "se" and self._board[current_pos[0]+1][current_pos[1]] != 0 \
                and (self._fence_board[current_pos[0]+1][current_pos[1]+1] == "v"
                     or self._fence_board[current_pos[0]+1][current_pos[1]+1] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles SE movement when the opposing pawn is to the right
        if dir == "se" and self._board[current_pos[0]][current_pos[1]+1] != 0 \
                and (self._fence_board[current_pos[0]+1][current_pos[1]+1] == "h"
                     or self._fence_board[current_pos[0]+1][current_pos[1]+1] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles SW movement when the opposing pawn is below
        if dir == "sw" and self._board[current_pos[0]+1][current_pos[1]] != 0 \
                and (self._fence_board[current_pos[0]+1][current_pos[1]] == "v"
                     or self._fence_board[current_pos[0]+1][current_pos[1]] == "vh"):
            print("Move blocked by fence!")
            return False
        # Handles SW movement when the opposing pawn is to the left
        if dir == "sw" and self._board[current_pos[0]][current_pos[1]-1] != 0 \
                and (self._fence_board[current_pos[0]+1][current_pos[1]-1] == "h"
                     or self._fence_board[current_pos[0]+1][current_pos[1]-1] == "vh"):
            print("Move blocked by fence!")
            return False
        return True

    def validate_turn(self, player):
        """Ensures that the correct player is making their move
        Parameters: Player object of the player attempting to make a move
        Returns: True if the correct player is playing / False if the player is playing out of turn
        """
        if self._current_player != player:
            print("It's not your turn! It's " + str(self._current_player.get_name()) + "'s turn!")
            return False
        else:
            return True

    def make_move(self, player):
        """Changes the active player after a move is successfully played
        Parameters: Player object of the player making a move
        Returns: None
        Note: Changes self._current_player to the other player
        """
        if player == self._player1:
            self._current_player = self._player2
        else:
            self._current_player = self._player1

    def check_win(self, player, pos):
        """Checks if a player has won the game
        Parameters: Player object, and current position of a pawn
        Returns: None
        Note: Sets self.game_won to true if a pawn reaches the opposite back rank
        """
        if player == self._player1:
            if pos[0] == 8:
                self._game_won = True
                print("Player One Wins!")
                self._winner = self._player1
        else:
            if pos[0] == 0:
                self._game_won = True
                print("Player Two Wins!")
                self._winner = self._player1

    def move_pawn(self, player_num, raw_pos):
        """Functions for moving a pawn within the parameters laid out in the game rules
        Parameters: Integer associated with a player, position entered by the user
        Returns: False if the move is invalid / True if the move is valid
        Note: If a move is valid, updates the pawn position on self._board
        """
        # Converts (n, m) notation to (m, n) notation
        pos = [[], []]
        pos[0] = raw_pos[1]
        pos[1] = raw_pos[0]
        # converts a player number to a player object
        player = self.lookup_player(player_num)
        # Gets the players pawn, and the pawn position
        pawn = player.get_pawn()
        current_pos = pawn.get_pos()
        # Ensures the game hasn't been won
        if self._game_won:
            print("The game is over!")
            return False
        # Ensures it is the proper turn
        if not self.validate_turn(player):
            return False
        # Ensure that no collisions occur with fences
        if not self.collision_check(pos, current_pos):
            return False
        # Ensures the move is valid
        if not self.validate_movement(pos, current_pos):
            return False
        # If the move is valid and no fences block the movement, move the pawn
        self._board[current_pos[0]][current_pos[1]] = 0
        self._board[pos[0]][pos[1]] = player.get_name()
        pawn.set_pos(pos)
        self.check_win(player, pos)
        self.make_move(player)
        return True

    def place_fence(self, player_num, direction, raw_pos):
        """Handles placing of fences
        Parameters: Integer associated with a player, fence direction, fence position entered by the user
        Returns: True if the fence placement is valid / False if it is invalid
        Note: If a placement is valid, the fence is placed on self._fence_board
        """
        # Converts (n, m) notation to (m, n) notation
        pos = [[], []]
        pos[0] = raw_pos[1]
        pos[1] = raw_pos[0]
        # converts a player number to a player object
        player = self.lookup_player(player_num)
        # Ensures the game has not been won
        if self._game_won:
            print("The game is over!")
            return False
        # Ensures it is the proper turn
        if not self.validate_turn(player):
            return False
        # Ensures that the player has fences to place
        if player.get_fences() < 1:
            print("You don't have any fences to place!")
            return False
        # Ensures that the fence can't be placed outside the game board
        if direction == "h" and (pos[0] < 1 or pos[0] > 8 or pos[1] < 0 or pos[1] > 8):
            print("Cannot place the fence outside the game board!")
            return False
        if direction == "v" and (pos[0] < 0 or pos[0] > 8 or pos[1] < 1 or pos[1] > 8):
            print("Cannot place the fence outside the game board!")
            return False
        # Ensures that the space doesn't already have a fence in the specified direction
        if self._fence_board[pos[0]][pos[1]] == direction:
            print("Cannot place overlapping fences")
            return False
        # Ensures that the space doesn't already have both vertical and horizontal fences
        if self._fence_board[pos[0]][pos[1]] == "vh":
            print("Cannot place overlapping fences")
            return False
        # If the fence placement is valid, adds the fence
        if self._fence_board[pos[0]][pos[1]] == 0:
            self._fence_board[pos[0]][pos[1]] = direction
        else:
            self._fence_board[pos[0]][pos[1]] = "vh"
        # Remove a fence from the player, and signify the placement was successful
        player.remove_fence()
        print(player.get_name() + " currently has " + str(player.get_fences()) + " fences remaining!")
        self.make_move(player)
        return True

    def draw_board(self):
        """Draws the position of pawns on the game board
        Parameters: None
        Returns: None
        Note: Used for debugging and not gameplay
        """
        print("Game Board:")
        for element in self._board:
            print(element)

    def draw_fence_board(self):
        """Draws the position of fences on the game board
        Parameters: None
        Returns: None
        Note: Used for debugging and not gameplay
        """
        print("Fence Board:")
        for element in self._fence_board:
            print(element)

    def is_winner(self, player_num):
        """Determines if a player is the winner of the game
        Parameters: The integer number associated with a player
        Returns: True if the player won the game / False if they did not win
        """
        player = self.lookup_player(player_num)
        if player == self._winner:
            return True
        else:
            return False


class Player:
    """Object representing one of the two players
    Contains references to the pawn associated with a given player, and the player fence count
    Needs to be reference by QuoridorGame objects for information about pawns/fences
    """
    def __init__(self, pawn, name):
        """Initializes a Player object
        Parameters: Pawn object associated with the player, name of the player
        Returns: None
        """
        self._fences = 10
        self._pawn = pawn
        self._name = name

    def get_pawn(self):
        """Returns the Pawn associated with this Player
        Parameters: None
        Returns: The Pawn object associated with this player
        """
        return self._pawn

    def get_name(self):
        """Returns the name associated with this Player
        Parameters: None
        Returns: The name of this player
        """
        return self._name

    def get_fences(self):
        """Returns the number of fences the player currently has
        Parameters: None
        Returns: The number of fences the player has remaining
        """
        return self._fences

    def remove_fence(self):
        """Removes one fence from the Player on successful placement
        Parameters: None
        Returns: None
        Note: Removes one fence from the player
        """
        self._fences -= 1


class Pawn:
    """Represents a Pawn within the game
    Contains functions for handling pawn position
    Must be referenced by Player and Quoridor game objects for pawn positioning"""
    def __init__(self, pos):
        """Initializes a Pawn
        Parameters: Position of the pawn
        Returns: None
        """
        self._pos = pos

    def get_pos(self):
        """Returns the current position of the Pawn
        Parameters: None
        Returns: The current position of the pawn
        """
        return self._pos

    def set_pos(self, pos):
        """Sets the current position of the Pawn
        Parameters: The target position of the pawn
        Returns: None
        """
        self._pos = pos
