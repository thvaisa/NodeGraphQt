


class Port:
    def __init__(self, name, node):
        self.name = name
        self.node = node
        self.connections = []
        self.data = None

    def get_connected_ports(self):
        if(len(self.connections)==0):
            raise RuntimeError("No connections")
        return self.connections

    def connect(self, connected_port):
        self.connections.append(connected_port)
        connected_port.connections.append(self)

    def set_data(self, data):
        self.data = data

    def get_data(self):
        print(self.get_connected_ports()[0].name)
        return self.get_connected_ports()[0].data

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


    def get_output_port_names(self):
        return [port.name for port in self.output_ports]

    def get_input_port_names(self):
        return [port.name for port in self.input_ports]


    def get_output_port(self, name):
        for port in self.output_ports:
            if port.name == name:
                return port

        raise RuntimeError("no output port with name {} within {}".format(name, self.get_output_port_names()))

    def get_input_port(self, name):
        for port in self.input_ports:
            if port.name == name:
                return port
        raise RuntimeError("no input port with name {} within {}".format(name, self.get_input_port_names()))

    def get_next_node(self, name):
        port = self.get_output_port(name)
        return port.get_connected_ports()[0].node

    def get_next_nodes(self, name):
        port = self.get_output_port(name)
        return [x.node for x in port.get_connected_ports()]
    
    def str_type(self):
        return self.str_type
    
