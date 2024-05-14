import configurations as con
import random
import printers



# create a csv file of trains
# each line is a train with the following format:
# id, route, where route is a sequence of station_ids
# each station needs to have at least one and at most MAX_TRAINS_P_STATION trains
# each train needs to have at least MIN_STATIONS_P_TRAIN and at most MAX_STATIONS_P_TRAIN stations
# a good route is one that has many intersections with other routes
class Station_for_train:
    def __init__(self, id, x, y) -> None:
        self.id = id
        self.x = int(x)
        self.y = int(y)

    def __str__(self) -> str:
        return self.__repr__()
        
    
    def __repr__(self) -> str:
        return f'Station {self.id} at {self.x}, {self.y}'
    
class Connection:
    def __init__(self, station1, station2) -> None:
        self.station1 = station1
        self.station2 = station2
        self.distance = ((station1.x - station2.x)**2 + (station1.y - station2.y)**2)**0.5

    def __str__(self) -> str:
        return f'Connection between {self.station1} and {self.station2}'
    
    def __repr__(self) -> str:
        return self.__str__()
    

def station_preparation():
    print("Preparing stations")
    with open(con.STATIONS_FILE, 'r') as f:
        stations = []
        lines = f.readlines()[1:]
        
        for station in lines:
            station_id, x, y, trains, layout = station.split(',')
            stations.append(Station_for_train(station_id, x, y))
        
    print("Stations prepared")
    
    return stations

def possible_routes_prep(stations):
    print("Preparing possible routes")
    possible_routes = []
    for station in stations:
        for station2 in stations:
            if station == station2:
                continue
            possible_routes.append(Connection(station, station2))
    print("Possible routes prepared", possible_routes)
    return possible_routes

def create_random_routes(stations, possible_routes):
    print("Creating random routes")
    routes = []
    for i in range(con.TRAINS_AMT):
        route = []
        route_length = random.randint(con.MIN_STATIONS_P_TRAIN, con.MAX_STATIONS_P_TRAIN)
        current_station = random.choice(stations)
        route.append(current_station)
        for i in range(route_length):
            current_station = random.choice([connection.station1 for connection in possible_routes if connection.station2 == current_station] + [connection.station2 for connection in possible_routes if connection.station1 == current_station])
            route.append(current_station)
        routes.append(route)
    print("Random routes created", routes)
    return routes
    
def exlude_connections_prep(stations, possible_routes):
    # exlude connections that have to acute angles

    # exlude connections that cover to much distance
    print("Preparing connections to exclude")
    exclude_connections = []
    for connection in possible_routes:
        # print(connection, connection.distance, con.CON_DISTANCE_MAX_PERCENT*con.GRID_WIDTH / 100)
        if connection.distance < con.CON_DISTANCE_MAX_PERCENT*con.GRID_WIDTH / 100:
            print("Excluding", connection, "distance", connection.distance, "max distance", con.CON_DISTANCE_MAX_PERCENT*con.GRID_WIDTH / 100)
            exclude_connections.append(connection)
    
    print("Connections to exclude prepared", exclude_connections)
    return exclude_connections
def main():
    stations = station_preparation()
    possible_routes = possible_routes_prep(stations)
    refined_connections = exlude_connections_prep(stations, possible_routes)
    # routes = create_random_routes(stations, possible_routes)
    # printers.print_stations_routes(stations, routes)
    # printers.print_stations_routes(stations, refined_connections, "connections")
    
    printers.print_stations_routes(stations, refined_connections, "exluded", possible_routes)

    
            


if __name__ == "__main__":
    main()