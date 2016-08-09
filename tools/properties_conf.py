from tools.entities import scp_con_data
from tools.property_fetcher import property_fetcher
from tools.entities import jenkins_data
import os.path
import os
import re
import logging


def get_scp_connection_data(instance, target_date, property_file):
    p_fetcher = property_fetcher(property_file)
    keys = get_scp_keys(p_fetcher)
    user = get_scp_user(p_fetcher)
    host = p_fetcher.get_property('amazonSyslogHosts', instance.take())
    server_file_path = get_server_file_path(p_fetcher, target_date)
    destination_path = get_destination_file_path(p_fetcher, instance.name, target_date)
    scp_data = scp_con_data.scp_data(keys, user, host, server_file_path, destination_path)
    return scp_data


def get_server_file_path(pfetcher, date):
    server_loc = re.sub('date', date.strftime('%Y/%m/%d'), pfetcher.get_property('logginig', 'amazon.ec2.instance.default.path'))
    logging.debug('server loc: ' + server_loc)
    return server_loc


def get_destination_file_path(pfetcher, instance, date):
    def_path = pfetcher.get_property('logginig', 'local.prod.log.default.path')
    date_str = date.strftime('%Y_%m_%d')
    instance_path = os.path.join(def_path, instance.lower(), date_str)
    file_path = os.path.join(instance_path, 'daily.log')
    logging.debug('file_path: ' + file_path)
    if not os.path.exists(instance_path):
        print 'shit'
        os.makedirs(instance_path)
    return file_path


def get_scp_keys(p_fetcher):
    return p_fetcher.get_property('logginig', 'local.amazon.key.path')


def get_scp_user(p_fetcher):
    return p_fetcher.get_property('logginig', 'amazon.ec2.instance.default.user')


def get_worker_log_path(property_file):
    p_fetcher = property_fetcher(property_file)
    return p_fetcher.get_property('logginig', 'local.default.log.path')


def get_logging_format(property_file):
    p_fetcher = property_fetcher(property_file)
    return p_fetcher.get_property('logginig', 'local.logger.format')


def get_jenkins_connection_data(property_file):
    p_fetcher = property_fetcher(property_file)
    url = p_fetcher.get_property('jenkinsCucumber', 'jenkins.url')
    username = p_fetcher.get_property('jenkinsCucumber', 'jenkins.username')
    password = p_fetcher.get_property('jenkinsCucumber', 'jenkins.password')
    console_log = p_fetcher.get_property('jenkinsCucumber', 'local.jenkins.build.console.log')
    report_log = p_fetcher.get_property('jenkinsCucumber', 'local.jenkins.build.report.log')
    cucumber_endpoint = p_fetcher.get_property('jenkinsCucumber', 'jenkins.cucumber.endpoint')
    jenkins_con_data = jenkins_data.jenkins_data(url, username, password, console_log, report_log, cucumber_endpoint)
    return jenkins_con_data

