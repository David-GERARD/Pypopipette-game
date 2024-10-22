# This file contains the GUI of the game.
import tkinter as tk
import numpy as np
from backend import Dots_and_squares

import matplotlib.pyplot as plt

class Game_GUI:
    """
    This class is responsible for the game GUI of the dots and squares game.
    """

    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self, grid_size, n_players) -> None:

        # Initialize the game instance
        self.game_instance = Dots_and_squares(grid_size, n_players)
        
        # Initialize the GUI
        self.grid_size = grid_size
        self.size_of_board = 600
        self.players_colors = generate_rainbow_hex_colors(n_players)
        symbol_size = (self.size_of_board / 3 - self.size_of_board / 8) / 2
        symbol_thickness = 50
        dot_color = '#7BC043'
        #player1_color = '#0492CF'
        #player1_color_light = '#67B0CF'
        #player2_color = '#EE4035'
        #player2_color_light = '#EE7E77'
        #Green_color = '#7BC043'
        self.dot_width = 0.25*grid_size[0]/grid_size[0]
        self.edge_width = 0.075*self.size_of_board/grid_size[0]
        self.distance_between_dots = self.size_of_board / (grid_size[0]+1)

        self.window = tk.Tk()
        self.window.title('Pypopipette')
        self.canvas = tk.Canvas(self.window, width=self.size_of_board, height=self.size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.draw_board()
        

    def mainloop(self):
        self.window.mainloop()


    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_board(self)->None:
        """
        This method draws the game board on the canvas.

        Returns:
        None
        """
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                start_x = j * self.distance_between_dots + self.distance_between_dots / 2
                start_y = i * self.distance_between_dots + self.distance_between_dots / 2
                end_x = start_x + self.distance_between_dots
                end_y = start_y + self.distance_between_dots
                
                self.canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='black', width=self.edge_width)


    def draw_edge(self, player_id, coordinates, action):
        """
        This method draws the edge on the canvas.

        Args:
        player_id (int): The id of the player.
        coordinates (tuple): The coordinates of the edge.
        action (str): ['r','c'] whether to draw a row or a column.

        Returns:
        None
        """
        # Compute the start and end coordinates of the edge
        if action == 'r':
            start_x = coordinates[1] * self.distance_between_dots + self.distance_between_dots / 2
            start_y = (coordinates[0]+1) * self.distance_between_dots - self.distance_between_dots / 2
            end_x = start_x + self.distance_between_dots
            end_y = start_y
            
        elif action == 'c':
            start_x = (coordinates[1]+1) * self.distance_between_dots - self.distance_between_dots / 2
            start_y = coordinates[0] * self.distance_between_dots + self.distance_between_dots / 2
            end_x = start_x
            end_y = start_y + self.distance_between_dots
        
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=self.players_colors[player_id], width=self.edge_width)

    def shade_boxes(self):
        """
        This method shades the boxes on the canvas by filling them with the color of the player who completed the box.

        Returns:
        None
        """

        for i in range(len(self.game_instance.squares)):
            for j in range(len(self.game_instance.squares[0])):
                if self.game_instance.squares[i][j] != -1:
                    start_x = j * self.distance_between_dots + self.distance_between_dots / 2 
                    start_y = i * self.distance_between_dots + self.distance_between_dots / 2 
                    end_x = start_x + self.distance_between_dots 
                    end_y = start_y + self.distance_between_dots 
                    self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=self.players_colors[int(self.game_instance.squares[i][j])], outline='')
                
        #self.canvas.create_rectangle(start_x, start_y, end_x, end_y,  outline = self.players_colors[player_id],fill=self.players_colors[player_id], width=self.edge_width)

    def display_gameover(self):
        #TODO: Implement this method
        pass

    def refresh_board(self):
        #TODO: Implement this method
        pass

    def display_turn_text(self):
        #TODO: Implement this method
        text = 'Next turn: '
        if self.game_instance.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-self.distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)
        


    def click(self, event):
        #TODO: Implement this method
        
        x, y = event.x, event.y
        coordinates, action = self.convert_click_to_action([x, y])
        player = self.game_instance.current_player

        if self.game_instance.player_turn(self.game_instance.current_player, coordinates, action):
            if player != self.game_instance.current_player:
                self.draw_edge((self.game_instance.current_player-1)%self.game_instance.n_players, coordinates, action)
            else:
                self.draw_edge(self.game_instance.current_player, coordinates, action)
            self.shade_boxes()



    def convert_click_to_action(self, grid_position)->tuple:
        """
        This method converts the click position to an action.

        Args:
        grid_position (list): The grid position of the click.

        Returns:
        tuple: The logical coordinates of the edge and action (whether it's a row or a column).

        """
        grid_position = np.array(grid_position)
        square_position = (grid_position - self.distance_between_dots / 2) // self.distance_between_dots 
        grid_position_adjusted = grid_position - (square_position * self.distance_between_dots + self.distance_between_dots / 2)

        if grid_position_adjusted[0] > grid_position_adjusted[1] and grid_position_adjusted[0] > -grid_position_adjusted[1] + self.distance_between_dots:
            action = 'c'
            coordinates = [int(square_position[1]), int(square_position[0])+1]
        elif grid_position_adjusted[0] < grid_position_adjusted[1] and grid_position_adjusted[0] < -grid_position_adjusted[1] + self.distance_between_dots:
            action = 'c'
            coordinates = [int(square_position[1]), int(square_position[0])]
        elif grid_position_adjusted[0] > grid_position_adjusted[1] and grid_position_adjusted[0] < -grid_position_adjusted[1] + self.distance_between_dots:
            action = 'r'
            coordinates = [int(square_position[1]), int(square_position[0])]
        elif grid_position_adjusted[0] < grid_position_adjusted[1] and grid_position_adjusted[0] > -grid_position_adjusted[1] + self.distance_between_dots:
            action = 'r'
            coordinates = [int(square_position[1])+1, int(square_position[0])]
        
        return coordinates, action
    
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
        
# Define a function to generate n colors from blue to red (rainbow spectrum)
def generate_rainbow_hex_colors(n):
    # Generate n evenly spaced values from 0 to 1 to represent the positions in the color map
    colors = plt.cm.rainbow(np.linspace(0, 1, n))
    
    # Convert the RGB colors to hexadecimal
    hex_colors = [rgb2hex(color[:3]) for color in colors]
    
    return hex_colors

        

if __name__ == '__main__':
    gui = Game_GUI((6, 6), 2)
    gui.mainloop()
    

    