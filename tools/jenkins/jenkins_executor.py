import subprocess

import errno
from jenkinsapi.jenkins import Jenkins
from bs4 import BeautifulSoup
import os
import re
import logging
import urllib
import jenkinsapi.constants


def get_job_revision(jenkins_con_data, job_name):
    J = Jenkins(jenkins_con_data.url, jenkins_con_data.username, jenkins_con_data.password)
    job = J.get_job(job_name)
    job_ids = job.get_build_ids()
    for j in job_ids:
        build = job.get_build(j)
        build_status = build.get_status()
        logging.info("build status is: "  + build_status)
        if (build_status != jenkinsapi.constants.RESULTSTATUS_FAILURE and build_status != jenkinsapi.constants.STATUS_SUCCESS) or build.is_running():
            logging.debug("skip build: " + str(build.get_number()) + ", cause status is: " + build_status)
            continue
        build_params = build.get_actions().get('parameters')
        branch = build_params[0].get('value')
        team = build_params[1].get('value')
        download_console_log(build, job.name, jenkins_con_data, branch, team)
        download_cuc_report_log(build, job.name, jenkins_con_data, branch, team)
    pass


def download_console_log(build, job_name, jenkins_con_data, branch, team):
    console_log_path = os.path.join(get_log_path(jenkins_con_data.console_log, job_name, team, branch, build.get_number()), 'console.log')
    log = build.get_console()
    logging.debug('write console log to: ' + console_log_path)
    write_to_file(console_log_path, log)


def download_cuc_report_log(build, job_name, jenkins_con_data, branch, team):
    cuc_report_path = get_log_path(jenkins_con_data.report_log, job_name, team, branch, build.get_number())
    logging.debug('save cucumber report to: ' + cuc_report_path)
    base_build_url = generate_build_url_for_fetch(jenkins_con_data, job_name, build.get_number())
    logging.debug('base_build_url: ' + base_build_url)
    download_report(base_build_url, cuc_report_path, jenkins_con_data.cuc_endpoint)


def get_log_path(console_log, job_name, team, branch, build_id):
    base_path = os.path.join(console_log, job_name, team, str(build_id) + '_' + branch)
    if not os.path.exists(base_path):
        logging.info('creating directory: ' + base_path)
        os.makedirs(base_path, 0755)
    return base_path


def generate_build_url_for_fetch(jenkins_con_data, job_name, build_id):
    base_url = re.sub(r'^(https?:\/\/)(.*\/)$', r'\1' + urllib.quote_plus(jenkins_con_data.username) + ':' + urllib.quote_plus(jenkins_con_data.password) + r'@\2', jenkins_con_data.url)
    logging.debug('generating base_url: ' + base_url)
    return url_joiner(base_url, ['job', job_name, str(build_id), jenkins_con_data.cuc_endpoint, '/'])


def download_report_file(link, base_url, dest):
   logging.info('downloading report: ' + link + ' to dest:' + dest)
   filename = os.path.join(dest, link)
   if filename[-1] == '/' and link == '':   # if url: didn't work??
       filename = filename[:-1]
   if os.path.exists(filename):
       logging.info('skipping download file: ' + link + ' cause it already exists')
       return filename
   if not os.path.exists(os.path.dirname(filename)):
      try:
         os.makedirs(os.path.dirname(filename))
      except OSError as exc:  # Guard against race condition
         logging.error('Error on creating report path')
         if exc.errno != errno.EEXIST:
            raise
   query = "curl -X GET " + url_joiner(base_url, [urllib.quote_plus(link)]) + " > " + filename
   logging.debug('executing download query: ' + query)
   subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
   return filename

def download_report(base_url, dest, t_url):
   strg = download_report_file('', base_url, url_joiner(dest, [t_url + ".html"]))
   html_content = read_file(strg)
   d = {'link': 'href', 'script': 'src', 'a': 'href'}
   soup = BeautifulSoup(html_content, "lxml")
   for key, value in d.iteritems():
      for tag in soup.find_all(key):
         if tag:
            if (tag.name == 'a' and (tag.attrs.get('id') is None or 'stats' not in  tag.attrs.get('id'))):
                continue
            link = tag.attrs.get(value)
            if link:
                logging.info('url for download additional files: ' + link)
                download_report_file(link, base_url, dest)
         else:
             logging.warning('haven\'t find such tag: ' + key)


def read_file(path):
    f = open(path, 'r')
    return f.read()


def write_to_file(path, obj):
    f = open(path, 'w')
    f.write(obj)
    f.close()
    return

def url_joiner(base_url, add_urls):
    if add_urls is None or not add_urls:
        return base_url
    url_builder = base_url
    for url in add_urls:
        if not url:
            continue
        if url_builder[-1] != '/' and url != '/':
            url_builder = url_builder + '/' + url
        else:
            url_builder = url_builder + url
    return url_builder
