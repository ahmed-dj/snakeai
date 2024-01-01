"""Module for the AI agent implementation."""
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam

from constants import MoveDirection


MoveDirectionIntEncoding = {
    MoveDirection.UP: 0,
    MoveDirection.RIGHT: 1,
    MoveDirection.DOWN: 2,
    MoveDirection.LEFT: 3,
}
MoveDirectionIntEncodingReverse = {
    i: d for d, i in MoveDirectionIntEncoding.items()
}


class Network(nn.Module):
    def __init__(self, in_channels: int, num_actions: int = len(MoveDirection)) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=4, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.flatten = nn.Flatten()
        self.fc2 = nn.Linear(196, num_actions)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.fc2(self.flatten(x))
        return self.softmax(x)
    

class ReinforceAgent:
    def __init__(self, num_frames_per_sample: int = 3, num_actions: int = len(MoveDirection), discount: float = 0.9) -> None:
        super().__init__()
        self.net = Network(in_channels=num_frames_per_sample, num_actions=num_actions)
        self.discount = discount
        self.actions_log_probs = []
        self.rewards = []
        self.optimizer = Adam(self.net.parameters())

    def select_policy_action(self, state: np.ndarray, eval: bool = False) -> MoveDirection:
        if eval:
            self.net.eval()
        state = torch.tensor(state)
        actions_probs = self.net(state)
        actions_probs_dist = torch.distributions.Categorical(actions_probs)
        action = actions_probs_dist.sample()
        self.actions_log_probs.append(actions_probs_dist.log_prob(action))
        return MoveDirectionIntEncodingReverse[action.item()]
    
    def add_reward(self, reward: int) -> None:
        self.rewards.append(reward)

    def train_step(self) -> None:
        exp_returns = torch.tensor([
            sum(
                self.rewards[k] * (self.discount ** (k-t))
                for k in range(t, len(self.rewards))
            )
            for t in range(len(self.rewards))
        ])
        exp_returns = (exp_returns - exp_returns.mean()) / (exp_returns.std() + 1e-9)
        
        losses = []
        for log_prob, exp_return in zip(self.actions_log_probs, exp_returns):
            losses.append(-log_prob * exp_return)

        self.optimizer.zero_grad()
        loss = torch.cat(losses).sum() # Pb with exp_returns,it's empty bus hould never be --> need to check the reward collection
        loss.backward()
        self.optimizer.step()

        self.clear()

    def clear(self):
        self.rewards = []
        self.actions_log_probs = []

    def save(self, output_path: Path) -> None:
        torch.save(self.net.state_dict(), output_path)

    def load(self, net_path: Path) -> None:
        self.net.load_state_dict(torch.load(net_path))

        


if  __name__ == "__main__":
    import numpy as np
    m = np.ones((1, 3, 15, 15), dtype=np.float32)


    net = Network(in_channels=m.shape[1], num_actions=4)
    agent = ReinforceAgent()

    print(agent.select_policy_action(state=m))
