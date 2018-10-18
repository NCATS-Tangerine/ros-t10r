from t10r.ros.lib.xray import XRay
from t10r.ros.lib.gamma import Gamma
from t10r.ros.lib.icees import Icees
from t10r.ros.lib.graphoperator import GraphOperator

class Plugin:
    """ A module for the Ros knowledge network development environment. """
    
    def __init__(self):
        self.description = "Translator workflow capabilities."
        self.name = "ros-t10r"
        
    def __repr__(self):
        return self.description
    
    def workflows (self):
        """ Describe a set of workflows provided by this module. """
        return [
            "workflow_one.ros",
        ]
    
    def libraries (self):
        """ Classes implementing the Ros Operator interface. """
        return [
            "t10r.ros.lib.bionames.Bionames",
            "t10r.ros.lib.xray.XRay",
            "t10r.ros.lib.gamma.Gamma",
            "t10r.ros.lib.icees.Icees",
            "t10r.ros.lib.graphoperator.GraphOperator"
        ]

    
            
