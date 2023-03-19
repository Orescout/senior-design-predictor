import json

class JsonConstructor:
    def __init__(self, number_of_chainlinks, chain_direction_o_clock):
        data = {
                "number_of_chainlinks": number_of_chainlinks,
                "chain_direction_o_clock": chain_direction_o_clock
            }
        json_data = json.dumps(data, indent=4)
            
        self.json = json_data
    
    def get_json(self, printit=False):
        if printit:
            print(self.json)
            
        return self.json