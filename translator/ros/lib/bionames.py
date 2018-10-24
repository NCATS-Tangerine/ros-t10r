import requests
import json
import logging
import os
from ros.framework import Operator
from pyparsing import Word, alphas, Literal, QuotedString, White, alphanums

logger = logging.getLogger("bionames")
logger.setLevel(logging.WARNING)

class Bionames (Operator):

    def __init__(self):
        """ Initialize the operator. """
        super(Bionames, self).__init__("bionames")
        self.url = "https://bionames.renci.org/lookup/{input}/{type}/"
        self.select_grammar = \
                              Literal("select") + White() + ( QuotedString('"') | Word( alphas+"_"+"$", alphanums+"_" ) ) + \
                              White() + Literal("from") + White() + Word(alphas) + White() + Literal("as") + White() + Word(alphas+"_")
        self.select_grammar = Literal("select") + White() + (QuotedString('"')|Word(alphas+"$"+"_")) + White() + Literal("from") + White() + Word(alphas+"_") + White() + Literal("as") + White() + Word(alphas+"_")
    def execute_query (self, query, context):

        #Literal("select") + White() + ( QuotedString('"') | Word( alphas+"_"+"$", alphanums+"_" ) ) + White() + Literal("from") + White() + Word(alphas)
        print (f"parsing query {query}")
        vals = self.select_grammar.parseString (query)
        print (vals)
        select_key, w0, input_string, w1, from_key, w2, category, w3, as_key, w4, name = self.select_grammar.parseString (query) #'select "this is a string" from bob')

#        logger.debug (f"
        context.set_result (name,
                            self.get_ids (
                                name = context.resolve_arg(input_string),
                                type_name = category))
        
    def get_ids (self, name, type_name):
        url = self.url.format (**{
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
        logger.debug (f"bionames result {result}")
        return result
    
    def invoke (self, event):
        result = {}
        if event.query:
            if isinstance(event.query, str):
                self.execute_query (q, event.context)
            elif isinstance(event.query, list):
                for q in event.query:
                    self.execute_query (q, event.context)
        else:
            result = self.get_ids (
                name=event.input,
                type_name=event.type)
        
        return result
