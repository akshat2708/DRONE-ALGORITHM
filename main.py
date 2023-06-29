import heapq

# Define the size of the 2-D grid
M = 10
N = 10

# Define a class to represent each drone
class Drone:
    def _init_(self, id, start, end, start_time):
        self.id = id
        self.start = start
        self.end = end
        self.start_time = start_time
        self.path = []
        self.current_pos = start

# Define a function to calculate the Manhattan distance between two points
def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Define a function to find the optimal path from start to end using A*
def find_path(start, end):
    # Create a dictionary to keep track of the cost of each cell
    cost_so_far = {}
    cost_so_far[start] = 0

    # Create a priority queue to keep track of cells to visit
    queue = [(0, start)]

    # Create a dictionary to keep track of the parent of each cell in the path
    came_from = {}

    while queue:
        # Get the cell with the lowest cost
        _, current = heapq.heappop(queue)

        # Check if we have reached the end
        if current == end:
            break

        # Explore the neighbors of the current cell
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)

            # Check if the neighbor is within the grid
            if next_pos[0] < 0 or next_pos[0] >= M or next_pos[1] < 0 or next_pos[1] >= N:
                continue

            # Calculate the cost to move to the neighbor
            new_cost = cost_so_far[current] + 1

            # Check if we have not visited the neighbor yet or if the cost to move to the neighbor is lower than the previous cost
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + manhattan_dist(end, next_pos)
                heapq.heappush(queue, (priority, next_pos))
                came_from[next_pos] = current

    # Reconstruct the path from start to end
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path

# Define a function to assign time slots to each drone
def assign_time_slots(drones):
    # Sort the drones by start time
    drones = sorted(drones, key=lambda x: x.start_time)

    # Assign time slots to each drone
    time_slots = {}
    for drone in drones:
        # Find the earliest time slot that is available for the drone to start flying
        earliest_slot = 0
        while True:
            available = True
            for d, slot in time_slots.items():
                if d != drone.id and slot == earliest_slot:
                    available = False
                    break
            if available:
                time_slots[drone.id] = earliest_slot
                break
            earliest_slot += 1

    return time_slots

# Define the main function to guide the drones
def guide_drones(drones):
    # Assign time slots to each drone
    time_slots = assign_time_slots(d)