import json
import os
from PIL import Image, ImageDraw, ImageFont

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Load constants
with open('constants.json', 'r') as constants_file:
    constants = json.load(constants_file)
    
# Use the configuration values
output_path = config["output_path"]
resource_pack_name = config["resource_pack_name"]
c_font_path = config["font_path"]
c_font_size = config["font_size"]
c_image_size = config["image_size"]
primary_coefficient = config["primary_coefficient"]
secondary_coefficient_subtraction = config["secondary_coefficient_subtraction"]
count_value = config["count_value"]
pack_description = config["pack_description"]
pack_format_version = config["pack_format_version"]

# Define the directories to save the .json files and textures
blockstates_directory = f"{output_path}/resourcepacks/{resource_pack_name}/assets/yacg/blockstates"
block_directory = f"{output_path}/resourcepacks/{resource_pack_name}/assets/yacg/models/block"
item_directory = f"{output_path}/resourcepacks/{resource_pack_name}/assets/yacg/models/item"
textures_directory = f"{output_path}/resourcepacks/{resource_pack_name}/assets/yacg/textures/block"
lang_directory = f"{output_path}/resourcepacks/{resource_pack_name}/assets/yacg/lang"

#add resourcepack folder in front of former directories
group_definitions_directory = f"{output_path}/config/yacg"
output_dir = f"{output_path}/kubejs/server_scripts"
group_definitions_file_name = "generators.json"

# Ensure the output directories exist
os.makedirs(blockstates_directory, exist_ok=True)
os.makedirs(block_directory, exist_ok=True)
os.makedirs(item_directory, exist_ok=True)
os.makedirs(textures_directory, exist_ok=True)
os.makedirs(group_definitions_directory, exist_ok=True)
os.makedirs(lang_directory, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Load the unified input definitions JSON
with open('input.json', 'r') as f:
    input_data = json.load(f)

# Initialize the language data dictionary
lang_data = {}
group_definitions_data = {}

# Template for the blockstates .json files
blockstates_template = constants["blockstates_template"] #

# Template for the block .json files
block_template = constants["block_template"] #

# Template for the item .json files
item_template = constants["item_template"] 

# Template suffix for the generator.json file
constant_groups = constants["constant_groups"]

# Function to create pack.mcmeta file
def create_pack_mcmeta(output_path, resource_pack_name, pack_format, description):
    pack_mcmeta_content = {
        "pack": {
            "pack_format": pack_format,
            "description": description
        }
    }
    pack_mcmeta_path = os.path.join(output_path, "resourcepacks", resource_pack_name, "pack.mcmeta")
    with open(pack_mcmeta_path, 'w') as pack_mcmeta_file:
        json.dump(pack_mcmeta_content, pack_mcmeta_file, indent=4)


# Function to fit text within a given width
def fit_text(draw, text, max_width, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textbbox((0, 0), text, font=font)[2]
    while text_width > max_width:
        # Reduce font size
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        text_width = draw.textbbox((0, 0), text, font=font)[2]
    return font

# Function to create placeholder textures
def create_placeholder_texture(texture_path, side_name, group_name):
    # Create a new image with mode 'RGB' and the configured background color
    img = Image.new('RGB', tuple([c_image_size,c_image_size]), color='#9e9e9e')
    # Get a drawing context
    d = ImageDraw.Draw(img)
    # Specify the path to the Arial font file on your system
    font_path = c_font_path  # Replace with the correct path for your system
    font_size = c_font_size  # Starting font size

    # Function to fit text in a given width
    def fit_text(text, max_width, font_path, font_size):
        font = ImageFont.truetype(font_path, font_size)
        text_width = d.textbbox((0, 0), text, font=font)[2]
        while text_width > max_width:
            # Reduce font size
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            text_width = d.textbbox((0, 0), text, font=font)[2]
        return font

    # Fit the side name in the top right corner
    fnt = fit_text(side_name, c_image_size, font_path, font_size)
    side_text_width = d.textbbox((0, 0), side_name, font=fnt)[2]
    side_text_position = (c_image_size - side_text_width, 0)
    d.text(side_text_position, side_name, font=fnt, fill='black')

    # Fit the group name on the left center
    fnt = fit_text(group_name, c_image_size, font_path, font_size)
    group_text_width, group_text_height = d.textbbox((0, 0), group_name, font=fnt)[2:4]
    group_text_position = (0, (c_image_size - group_text_height) / 2)
    d.text(group_text_position, group_name, font=fnt, fill='black')

    # Save the image
    img.save(texture_path)

# Function to generate textures for each side of a block group
def generate_textures_for_group(group_name):
    sides = ["Bottom", "Top", "Side", "Front", "Back"]
    for side in sides:
        texture_path = os.path.join(textures_directory, f"{group_name}/{side.lower()}.png")
        os.makedirs(os.path.dirname(texture_path), exist_ok=True)
        if not os.path.exists(texture_path):
            create_placeholder_texture(texture_path, side, group_name)

# Function to generate blockstates, block models, item models, and language entries
def generate_assets(group_name):
    # Generate blockstates JSON
    blockstates_path = os.path.join(blockstates_directory, f"{group_name}.json")
    with open(blockstates_path, 'w') as f:
        blockstates_content = json.dumps(blockstates_template).replace("{}", group_name)
        f.write(blockstates_content)

    # Generate block model JSON
    block_model_path = os.path.join(block_directory, f"{group_name}.json")
    with open(block_model_path, 'w') as f:
        block_content = json.dumps(block_template).replace("{}", group_name)
        f.write(block_content)

    # Generate item model JSON
    item_model_path = os.path.join(item_directory, f"{group_name}.json")
    with open(item_model_path, 'w') as f:
        item_content = json.dumps(item_template).replace("{}", group_name)
        f.write(item_content)

# Function to create the en-US.json file
def create_lang_file(input_data, lang_directory):
    lang_data = {}
    for group_name, group_data in input_data.items():
        # Create a string of item names separated by commas
        item_names = ", ".join(item.split(":")[1] for item in group_data['items'])  # Assumes 'minecraft:item_name' format
        #get rid of "_" from each item name and capitalize each word
        item_names = " ".join(item_names.split("_")).title()
        #add newline character after each item name
        item_names = item_names.replace(", ", ",\n")
        lang_data[f"block.yacg.{group_name}"] = f"{item_names}"

    # Set the file path for the en-US.json file
    lang_file_path = os.path.join(lang_directory, "en_us.json")

    # Write the language content to the file
    with open(lang_file_path, 'w') as lang_file:
        json.dump(lang_data, lang_file, indent=4, ensure_ascii=False)

# Start of the KubeJS script
kubejs_script = """
// This script was generated by a Python script
ServerEvents.recipes(event => { //listen for the "recipes" server event.
"""

# Process each group in the unified definitions
group_definitions = {"generators": {}}
for group_name, group_data in input_data.items():
    items = group_data['items']
    subtracted_value = primary_coefficient
    # Add group definitions data
    subtracted_value -= secondary_coefficient_subtraction
    group_definitions["generators"][group_name] = [
        {
            "itemId": item_id,
            "coefficient": primary_coefficient if index == 0 else subtracted_value,
            "count": count_value
        }
        for index, item_id in enumerate(items)
    ]
    recipe = group_data['recipe']
    generate_textures_for_group(group_name)
    generate_assets(group_name)

    
    # Generate KubeJS recipe part
    output_item = f"yacg:{group_name}"
    pattern = recipe['pattern']
    key = recipe['key']
    key_string = ', '.join(f"'{k}': '{v['item']}'" for k, v in key.items())
    kubejs_script += f"""
  event.shaped(Item.of('{output_item}', 1), [
    '{pattern[0]}',
    '{pattern[1]}',
    '{pattern[2]}'
  ], {{
    {key_string}
  }})
"""

# add constant groups to group definitions
group_definitions["generators"].update(constant_groups)

# End of the KubeJS script
kubejs_script += """
})
"""

# Write the KubeJS script to a file
script_path = os.path.join(output_dir, 'yacg_generator_recipes.js')
with open(script_path, 'w') as f:
    f.write(kubejs_script)

# Call the function to create the language file
create_lang_file(input_data, lang_directory)

# Call the function with the necessary details
create_pack_mcmeta(output_path, resource_pack_name, pack_format_version, f"{pack_description}")

# Write the group definitions content to the file
group_definitions_file_path = os.path.join(group_definitions_directory, group_definitions_file_name)
with open(group_definitions_file_path, 'w') as group_definitions_file:
    json.dump(group_definitions, group_definitions_file, indent=4)

print("KubeJS script generated successfully.")
print("Placeholder textures generated successfully.")
print("Blockstates, block models, and item models generated successfully.")
print("Language file generated successfully.")
