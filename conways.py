from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.oled.device import sh1107
import numpy as np
from PIL import Image
import time

# Initialize the display
bus = SMBus(3)
serial = i2c(bus=bus, address=0x3C)
device = sh1107(serial, rotate=0, height=128, width=128)

# Set up the grid with a smaller size
grid_size = 32
grid = np.zeros((grid_size, grid_size), dtype=np.uint8)

# Define the glider pattern
glider = np.array([[0, 1, 0],
                   [0, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)

# Calculate the position to place the glider (center of the grid)
center = grid_size // 2
start_row = center - 1
start_col = center - 1

# Place the glider pattern onto the grid
grid[start_row:start_row+3, start_col:start_col+3] = glider

def life_step(grid):
    # Calculate the number of neighbors for each cell with wrap-around
    neighbors = sum(
        np.roll(np.roll(grid, shift=i, axis=0), shift=j, axis=1)
        for i in (-1, 0, 1) for j in (-1, 0, 1)
        if not (i == 0 and j == 0)
    )
    # Apply Conway's Game of Life rules
    return ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(np.uint8)

try:
    while True:
        # Update the grid
        grid = life_step(grid)

        # Convert the grid to an image and upscale it
        img = Image.fromarray(grid * 255).convert('1')
        img = img.resize((128, 128), Image.NEAREST)

        # Display the image
        device.display(img)

        # Wait for a short interval
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
