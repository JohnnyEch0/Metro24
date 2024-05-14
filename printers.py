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

def draw_connections(draw, connections):
    for connection in connections:
        station1 = connection.station1
        station2 = connection.station2
        center1 = (station1.x * con.IMAGE_SCALE + con.IMAGE_SCALE // 2, station1.y * con.IMAGE_SCALE + con.IMAGE_SCALE // 2)
        center2 = (station2.x * con.IMAGE_SCALE + con.IMAGE_SCALE // 2, station2.y * con.IMAGE_SCALE + con.IMAGE_SCALE // 2)
        draw.line((center1, center2), fill="white", width=2)

def print_stations_routes(stations, routes, type="routes", exluded = []):
    image_width = con.GRID_WIDTH * con.IMAGE_SCALE
    image_height = con.GRID_HEIGHT * con.IMAGE_SCALE
    image = Image.new("RGB", (image_width, image_height), "black")
    draw = ImageDraw.Draw(image)

    station_color = (100, 100, 200)

    for station in stations:
        x = station.x * con.IMAGE_SCALE
        y = station.y * con.IMAGE_SCALE
        block_coords = (x, y, x + con.IMAGE_SCALE, y + con.IMAGE_SCALE)
        draw.rectangle(block_coords, fill=station_color)

        text_color = (255, 255, 255)
        text_coords = (x + con.IMAGE_SCALE // 2, y + con.IMAGE_SCALE // 2)
        draw.text(text_coords, str(station.id), fill=text_color, anchor="mm")

    if type == "connections":
        draw_connections(draw, routes)
        
    elif type == "exluded":
        for connection in exluded:
            station1 = connection.station1
            station2 = connection.station2
            center1 = (station1.x * con.IMAGE_SCALE + con.IMAGE_SCALE // 2, station1.y * con.IMAGE_SCALE + con.IMAGE_SCALE // 2)
            center2 = (station2.x * con.IMAGE_SCALE + con.IMAGE_SCALE // 2, station2.y * con.IMAGE_SCALE + con.IMAGE_SCALE // 2)
            draw.line((center1, center2), fill="red", width=1)
        draw_connections(draw, routes)
    
    else:
        for route in routes:
            for i in range(len(route) - 1):
                station1 = route[i]
                station2 = route[i + 1]
                center1 = (station1.x * con.IMAGE_SCALE + con.IMAGE_SCALE // 2, station1.y * con.IMAGE_SCALE + con.IMAGE_SCALE // 2)
                center2 = (station2.x * con.IMAGE_SCALE + con.IMAGE_SCALE // 2, station2.y * con.IMAGE_SCALE + con.IMAGE_SCALE // 2)
                draw.line((center1, center2), fill="blue", width=2)

    image.save("images/stations_routes.png")