from tools.ssh import ssh_executor
from tools import properties_conf
from tools.entities.base_entity import AmazonEc2Instance
from datetime import date, datetime
import sys, getopt

def main(argv):
   str_date = ''
   str_instance = ''
   try:
      opts, args = getopt.getopt(argv,"hd:i:",["date=","instance="])
   except getopt.GetoptError:
      print 'main.py -d <date(yyyy.mm.dd)> -i <instance>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -d <date(yyyy.mm.dd)> -i <instance>'
         sys.exit()
      elif opt in ("-d", "--date"):
          str_date = arg
      elif opt in ("-i", "--instance"):
         str_instance = arg
   tdate = datetime.strptime(str_date, '%Y.%m.%d')
   instance = AmazonEc2Instance.parse(str_instance)
   scp_connection_data = properties_conf.get_scp_connection_data(instance, tdate)
   print scp_connection_data.execute()
   ssh_executor.execute_download(scp_connection_data);


if __name__ == "__main__":
   main(sys.argv[1:])