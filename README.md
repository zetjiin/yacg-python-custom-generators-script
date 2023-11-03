README for Yet Another Cobblestone Generator (YACG) Resource Pack and Script

TL;DR
-----

To customize your Minecraft cobblestone generators:

1.  Install Python and the Pillow library.
2.  Install the KubeJS and YACG mods in Minecraft.
3.  Configure the `input.json` and `config.json` files.
4.  Run the Python script to generate your resource pack and scripts.
5.  Place the output folders into your Minecraft instance folder
6.  (optional) If you want, replace the textures in the resource pack with your own textures, it's pretty easy to do.
	- to help with this I created secondary script in secondary_script_to_generate_images folder
	
Enjoy your customized generators in Minecraft!
Thanks to the https://github.com/syorito-hatsuki for making this possible!

============================================================================

General Description
-------------------

This repository contains a Python script and associated JSON configuration files designed to work with the Minecraft mod "Yet Another Cobblestone Generator" (YACG). 
The script automates the creation of resource packs with textures and KubeJS recipe scripts for easy creation of custom generators.

Requirements
------------

To use this script, you will need:

*   **Python**: The script is written in Python, so you must have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
*   **Pillow Library**: This Python script uses the Pillow library for image processing. Install it using pip:
    
    Copy code
    
    `pip install Pillow`
    
*   **Minecraft Mods**: You must have the following mods installed in your Minecraft instance:
    *   KubeJS (for custom scripting in Minecraft)
    *   Yet Another Cobblestone Generator (YACG)

Setup
-----

1.  Clone the repository or download the files to your local machine.
2.  Ensure you have Python installed, and then install the required Python libraries using pip.
3.  Place the `config.json`, `constants.json`, and `input.json` files in the same directory as the Python script.

Configuration Files
-------------------

### `input.json`
This file defines the generators you want to create. 
You can specify the items you want to generate, along with their recipes. 

    Copy code

    '''
    {
    "generator_name": {
      "items": ["namespace:generatedblockname", "namespace:generatedblockname2", etc...],
      "recipe": {
        "pattern": ["KKK", "KCK", "KKK"],
        "key": {
          "K": {"item": "namespace:recipeblockk"},
          "C": {"item": "namespace:recipeblockc"}
        }
      }
    },etc...
  '''


For example:

    Copy code

    '''
    {
    "basic_building_blocks": {
      "items": ["minecraft:cobblestone", "minecraft:cobblestone_slab", "minecraft:cobblestone_stairs"],
      "recipe": {
        "pattern": ["KKK", "KCK", "KKK"],
        "key": {
          "K": {"item": "minecraft:cobblestone"},
          "C": {"item": "minecraft:cobblestone_slab"}
        }
      }
    },
    "stone_variants": {
      "items": ["minecraft:cobbled_deepslate", "minecraft:deepslate", "minecraft:dripstone_block"],
      "recipe": {
        "pattern": ["DDD", "DKD", "DDD"],
        "key": {
          "K": {"item": "minecraft:deepslate"},
          "D": {"item": "minecraft:dripstone_block"}
        }
      }
    },
    "precious_blocks": {
      "items": ["minecraft:gold_ore", "minecraft:diamond_ore", "minecraft:emerald_ore"],
      "recipe": {
        "pattern": ["GGG", "GDG", "GGG"],
        "key": {
          "G": {"item": "minecraft:gold_ore"},
          "D": {"item": "minecraft:diamond_ore"}
        }
      }
    }
  }
  '''

### `config.json`

This file contains the configuration for the resource pack, such as the output path, resource pack name, font settings, image size, and pack metadata.
primary coefficients, secondary coefficients, and count values.

For example, if you have a primary coefficient of 100 and a secondary coefficient subtraction of 10 for a generator with 5 items, the coefficients will be 100, 90, 80, 70, and 60 respectively.
*   **Output Path**: The directory where the resource pack and scripts will be saved, if you use your instances absolute path it will override the config and resource pack in your instance.
*   **Resource Pack Name**: The name of the resource pack.
*   **Font Path**: The path to the font file used for text in images.
*   **Font Size**: The base size of the font.
*   **Image Size**: The size of the placeholder textures.
*   **Pack Description**: A description for the resource pack.
*   **Pack Format Version**: The pack format version used in `pack.mcmeta`.

*   **Primary Coefficient**: This is the base probability of an item being generated.
*   **Secondary Coefficient**: This is a modifier that is subtracted from the primary coefficient for each subsequent item, ensuring a distribution of probabilities.
*   **Count Value**: This is the number of items generated per successful generation event.

Usage
-----

Run the Python script with the following command:

Copy code

`python script.py`

The script will:

*   Read the `input.json` and `config.json` files.
*   Generate placeholder textures for each block.
*   Create `.json` files for blockstates, blocks, and items.
*   Generate a `pack.mcmeta` file with the specified pack format and description.
*   Create a language file for the resource pack.

Troubleshooting
---------------

If you encounter any issues while using the script, such as errors during execution or problems with the generated resource pack, please refer to the following troubleshooting tips:

- Ensure that you have the correct version of Python installed and that the Pillow library is up to date.
- Check that the Minecraft mods are compatible with your version of Minecraft and are correctly installed in your instance folder.
- If you encounter any path-related issues, ensure that the paths specified in `config.json` are absolute and correctly formatted for your operating system.
- Make sure that the namespaces are correct, the mods for those namespaces installed, and there are no typos in the input or config files.

Contributing
------------

Contributions to this project are welcome!

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

Acknowledgments
---------------

- Thanks to the Minecraft modding community for their invaluable resources and support.
- Special thanks to [syorito-hatsuki](https://github.com/syorito-hatsuki) for the original mod that inspired this script.
- Thanks to OpenAI for the GPT that helped me with this entire thing.

Contact Information
-------------------

For support or queries, please open an issue on the GitHub repository or contact us directly at [email protected]

Changelog
---------

### v1.0.0 - 2023-11-03
- Initial release of the script.
- Default pack format in config set to 15
