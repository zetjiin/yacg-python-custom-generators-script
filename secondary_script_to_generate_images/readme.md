# YACG Texture Generator

The YACG (Yet Another Code Generator) Texture Generator is a Python script designed to create unique and varied textures for each side of a block in a resource pack. It uses a combination of OpenSimplex noise and random patterns to generate textures that can be used in game development, particularly for Minecraft-style games.

## Features

- Generates a base color and three accent colors for each texture set.
- Adds random patterns (ellipse, rectangle, triangle, line, arc, chord, polygon, star, spiral) to the textures.
- Applies OpenSimplex noise to create a more natural and varied look.
- Different noise scales and thresholds for each side of the block to ensure variation.
- Saves textures with appropriate names corresponding to each side of the block.

## Requirements

- Python 3.6 or higher
- NumPy (`numpy`)
- Pillow (`Pillow`)
- OpenSimplex (`opensimplex`)
- hashlib, os (standard library modules)

## Installation

Before running the script, ensure you have the required packages installed. You can install them using pip:

```bash
pip install numpy Pillow opensimplex
```

## Usage

To generate textures, simply run the script inside the resourcepack
1.Put the script in assets\yacg\textures\block in the resourcepack folder.
	It's containing subdirectories named after the blocks you wish to generate textures for. 
	The script will create a set of five textures for each folder (representing the Bottom, Top, Side, Front, and Back of a block) 
	and save them within the respective folder.
2.Use the script in that folder

```bash
python yacg_generator_texture_generator.py
```
## Customization

You can customize various aspects of the texture generation process by adjusting the parameters at the top of the script:

- `IMAGE_SIZE`: Tuple defining the width and height of the generated images.
- `SCALE`: Used to scale the noise function for different texture effects.
- `PATTERN_SIZE_RANGE`: A tuple defining the minimum and maximum size of the patterns.
- `NUM_PATTERNS_RANGE`: A tuple defining the minimum and maximum number of patterns to generate.
- `SHAPE_TYPES`: A list of shape types to be used in pattern generation.
- `SIDE_NAMES`: A list of names corresponding to each side of the block for which textures will be generated.
- `NOISE_SCALE`: A dictionary to define different scales of noise for each side of the block.
- `NOISE_THRESHOLD`: A dictionary to define different thresholds of noise application for each side of the block.

Adjust these parameters to suit the style and complexity of the textures you need for your blocks.

## Output

The script saves the generated textures into the specified folder, naming each file according to the corresponding side of the block:

- `Bottom.png`
- `Top.png`
- `Side.png`
- `Front.png`
- `Back.png`

Ensure that the folder name provided exists within the script's directory, as the script will attempt to save the generated images there.

## License

This script is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the script or the use or other dealings in the script.
