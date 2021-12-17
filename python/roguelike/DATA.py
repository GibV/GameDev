import json


# DATA FORMAT:

## { 
##  'levels': [{
##              'graph': [...],
##              'board': [...],
##              'mobs':  [...],
##             }, ...],
##  'options': {
##              'brightness': ...,
##              ...
##             }
## }


class DATA_MANAGER:

    def __init__(self, main_file_name):
        self.main_dir = main_file_name
##        self.main_file = open(main_file_name, 'wb+')
        self.data = []

    def save(self):
        with open(self.main_dir, 'w') as main_file:#.truncate(0)
##        print(main_file, self.data)
            json.dump(self.data, main_file)

    def load(self, zero_data):
        try:
            main_file = open(self.main_dir, 'r')
            content = main_file.read()
            if len(content)>0:
                self.data = json.loads(content)
            else:
                self.data = zero_data()
            main_file.close()
        except:
            self.data = zero_data()

##    def end(self):
##        self.save()
##        self.main_file.close()
