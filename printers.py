from PIL import Image, ImageDraw
import configurations as con


def print_station_coverage(station_coordinates, map, filename):
    image_width = con.GRID_WIDTH
    image_height = con.GRID_HEIGHT
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    for point in map.points:
        x = point.x
        y = point.y
        if point.covered:
            draw.point((x, y), fill="green")
        else:
            draw.point((x, y), fill="red")

    for station in station_coordinates:
        x, y = station
        draw.point((x, y), fill="blue")

    image.save(f"images/{filename}.png")