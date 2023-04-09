import ujson

class UJSONConstructor:
    def __init__(self, number_of_chainlinks, chain_direction_degrees):
        data = {
                "number_of_chainlinks": number_of_chainlinks,
                "chain_direction_degrees": chain_direction_degrees
            }
        self.json_data = ujson.dumps(data)
                
    def get_json(self, print=False):
        if print:
            print(self.json_data)
            
        return self.json_data