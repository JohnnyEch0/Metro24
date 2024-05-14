import configurations as con
import random



# create a csv file of trains
# each line is a train with the following format:
# id, route, where route is a sequence of station_ids
# each station needs to have at least one and at most MAX_TRAINS_P_STATION trains
# each train needs to have at least MIN_STATIONS_P_TRAIN and at most MAX_STATIONS_P_TRAIN stations
# 
class Station_for_train:
    def __init__(self, id, x, y) -> None:
        self.id = id
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'Station {self.id} at {self.x}, {self.y} with layout {self.layout}'

def main():
    with open(con.STATIONS_FILE, 'r') as f:
        stations = []
        lines = f.readlines()[1:]
        
        for station in lines:
            station_id, x, y, trains, layout = station.split(',')
            stations.append(Station_for_train(station_id, x, y))
        
    with open(con.TRAINS_FILE, 'w') as f:
        f.write('id,route\n')
        for i in range(con.TRAINS_AMT):
            route = []
            stations_p_train = random.randint(con.MIN_STATIONS_P_TRAIN, con.MAX_STATIONS_P_TRAIN)
            for j in range(stations_p_train):
                station = random.choice(stations)
                route.append(station.id)
            f.write(f'{i},{route}\n')
            


if __name__ == "__main__":
    main()