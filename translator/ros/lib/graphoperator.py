import collections
import copy
import json
import logging
import requests
import yaml
from ros.framework import Operator

logger = logging.getLogger("graphOperator")
logger.setLevel(logging.WARNING)

def update(d, u):
    """ Update values in d while preserving syblings of replaced keys at each level. """
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

class Service:
    """ Describe a service to invoke. """
    def __init__(self, spec):
        self.url = spec['url']
        self.name = spec['name']
        self.response = None
        
class GraphOperator(Operator):    
    """ Model invoking graph operators in the network generically. """

    def __init__(self):
        super(GraphOperator, self).__init__("graph-operator")
    
    def new_message (self, values):
        """ Create a new message populating omitted fields with defaults. """
        response = {
            "question_graph": {
                "nodes": [],
                "edges": []
            },
            "knowledge_graph": {
                "nodes": [],
                "edges": []
            },
            "knowledge_maps": []
        }
        update (response, values)
        return response
    
    def resolve(self, d, event, loop, index):
        result = d
        if isinstance(d, list):
            result = [ self.resolve(e, event, loop, index) for e in d ]
        elif isinstance(d, dict):
            for k, v in d.items():
                result[k] = self.resolve(v, event, loop, index)
        elif isinstance(d, str):
            if d.startswith('$'):
                key = d[1:]
                obj = loop[key][index] if key in loop and len(loop[key]) > index else None 
                if not obj:
                    obj = event.context.resolve_arg (d)
                result = obj
            elif d.startswith('select '):
                result = self.resolve_query (d, event)
        return result

    def resolve_query (self, value, event):
        """ Resolve arguments, including select statements, into values. """
        response = value
        if isinstance(value, str):
            syntax_valid = False
            tokens = value.split (" ")
            if len(tokens) == 4:
                select_keyword, pattern, from_keyword, source = tokens
                if select_keyword == 'select' and from_keyword == 'from':
                    pattern = pattern.strip ('"')
                    if source.startswith ("$"):
                        syntax_valid = True
                        resolved_source = event.context.resolve_arg (source)
                        logger.debug (f"resolved source {resolved_source} and pattern {pattern}.")
                        response = event.context.json.select (
                            query = pattern,
                            graph = resolved_source)
                        logger.debug (f"query-result: {response}")
            if not syntax_valid:
                logger.error (f"Incorrectly formatted statement: {value}. Supported syntax is 'select <pattern> from <variable>'.")
        return response

    def invoke (self, event):
        """ Invoke a generic graph operator, or set of these. """
        
        """ Look for select statements and execute them to populate the outbound question. """
        """ This is limited to jsonpath_rw queries at the moment. Maybe extend to cypher. """
        """ Also need to dig deeper into the object hierarchy when executing statements. """
        responses = []
        message =  self.new_message (event.message)
        message = self.resolve (message, event, loop=None, index=None)
        aggregate = [ self.invoke_service (event, message) ]        
        n = []
        e = []
        for a in aggregate:
            n = n + a[0]
            e = e + a[1]

        """ Return knowledge graph standard. """
        return event.context.tools.kgs (nodes = n, edges = e)
            
    def short_text(self, text, max_len=85):
        """ Generate a shortened form of text. """
        return (text[:max_len] + '..') if len(text) > max_len else text

    def invoke_service(self, event, message):
        """ Invoke each service endpoint. """
        responses = []
        services = [ Service(s) for s in event.services ]
        for service in services:
            logger.debug (f"calling service: {service.url} => {json.dumps(message, indent=2)}")

            """ Invoke the service; stash the response. """
            service.response = requests.post (
                url = service.url,
                json = message,
                headers = { "accept" : "application/json" })

            if service.response.status_code == 200:
                logger.debug (f"Invoking service {service.url} succeeded.")
                responses.append (service.response.json ())
            else:
                logger.error (f"Service {service.url} failed with error {service.response.status_code} and error: {service.response.text}")

        """ kludgy, but works. """
        edges = []
        nodes = []
        print (f"{json.dumps (responses, indent=2)}")
        for r in responses:
            if 'knowledge_graph' in r:
                kg = r['knowledge_graph']
                if 'result_list' in kg:
                    for g in kg['result_list']:
                        edges = edges + g['result_graph']['edge_list']
                        nodes = nodes + g['result_graph']['node_list']
                        print (f"....")
                        
        t = self.short_text (json.dumps(responses, indent=2))
        return [ nodes, edges ]
