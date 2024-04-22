class HeapNode_RideInfo:

    def __init__(self, ride_number: int, ride_cost: int, trip_duration: int, rbt_node=None):
        self.ride_number = ride_number
        self.ride_cost = ride_cost
        self.trip_duration = trip_duration
        self.index_number = 0

    def __repr__(self):
        # return f"Memory Address: {hex(id(self))} \n Ride Number: {self.ride_number}    Ride Cost :{self.ride_cost}" \
        #        f"    Trip Duration :{self.trip_duration}    Index :{self.index_number}"
        return f"({self.ride_number},{self.ride_cost},{self.trip_duration})"


class MinHeapRide:

    def __init__(self):
        self.ride_heap = []

    # Compares node to it's parent and swap if needed
    def __heapify_top(self, index=-1):
        if len(self.ride_heap) <= 1:
            return
        if index == -1:
            new_ride_index = len(self.ride_heap) - 1
        else:
            new_ride_index = index
        parent_index = (new_ride_index - 1) // 2
        while parent_index >= 0:
            if self.ride_heap[parent_index].ride_cost > self.ride_heap[new_ride_index].ride_cost:
                self.ride_heap[parent_index].index_number = new_ride_index
                self.ride_heap[new_ride_index].index_number = parent_index
                self.ride_heap[parent_index], self.ride_heap[new_ride_index] = self.ride_heap[new_ride_index] \
                    , self.ride_heap[parent_index]
                new_ride_index = parent_index
                parent_index = new_ride_index // 2
            elif self.ride_heap[parent_index].ride_cost == self.ride_heap[new_ride_index].ride_cost:
                if self.ride_heap[parent_index].trip_duration > self.ride_heap[new_ride_index].trip_duration:
                    self.ride_heap[parent_index].index_number = new_ride_index
                    self.ride_heap[new_ride_index].index_number = parent_index
                    self.ride_heap[parent_index], self.ride_heap[new_ride_index] = self.ride_heap[new_ride_index] \
                        , self.ride_heap[parent_index]
                    new_ride_index = parent_index
                    parent_index = new_ride_index // 2
                else:
                    break
            else:
                break

    # Compares node to its child nodes and swap if needed with lower cost or low trip duration
    def __heapify_bottom(self, index=0):
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        while left_child < len(self.ride_heap):
            if right_child < len(self.ride_heap):
                # Right child is smaller than left child
                if self.ride_heap[left_child].ride_cost > self.ride_heap[right_child].ride_cost:
                    if self.ride_heap[index].ride_cost > self.ride_heap[right_child].ride_cost:
                        self.ride_heap[index].index_number = right_child
                        self.ride_heap[right_child].index_number = index
                        self.ride_heap[index], self.ride_heap[right_child] = self.ride_heap[right_child], \
                            self.ride_heap[index]
                        index = right_child
                        left_child = 2 * index + 1
                        right_child = 2 * index + 2

                    elif self.ride_heap[index].ride_cost == self.ride_heap[right_child].ride_cost:
                        if self.ride_heap[index].trip_duration > self.ride_heap[right_child].trip_duration:
                            self.ride_heap[index].index_number = right_child
                            self.ride_heap[right_child].index_number = index
                            self.ride_heap[index], self.ride_heap[right_child] = self.ride_heap[right_child], \
                                self.ride_heap[index]
                            index = right_child
                            left_child = 2 * index + 1
                            right_child = 2 * index + 2
                        else:
                            break
                    else:
                        break
                # Right child equal to Left Child
                elif self.ride_heap[left_child].ride_cost == self.ride_heap[right_child].ride_cost:
                    if self.ride_heap[index].ride_cost > self.ride_heap[left_child].ride_cost:
                        if self.ride_heap[left_child].trip_duration > self.ride_heap[right_child].trip_duration:
                            self.ride_heap[index].index_number = right_child
                            self.ride_heap[right_child].index_number = index
                            self.ride_heap[index], self.ride_heap[right_child] = self.ride_heap[right_child], \
                                self.ride_heap[index]
                            index = right_child
                            left_child = 2 * index + 1
                            right_child = 2 * index + 2
                        else:
                            self.ride_heap[index].index_number = left_child
                            self.ride_heap[left_child].index_number = index
                            self.ride_heap[index], self.ride_heap[left_child] = self.ride_heap[left_child], \
                                self.ride_heap[index]
                            index = left_child
                            left_child = 2 * index + 1
                            right_child = 2 * index + 2
                    elif self.ride_heap[left_child].ride_cost == self.ride_heap[index].ride_cost:
                        if self.ride_heap[left_child].trip_duration > self.ride_heap[right_child].trip_duration:
                            if self.ride_heap[index].trip_duration > self.ride_heap[right_child].trip_duration:
                                self.ride_heap[index].index_number = right_child
                                self.ride_heap[right_child].index_number = index
                                self.ride_heap[index], self.ride_heap[right_child] = self.ride_heap[right_child], \
                                    self.ride_heap[index]
                                index = right_child
                                left_child = 2 * index + 1
                                right_child = 2 * index + 2
                            else:
                                break
                        else:
                            if self.ride_heap[index].trip_duration > self.ride_heap[left_child].trip_duration:
                                self.ride_heap[index].index_number = left_child
                                self.ride_heap[left_child].index_number = index
                                self.ride_heap[index], self.ride_heap[left_child] = self.ride_heap[left_child], \
                                    self.ride_heap[index]
                                index = left_child
                                left_child = 2 * index + 1
                                right_child = 2 * index + 2
                            else:
                                break
                    else:
                        break

                # Left child is smaller than right child
                else:
                    if self.ride_heap[index].ride_cost > self.ride_heap[left_child].ride_cost:
                        self.ride_heap[index].index_number = left_child
                        self.ride_heap[left_child].index_number = index
                        self.ride_heap[index], self.ride_heap[left_child] = self.ride_heap[left_child], \
                            self.ride_heap[index]
                        index = left_child
                        left_child = 2 * index + 1
                        right_child = 2 * index + 2

                    elif self.ride_heap[index].ride_cost == self.ride_heap[left_child].ride_cost:
                        if self.ride_heap[index].trip_duration > self.ride_heap[left_child].trip_duration:
                            self.ride_heap[index].index_number = left_child
                            self.ride_heap[left_child].index_number = index
                            self.ride_heap[index], self.ride_heap[left_child] = self.ride_heap[left_child], \
                                self.ride_heap[index]
                            index = left_child
                            left_child = 2 * index + 1
                            right_child = 2 * index + 2
                        else:
                            break
                    else:
                        break

            else:
                # check with left and swap if needed
                if self.ride_heap[index].ride_cost > self.ride_heap[left_child].ride_cost:
                    self.ride_heap[index].index_number = left_child
                    self.ride_heap[left_child].index_number = index
                    self.ride_heap[index], self.ride_heap[left_child] = self.ride_heap[left_child], \
                        self.ride_heap[index]
                    index = left_child
                    left_child = 2 * index + 1
                    right_child = 2 * index + 2

                elif self.ride_heap[index].ride_cost == self.ride_heap[left_child].ride_cost:
                    if self.ride_heap[index].trip_duration > self.ride_heap[left_child].trip_duration:
                        self.ride_heap[index].index_number = left_child
                        self.ride_heap[left_child].index_number = index
                        self.ride_heap[index], self.ride_heap[left_child] = self.ride_heap[left_child], \
                            self.ride_heap[index]
                        index = left_child
                        left_child = 2 * index + 1
                        right_child = 2 * index + 2
                    else:
                        break
                else:
                    break

    # Inserts as the last node and calls heapify top to find its appropriate location
    def insert_ride(self, ride_number: int, ride_cost: int, trip_duration: int, rbt_node):
        new_ride = HeapNode_RideInfo(ride_number, ride_cost, trip_duration, rbt_node)
        new_ride.index_number = len(self.ride_heap)
        rbt_node.add_ref(new_ride)
        self.ride_heap.append(new_ride)
        self.__heapify_top()

    # Returns the root of min heap without delete
    def get_min(self):
        if len(self.ride_heap) > 0:
            return self.ride_heap[0]

    # Returns the root node of min heap
    def remove_min(self):
        if len(self.ride_heap) > 1:
            output = self.ride_heap[0]
            self.ride_heap[0] = self.ride_heap[-1]
            self.ride_heap[0].index_number = 0
            del self.ride_heap[-1]
            self.__heapify_bottom()
        elif len(self.ride_heap) == 1:
            output = self.ride_heap.pop()
        else:
            output = None
        return output

    # Copy last node to the node which is to be deleted and then heapify bottom
    def delete_ride(self, index: int):
        if index < len(self.ride_heap):
            output = self.ride_heap[index]
            self.ride_heap[index] = self.ride_heap[-1]
            self.ride_heap[index].index_number = index
            del self.ride_heap[-1]
            self.__heapify_bottom(index)
            return output
        else:
            print("Something Went Wrong")

    # Update the node and call heapify top or heapify bottom based on the trip conditions
    def update_ride(self, index: int, new_trip_duration: int, is_cost_change: bool):
        if is_cost_change:
            self.ride_heap[index].trip_duration = new_trip_duration
            self.ride_heap[index].ride_cost += 10
            self.__heapify_bottom(index)
        else:
            self.ride_heap[index].trip_duration = new_trip_duration
            self.__heapify_top(index)
