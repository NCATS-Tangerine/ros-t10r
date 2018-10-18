import requests
import json
import logging
import os
from ros.framework import Operator

logger = logging.getLogger("bionames")
logger.setLevel(logging.WARNING)

class Bionames (Operator):

    def __init__(self):
        """ Initialize the operator. """
        super(Bionames, self).__init__("bionames")
        self.pattern = "https://bionames.renci.org/lookup/{input}/{type}/"

    def get_ids (self, name, type_name):
        url = self.pattern.format (**{
            "input" : name,
            "type"  : type_name
        })
        logger.debug (f"url: {url}")
        result = None
        response = requests.get(
            url = url,
            headers = {
                'accept': 'application/json'
            })
        if response.status_code == 200 or response.status_code == 202:
            result = response.json ()
        else:
            raise ValueError (response.text)
        return result
    
    def invoke (self, event):
        return self.get_ids (
            name=event.input,
            type_name=event.type)
        '''
        result = None
        
        url = self.pattern.format (**{
            "input" : event.input,
            "type"  : event.type
        })
        logger.debug (f"url: {url}")
        
        response = requests.get(
            url = url,
            headers = {
                'accept': 'application/json'
            })
        if response.status_code == 200 or response.status_code == 202:
            result = response.json ()
        else:
            raise ValueError (response.text)
        return result
        '''
