"""Module for main entrypoint to Snake."""
from pathlib import Path

from agent import ReinforceAgent
from snake_game import Game


def main():
    game = Game()
    agent = ReinforceAgent(num_frames_per_sample=1)
    game.play_agent(agent=agent, num_episodes=2000, render=False)
    model_dir_path = Path("models")
    output_path = model_dir_path / "trained_agent.pt"
    agent.save(output_path)

    # Eval
    agent.load(output_path)
    game_stats = game.play_agent(agent=agent, num_episodes=30, eval=True, render=False)
    game_stats.plot()
    #game.play()


if __name__ == "__main__":
    main()
