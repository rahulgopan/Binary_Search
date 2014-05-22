import commands
import re
import sys
import subprocess
import os
import time
HOME = os.environ['HOME']
#print "Home directory is %s" % HOME
def deploy_best_available_CN(BRANCH,BEGINCS,ENDCS) :

#       if TOTAL_ARG > 4 :

                #BRANCH = str(sys.argv[1])
                #BEGINCS = str(sys.argv[2])
                #ENDCS = str(sys.argv[3])
                CONFIG_FILE = open('BS.cfg','rU')
                for line in CONFIG_FILE :
                        if "PXEBENCH_SCRIPT" in line :
                                pxe_match = re.search('(?<=PXEBENCH_SCRIPT = )\w+\w+.\w+',line)
                                PXE_TEST = pxe_match.group()
                        if "RESULT_HowTo" in line :
                                res_match = re.search('(?<=RESULT_HowTo = )\d',line)
                        if "MACHINE_IP" in line :
                                ip_match = re.search('(?<=MACHINE_IP = )[\d+\.]+',line)
                                IP = ip_match.group()
                                print "IP is %s" % IP
                        if "LIMIT" in line :
                                match = re.findall(r'\d+\.?\d+',line)
                                floatlimit = [float(x) for x in match]
                        if "HIGHER_IS_BETTER" in line :
                                match = re.search('(?<=HIGHER_IS_BETTER = )\w+',line)
                                HIB = match.group()
                HOST = "root@%s" % IP

                BUILD_PATH = '/perfauto1/builds/visor/%s/release' % BRANCH
                #os.system('/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s' % (BRANCH,BEGINCS,ENDCS))
                NOofChanges = commands.getoutput('/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | wc -l' % (BRANCH,BEGINCS,ENDCS))
                print "Total Number of changes in between : %s" %NOofChanges
                CHANGES = commands.getoutput("/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | awk {'print $2'}" % (BRANCH,BEGINCS,ENDCS))
                print CHANGES
                CS = CHANGES.split('\n')
                HalfAChange = int(NOofChanges) / 2
                #print HalfAChange
                Mid_Change = CS[int(HalfAChange)]
                print "Probable middle change : %s" %Mid_Change
                status,output = commands.getstatusoutput('ls %s/visor-pxe-%s.tgz' % (BUILD_PATH,Mid_Change))
                #print "The status is %d" % status
                i = 1
                j = 1
                '''
                while status != 0 :
                OneAbove = HalfAChange - i
                Mid_Change = CS[int(OneAbove)]
                print Mid_Change
                statusOneAbove,output = commands.getstatusoutput('ls /perfauto1/builds/visor/vmcore-main/release/visor-pxe-%s.tgz' % Mid_Change)
                if statusOneAbove > 0 :
                        i = i + 1
                else :
                        status = 0
                        break
                OneBelow = HalfAChange + j
                Mid_Change = CS[int(OneBelow)]
                print Mid_Change
                statusOneBelow,output = commands.getstatusoutput('ls /perfauto1/builds/visor/vmcore-main/release/visor-pxe-%s.tgz' % Mid_Change)
                if statusOneBelow > 0 :
                        j = j + 1
                else :
                        status = 0
                        break
                '''
                '''
                def reboot_runtest() :
                print "System is about to reboot now"
                os.system("ssh root@IP 'reboot'")
                '''
                OrderedChanges = []
                if HalfAChange == 1 :
                        Append = CS[int(HalfAChange)]
                        OrderedChanges.append(Append)
                        OneAbove = HalfAChange + 1
                        Append = CS[int(OneAbove)]
                        OrderedChanges.append(Append)
                        OneBelow = HalfAChange - 1
                        Append = CS[int(OneBelow)]
                        OrderedChanges.append(Append)

                else :
                        if int(NOofChanges) % 2 == 0 :
                                for i in xrange(int(HalfAChange)) :
                                        j = HalfAChange + i
                                        k =  HalfAChange - (i + 1)
                                        #print j

                                        #OneAbove = HalfAChange + i
                                        Append = CS[int(j)]
                                        #print Append
                                        OrderedChanges.append(Append)
                                        Append = CS[int(k)]
                                        OrderedChanges.append(Append)
                        else :
                                for i in xrange(int(HalfAChange)) :
                                        j = HalfAChange + i
                                        k =  HalfAChange - (i + 1)
                                        Append = CS[int(j)]
                                        OrderedChanges.append(Append)
                                        Append = CS[int(k)]
                                        OrderedChanges.append(Append)
                                last = int(NOofChanges) - 1
                                Append = CS[int(last)]
                                OrderedChanges.append(Append)
                #print OrderedChanges


                for i in xrange(int(NOofChanges)) :
                        status,output = commands.getstatusoutput('ls %s/visor-pxe-%s.tgz' % (BUILD_PATH,OrderedChanges[i]))
                        print "Availability of change %s is %s" % (OrderedChanges[i],status)
                        Change_Unavailability = 1
                        if status == 0 and OrderedChanges[i] != BEGINCS and OrderedChanges[i] != ENDCS :
                                Change_Unavailability = 0
                                DEPLOY_CHANGE = OrderedChanges[i]
                                print "Build %s will be deployed" % OrderedChanges[i]
                                os.system('/home/performance/automation/eesx/scripts/deploy-visor-pxe.sh -s %s/visor-pxe-%s.tgz -d %s/nehlcurrentCS/ -k -r %s/devel-postboot-sh -v' % (BUILD_PATH,OrderedChanges[i],HOME,HOME))
                                os.system('sudo -u performance ssh pxeuser@suite ./PXEconfig.pl -m 90:b1:1c:1f:0e:8c -p %s/nehlcurrentCS/ -l WDC' % HOME)
                                print "Rebooting the machine"
                                #reboot_runtest()
                                print "System is about to reboot now"
                                #os.system("ssh root@%s 'reboot'" % IP)
                                reboot = subprocess.call(['ssh',HOST,'reboot'])
                                time.sleep(300)
                                ssh_status = 1
                                while ssh_status > 0 :
                                        ssh_status,output = commands.getstatusoutput("ssh %s 'ls' > deleteme" % HOST)
                                        #status,output = commands.getstatusoutput("ssh root@IP 'cd /vmfs/volumes/datastore1/playground;./pxebench.sh boothalt;exit;'")
#                               ssh = subprocess.call(['ssh',HOST,'cd /vmfs/volumes/datastore1/playground;./PXE_TEST boothalt > deleteme'])
                                #time.sleep(180)
                                os.system("ssh %s 'cd /vmfs/volumes/datastore1/playground;./%s boothalt > deleteme;'" % (HOST,PXE_TEST))
                              #  print "Running the boothalt test"
                #               print "Status of pxebench script %s" % status
                                status,results = commands.getstatusoutput("scp -r root@%s:/vmfs/volumes/datastore1/playground/benchdata %s/scripts/BS/tmp" % (IP,HOME))
                                print "Done with the testing"
                                print "Results displayed below"
                #               print results
                                if int(res_match.group()) == 1 :
                                        os.system("perl %s/get-scores.pl -i %s/scripts/BS/tmp/benchdata/boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb -n boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb -b -a > %s/scripts/BS/tmp/BStest" % (HOME,HOME,HOME))
                                        status,output = commands.getstatusoutput("cat %s/scripts/BS/tmp/BStest" % HOME)
                                else :
                                        status,output = commands.getstatusoutput("ssh root@%s 'cd /vmfs/volumes/datastore1/playground;grep -i vmqa benchdata/boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb;exit;'" % IP)
                                # status,output = commands.getstatusoutput("cat $HOME/scripts/BS/tmp/BStest")
                                #output = commands.getoutput("echo output | awk {'print $3'}")
                                #output = commands.getoutput("echo %s | awk {'print $3'}" %output)
                                #output = commands.getoutput("echo %s | awk {'print $2'} | cut -d: -f1" %output)
                                output = commands.getoutput("cat %s/scripts/BS/tmp/BStest | awk {'print $3'}" % HOME)
                                #term = output.strip().split('\t')
                                #term1 = str(term).split('|')
                                #print term1
                                print output
                                #numalone = re.findall(r'\d+\.\d\d\d+', output)
                                #numalone = re.findall(r'[0-9]+\.?[0-9]+', output)
                                #if type(output) == float :
                                numalone = re.findall(r'\d+\.?\d+', output)
                                print type(numalone)
                                print numalone
                                floatnums = [float(x) for x in numalone]
                                print floatnums
                                floatmean = sum(floatnums) / len(numalone)
#                              for i in xrange(len(numalone)) :
                                '''
                                else :
                                        numalone = re.findall(r'\d+', output)
                                        print type(numalone)
                                        print numalone
                                        floatnums = [int(x) for x in numalone]
                                        print floatnums
                                        floatmean = sum(floatnums) / len(numalone)
                                break
                                '''
                                break
                if Change_Unavailability == 1 :
                        print "None of the above changes are available ..SandBox Request is required"
                        SANDBOX_NECESSITY = 9
                        return ("Provide sandbox request for %s" % OrderedChanges[0],SANDBOX_NECESSITY)
                        sys.exit()

                print floatmean
                '''
                for line in CONFIG_FILE :
                        if "LIMIT" in line :
                                print "Inside limit if"
                                match = re.findall(r'\d+\.?\d+',line)
                                floatlimit = [float(x) for x in match]
                        if "HIGHER_IS_BETTER" in line :
                                match = re.search('(?<=HIGHER_IS_BETTER =) false',line)
                '''
                print "LIMIT in config file is %s" % floatlimit
                print "Mean of the latest test is %s" % floatmean
                if match :
                        if floatlimit[0] > floatmean :
                                print "Deployed change-set is a good one %s" % DEPLOY_CHANGE
                                GOODNESS = 1
                        else :
                                print "Deployed change-set is a bad one %s" % DEPLOY_CHANGE
                                GOODNESS = 0
                        return (DEPLOY_CHANGE,GOODNESS)
                else :
                        if floatlimit[0] < floatmean :
                                print "Deployed change-set is a good one %s" % DEPLOY_CHANGE
                                GOODNESS = 1
                        else :
                                print "Deployed change-set is a bad one %s" % DEPLOY_CHANGE
                                GOODNESS = 0
                        return (DEPLOY_CHANGE,GOODNESS)
#       else :
 #              print "Usage : python AtryonBS.py <branch_name> <BeginCS> <EndCS> <CONFIG FILE>"
