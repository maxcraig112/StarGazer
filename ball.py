import time
import random
import math
from luma.core.render import canvas
from luma.core.interface.serial import i2c
from luma.oled.device import sh1107
from PIL import ImageDraw
from smbus2 import SMBus

# Initialize the display
bus = SMBus(3)
serial = i2c(bus=bus, address=0x3C)
device = sh1107(serial, rotate=0, height=128, width=128)

class Ball:
    def __init__(self, x, y, vx, vy, radius):
        self.x = x  # X position
        self.y = y  # Y position
        self.vx = vx  # X velocity
        self.vy = vy  # Y velocity
        self.radius = radius  # Radius of the ball

def bouncingBalls():
    # Create 10 balls with varying sizes and initial velocities
    balls = []
    num_balls = 10
    max_attempts = 1000  # Max attempts to place a ball without overlap
    for _ in range(num_balls):
        radius = random.randint(3, 8)  # Random radius between 3 and 8

        # Try to place the ball without overlapping existing balls
        for attempt in range(max_attempts):
            x = random.randint(radius, device.width - radius)
            y = random.randint(radius, device.height - radius)
            vx = random.choice([-2, -1, 1, 2])  # Random initial velocity
            vy = random.choice([-2, -1, 1, 2])

            new_ball = Ball(x, y, vx, vy, radius)

            # Check for overlap with existing balls
            overlap = False
            for ball in balls:
                dx = new_ball.x - ball.x
                dy = new_ball.y - ball.y
                distance = math.hypot(dx, dy)
                min_dist = new_ball.radius + ball.radius
                if distance < min_dist:
                    overlap = True
                    break
            if not overlap:
                balls.append(new_ball)
                break
        else:
            print("Could not place a ball without overlap after maximum attempts.")
            continue

    try:
        while True:
            # Pre-check for collisions and adjust velocities accordingly
            # Check for collisions between balls
            for i in range(num_balls):
                for j in range(i + 1, num_balls):
                    ball1 = balls[i]
                    ball2 = balls[j]
                    dx = ball1.x - ball2.x
                    dy = ball1.y - ball2.y
                    distance = math.hypot(dx, dy)
                    min_dist = ball1.radius + ball2.radius
                    if distance < min_dist:
                        # Simple elastic collision response
                        # Swap velocities
                        ball1.vx, ball2.vx = ball2.vx, ball1.vx
                        ball1.vy, ball2.vy = ball2.vy, ball1.vy

            # Update positions and check for wall collisions
            for ball in balls:
                # Update position
                ball.x += ball.vx
                ball.y += ball.vy

                # Wall collision detection and response
                if ball.x - ball.radius <= 0:
                    ball.x = ball.radius
                    ball.vx = -ball.vx
                if ball.x + ball.radius >= device.width:
                    ball.x = device.width - ball.radius
                    ball.vx = -ball.vx
                if ball.y - ball.radius <= 0:
                    ball.y = ball.radius
                    ball.vy = -ball.vy
                if ball.y + ball.radius >= device.height:
                    ball.y = device.height - ball.radius
                    ball.vy = -ball.vy

            # Draw balls
            with canvas(device) as draw:
                for ball in balls:
                    draw.ellipse(
                        (ball.x - ball.radius, ball.y - ball.radius,
                         ball.x + ball.radius, ball.y + ball.radius),
                        outline="white",
                        fill="white"
                    )

            # Control frame rate
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass  # Allow the loop to be stopped with Ctrl+C

# Call the function to start the simulation
bouncingBalls()
