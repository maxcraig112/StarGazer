from PIL import Image
import numpy as np

def image_to_bw_array(image_path):
    """
    Converts an image to a 128x128 black and white array of 0's and 1's.

    Parameters:
    - image_path (str): The file path to the image.

    Returns:
    - np.ndarray: A 128x128 numpy array of 0's and 1's.
    """
    # Open the image
    img = Image.open(image_path)
    # Convert to grayscale
    img = img.convert('L')
    # Resize to 128x128 pixels
    img = img.resize((128, 128), Image.ANTIALIAS)
    # Convert to black and white using a threshold (128 for mid-point)
    threshold = 128
    img = img.point(lambda x: 0 if x < threshold else 255, '1')
    # Convert image data to a numpy array
    arr = np.array(img).astype(np.uint8)
    # In '1' mode, pixels are 0 or 255, normalize to 0 or 1
    # arr = arr // 255
    img.save("test.png")
    return arr

def array_to_image(arr, draw):
    """
    Draws a 128x128 array of 0's and 1's onto the provided draw object.

    Parameters:
    - arr (np.ndarray): A 128x128 numpy array of 0's and 1's.
    - draw (PIL.ImageDraw.Draw): The drawing context from the device canvas.
    """
    # Ensure the array is of type uint8
    arr = arr.astype(np.uint8)
    # Convert 0's and 1's to 0 and 255
    arr = arr * 255
    # Create an image from the array in '1' mode (black and white)
    img = Image.fromarray(arr, mode='L').convert('1')
    # Use draw.bitmap to draw the image onto the draw context
    draw.bitmap((0, 0), img, fill=0)


def save_array_to_file(array, filename):
    """
    Saves a 128x128 list or numpy array to a file using NumPy's save functionality.
    
    Parameters:
    - array (list or np.ndarray): The 128x128 list/array to save.
    - filename (str): The name of the file to save the array in (e.g., 'array.npy').
    """
    # Convert list to numpy array if necessary
    array = np.array(array)
    # Save the array to a file
    np.save(filename, array)

def read_array_from_file(filename):
    """
    Reads a 128x128 array from a file saved with NumPy's save functionality.
    
    Parameters:
    - filename (str): The name of the file to read the array from (e.g., 'array.npy').
    
    Returns:
    - np.ndarray: The loaded 128x128 numpy array.
    """
    # Load the array from the file
    array = np.load(filename)
    return array


if __name__ == "__main__":
    mercury = image_to_bw_array("mercury.jpg")
    venus = image_to_bw_array("venus.jpg")
    moon = image_to_bw_array("moon.jpg")
    for i in mercury:
        print(i)
    mars = image_to_bw_array("mars.png")

    save_array_to_file(mercury,"Mercury")
    save_array_to_file(venus,"Venus")
    save_array_to_file(moon,"Moon")
    save_array_to_file(mars,"Mars")
