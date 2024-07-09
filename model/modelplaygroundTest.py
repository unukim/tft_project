"""
_summary_
    This is the playground for better understanding of PPO Algorithm and Reinforcement learning
    THIS WILL NOT BE THE FINAL MODEL WE GOING TO USE.
"""

import gymnasium as gym
from stable_baselines3 import PPO

# Create the environment, 
# use render_mode to show the trained model interact with the enviroment
env = gym.make('CartPole-v1', render_mode="rgb_array")

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
