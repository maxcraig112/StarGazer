from PIL import Image, ImageDraw, ImageFont
import random

def draw_logo(image_size=(512, 512)):
    """
    Draws a simple planet with craters and bands on a black background,
    and adds texts below.

    Parameters:
    - image_size (tuple): Size of the image, e.g., (512, 512).

    Returns:
    - PIL Image object.
    """
    # Create a new image with black background
    img = Image.new('RGB', image_size, color='black')
    draw = ImageDraw.Draw(img)

    # Define center and radius
    # Shift the center upwards to make space for texts at the bottom
    center = (image_size[0] // 2, image_size[1] // 2 - 30)
    radius = 120  # Scaled up from 30 to 120 for 512x512 image

    x, y = center

    # Draw the planet (circle) with white outline and white fill
    draw.ellipse(
        [(x - radius, y - radius), (x + radius, y + radius)],
        outline='white',
        fill='white'
    )

    # Add craters or spots on the planet
    num_spots = 30  # Increased number for larger image
    for _ in range(num_spots):
        raw_radius = random.gauss(5, 3)
        spot_radius = max(2,int(round(raw_radius)))
        max_offset = radius - spot_radius
        offset_x = random.randint(-max_offset, max_offset)
        offset_y = random.randint(-max_offset, max_offset)
        spot_center = (x + offset_x, y + offset_y)
        draw.ellipse(
            [
                (spot_center[0] - spot_radius, spot_center[1] - spot_radius),
                (spot_center[0] + spot_radius, spot_center[1] + spot_radius)
            ],
            fill='black'  # Black spots
        )

    # Add horizontal lines to simulate planetary bands
    num_bands = 6  # Increased number for larger image
    band_spacing = radius // (num_bands + 1)
    for i in range(1, num_bands + 1):
        band_y = y - radius + i * band_spacing
        # Define the bounding box for the arc
        arc_bbox = [
            (x - radius, band_y - radius // 4),
            (x + radius, band_y + radius // 4)
        ]
        draw.arc(
            arc_bbox,
            start=0,
            end=180,
            fill='black'  # Black bands
        )

    # Add texts below the planet
    text1 = "Star Gazer"
    text2 = "By Max Craig"
    font_size1 = 38  # Adjust the font size as needed for larger image
    font_size2 = 22  # Adjust the font size as needed for larger image

    try:
        # Try to load a TrueType font
        font1 = ImageFont.truetype("Roboto-Medium.ttf", font_size1)
        font2 = ImageFont.truetype("Roboto-Medium.ttf", font_size2)
    except IOError:
        # If not available, use the default font
        font1 = ImageFont.load_default()
        font2 = ImageFont.load_default()

    # Calculate text sizes
    text1_width, text1_height = draw.textsize(text1, font=font1)
    text2_width, text2_height = draw.textsize(text2, font=font2)

    # Initial positions for texts
    text1_x = (image_size[0] - text1_width) / 2
    text1_y = y + radius + 20  # Position text1 just below the planet
    text2_x = (image_size[0] - text2_width) / 2
    text2_y = text1_y + text1_height + 10  # Position text2 below text1

    # Check if texts fit within the image bounds
    if text2_y + text2_height > image_size[1]:
        # Adjust the planet upwards
        shift = (text2_y + text2_height) - image_size[1] + 10  # Extra 10 pixels margin
        y -= shift
        center = (x, y)
        # Redraw the planet and its features
        # Clear the image
        draw.rectangle([(0, 0), image_size], fill='black')

        # Redraw the planet with white outline and white fill
        draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            outline='white',
            fill='white'
        )

        # Redraw spots with black fill
        for _ in range(num_spots):
            spot_radius = random.randint(max(radius // 20, 3), max(radius // 10, 6))
            max_offset = radius - spot_radius
            offset_x = random.randint(-max_offset, max_offset)
            offset_y = random.randint(-max_offset, max_offset)
            spot_center = (x + offset_x, y + offset_y)
            draw.ellipse(
                [
                    (spot_center[0] - spot_radius, spot_center[1] - spot_radius),
                    (spot_center[0] + spot_radius, spot_center[1] + spot_radius)
                ],
                fill='black'  # Black spots
            )

        # Redraw planetary bands with black arcs
        for i in range(1, num_bands + 1):
            band_y = y - radius + i * band_spacing
            draw.arc(
                [(x - radius, band_y - radius // 4), (x + radius, band_y + radius // 4)],
                start=0,
                end=180,
                fill='black'  # Black bands
            )

        # Recalculate text positions after shifting
        text1_y = y + radius + 20
        text2_y = text1_y + text1_height + 10

    # Draw the texts with white color
    draw.text((text1_x, text1_y), text1, font=font1, fill='white')  # White text
    draw.text((text2_x, text2_y), text2, font=font2, fill='white')  # White text

    return img

def generate_gif(num_frames=10, image_size=(512, 512), save_path='logo.gif', duration=500):
    """
    Generates a GIF by creating multiple images with variations and adding text.

    Parameters:
    - num_frames (int): Number of frames/images to generate.
    - image_size (tuple): Size of each image.
    - save_path (str): Path to save the GIF.
    - duration (int): Duration between frames in milliseconds.
    """
    frames = []
    for i in range(num_frames):
        img = draw_logo(image_size)
        frames.append(img)

    # Save as GIF
    frames[0].save(
        save_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    print(f"GIF saved as {save_path}")

if __name__ == "__main__":
    generate_gif()
