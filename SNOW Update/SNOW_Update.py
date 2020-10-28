import pysnow
import getpass
from netmiko import ConnectHandler

print("=============================================\n")
print("Program to update service now incident notes\n")
print("=============================================\n")

# class to connect device
class cls_incident:
    #intialising variables
    def __init__(self, uname, passowrd):
        self.uname=uname
        self.password=passowrd
        self.secret=password
        self.dev_type='cisco_ios'
        self.ip=""
        self.output=""
        # creating dictionary for netmiko
        self.dict={
            'device_type':self.dev_type,
            'ip':self.ip,
            'username':self.uname,
            'password':self.password,
            'secret':self.secret,
            'global_delay_factor':1,
            }
    # function to login to device and collect output of command
    def collectdata(self,ipaddress):
        self.dict_device['ip']=ipaddress
        self.net_connect=ConnectHandler(**self.dict_device)
        # opening command file
        cmd_file=open("command.txt")
        self.output=""
        # loop for reading command one by one
        for line in cmd_file:
            cmd=line.lstrip()
            self.output+="\nOutput of Command"+cmd+"\n"
            self.output+=self.net_connect.send_command(cmd)
            cmd_file.close()
            print(self.output)
            print("\nCommand Output Collected")

    # function to update service now
    def inc_update(self, inc_number,s_uname,s_password,s_instance):
        # connecting with service now
        snow=pysnow.Client(instance=s_instance,user=s_uname,password=s_password)
        incident=snow.resource(api_path='/table/incident')
        # payload=self.output
        update={'work_notes':self.output,'state':5}
        # update incident record
        updated_record=incident.update(query={'number':inc_number},payload=update)
        print("Incident note updated")

    def main():
        # collecting service now details
        instance=raw_input("Enter service now instance name in format of 'company.service-now.com':")
        instance=instance.rstrip('.service-now.com')
        s_uname=raw_input("Enter service now username:")
        s_password=getpass.getpass("Password:")
        # collecting device credential
        dev_uname=raw_input("\nEnter Device user name:")
        dev_password=getpass.getpass("Password:")
        objDev=cls_incident(dev_uname,dev_password)

        while True:
            try:
                inc_number=raw_input("Enter incident number:")
                ip_address=raw_input("Enter IP address of device:")
                print("Connecting device and collecting data")
                # creating class object
                objDev.collectdata(ip_address)

                print("Updating service now")
                # updating service now
                objDev.inc_update(inc_number.s_uname,s_password,instance)
                print("\nThis program will keep running, press ctrl+C to exit")
                print("Enter details for next invident \n")
            except:
                print("Error on execution:",e)
                if __name__=="__main__":
                    main()