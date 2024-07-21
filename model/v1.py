import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import numpy as np
import gym

class PPOAgent:
    
    def __init__(self, 
                 env, 
                 learning_rate=0.0003, 
                 gamma=0.99, 
                 clip_ratio=0.2, 
                 epochs=10, 
                 batch_size=64) -> None:
        
        self.env = env
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.clip_ratio = clip_ratio
        self.epochs = epochs
        self.batch_size = batch_size

        self.policy_net = self.create_policy_network()
        self.value_net = self.create_value_network()
        self.policy_optimizer = optimizers.Adam(learning_rate=self.learning_rate)
        self.value_optimizer = optimizers.Adam(learning_rate=self.learning_rate)
        
    