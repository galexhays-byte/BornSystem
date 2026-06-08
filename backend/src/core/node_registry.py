class NodeRegistry:
    def __init__(self):
        self.nodes = []

    def register(self, node):
        self.nodes.append(node)

    def list_nodes(self):
        return self.nodes

    def select_node(self, name=None):
        if name:
            for node in self.nodes:
                if node.name == name:
                    return node
            raise Exception(f"Node '{name}' not registered")

        if not self.nodes:
            raise Exception("No nodes registered")
        return self.nodes[0]
