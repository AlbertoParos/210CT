import re
import string


def main():
    text = read_file()
    list_words = split_lines(text)
    tree = create_tree(list_words)
    print(tree.find_element(tree.root, "and"))
    tree.inorder(tree.root)
    tree.get_first_66(tree.root)


class List66:
    """
    The constructor of the List66 class
    """

    def __init__(self):
        self.list66 = []
        self.min_value = 0
        self.min_element_value = None

    def insert(self, node):
        """
        The insert method receives a node that will be compared with
        every element from the list and insert. If the list is full (66)
        the element with the minimum appearance from the list will be replaced
        :param node: A node, that is compared with the list elements
        """
        if len(self.list66) < 66:
            self.list66.append(node)
            if self.min_value < node.count:
                self.find_new_min(node.count, node)
                self.min_element_value = node
        else:
            if node.count > self.min_value:
                n = self.list66.index(self.min_element_value)
                self.list66[n] = node
                self.find_new_min(node.count, node)

    def find_new_min(self, value, element):
        """
        The find_new_min method finds the element with the fewest appearance from
        the list and changes the values of the attributes
        :param value: the number of appearance of the node
        :param element: the node
        """
        min = 100000
        for word in self.list66:
            if word.count < min:
                min = word.count
                self.min_value = min
                self.min_element_value = word
        if min > value:
            self.min_value = value
            self.min_element_value = element


class Tree:
    """
    The constructor of the Tree class
    """

    def __init__(self, node):
        self.root = node
        self.first_66 = List66()

    def get_root(self):
        """
        The get_root method return the current node of the tree
        :return: The current node of the tree
        """
        return self.root

    def inorder(self, root):
        """
        The inorder method prints out the tree from left to right
        :param root: Current node of the tree
        """
        if root is not None:
            self.inorder(root.left)
            print(root.value, "(", root.count, ")",
                  end=" ")
            self.inorder(root.right)

    def get_first_66(self, root):
        """
        The get_first_66 method searches the tree and fills the list of the tree
        with the 66 most common words
        :param root: The current node
        """
        if root is not None:
            self.get_first_66(root.get_left_node())
            if root.get_value() != 'a' or root.get_value() != "the":
                self.first_66.insert(root)
            self.get_first_66(root.get_right_node())

    def add_node(self, value, root):
        """
        The add_node method adds a node to the tree
        :param value: The value that will be added
        :param root: The current node
        """
        if value == root.get_value():
            root.count += 1
        elif value < root.get_value():
            if root.get_left_node() is None:
                node = Node(value)
                node.parent = root
                root.set_left_node(node)
            else:
                self.add_node(value, root.get_left_node())
        else:
            if root.get_right_node() is None:
                node = Node(value)
                node.parent = root
                root.set_right_node(node)
            else:
                self.add_node(value, root.get_right_node())

    def delete_node(self, value, root):
        """
        The delete_node method deletes a node from the tree
        :param value: The value that will be deleted
        :param root: The current node
        """
        if value == root.get_value():
            if root.count > 1:
                root.count -= 1
            elif root.count == 1:
                if root.get_right_node() is None and root.get_left_node() is None:
                    if root.parent is not None:
                        if root.parent.get_left_node() == root:
                            root.parent.set_left_node(None)
                        else:
                            root.parent.set_right_node(None)
                    else:
                        self.root = None
                elif root.get_right_node() is None:
                    node = root.get_left_node()
                    node.parent = root.parent
                    root.parent.set_left_node(node)
                    root.set_left_node(None)
                elif root.get_left_node() is None:
                    node = root.get_right_node()
                    node.parent = root.parent
                    root.parent.set_right_node(node)
                    root.set_right_node(None)
                else:
                    current = self.min_value(root.get_right_node())
                    root.value = current.value
                    root.count = current.count
                    self.delete_node(current.value, root.get_right_node())
        elif value < root.get_value():
            self.delete_node(value, root.get_left_node())
        elif value > root.get_value():
            self.delete_node(value, root.get_right_node())

    def min_value(self, root):
        """
        The min_value method return the node with the minimum value
        :param root: The current node
        """
        current = root
        while current.get_left_node() is not None:
            current = current.get_left_node()
        return current

    def find_element(self, root, element):
        """
        The find_element method searches the tree for a value
        :param root: The current node
        :param element: The value searched for
        """
        if element == root.get_value():
            return root.count
        elif element < root.get_value() and root.get_left_node() is not None:
            return self.find_element(root.get_left_node(), element)
        elif element > root.get_value() and root.get_right_node() is not None:
            return self.find_element(root.get_right_node(), element)


class Node:
    """
    The constructor of the Node class
    """

    def __init__(self, value):
        self.value = value
        self.count = 1
        self.left = None
        self.right = None
        self.parent = None

    def get_value(self):
        """
        The get_value returns the Node value
        :return: Value of the node
        """
        return self.value

    def set_left_node(self, node):
        """
        The set_left_node method sets the left child of the Node
        :param node: A node that will be the node left child
        """
        self.left = node

    def set_right_node(self, node):
        """
        The set_right_node method sets the right child of the Node
        :param node: A node that will be the node right child
        """
        self.right = node

    def get_left_node(self):
        """
        The get_left_node returns the left child of the Node
        :return: A node that is the left child
        """
        return self.left

    def get_right_node(self):
        """
        The get_right_node returns the right child of the Node
        :return: A node that is the right child
        """
        return self.right


def read_file():
    """
    The read_file function reads a file and returns the lines of it
    :return: A list of lines
    """
    with open("Shakespeare2.txt") as file:
        lines = []
        i = 0
        for line in file:
            i += 1
            if i >= 90 and i <= 2703:
                lines.append(line)
            if i > 2703:
                break
        return lines


def split_lines(lines):
    """
    The split_lines function formats a list of strings in a list of words
    :param lines: A list of strings
    :return:
    """
    list_of_words = []
    for line in lines:
        if line.strip().isdigit() or line == "\n":
            continue
        words = re.sub('[' + string.punctuation + ']', '', line).split()
        list_of_words.extend(words)
    return list_of_words


def create_tree(list_of_words):
    """
    The create_tree function creates a tree and returns it
    :param list_of_words: The list of values that will populate the tree
    :return: A tree filled with given values
    """
    node = Node(list_of_words[0].lower())
    tree = Tree(node)
    list_of_words.pop(0)
    for word in list_of_words:
        word = word.lower()
        tree.add_node(word, tree.root)
    return tree


main()
