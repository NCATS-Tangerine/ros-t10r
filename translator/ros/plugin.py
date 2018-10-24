from translator.ros.lib.xray import XRay
from translator.ros.lib.gamma import Gamma
from translator.ros.lib.icees import Icees
from translator.ros.lib.graphoperator import GraphOperator

class Plugin:
    """ A module for the Ros knowledge network development environment. """
    
    def __init__(self):
        self.description = "Translator workflow capabilities."
        self.name = "ros-translator"
        
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
            "translator.ros.lib.bionames.Bionames",
            "translator.ros.lib.biothings.Biothings",
            "translator.ros.lib.xray.XRay",
            "translator.ros.lib.gamma.Gamma",
            "translator.ros.lib.icees.Icees",
            "translator.ros.lib.graphoperator.GraphOperator"
        ]

    
            
