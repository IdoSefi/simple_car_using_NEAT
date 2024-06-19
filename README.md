# README

## Overview

This project is a car simulation game developed using Pygame and NEAT (NeuroEvolution of Augmenting Topologies) for training artificial intelligence. The game involves cars navigating a track, with their movements controlled by a neural network trained through NEAT.

## Features

- **Car Movement and Control**: The cars move based on their velocity and angle, with the ability to steer left and right.
- **Radar System**: Each car is equipped with a radar to detect distances to obstacles and boundaries.
- **Collision Detection**: The game includes collision detection to determine if a car has gone off the track.
- **Neural Network Training**: Uses NEAT to evolve the neural networks controlling the cars' movements over multiple generations.
- **Fitness Evaluation**: The fitness of each neural network is evaluated based on the car's performance on the track.

## Requirements

- Python 3.x
- Pygame
- NEAT-Python
- Pandas

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/car-simulation-game.git
   cd car-simulation-game
   ```

2. **Install the required libraries**:
   ```
   pip install pygame neat-python pandas
   ```

3. **Assets**: Ensure the following files are present in the `assets` folder:
   - `red-car.png`: Image file for the car.
   - `gray good map.png`: Image file for the background map.

4. **Configuration**: Ensure the `config-feedforward.txt` file is present in the root directory.

## How to Run

1. **Run the Simulation**:
   ```
   python car_simulation.py
   ```

2. **NEAT Training**: The neural networks are trained using the NEAT algorithm. The training process runs for 100 generations by default.

## Code Explanation

### Main Components

#### 1. `Car` Class
- **Initialization**: Loads the car image, sets initial position, angle, acceleration, and velocity.
- **Movement**: Updates the car's position and angle based on its velocity.
- **Collision Detection**: Checks for collisions with the track boundaries.
- **Radar System**: Calculates the distance to obstacles using a radar mechanism.

#### 2. `draw_all` Function
- Draws the car on the screen.

#### 3. `move_all` Function
- Updates the position of all cars.

#### 4. `loose` Function
- Handles the removal of cars that go off the track.

#### 5. `main` Function
- Core game loop that initializes the neural networks, evaluates fitness, and processes user inputs.

#### 6. `run` Function
- Configures and runs the NEAT algorithm, saving the best-performing neural network.

### NEAT Configuration
- The NEAT configuration file (`config-feedforward.txt`) specifies the parameters for the neural network evolution, such as population size, mutation rates, and network structure.

### Files
- **car_simulation.py**: Main Python script containing the game and NEAT training logic.
- **assets/red-car.png**: Image file for the car.
- **assets/gray good map.png**: Background map for the track.
- **config-feedforward.txt**: Configuration file for NEAT.

## Usage

- The game starts with the cars being controlled by randomly initialized neural networks.
- Over generations, the neural networks evolve to improve their performance in navigating the track.
- The best-performing neural network is saved to a file (`best car mix.pickle`).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- The NEAT-Python library for the implementation of the NEAT algorithm.
- Pygame for the game development framework.

## Contact

For any questions or suggestions, feel free to open an issue or contact the project maintainers at `your.email@example.com`.
