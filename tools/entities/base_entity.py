from enum import Enum, unique

class base_entity:
    def __init__(self):
        pass

    def execute(self):
        return ""

@unique
class AmazonEc2Instance(Enum):
    Development3='development3'
    Integration1='integration1'
    Integration4='integration4'
    Integration5='integration5'
    Integration6='integration6'
    Qalab1='qalab1'
    Qalab2='qalab2'
    Qalab4='qalab4'
    Qalab5='qalab5'
    Prod='production2'


    def take(self):
        return 'amazon.ec2.instance.' + self.value + '.syslog'

    @staticmethod
    def parse(instance):
        for name, member in AmazonEc2Instance.__members__.items():
            if name.lower() == instance.lower():
                return member