import numpy as np
from PIL import Image, ImageDraw
from opensimplex import OpenSimplex
import hashlib
import os

# Parameters
# Parameters
IMAGE_SIZE = (128, 128)  # This should be a tuple representing the image size
SCALE = 100
PATTERN_SIZE_RANGE = (10, 40)
NUM_PATTERNS_RANGE = (3, 10)
SHAPE_CHOICES = ['ellipse', 'rectangle', 'triangle', 'line', 'arc', 'chord', 'polygon', 'star', 'spiral']
SIDE_NAMES = ["Bottom", "Top", "Side", "Front", "Back"]
NOISE_SCALE = {
    "Bottom": 180,
    "Top": 150,
    "Side": 120,
    "Front": 130,
    "Back": 140
}
NOISE_THRESHOLD = {
    "Bottom": 0.55,
    "Top": 0.05,
    "Side": -0.15,
    "Front": 0.25,
    "Back": -0.33
}

def folder_name_to_seed(folder_name):
    # Convert folder name to a seed value and ensure it is within the valid range for NumPy
    return int(hashlib.sha256(folder_name.encode('utf-8')).hexdigest(), 16) % (2**32)

def generate_color_theme(base_seed):
    # Seed the random number generator for color theme consistency
    np.random.seed(base_seed)
    # Generate a base color theme (e.g., a main color and accent colors)
    main_color = tuple(np.random.randint(0, 255, 3).tolist())
    accent_colors = [tuple(np.random.randint(0, 255, 3).tolist()) for _ in range(3)]
    return main_color, accent_colors

def add_patterns(image, base_seed, accent_colors):
    np.random.seed(base_seed)
    pattern_size = np.random.randint(*PATTERN_SIZE_RANGE)  # Randomize pattern size
    num_patterns = np.random.randint(*NUM_PATTERNS_RANGE)  # Randomize the number of patterns

    # Create a temporary image for the pattern
    pattern_image = Image.new('RGB', (pattern_size, pattern_size))
    pattern_draw = ImageDraw.Draw(pattern_image)

    # Define shape choices

    for _ in range(num_patterns):
        # Randomize pattern position within the temporary image
        x = np.random.randint(0, pattern_size)
        y = np.random.randint(0, pattern_size)
        # Randomize pattern color
        pattern_color = accent_colors[np.random.randint(0, len(accent_colors))]
        # Randomize pattern shape
        shape_type = np.random.choice(SHAPE_CHOICES)
        
        # Drawing logic for each shape type
        if shape_type == 'ellipse':
            rx = np.random.randint(5, pattern_size)
            ry = np.random.randint(5, pattern_size)
            pattern_draw.ellipse([x, y, x + rx * 2, y + ry * 2], outline=pattern_color, fill=pattern_color)
        elif shape_type == 'rectangle':
            rw = np.random.randint(5, pattern_size)
            rh = np.random.randint(5, pattern_size)
            pattern_draw.rectangle([x, y, x + rw, y + rh], outline=pattern_color, fill=pattern_color)
        elif shape_type == 'triangle':
            points = [(x, y),
                      (x + np.random.randint(5, pattern_size), y + np.random.randint(5, pattern_size)),
                      (x + np.random.randint(5, pattern_size), y - np.random.randint(5, pattern_size))]
            pattern_draw.polygon(points, outline=pattern_color, fill=pattern_color)

        elif shape_type == 'line':
            start_point = (x, y)
            end_point = (x + np.random.randint(0, pattern_size), y + np.random.randint(0, pattern_size))
            pattern_draw.line([start_point, end_point], fill=pattern_color, width=2)

        elif shape_type == 'arc':
            start_angle = np.random.randint(0, 360)
            end_angle = start_angle + np.random.randint(0, 360)
            pattern_draw.arc([x, y, x + pattern_size, y + pattern_size], start=start_angle, end=end_angle, fill=pattern_color)

        elif shape_type == 'chord':
            start_angle = np.random.randint(0, 360)
            end_angle = start_angle + np.random.randint(0, 360)
            pattern_draw.chord([x, y, x + pattern_size, y + pattern_size], start=start_angle, end=end_angle, fill=pattern_color)

        elif shape_type == 'polygon':
            num_points = np.random.randint(3, 6)  # Triangles to pentagons
            points = [(np.random.randint(x, x + pattern_size), np.random.randint(y, y + pattern_size)) for _ in range(num_points)]
            pattern_draw.polygon(points, outline=pattern_color, fill=pattern_color)

        elif shape_type == 'star':
            # This is a simple 5-point star for example
            cx, cy = x + pattern_size // 2, y + pattern_size // 2  # Center of the star
            points = []
            for i in range(5):
                points.append((cx + int(pattern_size // 2 * np.cos(np.pi/2 + i*2*np.pi/5)),
                               cy - int(pattern_size // 2 * np.sin(np.pi/2 + i*2*np.pi/5))))
                points.append((cx + int(pattern_size // 4 * np.cos(np.pi/2 + (i+0.5)*2*np.pi/5)),
                               cy - int(pattern_size // 4 * np.sin(np.pi/2 + (i+0.5)*2*np.pi/5))))
            pattern_draw.polygon(points, outline=pattern_color, fill=pattern_color)

        elif shape_type == 'spiral':
            # This is a simple spiral for example
            for i in range(0, pattern_size, 2):
                angle = 0.1 * i
                x_offset = int(pattern_size // 2 + angle * np.cos(angle))
                y_offset = int(pattern_size // 2 + angle * np.sin(angle))
                pattern_draw.point((x_offset, y_offset), fill=pattern_color)

    # Tile the pattern across the entire image
    for i in range(0, IMAGE_SIZE[0], pattern_size):
        for j in range(0, IMAGE_SIZE[1], pattern_size):
            image.paste(pattern_image, (i, j))

def generate_texture(base_seed, side_name, main_color, accent_colors):
    # Initialize OpenSimplex with the base seed
    simplex = OpenSimplex(seed=base_seed)
    
    # Generate a texture using OpenSimplex noise and the provided color theme
    image = Image.new('RGB', IMAGE_SIZE, main_color)
    draw = ImageDraw.Draw(image)
    
    # Add random shapes based on the side name
    side_seed = int(hashlib.sha256(side_name.encode('utf-8')).hexdigest(), 16) % (2**32)
    np.random.seed(side_seed)
    add_patterns(image, base_seed, accent_colors)  # Pass the image object here
    
    # Convert to numpy array for noise addition
    image_array = np.array(image)
    for i in range(IMAGE_SIZE[0]):
        for j in range(IMAGE_SIZE[1]):
            noise_val = simplex.noise2(x=i / NOISE_SCALE[side_name], y=j / NOISE_SCALE[side_name])
            if noise_val > NOISE_THRESHOLD[side_name]:  # Apply noise with variation per side
                image_array[i, j] = image_array[i, j] * (1 - noise_val) + np.array(main_color) * noise_val
    
    return image_array

def save_images(folder_name, images):
    # Save the generated images with the given names
    for img, name in zip(images, SIDE_NAMES):
        Image.fromarray(img.astype('uint8'), 'RGB').save(f'{folder_name}/{name}.png')

def generate_folder_textures(folder_name):
    base_seed = folder_name_to_seed(folder_name)
    main_color, accent_colors = generate_color_theme(base_seed)
    
    images = []
    for side_name in SIDE_NAMES:
        images.append(generate_texture(base_seed, side_name, main_color, accent_colors))
    
    save_images(folder_name, images)

def generate_all_folder_textures():
    # Get all folders in the current directory
    folders = [f for f in os.listdir('.') if os.path.isdir(f)]
    
    # Loop through each folder and generate textures
    for folder in folders:
        print(f"Generating textures for folder: {folder}")
        generate_folder_textures(folder)
        print(f"Finished generating textures for folder: {folder}")

# Example usage for a single folder
# Run the texture generation for all folders
generate_all_folder_textures()
