import csv
from PIL import Image, ImageDraw

# Load the stations_gen.csv file
with open('stations_gen.csv', 'r') as file:
    reader = csv.reader(file)
    stations = list(reader)

# Create a new image with a background
background_color = (0, 0, 0)  # White
image_width = 480
image_height = 300
image = Image.new('RGB', (image_width, image_height), background_color)
draw = ImageDraw.Draw(image)

# Calculate the size of each station block
num_stations = len(stations)
block_width = 10
block_height = 10

# Place the stations on the image
for i, station in enumerate(stations[1:]):
    station_name = station[0]
    station_x = int(station[1])  * block_width
    station_y = int(station[2])  * block_height

    # Draw a blue block at the station position
    block_color = (100, 100, 200)  # Blue
    block_coords = (station_x, station_y, station_x + block_width, station_y + block_height)
    draw.rectangle(block_coords, fill=block_color)

    # Add the station name as text
    text_color = (255, 255, 255)  # Black
    text_coords = (station_x + block_width // 2, station_y + block_height // 2)
    draw.text(text_coords, station_name, fill=text_color, anchor='mm')

# Save the image
image.save('stations_image.png')