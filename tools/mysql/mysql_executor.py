import subprocess

from tools.entities.mysql_object import mysql_object


def execute(query_file_name):
    d = mysql_object("root", "root", "localhost", query_file_name)
    write_sql(query_file_name, ('show processlist',))
    execute_query(d)


def execute_query(d):
    query = d.execute()
    print "query: " + query
    s = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    print s.strip()
    print len(s.split("\n"))
    parse_response(s.split("\n"))


def parse_response(response):
    l_m = []
    if len(response) > 1:
        header = response[0].split("\t")
        for i in range(1, len(response), 1):
            m = {}
            row = response[i].split("\t")
            for k in range(0, len(header), 1):
                m[header[k]] = row[k]
            l_m.append(m)
    else:
        print "empty response"
    print l_m


def write_sql(sql_name, queries):
    file_ = open(sql_name, 'w')
    for line in queries:
        file_.write(line)
    file_.close()