import pandas as pd
import numpy as np
import ast
from pathlib import Path
from tqdm import tqdm
import os
import matplotlib.pyplot as plt  

def parse_cluster_pixels(cluster_pixels_str):
    """
    Parses a string in the format '[x, y, E, t][x, y, E, t]...' into a list of coordinates and energy values.
    """
    cluster_pixels = ast.literal_eval(cluster_pixels_str.replace('][', '],['))
    return [(int(x), int(y), float(E)) for x, y, E, t in cluster_pixels]

def normalize_energy(data, E_min, E_max):
    """
    Normalizes energy values within the range [E_min, E_max].
    """
    return [(x, y, (E - E_min) / (E_max - E_min)) for x, y, E in data]

def center_and_scale_coordinates(cluster_data, image_size):
    """
    Centers the cluster coordinates within the image and scales them.
    """
    x_coords = np.array([x for x, _, _ in cluster_data])
    y_coords = np.array([y for _, y, _ in cluster_data])
    
    # Determine shifts for centering
    x_center_shift = (image_size[0] // 2) - int(np.round(x_coords.mean()))
    y_center_shift = (image_size[1] // 2) - int(np.round(y_coords.mean()))
    
    # Apply shifts to the coordinates
    x_centered = x_coords + x_center_shift
    y_centered = y_coords + y_center_shift
    
    # Clamp coordinates to image boundaries
    x_centered = np.clip(x_centered, 0, image_size[0] - 1)
    y_centered = np.clip(y_centered, 0, image_size[1] - 1)

    # Reassemble the new coordinates considering energy
    centered_cluster_data = [(x, y, E) for (x, y, E), x, y in zip(cluster_data, x_centered, y_centered)]
    
    return centered_cluster_data

def create_image(cluster_data, image_size=(256, 256)):
    """
    Creates a 2D image based on coordinates and energy values.
    """
    image = np.zeros(image_size)
    for x, y, E in cluster_data:
        if 0 <= x < image_size[0] and 0 <= y < image_size[1]:
            image[x, y] = E
    return image

def process_file(input_file, output_dir, E_min, E_max, image_size=(256, 256), max_rows=None):
    """
    Processes a file containing clusters and saves images.
    """
    # Create directory for saving images
    os.makedirs(output_dir, exist_ok=True)

    # Read the file
    df = pd.read_csv(input_file, sep='\t')

    # If a row limit is specified
    if max_rows is not None:
        df = df.head(max_rows)

    # Extract and process 'ClusterPixels'
    for index, row in tqdm(df.iterrows(), total=len(df)):
        cluster_pixels_str = row['ClusterPixels']
        cluster_data = parse_cluster_pixels(cluster_pixels_str)

        # Normalize energy
        cluster_data = normalize_energy(cluster_data, E_min, E_max)

        # Center and scale coordinates
        cluster_data = center_and_scale_coordinates(cluster_data, image_size)

        # Create the image
        image = create_image(cluster_data, image_size=image_size)

        # Save the image
        output_path = Path(output_dir) / f"image_{index}.npy"
        np.save(output_path, image)

def compute_global_energy_range(files):
    E_min = float('inf')
    E_max = float('-inf')
    for file in files:
        df = pd.read_csv(file, sep='\t')
        for _, row in df.iterrows():
            cluster_pixels_str = row['ClusterPixels']
            cluster_data = parse_cluster_pixels(cluster_pixels_str)
            energies = [E for _, _, E in cluster_data]
            E_min = min(E_min, min(energies))
            E_max = max(E_max, max(energies))
    return E_min, E_max

def visualize_image(image_path):
    """
    Visualizes an image saved in .npy format.
    """
    image = np.load(image_path)
    plt.figure(figsize=(5, 5))
    plt.imshow(image, cmap='viridis')
    plt.colorbar(label='Normalized Energy')
    plt.title("Cluster Image")
    plt.show()

# Parameters
experiment_file = "Am_TPX3_vacuum_prelim_E_5p49MeV.clist"
simulation_file = "80V_TPX3_alpha_particle_simulation_in_vacuum.clist"
simulation_file_new = "Simulation_TPX3_500um_Si_vacuum_Am.clist"
output_dir_experiment = "processed_experiment_images_12"
output_dir_simulation = "processed_simulation_images_12"
output_dir_simulation_new = "processed_simulation_images_new_12"
image_size = (12, 12)  
max_rows_experiment = 2500  

# Compute global energy range
E_min, E_max = compute_global_energy_range([experiment_file])
# print(E_max, E_min)
E_min, E_max = compute_global_energy_range([simulation_file_new])
# print(E_max, E_min)
# Process data
process_file(experiment_file, output_dir_experiment, E_min, E_max, image_size, max_rows=max_rows_experiment)
process_file(simulation_file, output_dir_simulation, E_min, E_max, image_size)
process_file(simulation_file_new, output_dir_simulation_new, E_min, E_max, image_size)

# Visualize an example
example_image_path = Path(output_dir_simulation_new) / "image_0.npy"
visualize_image(example_image_path)
