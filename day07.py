class Node:
    def __init__(self, name: str, is_file: bool, size: int = 0):
        self.name = name
        self.is_file = is_file
        self.size = size
        self.children = {}
        self.parent: Node

    def get_size(self):
        if self.is_file:
            return self.size
        return sum(map(Node.get_size, self.children.values()))

    def get_child_dir(self, name: str) -> "Node":
        if name not in self.children:
            child = Node(name, False)
            child.parent = self
            self.children[name] = child
        return self.children[name]


def main():
    with open("day07.txt", "r") as f:
        lines = f.read().split("\n")
    root = Node("/", False)
    current_node: Node = root
    for line in lines:
        parts = line.split(" ")
        if parts[0] == "$":
            if parts[1] == "cd":
                if parts[2] == "/":
                    current_node = root
                elif parts[2] == "..":
                    current_node = current_node.parent
                else:
                    current_node = current_node.get_child_dir(parts[2])
            elif parts[1] == "ls":
                continue
        elif parts[0] == "dir":
            current_node.get_child_dir(parts[1])
        else:
            size = int(parts[0])
            name = parts[1]
            current_node.children[name] = Node(name, True, size)
    print(sum(filter(lambda x: x <= 100000, get_dir_sizes(root))))

    free = 70000000 - root.get_size()
    missing = 30000000 - free
    dir_sizes = filter(lambda x: x >= missing, get_dir_sizes(root))
    print(min(dir_sizes))


def get_dir_sizes(node: Node):
    dir_sizes = []
    for c in node.children.values():
        if not c.is_file:
            dir_sizes.extend(get_dir_sizes(c))
    return dir_sizes + [node.get_size()]


if __name__ == "__main__":
    main()