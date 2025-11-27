from ai.node import Node
from ai.connection import Connection
import random

# a Node represents a neuron in the neural network
# Connection represents a weighted link between 2 nodes

class Brain:
    # inputs is how many neurons the network will have
    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
        # Create input nodes
            for i in range(0, self.inputs):
                self.nodes.append(Node(i))
                self.nodes[i].layer = 0 # input layer

            # Create bias node (always outputs 1)
            bias_id = self.inputs
            self.nodes.append(Node(bias_id))
            self.nodes[bias_id].layer = 0

            # Create output node - the decision neuron
            output_id = self.inputs + 1
            self.nodes.append(Node(output_id))
            self.nodes[output_id].layer = 1 # output layer

            # Create connections from each input node to the output node
            for i in range(0, 4):
                self.connections.append(Connection(self.nodes[i],self.nodes[4],
                                                    random.uniform(-1, 1))) # random initial weight

    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])

    # group nodes by layer order so that nodes are activated in order
    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])

    # evaluate the network with a list of input values vision
    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        self.nodes[3].output_value = 1 # bias node output is 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        output_value = self.nodes[4].output_value

        # Reset node input values
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value # returns the network's output used by the player to make a decisiom

    def clone(self):
        clone = Brain(self.inputs, True)

        # Clone all the nodes
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Clone all connections
        for c in self.connections:
            clone.connections.append(c.clone(clone.get_node(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def get_node(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    # 80% chance that a connection undergoes mutation
    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()

