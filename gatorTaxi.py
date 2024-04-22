import sys

import rbt
import heap


class GatorTaxi:
    # Initialize the Min Heap and Red Black Tree
    def __init__(self):
        self.min_heap = heap.MinHeapRide()
        self.red_black_tree = rbt.RBTree()

    # Check and Insert Ride in RB Tree. Later Insert In Heap.
    def insert_ride(self, ride_number: int, ride_cost: int, trip_duration: int):
        rbt_node = self.red_black_tree.insert_ride(ride_number, ride_cost, trip_duration)
        if rbt_node is not None:
            self.min_heap.insert_ride(ride_number, ride_cost, trip_duration, rbt_node)
            return True
        else:
            return False

    # Searches in RB Tree and returns ride if present or returns (0,0,0)
    def print_ride(self, ride_number: int):
        ride = self.red_black_tree.search_ride(ride_number)
        if ride is None:
            output = "(0,0,0)"
        else:
            output = ride.__repr__()
        # print(output)
        return output

    # gets ride with min cost and trip duration from head and deletes from RB tree
    def get_next_ride(self):
        ride = self.min_heap.remove_min()
        if ride is None:
            output = "No active ride requests"
        else:
            self.red_black_tree.delete_ride(ride.ride_number)
            output = ride.__repr__()
        # print(output)
        return output

    # Search in RB Tree and delete from both Data Structures
    def cancel_ride(self, ride_number: int):
        heap_ref = self.red_black_tree.delete_ride(ride_number)
        if heap_ref is not None:
            self.min_heap.delete_ride(heap_ref.index_number)

    # Search in RB Tree and delete from both Data Structures based on the given conditions
    def update_ride(self, ride_number: int, new_trip_duration: int):
        ride = self.red_black_tree.search_ride(ride_number)
        if ride is not None:
            existing_trip_duration = ride.trip_duration
            # Case 1
            if existing_trip_duration == new_trip_duration:
                return
            # Case 1
            if new_trip_duration < existing_trip_duration:
                ride.trip_duration = new_trip_duration
                self.min_heap.update_ride(ride.heap_node.index_number, new_trip_duration, False)
            # Case 2
            elif existing_trip_duration < new_trip_duration <= 2 * existing_trip_duration:
                ride.trip_duration = new_trip_duration
                ride.ride_cost += 10
                self.min_heap.update_ride(ride.heap_node.index_number, new_trip_duration, True)
            # Case 3
            else:
                self.cancel_ride(ride_number)

    # Prints from RBtree for given range
    def print_range(self, l_ride_number: int, b_ride_number: int):
        return self.red_black_tree.print_range(l_ride_number, b_ride_number)


if __name__ == "__main__":
    gator_taxi = GatorTaxi()  # Create GatorTaxi Object
    file_name = sys.argv[1]  # Takes first argument
    with open(file_name, "r") as f:
        with open("output_file.txt", "w") as f1:
            lines = f.readlines()
            arg_list = []
            # Read file line by line and execute appropriate functions
            for line in lines:
                func_name, args = line.split("(", 1)
                args = args.replace("\n", "")
                arg_list = args.replace(")", "").split(",")
                if func_name == "Insert":
                    is_inserted = gator_taxi.insert_ride(int(arg_list[0]), int(arg_list[1]), int(arg_list[2]))
                    if not is_inserted:
                        f1.write("Duplicate RideNumber")
                        break
                elif func_name == "Print":
                    if len(arg_list) == 1:
                        f1.write(gator_taxi.print_ride(int(arg_list[0])))
                        f1.write("\n")
                    elif len(arg_list) == 2:
                        f1.write(gator_taxi.print_range(int(arg_list[0]), int(arg_list[1])))
                        f1.write("\n")
                elif func_name == "GetNextRide":
                    f1.write(gator_taxi.get_next_ride())
                    f1.write("\n")
                elif func_name == "CancelRide":
                    gator_taxi.cancel_ride(int(arg_list[0]))
                elif func_name == "UpdateTrip":
                    gator_taxi.update_ride(int(arg_list[0]), int(arg_list[1]))
                else:
                    print("Unidentified Function Name")
