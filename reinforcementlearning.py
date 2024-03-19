import gymnasium as gym
import numpy as np
def demo():
    """run the MountainCar environment with random actions"""
    
    env = gym.make('MountainCar-v0', render_mode='human')  #  create an instance of the environment

    state = env.reset()  # reset the current game

    for _ in range(200):  # play 200 random actions
        env.render()  # render the current game state to screen
        a = env.action_space.sample()  # get a random action
        state, reward, terminated, truncated, info = env.step(a) # take the action and return the outcome
        
    env.close()
env = gym.make('MountainCar-v0')  # no rendering!

# get usefull information about the environment:
state = env.reset()
print('start state:', state)
print('Number of sctions in the action space:', env.action_space.n)
print('Lowest state in the state space:', env.observation_space.low)
print('Hightest state in the state space:', env.observation_space.high)
#perform one step of the game for action a=1
a=1
state, reward, terminated, truncated, info = env.step(a)
print('After the step with (a=1):',state, reward, terminated, truncated, info )

def s2q(s):
    # convert continous state values to discrete location indices inside the Q matrix
    
    #----------ADD CODE HERE---------#
    position_bins = np.linspace(-1.2, 0.6, 20)
    velocity_bins  = np.linspace(-0.07, 0.07, 20)
    return [np.digitize(s[0], position_bins) , np.digitize(s[1], velocity_bins)]

def qLearn(Q, α, γ, ϵ, ϵ_min, num_games):
    """ 
    learns the Q table by interacting with the environment and applying the Bellman eqation 
    Q: q-table (n-dimensional ndarray)
    α: learning rate
    γ: discount factor
    ϵ: probability of taking a random action in the epsilon-greedy policy
    ϵ_min: minimum value ϵ can take when applying a reduction algortihm to ϵ
    """
    wins = 0

    for i in range(num_games):
        state = env.reset()[0]  
        state  = s2q(state)
        state_pos = state[0]
        state_vel = state[1]
        terminated = False
        truncated = False
        while truncated == False: 
            random_number = np.random.uniform(0,1)
            if random_number < ϵ:
                a = env.action_space.sample()
            else:
                a = np.argmax(Q[state_pos][state_vel])

            next_state, reward, terminated, truncated, info = env.step(a)
            next_state = s2q(next_state)
            next_state_pos = next_state[0]
            next_state_vel = next_state[1]
            Q[state_pos][state_vel][a] = Q[state_pos][state_vel][a] + α * (reward + γ * np.max(Q[next_state_pos][next_state_vel]) - Q[state_pos][state_vel][a])
            state = next_state
        if ϵ > ϵ_min:
            ϵ *= 0.99

Qdim = (20, 20, 3)  
Q = np.zeros(shape=Qdim)
state = env.reset()
# set the hyperparameters
α =   0.1
γ =   0.1
ϵ =   0.1
ϵ_min =   0.01
num_games = 100
# train the agent and store results
qLearn(Q, α, γ, ϵ, ϵ_min, num_games)
np.save('qrun1.npy', Q)

# replay the game using the trained Q matrix
Q = np.load('qrun1.npy')

# create and reset the environment with render mode on
env = gym.make('MountainCar-v0', render_mode='human')
state = env.reset()[0]
    
# play a single episode with max. 1000 actions
for _ in range(1000):           
    env.render()                
    loc = s2q(state)
    state_pos = loc[0]
    state_vel = loc[1]
    a = np.argmax(Q[state_pos][state_vel])
    state, reward, terminated, truncated, info = env.step(a) 
        
    if terminated: 
        print('Qplay Output:', reward, terminated, truncated, info)
        break

env.close()