import configurations as con
import random
import classes
from printers import print_station_coverage
import helpers


PRINT_IMAGES = True



# create a csv file of stations
# each line is a station with the following format:
# id, x, y, trains
def main():
    coordinates = set()
    with open(con.STATION_GEN_FILE_NAME, 'w') as f:
        f.write('id,x,y,trains, layout\n')
        stations = []
        for i in range(con.STATIONS_AMT):
            x = random.randint(con.STATION_COVERAGE_RADIUS, con.GRID_WIDTH-con.STATION_COVERAGE_RADIUS)
            y = random.randint(con.STATION_COVERAGE_RADIUS, con.GRID_HEIGHT-con.STATION_COVERAGE_RADIUS)
            trains = None
            random_size = random.random()
            if random_size < 0.15:
                layout = "horizontal"
            elif random_size < 0.3:
                layout = "vertical"
            elif random_size < 0.4:
                layout = "square"
            else:
                layout = "basic"
            
            # check if overlapping
            if not check_overlapping(x, y, layout, coordinates):
                i -= 1
                continue
            
            coordinates.add((x, y))
            stations.append(Station(x, y))
        
        stations = refine_stations(stations)

        for i, station in enumerate(stations):   
            f.write(f'{i},{station.x},{station.y},{trains},{layout}\n')
        
        print("CSV file created")


class Point:
    def __init__(self, x, y, covered) -> None:
        self.x = x
        self.y = y
        self.covered = covered

class Map:
    def __init__(self, columns, rows) -> None:
        self.points = []
        for x in columns:
            for y in rows:
                self.points.append(  Point(x, y, False)  )

    def clear_coverage(self):
        for point in self.points:
            point.covered = False

class Station:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.coverage = 0
        self.coverage_points = []

    def __str__(self) -> str:
        return f'Station at {self.x}, {self.y} with coverage {self.coverage}'
    


def refine_stations(stations):
    # for each station, move it one unit if that place has a better coverage
    # coverage here is as the numbe of points that are covered by the station
        # a point is covered if its within 2 units of the station
    map = Map(range(con.GRID_WIDTH), range(con.GRID_HEIGHT))
    
    for station in stations:
        station.coverage = check_station_coverage(station, map, mode="initial")

    print_station_coverage([(station.x, station.y) for station in stations], map, filename="station_coverage_initial")

    print("Station Refinement")

    for i in range(con.STATIONS_GEN_REFINE_MAX):
        # for each station, move it one unit if that place has a better coverage
        improved = False
        print("Station Refinement, Iteration", i, "of", con.STATIONS_GEN_REFINE_MAX, "iterations")
        
        for station in stations:
            x, y = station.x, station.y
            max_coverage = station.coverage
            max_x, max_y = x, y
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    new_x, new_y = x + dx, y + dy
                    if new_x < 0 or new_x >= con.GRID_WIDTH or new_y < 0 or new_y >= con.GRID_HEIGHT:
                        continue
                    station_ = Station(new_x, new_y)
                    
                    clear_station_coverage(station, stations, map)

                    coverage = check_station_coverage(station_, map, mode="test")
                    if coverage > max_coverage:
                        max_coverage = coverage
                        max_x, max_y = new_x, new_y
                        print("New best coverage", max_coverage,"at point ",  max_x, max_y, "for station", station.x, station.y)
                        improved = True
            
            station.x, station.y = max_x, max_y
            station.coverage = check_station_coverage(station, map, mode="final") # max_coverage?
        
        for station in stations:
            check_station_coverage(station, map, mode="final")


        if PRINT_IMAGES:
            if improved:
                filename = f"station_coverage_refined_{i}"
                station_coordinates = [(station.x, station.y) for station in stations]
            
                print_station_coverage(station_coordinates, map, filename=f"{filename}")
        if not improved:
            print("No improvement found, breaking")
            break
    
    return stations

def check_station_coverage(station, map, mode="initial"):
    """Check the coverage of a station in the map, if the mode is initial or final, 
    the points will also be marked as covered and added to the stations coverage_points list.
    If the mode is test, the points will not be marked as covered."""
    x, y = station.x, station.y
    coverage = 0
    for point in map.points:
        if not point.covered:
            if (point.x - x)**2 + (point.y - y)**2 <= con.STATION_COVERAGE_RADIUS**2:
                if mode == "initial" or mode == "final":
                    point.covered = True
                    station.coverage_points.append(point)
                coverage += 1
    return coverage

def clear_station_coverage(station, stations, map):
    

    for point in map.points:
        # remove every point from the station's coverage
        if point in station.coverage_points:
            station.coverage_points.remove(point)
            point.covered = False

            # if the point is covered by another station, skip it
            for station_i in stations:
                if point in station_i.coverage_points and station_i != station:
                    print("clear_station found another station covering the point", point.x, point.y, "Station", station_i.x, station_i.y)
                    point.covered = True
                    break
            if point.covered:
                continue

    station.coverage = 0

    # print("Station Covaerage Cleared", station.x, station.y, "Coverage", station.coverage, "Points", len(station.coverage_points))

def check_overlapping(x, y, layout, coordinates):

    if (x,y) in coordinates:
        return False
        
    elif layout == "horizontal":
        if (x+1, y) in coordinates in coordinates:
            return False
    elif layout == "vertical":
        if (x, y+1) in coordinates in coordinates:
            return False
    elif layout == "square":
        if (x+1, y+1) in coordinates:
            return False
    return True


def create_stations():
    stations = []
    for i in range(STATIONS_AMT):
        x = random.randint(0, con.GRID_WIDTH)
        y = random.randint(0, con.GRID_HEIGHT)
        station = classes.Station(id=i, pos=(x, y), trains=[])
        print(station)

if __name__ == "__main__":

    if PRINT_IMAGES:
        helpers.delete_images()
        
        
    main()