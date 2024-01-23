import pygame
from math import sqrt
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
from minisom import MiniSom


def init_color_display(colors_with_ids):
    pygame.init()

    # Screen dimensions and setup
    screen_width = 1200
    screen_height = 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Color Display")

    color_width = screen_width // len(colors_with_ids)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a white background
        screen.fill((255, 255, 255))

        # Draw the color rectangles
        for i, color_with_id in enumerate(colors_with_ids):
            pygame.draw.rect(screen, pygame.Color(color_with_id[0]), (i * color_width, 0, color_width, screen_height))

        # Update the display
        pygame.display.flip()

    # Clean up
    pygame.quit()

def generate_colors_with_ids(n_colors):
    return [(np.random.randint(0, 255, 3), i) for i in range(n_colors)]

def sort_by_color_distance(colors):
    colors = np.array(colors) / 255.0

    def color_distance(c1, c2):
        return np.linalg.norm(np.array(c1) - np.array(c2))

    dist_matrix = squareform(pdist(colors, lambda u, v: color_distance(u, v)))

    row_index, col_ind = linear_sum_assignment(dist_matrix)

    print(row_index)

    return [tuple(int(c * 255) for c in color) for color in colors[col_ind]]

def sort_by_luminance(colors):
    luminances = []
    for color in colors:
        luminance = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        luminances.append(luminance)
    return [color for (_, color) in sorted(zip(luminances, colors), reverse=True)]

def sort_by_greyscale(colors_with_ids):
    brightnesses = []
    for color_with_id in colors_with_ids:
        brightness = sqrt(0.299 * pow(color_with_id[0][0], 2) + 0.587 * pow(color_with_id[0][1], 2) + 0.114 * pow(color_with_id[0][2], 2)) 
        brightnesses.append(brightness)
    return [color_with_id for (_, color_with_id) in sorted(zip(brightnesses, colors_with_ids), reverse=True)]

def get_hue(color):
    r = color[0] / 255
    g = color[1] / 255
    b = color[2] / 255
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin
    if delta == 0:
        hue = 0
    elif cmax == r:
        hue = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        hue = 60 * (((b - r) / delta) + 2)
    elif cmax == b:
        hue = 60 * (((r - g) / delta) + 4)

    if hue > 360:
        print(hue)

    return hue

def sort_by_hue(colors):
    hues = []
    for color in colors:
        hues.append(get_hue(color))
        
    return [color for (_, color) in sorted(zip(hues, colors))]

def sort_by_rainbow(colors_with_ids):
    hue_ranges = {
        'red': [(0.0, 0.083), (0.917, 1.001)],
        'yellow': [(0.083, 0.25)],
        'green':[(0.25, 0.430)],
        'cyan': [(0.430, 0.583)],
        'blue': [(0.583, 0.75)],
        'magenta': [(0.75, 0.917)]
    }

    categorized_colors = {color: [] for color in hue_ranges}

    for color_with_id in colors_with_ids:
        hue = get_hue(color_with_id[0]) / 360
        for rainbow_color, hue_range in hue_ranges.items():
            for (low, high) in hue_range:
                if low <= hue < high:
                    categorized_colors[rainbow_color].append(color_with_id)
                    break

    straight_colors = []

    for hue_range in hue_ranges:
        sorted_hue = sort_by_greyscale(categorized_colors[hue_range])
        
        # head = sorted_hue[0::2]
        # tail = sorted_hue[1::2]
        # straight_colors += head + tail[::-1]

        straight_colors += sorted_hue
    

    return straight_colors
    
def sort_by_SOM(colors_with_ids, som_length=100):
    # to prevent ids being duplicated if color is exactly the same
    used_ids = set()

    # Extract just the color values for SOM training
    colors = np.array([color for color, _ in colors_with_ids])

    som = MiniSom(1, som_length, 3, sigma=5.0, learning_rate=0.8)
    som.random_weights_init(colors)
    som.train_random(colors, num_iteration=10000)

    # Retrieve the sorted colors and their IDs
    sorted_colors_with_ids = []
    win_map = som.win_map(colors)
    for i in range(som_length):
        # Find the best matching unit for each neuron
        if (0, i) in win_map:
            for color in win_map[(0, i)]:
                # Find the original ID of the color
                for original_color, color_id in colors_with_ids:
                    if np.array_equal(original_color, color) and color_id not in used_ids:
                        sorted_colors_with_ids.append((color, color_id))
                        used_ids.add(color_id)
                        break

    return sorted_colors_with_ids


if __name__ == '__main__':
    rgb_colors = generate_colors_with_ids(600)  # 100 random colors

    init_color_display(rgb_colors)
    sorted_colors_with_ids = sort_by_SOM(rgb_colors)
    sorted_colors = np.array([color for color, _ in sorted_colors_with_ids])
    init_color_display(sorted_colors.reshape(-1, 1, 3))