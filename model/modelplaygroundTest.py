"""
_summary_
    This is the playground for better understanding of PPO Algorithm and Reinforcement learning
    THIS WILL NOT BE THE FINAL MODEL WE GOING TO USE.
    
    Here are some examples of different environments you can use:

    Classic Control Tasks:
        Acrobot-v1
        MountainCar-v0
        MountainCarContinuous-v0
        Pendulum-v1

    Box2D Environments (install with pip install gymnasium[box2d]):
        LunarLander-v2
        LunarLanderContinuous-v2
        BipedalWalker-v3
        BipedalWalkerHardcore-v3

    Atari Games (install with pip install gymnasium[atari]):
        Pong-v4
        Breakout-v4
        SpaceInvaders-v4

    Mujoco Environments (install with pip install gymnasium[mujoco]):
        HalfCheetah-v4
        Hopper-v4
        Ant-v4
        Walker2d-v4

Here’s an example of how to use the LunarLander-v2 environment with the PPO algorithm:
    
"""

import gymnasium as gym
from stable_baselines3 import PPO

# Create the environment, 
# use render_mode to show the model interact with the enviroment during training
env = gym.make('CartPole-v1', render_mode="human")

# Create the PPO model
model = PPO('MlpPolicy', env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save the model
model.save("test_model/ppo_cartpole")

# To load the model later, use:
# model = PPO.load("test_model/ppo_cartpole")

# Test the trained model
obs, info = env.reset()

for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, terminated, truncated, info = env.step(action)
    env.render()
    
    if terminated or truncated:
        obs, info = env.reset()

env.close()
