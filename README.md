# py_bs

this is python bull shit for bullshiting simple shit

it can download cucumber reports and console log from your jenkins builds and also download log from some instance via scp.
F.e. I'm using it for bash which started by cron 4 times in a day

Usage: 

    python main.py [action] [options]  note: will work only for 1 of action

    Actions:
      -s, --syslog - fetch syslog from server(required options are date, instance_type and property file)
      -r, --report - fetch from jenkins cucumber report(required options property file and job name)
      
    Options:
      -j, --job - jenkins job name *required for --report action*
      -d, --date  - date in format year.mount.day *required for --syslog action*
      -i, --instance - instance type of aws ec2 instance *required for --syslog action*. taken from property file
      -p, --pfile - path to property file, *required for --syslog and --report action*
