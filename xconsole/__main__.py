import sys
import commands
import pexpect
import ttyUSBID
import os
def find_in( s, first, last):
    try:
        start = s.index( first ) + len( first ) 
        if last =="":
            end = len(s)
        else:
            end = s.index( last, start ) 
        return s[start:end]
    except ValueError:
        return ""
def ssh_tty(host="",hostpass="",hostprom="~",ttyUSB="",force=False,log="",speed=115200,timeout=1*60):
    if ttyUSB == "" or host == "" or hostpass == "":
        return None,1
    if ttyUSB.find("tty") == -1:
        tty_serials,tty_dmesgs = ttyUSBID.get_ttydata_ssh(host,hostpass)
        ttyUSB = ttyUSBID.id2tty(tty_serials,ttyUSB)
    tty = pexpect.spawn ("ssh -o 'StrictHostKeyChecking no' %s" %(host) ,timeout=300000)
    #tty.logfile_read = sys.stdout
    if log != "":
        tty.logfile_read = open(log, 'a+')
    if tty.expect(["password",pexpect.EOF,pexpect.TIMEOUT],timeout=timeout) != 0:
        return None,2
    tty.sendline(hostpass)
    if tty.expect([hostprom,pexpect.EOF,pexpect.TIMEOUT],timeout=timeout) != 0:
        return None,3
    if force:
        tty.sendline("sudo fuser -k /dev/%s" %(ttyUSB))
    else :
        tty.sendline("sudo echo %s" %(ttyUSB))
    if tty.expect(["password",pexpect.EOF,pexpect.TIMEOUT],timeout=timeout) != 0:
        return None,4
    tty.sendline(hostpass)
    if tty.expect([hostprom,pexpect.EOF,pexpect.TIMEOUT],timeout=timeout) != 0:
        return None,5
    tty.sendline("sudo echo set line /dev/%s          > ./.kermit_%s" %(ttyUSB,ttyUSB))
    tty.sendline("sudo echo set speed %d             >> ./.kermit_%s" %(speed,ttyUSB))   
    tty.sendline("sudo echo set carrier-watch off    >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set handshake none       >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set flow-control none    >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo robust                   >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set file type bin        >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set file name lit        >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set rec pack 1000        >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set send pack 1000       >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo echo set window 5             >> ./.kermit_%s" %(ttyUSB))     
    tty.sendline("sudo kermit -c -y ./.kermit_%s;exit" %(ttyUSB))
    re = tty.expect(["--------","Locked by process",pexpect.EOF,pexpect.TIMEOUT],timeout=timeout)
    if re == 1:
        print "Locked by process"
    return tty,re
def local_tty(ttyUSB="",force=False,log="",speed=115200,timeout=1*60):
    if ttyUSB == "" :
        return None,1
    if ttyUSB.find("tty") == -1:
        tty_serials,tty_dmesgs = ttyUSBID.get_ttydata()
        ttyUSB = ttyUSBID.id2tty(tty_serials,ttyUSB)
    os.system("echo set line /dev/%s          > ./.kermit_%s" %(ttyUSB,ttyUSB))
    os.system("echo set speed %d             >> ./.kermit_%s" %(speed,ttyUSB))   
    os.system("echo set carrier-watch off    >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set handshake none       >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set flow-control none    >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo robust                   >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set file type bin        >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set file name lit        >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set rec pack 1000        >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set send pack 1000       >> ./.kermit_%s" %(ttyUSB))     
    os.system("echo set window 5             >> ./.kermit_%s" %(ttyUSB))
    if force:
        os.system("sudo fuser -k /dev/%s" %(ttyUSB))
    tty = pexpect.spawn ("kermit -c -y ./.kermit_%s" %(ttyUSB) ,timeout=300000)
    if log != "":
        tty.logfile_read = open(log, 'a+')
    re=tty.expect(["--------","Locked by process",pexpect.EOF,pexpect.TIMEOUT],timeout=timeout)
    if re == 1 :
        print tty.before
    return tty,re
def sol_tty(bmcip="",sol="",log=""):
    if bmcip == "" or sol == "":
        return None,1
    os.system("ipmitool -H%s -UADMIN -PADMIN -Ilanplus sol deactivate instance=%s" %(bmcip,sol))
    tty = pexpect.spawn ("ipmitool -H%s -UADMIN -PADMIN -Ilanplus sol activate instance=%s" %(bmcip,sol),timeout=300000)
    if log != "":
        tty.logfile_read = open(log, 'a+')
    return tty,0
def tty(bmcip="",sol="",host="",hostpass="",hostprom="~",ttyUSB="",force=False,log="",speed=115200,timeout=20):
    tty = None
    if tty == None and host != "":
        tty = ssh_tty(host=host,hostpass=hostpass,hostprom=hostprom,ttyUSB=ttyUSB,force=force,log=log)
    if tty == None and host == "" and ttyUSB != "":
        tty = local_tty(ttyUSB=ttyUSB,force=force,log=log)
    if tty == None and host == "" and ttyUSB == "" and bmcip != "": 
        tty = sol_tty(bmcip=bmcip,sol=sol)
    return tty
if __name__ == "__main__":
    bmcip = ""
    ttyUSB = ""
    log = ""
    host = ""
    hostpass = ""
    sol=""
    tty = None
    if len(sys.argv) >= 2 :
        if sys.argv[1].find("@") != -1:
            host = sys.argv[1]
            if len(sys.argv) >  4:
                log = sys.argv[4]
            if len(sys.argv) > 2:
                hostpass = sys.argv[2]
            if len(sys.argv) >  3:
                ttyUSB = sys.argv[3]
                tty,err = ssh_tty(host=host,hostpass=hostpass,ttyUSB=ttyUSB,log=log)
        elif sys.argv[1].count(".") == 3:
            bmcip = sys.argv[1]
            if len(sys.argv) > 3:
                log = sys.argv[3]
            if len(sys.argv) > 2:
                sol = sys.argv[2]
                tty,err = sol_tty(bmcip=bmcip,sol=sol,log=log)
        elif sys.argv[1].find("tty") != -1 or len(sys.argv[1]) == 8:
            ttyUSB = sys.argv[1]
            if len(sys.argv) > 2:
                log = sys.argv[2]
            tty,err = local_tty(ttyUSB=ttyUSB,log=log)
    if tty == None:
        print "Help"
    else:
        tty.interact()
        sys.exit()