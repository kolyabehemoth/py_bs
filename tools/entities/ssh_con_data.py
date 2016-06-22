from base_entity import base_entity

class ssh_data(base_entity):

    def __init__(self, keys, user, host, path):
        base_entity.__init__(self)
        self.keys = keys;
        self.user = user;
        self.host = host;
        self.script = path;


    def execute(self):
        return "ssh -i " + self.keys + " " + self.user + "@" + self.host + ":" + self.script;