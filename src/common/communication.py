import os
import json

class CommunicationViaJson():
    def __init__(self):
        # Initializing the class.

        # calculating parent path
        path = path = os.getcwd()
        self.save_path = os.path.abspath(os.path.join(path, os.pardir, 'common'))

        self.file_path = os.path.join(self.save_path,'common_file.json')
        if os.path.exists(self.file_path):
            self.receive_information()
        else:
            self.data = {}

    def send_information(self):
        # Writing the data to a file.
        json_object = json.dumps(self.data, indent=4)
        with open(self.file_path, 'w') as output:
            output.write(json_object)
            output.close()
    
    def receive_information(self):
        # Reading the json file and loading it into the data variable.
        with open(self.file_path, 'r') as input:
            self.data = json.load(input)
            input.close()

    
    def add_value(self, variable, new_value):
        # A function that changes the value of a variable in the data and writes it into a json file
        self.data[variable] = new_value
        self.send_information()

    def get_value(self, variable):
        self.receive_information()
        if variable in self.data:
            return self.data[variable]
        else:
            return None

    def get_hash_algorithm(self):
        pass
        # TODO: function to get the algorithm to use

    def write_bytes(self, byte_array, description):
        path = os.path.join(self.save_path, description)
        with open(path, 'wb') as file:
            file.write(byte_array)
            file.close()

    def get_bytes(self, description):
        path = os.path.join(self.save_path, description)
        with open(path, 'rb') as file:
            byte_array = file.read()
            file.close()
        return byte_array