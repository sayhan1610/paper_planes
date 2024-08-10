Here's a `README.md` for your `paper_planes` game repository. It provides a general overview, setup instructions, and a guide to the game:

````markdown
# Paper Airplane Game

Welcome to the **Paper Airplane Game**! This is a fun and engaging game where you control a paper airplane and navigate through various obstacles while collecting items and power-ups. Built with Pygame, this project is a great example of using Python for game development.

## Features

- **Control the Plane**: Use the SPACEBAR to make the plane fly upwards and avoid falling.
- **Obstacles**: Encounter static, moving, and rotating obstacles that challenge your reflexes.
- **Power-Ups**: Collect power-ups like shields, speed boosts, and slow-motion effects to enhance your gameplay.
- **Bonus Items**: Grab coins and stars to increase your score.
- **Wind Effects**: Experience the challenge of upwinds and downwinds that affect your plane's movement.
- **Score Multiplier**: Accumulate a score multiplier with power-ups to boost your final score.

## Installation

To get started with the Paper Airplane Game, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sayahan1610/paper_planes.git
   cd paper_planes
   ```
````

2. **Install Dependencies:**

   Make sure you have Python 3 and Pygame installed. You can install Pygame using pip:

   ```bash
   pip install pygame
   ```

3. **Download Game Assets:**

   Ensure that the game assets (images and sounds) are in the correct directories as referenced in the code. The required assets are:

   - Images: `sky.png`, `plane.gif`, `upwind.png`, `downwind.png`, `speed_up.png`, `speed_down.png`, `shield.png`, `coin.png`, `star.png`, `object0.png` to `object9.png`
   - Sounds: `bg_music.mp3`, `crash.mp3`, `item.mp3`, `wind.mp3`

   You should create an `images` and `sounds` directory in the project folder and place the corresponding files there.

4. **Run the Game:**

   Execute the game script using Python:

   ```bash
   python main.py
   ```

## Gameplay

1. **Home Page**: Press `ENTER` to start the game or `I` to view the instructions.
2. **Instructions Page**: Read the instructions to understand game mechanics. Press `ENTER` to return to the home page.
3. **Game Controls**:

   - **SPACEBAR**: Make the plane fly upwards.
   - **Avoid Obstacles**: Static, moving, and rotating obstacles are scattered throughout the game.
   - **Collect Items**: Grab coins and stars for points and power-ups for special effects.
   - **Wind Effects**: Be aware of upwinds and downwinds that affect your plane's velocity.

4. **Score Reporting**: After a crash, the final score is displayed. Press `ENTER` to retry the game or `ESCAPE` to quit.

## Code Structure

- **`main.py`**: Contains the main game logic, including the game loop, event handling, and rendering.
- **`Plane`**: Manages the player's plane, including movement, drawing, and power-ups.
- **`Obstacle`**: Defines obstacles in the game, including their movement and drawing.
- **`Wind`**: Represents wind effects and their impact on the plane.
- **`PowerUp`**: Handles different power-ups and their effects.
- **`BonusItem`**: Manages collectible bonus items and their effects on the score.

## Contributing

Feel free to contribute to the Paper Airplane Game by creating pull requests or reporting issues. Your feedback and improvements are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Pygame**: For the game development framework.
- **Assets**: Special thanks to the creators of the images and sounds used in the game.

Enjoy flying your paper airplane and see how high you can score!
