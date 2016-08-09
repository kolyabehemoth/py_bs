import sys
import getopt
from datetime import datetime
from tools.entities.base_entity import AmazonEc2Instance
from tools import properties_conf
from tools.jenkins import jenkins_executor
from tools.ssh import ssh_executor
import logging


def config_logging(log_path, log_format):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_path)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(log_format)
    logger.addHandler(config_logging_handler(fh, logging.DEBUG, formatter))
    logger.addHandler(config_logging_handler(ch, logging.DEBUG, formatter))


def config_logging_handler(handler, level, formatter):
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def main(argv):
    is_action_syslog = False
    is_action_report = False
    property_file = None
    instance = None
    job_name = None
    date = None
    try:
        opts, args = getopt.getopt(argv, "hsr:jd:i:p:", ["syslog", "report", "job=", "date=", "instance=", "pfile="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-d", "--date"):
            date = arg
        elif opt in ("-i", "--instance"):
            instance = arg
        elif opt in ("-p", "--pfile"):
            property_file = arg
        elif opt in ("-j", "--job"):
            job_name = arg
        elif opt in ("-s", "--syslog"):
            is_action_syslog = True
        elif opt in ("-r", "--report"):
            is_action_report = True

    if property_file is None:
        print 'property file can\'t be None'
        print_help()
        sys.exit(2)
    log_path = properties_conf.get_worker_log_path(property_file)
    log_format = properties_conf.get_logging_format(property_file)
    config_logging(log_path, log_format)

    if not is_action_syslog and not is_action_report:
        logging.error('You should choose one action')
        print_help()
        sys.exit(2)

    if is_action_syslog:
        tdate = datetime.strptime(date, '%Y.%m.%d')
        logging.info('start fetching syslog from instance: ' + instance + " for date: " + date)
        instance = AmazonEc2Instance.parse(instance)
        scp_data = properties_conf.get_scp_connection_data(instance, tdate, property_file)
        ssh_executor.execute_download(scp_data)
    else:
        jenkins_con_data = properties_conf.get_jenkins_connection_data(property_file)
        jenkins_executor.get_job_revision(jenkins_con_data, job_name)
        pass
    return


def print_help():
    print '\nUsage:python main.py [action] [options]\n'\
          'Actions: \n' \
          '  -s, --syslog - fetch syslog from server(required options are date, instance_type and property file)\n'\
          '  -r, --report - fetch from jenkins cucumber report(required options property file and job name)\n'\
          'Options: \n'\
          '  -j, --job - jenkins job name *required for --report action*\n'\
          '  -d, --date  - date in format year.mount.day *required for --syslog action*\n'\
          '  -i, --instance - instance type of aws ec2 instance *required for --syslog action*. taken from property file\n'\
          '  -p, --pfile - path to property file, *required for --syslog and report action*\n'


if __name__ == "__main__":
   main(sys.argv[1:])