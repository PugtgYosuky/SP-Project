"""
Authors:
- Joana Simoes, n.º 2019217013
- Tomas Ferreira, n.º 2019224786
"""

import os
import json

# Communication class - exchanges messages between the two parties
class Communication():
    def __init__(self):
        # Initializing of the communication class - the communication is made using files (json and binary files)

        # calculating parent path of where to save the communication messages
        path = path = os.getcwd()
        self.save_path = os.path.abspath(os.path.join(path, os.pardir, 'common'))
        # creating the json file
        self.file_path = os.path.join(self.save_path,'common_file.json')
        # if there is already a communication file, it loads it. If there is no communication 
        # file, it will create a empty dictionary
        if os.path.exists(self.file_path):
            self.receive_information()
        else:
            self.data = {}

    def send_information(self):
        # Writes the data to the json file.
        json_object = json.dumps(self.data, indent=4)
        with open(self.file_path, 'w') as output:
            output.write(json_object)
            output.close()
    
    def receive_information(self):
        # Reads the json file and loading it into the data variable.
        with open(self.file_path, 'r') as input:
            self.data = json.load(input)
            input.close()

    
    def add_value(self, new_value, variable):
        """
        A function that adds (or changes) a value of a variable in the data and writes it into a json file

        :param variable: the name of the variable to be added
        :param new_value: the value to be added
        """
        self.data[variable] = new_value
        self.send_information()

    def get_value(self, variable):
        """
        A function that retrieves a value of a variable in the data
        """
        self.receive_information()
        if variable in self.data:
            return self.data[variable]
        else:
            return None

    def write_bytes(self, byte_array, description):
        """
        A function that writes a list of bytes to a binary file

        :param byte_array: the list of bytes to be written
        :param description: the name of the file
        """
        path = os.path.join(self.save_path, description)
        with open(path, 'wb') as file:
            file.write(byte_array)
            file.close()

    def get_bytes(self, description):
        """
        A function that retrieves a list of bytes from a binary file
        
        :param description: the name of the file
        """
        path = os.path.join(self.save_path, description)
        if os.path.exists(path):
            with open(path, 'rb') as file:
                byte_array = file.read()
                file.close()
            return byte_array
        else:
            print(f"Could not found file{description}")
            return None
