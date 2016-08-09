class jenkins_data(object):

    def __init__(self, url, username, password, console_log, report_log, cuc_endpoint):
        self.url = url
        self.username = username
        self.password = password
        self.console_log = console_log
        self.report_log = report_log
        self.cuc_endpoint = cuc_endpoint
