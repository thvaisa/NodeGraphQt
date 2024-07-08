
from NodeGraphQt.qt_free_access.node_wrapper import NodeWrapper


class Logger:
    def warning(self, txt, *args, **kwargs):
        print(txt)


## improve later to access other nodes. It can do like this for now

class GraphWrapper:
    def __init__(self, serialized_data, node_templates={}, logger=Logger()):
        self.serialized_data = serialized_data 
        self.node_templates = node_templates 
        self.wrapped_nodes = {}

        #create nodes
        for (id, node) in self.serialized_data["nodes"].items():            
            nodeType = node["type_"]
            type_ = node_templates.get(nodeType, None)
            if nodeType not in node_templates.keys():
                logger.warning("Type '{}' not found in the node_templates. Using default NodeWrapper".format(nodeType))
                type_ = NodeWrapper
            self.wrapped_nodes[id] = type_(node, id, self)
    
        #create connections
        for conn in self.serialized_data["connections"]:
            out = conn["out"]
            output = self.wrapped_nodes[out[0]].get_output_port(out[1])
            in_ = conn["in"]
            input_ = self.wrapped_nodes[in_[0]].get_input_port(in_[1])
            output.connect(input_)



    def get_nodes_of_type(self, type_):
        nodes = []
        for node in self.get_nodes().values():
            if(isinstance(type_, str)):
                if type_ == node.str_type():
                    nodes.append(node)
            else:
                if isinstance(node, type_):
                    nodes.append(node)
        return nodes
    
    def get_nodes(self):
        return self.wrapped_nodes

    def get_serialized_connections(self):
        return self.serialized_data["connections"]

    