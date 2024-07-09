


class Port:
    def __init__(self, name, node):
        self.name = name
        self.node = node
        self.connections = []

    def get_connected_ports(self):
        if(len(self.connections)==0):
            raise RuntimeError("No connections")
        return self.connections

    def connect(self, connected_port):
        self.connections.append(connected_port)
        connected_port.connections.append(self)

class NodeWrapper:
    def __init__(self, data, id, graph_access):
        self.input_ports = []
        self.output_ports = []
        self.id = id
        self.graph_access = graph_access
        self.data = data 
        self.str_type = data["type_"]
        for port_name in data["input_ports"]:
            self.input_ports.append(Port(port_name, self))

        for port_name in data["output_ports"]:
            self.output_ports.append(Port(port_name, self))

        for (key, variable) in self.data.items():
            if key not in ["type_", "icon", "name", "color", 
                            "border_color", "text_color", "disabled", 
                            "selected", "visible", "width", "height", "input_ports", "output_ports",
                            "pos", "layout_direction", "port_delection_allowed", "subgraph_session"]:
                setattr(self, key, variable)

    def get_output_port(self, name):
        for port in self.output_ports:
            if port.name == name:
                return port

        raise RuntimeError("no output port with name {}".format(name))

    def get_input_port(self, name):
        for port in self.input_ports:
            if port.name == name:
                return port
        raise RuntimeError("no input port with name {}".format(name))

    def get_next_node(self, name):
        port = self.get_output_port(name)
        return port.get_connected_ports()[0].node

    def str_type(self):
        return self.str_type
    
