from dicewars import player
from random import choice
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Activation
from keras.optimizers import Adam
class Player(player.Player):

    """
    Modify the get_attack_areas function using your own player.

    An example of a player which plays random moves is implemented here
    """
    def __init__(self):
        """
        do all required initialization here 
        use relative paths for access to stored files that you require
        use self.variable to store your variables such that your class has access.
        """
        self.playername='AIPlayer'
        print(f'Initializing player from: {__file__} with name:',self.playername)
        
        # Initialize Q-network
        self.q_network = self.create_q_network()
        self.replay_buffer = []  # Initialize replay buffer
        self.epsilon = 1.0  # Initial exploration rate
        self.epsilon_decay = 0.995  # Decay rate for exploration rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.gamma = 0.95  # Discount factor

    def create_q_network(self):
        # Define neural network architecture
        model = Sequential()
        model.add(Flatten(input_shape = (1,) ))
        model.add(Dense(2))
        model.add(Activation('relu'))
        model.add(Dense(10))
        model.add(Activation('relu'))
        model.add(Dense(20))
        model.add(Activation('relu'))
        model.add(Dense(10))
        model.add(Activation('relu'))
        model.add(Dense(1))
        print(model.summary())

    
        model.compile(optimizer='adam', loss='mse')  # Compile the model
        return model
    
    

    def get_attack_areas(self, grid, match_state):
        self.grid = grid
        self.match_state = match_state
        possible_attacks = self.get_possible_attacks(grid, match_state)
        
        if np.random.rand() < self.epsilon:
            return choice(possible_attacks)
        else:
            q_values = self.q_network.predict(state)


    def get_possible_attacks(self, grid, match_state):
        """
        REWRITE THIS FUNCTION FOR YOUR OWN MACHINE LEARNING AGENT
        """
        from_player = match_state.player # the index of the current player
        player_areas = match_state.player_areas # the areas belonging to each player
        area_num_dice = match_state.area_num_dice # the amount of dice on each area
        
        # add ending the turn to the list of possibilities
        possible_attacks = [None]

        # loop over all areas in posession of the current player
        for from_area in player_areas[from_player]:

            # check if the area has more than 1 dice
            if area_num_dice[from_area] > 1:

                # loops over all neigbors of the current area
                for to_area in grid.areas[from_area].neighbors:
                    #check if the neigboring area is not your own
                    if to_area not in player_areas[from_player]:
                        #append the area to the possible attack options
                        possible_attacks.append( (from_area, to_area) )
        
        return possible_attacks
