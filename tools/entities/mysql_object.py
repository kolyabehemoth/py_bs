from base_entity import base_entity

class mysql_object(base_entity):

    def __init__(self, user, password, host, script):
        base_entity.__init__(self)
        self.user = user;
        self.password = password;
        self.host = host;
        self.script = script;

    def execute(self):
        return "mysql -u" + self.user + " -p" + self.password + " -A -h " + self.host + " < " + self.script;
