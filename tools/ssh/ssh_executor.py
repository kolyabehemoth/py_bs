import subprocess
import logging


def execute_download(scp_data):
    request = scp_data.execute()
    logging.info("the request for downloading log from ec2: " + request)
    s = subprocess.Popen(request, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    logging.info("end download log")
    logging.info(s.strip())

