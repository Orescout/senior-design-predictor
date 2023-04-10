import ujson

class UJSONConstructor:
    def __init__(self, number_of_chainlinks, chain_direction_degrees):
        data = {
                "chainlinks_count": number_of_chainlinks,
                "chain_direction_degrees": chain_direction_degrees
            }
        self.json_data = ujson.dumps(data)
                
    def get_json(self, printit=False):
        if printit:
            print(self.json_data)
        return self.json_data