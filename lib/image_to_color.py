import requests
from PIL import Image
from io import BytesIO

def image_to_color(image_url):
    if not image_url:
        return (0, 0, 0)

    # Fetch the image from the URL
    response = requests.get(image_url)
    if response.status_code != 200:
        return (0, 0, 0)

    # Open the image
    with Image.open(BytesIO(response.content)) as img:
        # Resize the image to reduce computation if it's very large
        img.thumbnail((100, 100))

        # Initialize variables to store the sum of all colors
        r_total, g_total, b_total = 0, 0, 0

        # Iterate over each pixel
        for x in range(img.width):
            for y in range(img.height):
                try:
                    r, g, b = img.getpixel((x, y))
                    r_total += r
                    g_total += g
                    b_total += b
                except ValueError:
                    print(image_url)
                    return (0, 0, 0)
                

        # Calculate the average color
        num_pixels = img.width * img.height
        avg_r = r_total // num_pixels
        avg_g = g_total // num_pixels
        avg_b = b_total // num_pixels

        return (avg_r, avg_g, avg_b)
