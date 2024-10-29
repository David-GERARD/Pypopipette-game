# This file contains the backend logic of the game. 
# It is the Model in the Model-View-Controller (MVC) design pattern. 

import numpy as np

class Dots_and_squares():
    """
    This class is responsible for the game logic of the dots and squares game. 
    """
    def __init__(self, grid_size, n_players) -> None:
        self.n_players = n_players
        self.current_player = 0
        self.n_rows = grid_size[0]
        self.n_cols = grid_size[1]
        self.squares = -1*np.ones((self.n_rows, self.n_cols))
        self.columns = -1*np.ones((self.n_rows, self.n_cols+1))
        self.columns[:,0] = -2 # -2 means that the column is already taken by a non-player (map feature, in this case the leftmost column)
        self.columns[:,-1] = -2 # -2 means that the column is already taken by a non-player (map feature, in this case the rightmost column)
        self.rows = -1*np.ones((self.n_rows+1, self.n_cols))
        self.rows[0,:] = -2 # -2 means that the row is already taken by a non-player (map feature, in this case the top row)
        self.rows[-1,:] = -2 # -2 means that the row is already taken by a non-player (map feature, in this case the bottom row)
        self.scores = np.zeros(n_players)
        self.log = []



    def is_game_over(self)->bool:
        """
        This method checks if the game is over.

        Returns:
        bool: True if the game is over, False otherwise.
        """
        return np.all(self.squares != -1)
    
    def player_turn(self, player_id, coordinates, action) -> bool:
        """ 
        This method represents the turn of a player.

        Args:
        player_id (int): The id of the player.
        coordinates (tuple): The coordinates of the action.
        action (str) : ["r","c"] The action to perform.
        
        Returns:
        bool: True if the player's turn was successful (they clicked on a previously unoccupied edge), False otherwise.
        """
        self.log.append({"turn":len(self.log),"player_id": player_id, "coordinates": coordinates, "action": action})

        if action == "r": # If the action is to update a row
            if self.update_row(coordinates, player_id): # If the row was updated skip to the next player
                self.current_player = (self.current_player + 1) % self.n_players
                return True
            else:
                return False # Ask the player to play again as he made an invalid move
            
        elif action == "c": # If the action is to update a column
            if self.update_column(coordinates, player_id): # If the column was updated skip to the next player
                self.current_player = (self.current_player + 1) % self.n_players
                return True
            else:
                return False # Ask the player to play again as he made an invalid move


    def update_row(self, coordinates, player_id)->bool:
        """
        This method updates the row of the game board with the player's id.

        Args:
        coordinates (tuple): The coordinates of the row to update.
        player_id (int): The id of the player.

        Returns:
        bool: True if the row was updated, False otherwise.
        """
        
        # Check if the position exists
        if coordinates[0] < 0 or coordinates[0] >= self.n_rows+1:
            return False
        if coordinates[1] < 0 or coordinates[1] >= self.n_cols:
            return False
        
        # Check if the position is already taken
        if self.rows[coordinates[0], coordinates[1]] != -1:
            return False
        
        # Update the row
        self.rows[coordinates[0], coordinates[1]] = player_id
        uper_square = self.update_square((coordinates[0], coordinates[1]), player_id)
        lower_square = self.update_square((coordinates[0]-1, coordinates[1]), player_id)
        if uper_square or lower_square:
            self.current_player = (self.current_player - 1) % self.n_players
        return True

    def update_column(self, coordinates, player_id)->bool:
        """
        This method updates the column of the game board with the player's id.

        Args:
        coordinates (tuple): The coordinates of the column to update.
        player_id (int): The id of the player.

        Returns:
        bool: True if the column was updated, False otherwise.
        """
        
        # Check if the position exists
        if coordinates[0] < 0 or coordinates[0] >= self.n_rows:
            return False
        if coordinates[1] < 0 or coordinates[1] >= self.n_cols+1:
            return False
        
        # Check if the position is already taken
        if self.columns[coordinates[0], coordinates[1]] != -1:
            return False
        
        # Update the column
        self.columns[coordinates[0], coordinates[1]] = player_id
        left_square = self.update_square((coordinates[0], coordinates[1]), player_id)
        right_square = self.update_square((coordinates[0], coordinates[1]-1), player_id)
        if left_square or right_square:
            self.current_player = (self.current_player - 1) % self.n_players
        return True
    
    def update_square(self, coordinates, player_id)->bool:
        """
        This method updates the square of the game board with the player's id.

        Args:
        coordinates (tuple): The coordinates of the square to update.
        player_id (int): The id of the player.

        Returns:
        bool: True if the square was updated, False otherwise.
        """
        
        # Check if the position exists
        if coordinates[0] < 0 or coordinates[0] >= self.n_rows:
            return False
        if coordinates[1] < 0 or coordinates[1] >= self.n_cols:
            return False
        
        # Check if the position is already taken
        if self.squares[coordinates[0], coordinates[1]] != -1:
            return False
       
        # Update the square
        if self.rows[coordinates[0], coordinates[1]] != -1 and self.rows[coordinates[0]+1, coordinates[1]] != -1 and self.columns[coordinates[0], coordinates[1]] != -1 and self.columns[coordinates[0], coordinates[1]+1] != -1:
            self.squares[coordinates[0], coordinates[1]] = player_id
            self.scores[player_id] += 1
            return True
        return False