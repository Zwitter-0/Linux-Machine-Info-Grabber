import os 
import sys
import pwd , grp

# function to copy cpuinfo file to text and then filter the results
def copy_txt():
    # locating to file address cpuinfo
    Processors=os.popen("cat /proc/cpuinfo")
    with open("machine_info.txt",'a') as f:
        f.write("\n\n------- machine Hardware info ---------\n")
        # reading line by line the info file
        for line in Processors.readlines():
            # look for the  words and writting whole file to text file
            if line[:9]=="processor":
                f.write('\n--------------------------------\n')
                f.write(line)
            if line[:9]=="vendor_id":
                f.write(line)
            if line[:5]=="model":
                f.write(line)
            if line[:5]=="cache":
                f.write(line)

# function to access and save system services to our file
def pro():
    # linux system call to access servies popen to execute any terminal command with python
    services=os.popen("systemctl --all")

    with open("machine_info.txt",'a') as f:
        f.write("\n\n------- Services on machine ---------\n") 
        for line in services.readlines():
            if line[0:7]=="LOAD   ":
                break
            f.write(line)


# main function  
def main():
    # command to check if the script is run with sudo privilages or not
    if not os.geteuid() == 0:
        # if not with sudo exit with following message
        sys.exit("\nOnly root can run this script\n")
    # create file 
    with open("machine_info.txt","w") as f1:
        f1.write("------- Machine information -------")

    with open("machine_info.txt","a") as f1:
        # get the machine related info with Uname function of Os module
        hname = os.uname()
        # changing a object type to string type
        hname = str(hname)
        # getting only bracte part and elemenating all other junk data
        lst = (hname[hname.find("(")+1:-1])
        # separate the info in dtring from ,(comma)
        for  ele in lst.strip().split(','):
            ele = ele.replace('\'',' ')
            f1.write("\n{}".format(ele))
        f1.write("\n\n------- Users and groups ---------")
        for p in pwd.getpwall():
            # getting the users and groups information
            f1.write(("\n{} :\n      {}".format(p[0],grp.getgrgid(p[3])[0])))  
    # calling the function 
    pro()
    copy_txt()

# calling main function.......!
if __name__ == '__main__' :
    main()
