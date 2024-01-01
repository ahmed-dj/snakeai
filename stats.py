"""Module for the GameStats class."""
import matplotlib.pyplot as plt


class GameStats:
    def __init__(self) -> None:
        super().__init__()
        self.episodes = []

    def add_episode(self, reward: int, duration: int) -> None:
        self.episodes.append((
            len(self.episodes) + 1,
            reward,
            duration
        ))

    def plot(self):
        idx, rewards, durations = zip(*self.episodes)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.set_title("Rewards")
        ax2.set_title("Episode length")
        ax1.set_xlabel("Episode")
        ax2.set_xlabel("Episode")
        ax1.set_ylabel("Rewards")
        ax2.set_ylabel("Length")

        ax1.plot(idx, rewards)
        ax2.plot(idx, durations)

        plt.show()
