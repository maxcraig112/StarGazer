from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1107
from smbus2 import SMBus
from PIL import ImageFont
from time import sleep
import math
import random
import bitmap

bus = SMBus(3) 
serial = i2c(bus=bus, address=0x3C)
device = sh1107(serial, rotate=0, height=128, width=128)
def displayText(lines):
    if type(lines) is str:
        lines = [lines]
    with canvas(device) as draw:
        max_width, max_height = 128, 128
        min_font_size = 12  # Minimum font size
        font_size = 40  # Start with a large font size
        font = None
        fits = False

        while font_size >= min_font_size and not fits:
            font = ImageFont.truetype("Tests/fonts/FreeMono.ttf", font_size)
            text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])
            
            # Check if the total height fits within the screen
            if text_height <= max_height:
                # Check if each line fits within the screen's width
                fits = all([(draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]) <= max_width for line in lines])
            
            if not fits:
                font_size -= 1  # Decrease the font size and try again

        # If font size is smaller than the minimum allowed, wrap text to new lines
        if font_size < min_font_size:
            font = ImageFont.truetype("Tests/fonts/FreeMono.ttf", min_font_size)
            wrapped_lines = []
            for line in lines:
                words = line.split(' ')
                current_line = ''
                for word in words:
                    test_line = current_line + ' ' + word if current_line else word
                    text_width = draw.textbbox((0, 0), test_line, font=font)[2] - draw.textbbox((0, 0), test_line, font=font)[0]
                    if text_width <= max_width:
                        current_line = test_line
                    else:
                        wrapped_lines.append(current_line)
                        current_line = word
                if current_line:
                    wrapped_lines.append(current_line)
            lines = wrapped_lines

        # Calculate total height for the wrapped lines
        text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])
        
        # Start drawing text from a position that centers it vertically
        y = (128 - text_height) // 2

        for line in lines:
            # Calculate the width of the current line using textbbox
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            # Center the text horizontally
            x = (128 - text_width) // 2
            draw.text((x, y), line, font=font, fill="white")
            y += text_bbox[3] - text_bbox[1] + 5  # Move y down for the next line

def displayAltitudeArrow(targetAltitude: float, altitude: float):
    with canvas(device) as draw:
        difference = targetAltitude - altitude
        print(f"difference: {difference}")
        
        # Limit the difference to a range between -90 and 90 degrees
        if difference < 0:
            difference = max(-90, difference)
        else:
            difference = min(90, difference)
        
        absDifference = abs(difference)
        
        # Calculate padding to center the arrow vertically
        padding = int((128 - absDifference) / 2)
        
        # Draw the vertical line representing the arrow shaft
        draw.line(
            [(64, padding), (64, min(120, absDifference + padding))],
            fill="white",
            width=3
        )
        
        # Determine the length of the arrowhead
        arrowLength = 10 if absDifference > 10 else absDifference
        
        # Decide the text to display and draw the arrowhead
        if difference > 0:
            # Arrow pointing up
            draw.line(
                [
                    (64 - arrowLength, absDifference + padding - arrowLength),
                    (64, absDifference + padding),
                    (64 + arrowLength, absDifference + padding - arrowLength)
                ],
                fill="white",
                width=3
            )
            text = "tilt telescope up"
        else:
            # Arrow pointing down
            draw.line(
                [
                    (64 - arrowLength, padding + arrowLength),
                    (64, padding),
                    (64 + arrowLength, padding + arrowLength)
                ],
                fill="white",
                width=3
            )
            text = "tilt telescope down"
        
        font = ImageFont.truetype("Roboto-Medium.ttf", 14)  # Load the font

        # --- Add azimuth text at the top ---
        altitude_text = f"Altitude: {altitude:.1f}°"
        
        # Calculate text width and height to center it horizontally
        altitude_text_width, altitude_text_height = draw.textsize(altitude_text, font=font)
        altitude_text_x = (128 - altitude_text_width) / 2  # Center the text horizontally
        altitude_text_y = 0  # Position the text at the top
        
        # Draw the azimuth text
        draw.text((altitude_text_x, altitude_text_y), altitude_text, font=font, fill="white")

        # --- Add azimuth text at the top ---
        target_text = f"Target: {targetAltitude:.1f}°"
        
        # Calculate text width and height to center it horizontally
        target_text_width, target_text_height = draw.textsize(target_text, font=font)
        target_text_x = (128 - target_text_width) / 2  # Center the text horizontally
        target_text_y = altitude_text_height + 2  # Position the text at the top
        
        # Draw the azimuth text
        draw.text((target_text_x, target_text_y), target_text, font=font, fill="white")
        
        # Calculate text width and height to center it
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (128 - text_width) / 2  # Center the text horizontally
        text_y = 128 - text_height       # Position the text at the bottom
        
        # Draw the text
        draw.text((text_x, text_y), text, font=font, fill="white")

def displayAzimuthArrow(azimuth: float, targetazimuth: float):
    with canvas(device) as draw:
        difference = targetazimuth - azimuth
        diff = (targetazimuth - azimuth) % 360
        print(f"difference: {difference}")
        
        # Limit the difference to a range between -180 and 180 degrees
        if difference < -180:
            difference += 360
        elif difference > 180:
            difference -= 360
        
        absDifference = abs(difference) / 2
        
        # Calculate padding to center the arrow horizontally
        padding = int((128 - absDifference) / 2)
        
        # Draw the horizontal line representing the arrow shaft
        draw.line(
            [(padding, 64), (padding + absDifference, 64)],
            fill="white",
            width=3
        )
        
        # Determine the length of the arrowhead
        arrowLength = 10 if absDifference > 10 else absDifference
        
        # Decide the text to display and draw the arrowhead
        if diff <= 180:
            # Arrow pointing right
            draw.line(
                [
                    (padding + absDifference - arrowLength, 64 - arrowLength),
                    (padding + absDifference, 64),
                    (padding + absDifference - arrowLength, 64 + arrowLength)
                ],
                fill="white",
                width=3
            )
            turn_text = "Turn Right"
        else:
            # Arrow pointing left
            draw.line(
                [
                    (padding + arrowLength, 64 - arrowLength),
                    (padding, 64),
                    (padding + arrowLength, 64 + arrowLength)
                ],
                fill="white",
                width=3
            )
            turn_text = "Turn Left"
        
        font = ImageFont.truetype("Roboto-Medium.ttf", 14)  # Load the font

        # --- Add azimuth text at the top ---
        azimuth_text = f"Azimuth: {azimuth:.1f}°"
        
        # Calculate text width and height to center it horizontally
        azimuth_text_width, azimuth_text_height = draw.textsize(azimuth_text, font=font)
        azimuth_text_x = (128 - azimuth_text_width) / 2  # Center the text horizontally
        azimuth_text_y = 0  # Position the text at the top
        
        # Draw the azimuth text
        draw.text((azimuth_text_x, azimuth_text_y), azimuth_text, font=font, fill="white")

        # --- Add azimuth text at the top ---
        target_text = f"Target: {targetazimuth:.1f}°"
        
        # Calculate text width and height to center it horizontally
        target_text_width, target_text_height = draw.textsize(target_text, font=font)
        target_text_x = (128 - target_text_width) / 2  # Center the text horizontally
        target_text_y = azimuth_text_height + 2  # Position the text at the top
        
        # Draw the azimuth text
        draw.text((target_text_x, target_text_y), target_text, font=font, fill="white")
        
        # --- Add turn direction text at the bottom ---
        turn_text_width, turn_text_height = draw.textsize(turn_text, font=font)
        turn_text_x = (128 - turn_text_width) / 2  # Center the text horizontally
        turn_text_y = 128 - turn_text_height       # Position the text at the bottom
        
        # Draw the turn direction text
        draw.text((turn_text_x, turn_text_y), turn_text, font=font, fill="white")


def displayHoldStill():
    """
    Displays a cross on the screen and shows the text 'hold device still for 2 seconds'.

    Parameters:
    - device: The display device to draw on.
    """
    with canvas(device) as draw:
        # --- Add text at the bottom ---
        text = "hold still for 2 seconds"
        font = ImageFont.truetype("Roboto-Medium.ttf", 12)

        # Calculate text width and height to center it
        text_width, text_height = draw.textsize(text, font=font)
        text_x = (128 - text_width) / 2
        text_y = 128 - text_height

        # Draw the text
        draw.text((text_x, text_y), text, font=font, fill="white")

        # --- Draw a cross in the center of the display ---
        center_x = 64  # Horizontal center
        center_y = 64  # Vertical center

        # Calculate the bottom limit of the vertical line to avoid overlapping the text
        vertical_line_bottom = text_y - 5  # Leave a small gap above the text

        # Draw horizontal line
        draw.line((0, center_y, 128, center_y), fill="white", width=2)

        # Draw vertical line, adjusted to avoid overlapping the text
        draw.line((center_x, 0, center_x, vertical_line_bottom), fill="white", width=2)

def drawLogo(center, radius):
    """
    Draws a simple planet onto the given draw context.

    Parameters:
    - draw (ImageDraw.Draw): The drawing context.
    - center (tuple): The (x, y) coordinates of the planet's center.
    - radius (int): The radius of the planet.
    """
    x, y = center
    with canvas(device) as draw:

        draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            outline=0,  # Black outline
            fill=1      # White fill (in '1' mode', 1 is white)
        )

        # Add craters or spots on the planet
        num_spots = 20  # Number of spots to draw
        for _ in range(num_spots):
            spot_radius = random.randint(radius // 20, radius // 10)
            # Ensure the spot is within the planet's boundary
            max_offset = radius - spot_radius
            offset_x = random.randint(-max_offset, max_offset)
            offset_y = random.randint(-max_offset, max_offset)
            spot_center = (x + offset_x, y + offset_y)
            draw.ellipse(
                [
                    (spot_center[0] - spot_radius, spot_center[1] - spot_radius),
                    (spot_center[0] + spot_radius, spot_center[1] + spot_radius)
                ],
                fill=0  # Black spots
            )

        # Optionally, add horizontal lines to simulate planetary bands
        num_bands = 6
        band_spacing = radius // (num_bands + 1)
        for i in range(1, num_bands + 1):
            band_y = y - radius + i * band_spacing
            draw.arc(
                [(x - radius, band_y - radius // 4), (x + radius, band_y + radius // 4)],
                start=0,
                end=180,
                fill=0
            )

        # Write the texts "Star Gazer" and "By Max Craig" below the planet
        text1 = "Star Gazer"
        text2 = "Max Craig"
        font_size1 = 19  # Adjust the font size as needed
        font_size2 = 11  # Adjust the font size as needed


        try:
            # Try to load a TrueType font
            font1 = ImageFont.truetype("Roboto-Medium.ttf", font_size1)
            font2 = ImageFont.truetype("Roboto-Medium.ttf", font_size2)

        except IOError:
            # If not available, use the default font
            font = ImageFont.load_default()
            font_size = font.getsize(text1)[1]  # Update font size for positioning
        # Calculate text sizes
        text1_width, text1_height = draw.textsize(text1, font=font1)
        text2_width, text2_height = draw.textsize(text2, font=font2)

        # Calculate total height of texts and spacing
        total_text_height = text1_height + text2_height + 5  # 5 pixels spacing between texts

        # Initial positions for texts
        text1_x = (draw.im.size[0] - text1_width) / 2
        text1_y = y + radius + 5  # Position text1 just below the planet
        text2_x = (draw.im.size[0] - text2_width) / 2
        text2_y = text1_y + text1_height + 5  # Position text2 below text1

        # Check if texts fit within the image bounds
        if text2_y + text2_height > draw.im.size[1]:
            # Adjust the planet upwards
            shift = (text2_y + text2_height) - draw.im.size[1] + 5  # Extra 5 pixels margin
            y -= shift
            # Clear the drawing and redraw at new position
            draw.rectangle([(0, 0), draw.im.size], fill=1)  # Clear with white background

            # Redraw the planet at the new position
            # Draw the main circle
            draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)],
                outline=0,
                fill=1
            )

            # Redraw spots
            for _ in range(num_spots):
                spot_radius = random.randint(radius // 20, radius // 10)
                max_offset = radius - spot_radius
                offset_x = random.randint(-max_offset, max_offset)
                offset_y = random.randint(-max_offset, max_offset)
                spot_center = (x + offset_x, y + offset_y)
                draw.ellipse(
                    [
                        (spot_center[0] - spot_radius, spot_center[1] - spot_radius),
                        (spot_center[0] + spot_radius, spot_center[1] + spot_radius)
                    ],
                    fill=0
                )

            # Redraw planetary bands
            for i in range(1, num_bands + 1):
                band_y = y - radius + i * band_spacing
                draw.arc(
                    [(x - radius, band_y - radius // 4), (x + radius, band_y + radius // 4)],
                    start=0,
                    end=180,
                    fill=0
                )

            # Recalculate text positions after shifting
            text1_y = y + radius + 5
            text2_y = text1_y + text1_height + 5

        # Draw the texts
        draw.text((text1_x, text1_y), text1, font=font1, fill=1)
        draw.text((text2_x, text2_y), text2, font=font2, fill=1)



def drawPlanet(center, radius,planet: str):
    """
    Draws a simple planet onto the given draw context.

    Parameters:
    - draw (ImageDraw.Draw): The drawing context.
    - center (tuple): The (x, y) coordinates of the planet's center.
    - radius (int): The radius of the planet.
    """
    x, y = center
    with canvas(device) as draw:

        draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            outline=0,  # Black outline
            fill=1      # White fill (in '1' mode', 1 is white)
        )

        # Add craters or spots on the planet
        num_spots = 20  # Number of spots to draw
        for _ in range(num_spots):
            spot_radius = random.randint(radius // 20, radius // 10)
            # Ensure the spot is within the planet's boundary
            max_offset = radius - spot_radius
            offset_x = random.randint(-max_offset, max_offset)
            offset_y = random.randint(-max_offset, max_offset)
            spot_center = (x + offset_x, y + offset_y)
            draw.ellipse(
                [
                    (spot_center[0] - spot_radius, spot_center[1] - spot_radius),
                    (spot_center[0] + spot_radius, spot_center[1] + spot_radius)
                ],
                fill=0  # Black spots
            )

        # Optionally, add horizontal lines to simulate planetary bands
        num_bands = 6
        band_spacing = radius // (num_bands + 1)
        for i in range(1, num_bands + 1):
            band_y = y - radius + i * band_spacing
            draw.arc(
                [(x - radius, band_y - radius // 4), (x + radius, band_y + radius // 4)],
                start=0,
                end=180,
                fill=0
            )

        # Write the texts "Star Gazer" and "By Max Craig" below the planet
        text1 = "now looking at"
        text2 = ""
        if planet == "Moon":
            text2 = "The Moon"
        else:
            text2 = planet
        font_size1 = 16  # Adjust the font size as needed
        font_size2 = 14  # Adjust the font size as needed


        try:
            # Try to load a TrueType font
            font1 = ImageFont.truetype("Roboto-Medium.ttf", font_size1)
            font2 = ImageFont.truetype("Roboto-Medium.ttf", font_size2)

        except IOError:
            # If not available, use the default font
            font = ImageFont.load_default()
            font_size = font.getsize(text1)[1]  # Update font size for positioning
        # Calculate text sizes
        text1_width, text1_height = draw.textsize(text1, font=font1)
        text2_width, text2_height = draw.textsize(text2, font=font2)

        # Calculate total height of texts and spacing
        total_text_height = text1_height + text2_height + 5  # 5 pixels spacing between texts

        # Initial positions for texts
        text1_x = (draw.im.size[0] - text1_width) / 2
        text1_y = y + radius + 5  # Position text1 just below the planet
        text2_x = (draw.im.size[0] - text2_width) / 2
        text2_y = text1_y + text1_height + 5  # Position text2 below text1

        # Check if texts fit within the image bounds
        if text2_y + text2_height > draw.im.size[1]:
            # Adjust the planet upwards
            shift = (text2_y + text2_height) - draw.im.size[1] + 5  # Extra 5 pixels margin
            y -= shift
            # Clear the drawing and redraw at new position
            draw.rectangle([(0, 0), draw.im.size], fill=1)  # Clear with white background

            # Redraw the planet at the new position
            # Draw the main circle
            draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)],
                outline=0,
                fill=1
            )

            # Redraw spots
            for _ in range(num_spots):
                spot_radius = random.randint(radius // 20, radius // 10)
                max_offset = radius - spot_radius
                offset_x = random.randint(-max_offset, max_offset)
                offset_y = random.randint(-max_offset, max_offset)
                spot_center = (x + offset_x, y + offset_y)
                draw.ellipse(
                    [
                        (spot_center[0] - spot_radius, spot_center[1] - spot_radius),
                        (spot_center[0] + spot_radius, spot_center[1] + spot_radius)
                    ],
                    fill=0
                )

            # Redraw planetary bands
            for i in range(1, num_bands + 1):
                band_y = y - radius + i * band_spacing
                draw.arc(
                    [(x - radius, band_y - radius // 4), (x + radius, band_y + radius // 4)],
                    start=0,
                    end=180,
                    fill=0
                )

            # Recalculate text positions after shifting
            text1_y = y + radius + 5
            text2_y = text1_y + text1_height + 5

        # Draw the texts
        draw.text((text1_x, text1_y), text1, font=font1, fill=1)
        draw.text((text2_x, text2_y), text2, font=font2, fill=1)

if __name__ == "__main__":
    # arr = bitmap.read_array_from_file("Mercury.npy")
    # # for i in arr:
    # #     print(i)
    # with canvas(device) as draw:
    #     bitmap.array_to_image(arr, draw)
    # sleep(2)
    # arr = bitmap.read_array_from_file("Venus.npy")
    # # for i in arr:
    # #     print(i)
    # with canvas(device) as draw:
    #     bitmap.array_to_image(arr, draw)
    # sleep(2)
    # arr = bitmap.read_array_from_file("Moon.npy")
    # # for i in arr:
    # #     print(i)
    # with canvas(device) as draw:
    #     bitmap.array_to_image(arr, draw)
    # sleep(2)
    # arr = bitmap.read_array_from_file("Mars.npy")
    # # for i in arr:
    # #     print(i)
    # with canvas(device) as draw:
    #     bitmap.array_to_image(arr, draw)
    # sleep(2)
    # for i in range(5):
    #     drawLogo((64,44),40)
    #     sleep(1)
    # target = 53
    # displayAzimuthArrow(0,90)
    # input()
    # displayAzimuthArrow(0,180)
    # input()
    # displayAzimuthArrow(0,270)
    # input()
    # displayAzimuthArrow(0,360)
    # input()
    # displayAzimuthArrow(0,0)
    # input()
    while True:
        drawLogo((64,44),40)
    displayHoldStill()
    sleep(2)
    current = 180
    target = 0
    for i in range(0,360,5):
        print(i)
        displayAzimuthArrow(current,target + i)
        sleep(0.1)

    current = 0
    target = 0
    for i in range(0,65,5):
        print(i)
        displayAltitudeArrow(60,i)
        sleep(0.1)

    current = 0
    target = 0
    for i in range(60,100,5):
        print(i)
        displayAltitudeArrow(60,i)
        sleep(0.1)
    # displayText(["Star Gazer","By Max Craig"])
    # sleep(4)
    # displayText(["Calibrating Device, please stand by"])
    # sleep(4)
