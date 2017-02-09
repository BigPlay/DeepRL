# -*- coding: utf8 -*-
import numpy as np

class Learner(object):
    """Reinforcement Learner"""
    def __init__(self, env, **usercfg):
        super(Learner, self).__init__()
        self.env = env
        self.ob_space = self.env.observation_space
        self.action_space = self.env.action_space
        self.nO = self.ob_space.shape[0]
        self.config = dict(
            episode_max_length=100,
            timesteps_per_batch=10000,
            n_iter=100)
        self.config.update(usercfg)

    def act(self, state, task=0):
        """Return which action to take based on the given state"""
        pass

    def reset_env(self, env):
        """Reset the current environment and get the initial state"""
        return env.reset()

    def step_env(self, env, action):
        """Execute an action in the current environment."""
        return env.step(action)

    def get_trajectory(self, env, task=None, render=False):
        """
        Run agent-environment loop for one whole episode (trajectory)
        Return dictionary of results
        """
        state = self.reset_env(env)
        states = []
        actions = []
        rewards = []
        for _ in range(self.config['episode_max_length']):
            action = self.act(state, task)
            states.append(state)
            for _ in range(self.config['repeat_n_actions']):
                state, rew, done, _ = self.step_env(env, action)
                if done:  # Don't continue if episode has already ended
                    break
            actions.append(action)
            rewards.append(rew)
            if done:
                break
            if render:
                env.render()
        return {"reward": np.array(rewards),
                "state": np.array(states),
                "action": np.array(actions),
                "done": done  # Tajectory ended because a terminal state was reached
                }

    def get_trajectories(self, env=None, task=None):
        """Generate trajectories until a certain number of timesteps or trajectories."""
        if env is None:
            env = self.env
        use_timesteps = self.config["batch_update"] == "timesteps"
        trajectories = []
        timesteps_total = 0
        i = 0
        while (use_timesteps and timesteps_total < self.config["timesteps_per_batch"]) or (not(use_timesteps) and i < self.config["trajectories_per_batch"]):
            i += 1
            trajectory = self.get_trajectory(env, task)
            trajectories.append(trajectory)
            timesteps_total += len(trajectory["reward"])
        return trajectories

    def learn(self):
        """Learn in the current environment."""
        pass
