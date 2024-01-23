import pygame
from math import sqrt
import numpy as np
from colormath.color_objects import LabColor, LCHabColor
from colormath.color_conversions import convert_color
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
from itertools import groupby


def init_color_display(colors):
    pygame.init()

    # Screen dimensions and setup
    screen_width = 1200
    screen_height = 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Color Display")

    color_width = screen_width // len(colors)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a white background
        screen.fill((255, 255, 255))

        # Draw the color rectangles
        for i, color in enumerate(colors):
            pygame.draw.rect(screen, pygame.Color(color), (i * color_width, 0, color_width, screen_height))

        # Update the display
        pygame.display.flip()

    # Clean up
    pygame.quit()


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

def sort_by_greyscale(colors):

    brightnesses = []
    for color in colors:
        brightness = sqrt(0.299 * pow(color[0], 2) + 0.587 * pow(color[1], 2) + 0.114 * pow(color[2], 2)) 
        brightnesses.append(brightness)
    return [color for (_, color) in sorted(zip(brightnesses, colors), reverse=True)]

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

def sort_by_rainbow(colors):
    hue_ranges = {
        'red': [(0.0, 0.083), (0.917, 1.001)],
        'yellow': [(0.083, 0.25)],
        'green':[(0.25, 0.430)],
        'cyan': [(0.430, 0.583)],
        'blue': [(0.583, 0.75)],
        'magenta': [(0.75, 0.917)]
    }

    categorized_colors = {color: [] for color in hue_ranges}

    for color in colors:
        hue = get_hue(color) / 360
        for rainbow_color, hue_range in hue_ranges.items():
            for (low, high) in hue_range:
                if low <= hue < high:
                    categorized_colors[rainbow_color].append(color)
                    break

    straight_colors = []

    for hue_range in hue_ranges:
        sorted_hue = sort_by_greyscale(categorized_colors[hue_range])
        head = sorted_hue[0::2]
        tail = sorted_hue[1::2]
        straight_colors += head + tail[::-1]

    return straight_colors
    

if __name__ == '__main__':
    color_count = 600
    for i in range(1):
        rgb_colors = np.random.rand(color_count, 3) * 255.0  # 100 random colors

        colors = sort_by_rainbow(rgb_colors)
        init_color_display(colors)