# import copy

class RBTNode_RideInfo:

    def __init__(self, ride_number: int, ride_cost: int, trip_duration: int):
        self.heap_node = None
        self.ride_number = ride_number
        self.ride_cost = ride_cost
        self.trip_duration = trip_duration
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1

    # Function to update heap_ref
    def add_ref(self, heap_node):
        self.heap_node = heap_node

    def __repr__(self):
        return f"({self.ride_number},{self.ride_cost},{self.trip_duration})"


class RBTree:
    def __init__(self):
        self.NULL = RBTNode_RideInfo(None, None, None)
        self.NULL.color = 0
        self.root = self.NULL

    # Helper function to Search (Same As BST)
    def __search_helper(self, ride_number: int):
        node = self.root
        searched_node = self.NULL
        while node != self.NULL:
            if node.ride_number == ride_number:
                searched_node = node
                break
            if node.ride_number <= ride_number:
                node = node.right
            else:
                node = node.left

        if searched_node == self.NULL:
            return None
        else:
            return searched_node

    # Helper Function to do RR Rotation
    def __rotate_right(self, node: RBTNode_RideInfo):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.NULL:
            left_child.right.parent = node

        # Change parent of left_child as parent of node
        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    # Helper Function to do LL Rotation
    def __rotate_left(self, node: RBTNode_RideInfo):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.NULL:
            right_child.left.parent = node

        # Change parent of right_child as parent of node
        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    # Traverse left subtree to find Min Ride Number
    def __minimum(self, node: RBTNode_RideInfo):
        while node.left != self.NULL:
            node = node.left
        return node

    # Helper function to execute rebalancing Strategies to Correct the RB Tree
    def __fix_insert_tree(self, p: RBTNode_RideInfo):
        while p.parent.color == 1:
            pp = p.parent
            gp = p.parent.parent
            # X = Right child
            if pp == gp.right:
                # Left child of grandparent
                d = gp.left
                # RYr
                if d.color == 1:
                    d.color = 0
                    pp.color = 0
                    gp.color = 1
                    p = gp
                # RYb
                else:
                    # RLb it takes two Rotations to fix this
                    if p == pp.left:
                        p = pp
                        self.__rotate_right(p)
                    p.parent.color = 0
                    p.parent.parent.color = 1
                    self.__rotate_left(p.parent.parent)
            # X = Left child
            else:
                # Right child of grandparent
                d = gp.right
                # LYr
                if d.color == 1:
                    d.color = 0
                    pp.color = 0
                    gp.color = 1
                    p = gp
                # LYb
                else:
                    # LRb
                    if p == pp.right:
                        p = pp
                        self.__rotate_left(p)
                    p.parent.color = 0
                    p.parent.parent.color = 1
                    self.__rotate_right(p.parent.parent)
            # Break when we get to the Root
            if p == self.root:
                break
        # Root Should always be Black
        self.root.color = 0

    # Healper function to replace the replace_node with the node to be deleted
    def __transplant(self, delete_node: RBTNode_RideInfo, replace_node: RBTNode_RideInfo):
        if delete_node.parent is None:
            self.root = replace_node
        elif delete_node == delete_node.parent.left:
            delete_node.parent.left = replace_node
        else:
            delete_node.parent.right = replace_node
        replace_node.parent = delete_node.parent

    # Helper function to execute rebalancing Strategies to correct the RB Tree after Delete
    def __fix_delete_tree(self, y: RBTNode_RideInfo):

        while y != self.root and y.color == 0:
            py = y.parent
            if y == py.left:
                v = py.right
                # Rr(n)
                if v.color == 1:
                    v.color = 0
                    py.color = 1
                    self.__rotate_left(py)
                    v = py.right
                if v.left.color == 0 and v.right.color == 0:
                    v.color = 1
                    y = py
                else:
                    if v.right.color == 0:
                        v.left.color = 0
                        v.color = 1
                        self.__rotate_right(v)
                        v = py.right
                    v.color = py.color
                    py.color = 0
                    v.right.color = 0
                    self.__rotate_left(py)
                    y = self.root

            else:
                v = py.left
                if v.color == 1:
                    v.color = 0
                    py.color = 1
                    self.__rotate_right(py)
                    v = py.left

                if v.right.color == 0 and v.left.color == 0:
                    v.color = 1
                    y = py
                else:
                    if v.left.color == 0:
                        v.right.color = 0
                        v.color = 1
                        self.__rotate_left(v)
                        v = py.left

                    v.color = py.color
                    py.color = 0
                    v.left.color = 0
                    self.__rotate_right(py)
                    y = self.root
        y.color = 0

    # Helper function to get the output nodes (Ignores the subtrees which are out of the given range)
    def print_range_helper(self, node: RBTNode_RideInfo, l_ride_number: int, b_ride_number: int, output: str):
        if node == self.NULL:
            return

        # Don't traverse if the node is out of range
        if node.ride_number > l_ride_number:
            self.print_range_helper(node.left, l_ride_number, b_ride_number, output)

        if l_ride_number <= node.ride_number <= b_ride_number:
            output.append(node)

        if node.ride_number < b_ride_number:
            self.print_range_helper(node.right, l_ride_number, b_ride_number, output)

    # Function to Insert new ride and calls insert helper function to rebalance the Tree
    def insert_ride(self, ride_number: int, ride_cost: int, trip_duration: int):
        check_ride = self.__search_helper(ride_number)
        if check_ride is None:
            new_ride = RBTNode_RideInfo(ride_number, ride_cost, trip_duration)
            new_ride.left = self.NULL
            new_ride.right = self.NULL
            parent = None

            current_node = self.root
            while current_node != self.NULL:
                parent = current_node
                if current_node.ride_number > new_ride.ride_number:
                    current_node = current_node.left
                else:
                    current_node = current_node.right

            new_ride.parent = parent
            if parent is None:
                self.root = new_ride
                new_ride.color = 0
                return new_ride
            elif new_ride.ride_number < parent.ride_number:
                parent.left = new_ride
            else:
                parent.right = new_ride

            if new_ride.parent.parent is None:
                return new_ride

            self.__fix_insert_tree(new_ride)
            return new_ride
        else:
            return None

    # Function to delete the given ride and calls delete helper function to rebalance the Tree
    def delete_ride(self, ride_number: int):
        # node = self.root
        del_node = self.__search_helper(ride_number)
        if del_node is None:
            return None

        searched_node = del_node
        searched_node_color = searched_node.color
        # if del_node has no child or no left child
        if del_node.left == self.NULL:
            y = del_node.right
            self.__transplant(del_node, del_node.right)
        # if del_node has no right child
        elif del_node.right == self.NULL:
            y = del_node.left
            self.__transplant(del_node, del_node.left)
        # if del_node has both child nodes
        else:
            searched_node = self.__minimum(del_node.right)
            searched_node_color = searched_node.color
            y = searched_node.right
            if searched_node.parent == del_node:
                y.parent = searched_node
            else:
                self.__transplant(searched_node, searched_node.right)
                searched_node.right = del_node.right
                searched_node.right.parent = searched_node
            self.__transplant(del_node, searched_node)
            searched_node.left = del_node.left
            searched_node.left.parent = searched_node
            searched_node.color = del_node.color

        if searched_node_color == 0:
            self.__fix_delete_tree(y)
        return del_node.heap_node

    # Function to search ride
    def search_ride(self, ride_number: int):
        return self.__search_helper(ride_number)

    # Function to call print in the given range
    def print_range(self, l_ride_number: int, b_ride_number: int):
        node = self.root
        outputs = []
        self.print_range_helper(node, l_ride_number, b_ride_number, outputs)
        if len(outputs) == 0:
            output = "(0,0,0)"
        else:
            output = ",".join([opt.__repr__() for opt in outputs])
        # print(output)
        return output
