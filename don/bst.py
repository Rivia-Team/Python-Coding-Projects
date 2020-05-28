# bst.py
# ===================================================
# Implement a binary search tree that can store any
# arbitrary object in the tree.
# ===================================================


class Student:
    def __init__(self, number, name):
        self.grade = number  # this will serve as the object's key
        self.name = name

    def __lt__(self, kq):
        return self.grade < kq.grade

    def __gt__(self, kq):
        return self.grade > kq.grade

    def __eq__(self, kq):
        return self.grade == kq.grade

    def __str__(self):
        if self.grade is not None:
            return self.name + " grades are " + str(self.grade)


class TreeNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val  # when this is a primitive, this serves as the node's key


class BST:
    def __init__(self, start_tree=None) -> None:
        """ Initialize empty tree """
        self.root = None

        # populate tree with initial nodes (if provided)
        if start_tree is not None:
            for value in start_tree:
                self.add(value)


    def __str__(self):
        """
        Traverses the tree using "in-order" traversal
        and returns content of tree nodes as a text string
        """
        values = [str(_) for _ in self.in_order_traversal()]
        return "TREE in order { " + ", ".join(values) + " }"


    def add(self, val):
        """
        Creates and adds a new node to the BSTree.
        If the BSTree is empty, the new node should added as the root.

        Args:
            val: Item to be stored in the new node
        """
        parent_node = None
        current_node = self.root
        if self.root is None:
            self.root = TreeNode(val)
        else:
            while current_node is not None:
                parent_node = current_node
                if val < parent_node.val:
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            if val < parent_node.val:
                parent_node.left = TreeNode(val)
            else:
                parent_node.right = TreeNode(val)


    def in_order_traversal(self, cur_node=None, visited=None) -> []:
            """
            Perform in-order traversal of the tree and return a list of visited nodes
            """
            if visited is None:
                # first call to the function -> create container to store list of visited nodes
                # and initiate recursive calls starting with the root node
                visited = []
                self.in_order_traversal(self.root, visited)

            # not a first call to the function
            # base case - reached the end of current subtree -> backtrack
            if cur_node is None:
                return visited

            # recursive case -> sequence of steps for in-order traversal:
            # visit left subtree, store current node value, visit right subtree
            self.in_order_traversal(cur_node.left, visited)
            visited.append(cur_node.val)
            self.in_order_traversal(cur_node.right, visited)
            return visited


    def pre_order_traversal(self) -> []:
        """
        Perform pre-order traversal of the tree and return a list of visited nodes

        Returns:
            A list of nodes in the specified ordering
        """
        visited = []
        if visited is None:
            if not self.root:
                return visited
        process_trees = [self.root]
        tree = self.root
        while process_trees:
            visited.append(tree.val)
            if tree.right:
                process_trees.append(tree.right)
            tree = tree.left
            if not tree and process_trees:
                tree = process_trees.pop()
        return visited


    def post_order_traversal(self) -> []:
        """
        Perform post-order traversal of the tree and return a list of visited nodes

        Returns:
            A list of nodes in the specified ordering
        """
        process_trees = [self.root]
        visited = []
        if visited is None:
            if not self.root:
                return visited

        while process_trees:
            tree = process_trees.pop()
            if tree:
                visited = [tree.val] + visited
                if tree.left:
                    process_trees.append(tree.left)
                if tree.right:
                    process_trees.append(tree.right)

        return visited


    def contains(self, kq):
        """
        Searches BSTree to determine if the query key (kq) is in the BSTree.

        Args:
            kq: query key

        Returns:
            True if kq is in the tree, otherwise False
        """
        values = self.in_order_traversal()
        if kq in values:
            return True
        else:
            return False


    def left_child(self, node):
        """
        Returns the left-most child in a subtree.

        Args:
            node: the root node of the subtree

        Returns:
            The left-most node of the given subtree
        """
        while node.left is not None:
            node = node.left
        return node


    def remove(self, kq, node=None):
        """
        Removes node with key k, if the node exists in the BSTree.

        Args:
            node: root of Binary Search Tree
            kq: key of node to remove

        Returns:
            True if k is in the tree and successfully removed, otherwise False
        """
        if self.contains(kq):
            values = self.in_order_traversal()
            target, parent = self.find(kq)
            if parent is None:
                in_order_successor = values[values.index(kq) + 1]
                successor, p_successor = self.find(in_order_successor)
                successor.left = target.left
                if successor is not target.right:
                    p_successor.left = successor.right
                    successor.right = target.right
                self.root = successor
                return True
            elif target.left is None and target.right is None:
                if parent.left.val == kq:
                    parent.left = None
                    return True
                elif parent.right.val == kq:
                    parent.right = None
                    return True
            elif target.right is not None and target.left is not None:
                in_order_successor = values[values.index(kq) + 1]
                successor, p_successor = self.find(in_order_successor)
                successor.left = target.left
                p_successor.left = successor.right
                successor.right = target.right
            elif target.right is not None:
                parent.right = target.right
                return True
            elif target.left is not None:
                parent.left = target.left
                return True
        else:
            return False


    def find(self, kq):
        par_node = None
        cur_node = self.root
        while cur_node is not None:
            if cur_node.val == kq:
                return cur_node, par_node
            elif kq < cur_node.val:
                par_node = cur_node
                cur_node = cur_node.left
            elif kq > cur_node.val:
                par_node = cur_node
                cur_node = cur_node.right


    def get_first(self):
        """
        Gets the val of the root node in the BSTree.

        Returns:
            val of the root node, return None if BSTree is empty
        """
        if self.root is None:
            return None
        else:
            return self.root.val


    def remove_first(self):
        """
        Removes the val of the root node in the BSTree.

        Returns:
            True if the root was removed, otherwise False
        """
        if self.root.right is None:
            self.root = self.root.left
        else:
            self.remove(self.root.val)


def main():
    tree = BST()
    #tree.add(50)
    #print(tree.get_first())
    #print(tree.contains(50))
    tree.add(9)
    tree.add(10)
    tree.add(8)
    tree.add(11)
    tree.add(7)
    tree.add(12)
    tree.add(6)
    tree.add(13)
    tree.add(5)
    tree.add(4)
    tree.add(3)
    print(tree.pre_order_traversal())

    print(tree)

if __name__ == "__main__":
    main()