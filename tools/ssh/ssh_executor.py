import subprocess


def execute_download(d):
    request = d.execute()
    print "request: " + request
    #s = subprocess.Popen(request, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    #print s.strip()