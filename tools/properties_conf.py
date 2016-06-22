from tools.entities import scp_con_data
import ConfigParser
import os.path
import re

def get_scp_connection_data(instance, target_date):
    keys = get_keys()
    user = get_user()
    host = get_property('amazonSyslogHosts', instance.take())
    server_file_path = get_server_file_path(target_date)
    destination_path = get_destination_file_path(instance.name, target_date)
    scp_data = scp_con_data.scp_data(keys, user, host, server_file_path, destination_path)
    return scp_data


def get_property(section, value):
    config = ConfigParser.RawConfigParser()
    config.read('some.properties')
    return config.get(section, value)

def get_server_file_path(date):
    server_loc = re.sub('date', date.strftime('%Y/%m/%d'), get_property('logPath', 'amazon.ec2.instance.default.path'))
    print server_loc
    return server_loc


def get_destination_file_path(instance, date):
    def_path = get_property('logPath', 'local.default.path')
    date_str = date.strftime('%Y_%m_%d')
    file_path = os.path.join(def_path, instance, date_str, 'daily.log')
    print 'file_path: ' + file_path
    if os.path.exists(file_path):
        print 'shit'
    return file_path


def get_keys():
    return get_property('logPath', 'local.amazon.key.path')


def get_user():
    return get_property('logPath', 'amazon.ec2.instance.default.user')


