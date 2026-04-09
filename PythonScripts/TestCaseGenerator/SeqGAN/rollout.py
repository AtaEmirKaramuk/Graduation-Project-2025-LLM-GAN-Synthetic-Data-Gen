import torch
import torch.nn as nn
import copy
import numpy as np

class Rollout:
    def __init__(self, generator, update_rate=0.8):
        self.generator = generator
        self.own_gen = copy.deepcopy(generator)
        self.update_rate = update_rate

    def get_reward(self, input_x, rollout_num, discriminator, start_letter, max_seq_len):
        """
        For each partial sequence in input_x, perform rollout_num simulations,
        and get average reward from the discriminator.
        """
        rewards = []
        batch_size = input_x.size(0)

        for t in range(1, max_seq_len + 1):
            samples = []
            for _ in range(rollout_num):
                # generate completions from partial sequence input_x[:, :t]
                sample = self.own_gen.sample(batch_size, seq_len=max_seq_len, given_seq=input_x[:, :t], start_letter=start_letter)
                samples.append(sample)
            samples = torch.stack(samples).view(-1, max_seq_len)  # shape: (rollout_num * batch, max_seq_len)
            pred = discriminator.batchClassify(samples)
            pred = pred.view(rollout_num, batch_size).mean(0)  # average reward over rollouts
            rewards.append(pred)

        return torch.stack(rewards, dim=1)  # shape: (batch_size, max_seq_len)

    def update_params(self):
        for target_param, src_param in zip(self.own_gen.parameters(), self.generator.parameters()):
            target_param.data = self.update_rate * target_param.data + (1 - self.update_rate) * src_param.data
