import time
import sys


class RoutePlotter:
    #on run script asks for filename ✅
    #when provided with valid filename and valid route, outputs grid and coords ✅
    #when given invalid filename prompt is given in loop ✅
    #STOP stops the programme without error ✅
    #invalid route gives error message and reprints input prompt ✅

    def __init__(self):
        #set variables for valid grid size
        self.max_x = 12
        self.max_y = 12
        self.min_x = 1
        self.min_y = 1
        #grab filename from user input
        self.res = self.inputter()
        res = self.res 
        #read the data, setting the return value as 'coordinate_data' variable
        coordinate_data = self.read_data(res)
        #ensure the route is valid
        if self.validate_route(coordinate_data):
            #create a grid with the route plotted
            grid = self.plot_route(coordinate_data)
            #print the route and coordinate data 
            printer = self.printer(grid, coordinate_data)
        else:
            pass

    def inputter(self):
        """Method to get filename from user.
        Loops until either 'STOP' is entered, or until a valid routefile is entered."""
        while True:
            res = input("Enter file name for route, e.g. 'Route001.txt \nType 'STOP' to quit.\n: ")
            if res == "STOP":
                sys.exit(0)
            try:
                with open(res):
                    return res
            except FileNotFoundError:
                self.print_formatter(f"File '{res}' not found", delay=0.05, extra_delay=1)

    def read_data(self, file):
        """method to open the user inputted file and output a list of tuples with
        all the coordinates of the route"""
        with open(file) as f:
            coord = []
            all_coords = []
            counter = 0
            for line in f:
                #Find starting coordinates, add tuple to list as first item
                if counter < 2:
                    coord.append(int(line.strip('\ufeff')))
                    counter += 1
                if counter == 2:
                    coord.append("*")
                    all_coords.append(tuple(coord))
                    counter +=1
                    current_coord = coord.copy()
                #Add all following coordinates (those that are after start point)
                #compass direction serves as conditional to increment x/y coordinates
                if counter > 1:
                    current_coord = current_coord[:2].copy()
                    if line.strip() == 'S':
                        current_coord[1] -= 1
                        current_coord.append(line.strip())
                        all_coords.append(tuple(current_coord))
                    if line.strip() == 'W':
                        current_coord[0] -= 1
                        current_coord.append(line.strip())
                        all_coords.append(tuple(current_coord))
                    if line.strip() == 'E':
                        current_coord[0] += 1
                        current_coord.append(line.strip())
                        all_coords.append(tuple(current_coord))
                    if line.strip() == 'N':
                        current_coord[1] += 1
                        current_coord.append(line.strip())
                        all_coords.append(tuple(current_coord))
                        counter +=1
        #Return a list of tuples. Each tuple is in format: (x, y, Direction), e.g. (10,9,'S').
        return all_coords

    def validate_route(self, coordinate_data):
        """method to ensure that the route is valid.
        The route is valid if it follows a course within the specified grid squares"""
        for x in coordinate_data:
            if x[0]>self.max_x or x[0]<self.min_x:
                self.print_formatter(f"Error: The route is outside of the grid", delay=0.05)
                return False
            if x[1]>self.max_y or x[1]<self.min_y:
                self.print_formatter(f"Error: The route is outside of the grid", delay=0.05)
                return False
        return True

    def plot_route(self, data):
        """Method to output a grid with coordinates of route specified.
        data argument should be a list of tuples (x, y, direction)"""
        grid = []
        for x_coordinate in range(self.max_x+1):
            row = []
            if len(str(12-x_coordinate)) == 1:
                row.append(f"|00{str(12-x_coordinate)}|")
            else:
                row.append(f"|0{str(12-x_coordinate)}|")
            for x_coordinate in range(self.max_y+1):
                    row.append('~~~|')
            
            row.pop()
            grid.append(row)
        
        grid[12] = ['|---|']
        for y_coordinate in range(self.max_x):
            if y_coordinate < (self.max_y-3):
                grid[12].append(f"00{y_coordinate+1}|")
            else:
                grid[12].append(f"0{y_coordinate+1}|")
    
        # Plot the data points on the grid
    
        for x, y, z in data:
            if z == 'N':
                grid[12 - y][x] = ' ^ |'
            elif z == 'S':
                grid[12 - y][x] = ' v |'
            elif z == 'W':
                grid[12 - y][x] = ' < |'
            elif z == 'E':
                grid[12 - y][x] = ' > |'
            else:
                grid[12 - y][x] = ' * |'
        
        return grid
     
    def printer(self, grid, coordinate_data):
        """method to print the output of a valid route"""
        print("\nGrid Layout: \n")
        for row in grid:
            self.print_formatter(''.join(row), delay=0.001)
        self.print_formatter("\nCoordinates: \n", delay=0.01)
        for coordinate in coordinate_data:
            self.print_formatter(f"({coordinate[0]}, {coordinate[1]}, {coordinate[2]})", delay=0.005)

    def print_formatter(self, message, delay, extra_delay=None):
        """Method to delay printed output in order to enhance readability for user"""
        for char in message:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        if extra_delay:
            time.sleep(extra_delay)

if __name__ == "__main__":
    while True:
        r = RoutePlotter()
 