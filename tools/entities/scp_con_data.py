from base_entity import base_entity

class scp_data(base_entity):

    def __init__(self, keys, user, host, server_path, local_path, log):
        base_entity.__init__(self)
        self.keys = keys
        self.user = user
        self.host = host
        self.server_path = server_path
        self.local_path = local_path
        self.log = log


    def execute(self):
        return "scp -i " + self.keys + " " + self.user + "@" + self.host + ":" + self.server_path + " " + self.local_path