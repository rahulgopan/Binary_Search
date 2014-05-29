import commands
import re
import sys
import subprocess
import os
import time
import log
HOME = os.environ['HOME']
PWD = os.environ['PWD']
def deploy_best_available_CN(BRANCH,BEGINCS,ENDCS) :
                log.info('Function \"deploy_best_available_CN\" called with arguments BRANCH=%s,GOOD_CN=%s,BAD_CN=%s' % (BRANCH,BEGINCS,ENDCS))
                CONFIG_FILE = open('Binary_search.cfg','rU')
                MAC_FILE = open('mac','rU')
                log.info('Using Binary_search.cfg file to get neccessary inputs')
                ENTRY = 1
                for line in CONFIG_FILE :
                        if "PXEBENCH_SCRIPT" in line :
                                pxe_match = re.search('(?<=PXEBENCH_SCRIPT = )[\w+\W+]+',line)
                                PXE_TEST = pxe_match.group()
                                PXE_TEST = PXE_TEST.strip()
                                print "PXEBENCH_SCRIPT=%s" % PXE_TEST
                                log.info('PXEBENCH_SCRIPT=%s' % PXE_TEST)
                                PXEBENCH_DIR = os.path.dirname("%s" % PXE_TEST)
                                PXEBENCH_FILE = os.path.basename("%s" % PXE_TEST)
                        if "RESULT_HowTo" in line :
                                res_match = re.search('(?<=RESULT_HowTo = )[\w+\W+]+',line)
                                RESULT_HowTo = res_match.group()
                                RESULT_HowTo = RESULT_HowTo.strip()
                                print "RESULT_HowTo=%s" % RESULT_HowTo
                                log.info('RESULT_HowTo=%s' % RESULT_HowTo)
                        if "MACHINE_IP" in line :
                                ip_match = re.search('(?<=MACHINE_IP = )[\d+\.]+',line)
                                IP = ip_match.group()
                                print "IP is %s" % IP
                                log.info('IP=%s' % IP)
                        if "LIMIT" in line :
                                match = re.findall(r'\d+\.?\d+',line)
                                floatlimit = [float(x) for x in match]
                                print "LIMIT=%s" % floatlimit
                                log.info('LIMIT=%s' % floatlimit)
                        if "HIGHER_IS_BETTER" in line :
                                match = re.search('(?<=HIGHER_IS_BETTER = )\w+',line)
                                HIB = match.group()
                                print "HIGHER_IS_BETTER=%s" % HIB
                                log.info('HIGHER_IS_BETTER=%s' % HIB)
                        if "NOISY" in line :
                                match = re.search('(?<=NOISY = )\d',line)
                                noisy = match.group()
                                print "NOISY=%s" % noisy
                                log.info('NOISY=%s' % noisy)
                        if "NOISE_RANGE" in line :
                                match = re.search('(?<=NOISE_RANGE = )\d',line)
                                NOISE_VALUE_BEGIN = match.group()
                                match = re.search('(?<=NOISE_RANGE = \d - )\d+',line)
                                NOISE_VALUE_END = match.group()
                                print "Range is %s - %s" % (NOISE_VALUE_BEGIN,NOISE_VALUE_END)
                                log.info('Range=%s - %s' % (NOISE_VALUE_BEGIN,NOISE_VALUE_END))
                        if "RUNLIST" in line :
                                match = re.search('(?<=RUNLIST = )[\w+\W+]+',line)
                                RUNLIST = match.group()
                                RUNLIST = RUNLIST.strip()
                                print "RUNLIST=%s" % RUNLIST
                                log.info('RUNLIST=%s' % RUNLIST)
                        if "TEST" in line :
                                match = re.search('(?<=TEST = )[\w+\W+]+',line)
                                TEST = match.group()
                                TEST = TEST.strip()
                                print "TEST=%s" % TEST
                                log.info('TEST=%s' % TEST)
                for line in MAC_FILE :
                        if IP in line :
                                ENTRY = 0
                                line = line.split()
                                MAC = line[0]
                                print "MAC ADDR=%s" % MAC
                                log.info('MAC ADDRESS=%s' % MAC)
                                LOCATION = line[3]
                                print "TESTBED LOCATION=%s" % LOCATION
                                log.info('TESTBED LOCATION=%s' % LOCATION)
                                PXE_DIRECTORY = line[2]
                                print "PXE_DIRECTORY=%s" % PXE_DIRECTORY
                                log.info('PXE_DIRECTORY=%s' % PXE_DIRECTORY)
                if ENTRY !=0 :
                        print "Entries for the given IP from cfg file are not available in mac file. Run mac-setup.py to add new test bed data"
                        sys.exit()
                HOST = "root@%s" % IP

                BUILD_PATH = '/perfauto1/builds/visor/%s/release' % BRANCH
                NOofChanges = commands.getoutput('/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | wc -l' % (BRANCH,BEGINCS,ENDCS))
                print "Total Number of changes in between : %s" %NOofChanges
                log.info('Total number of changes in between %s and %s is %s' % (BEGINCS,ENDCS,NOofChanges))
                CHANGES = commands.getoutput("/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | awk {'print $2'}" % (BRANCH,BEGINCS,ENDCS))
                print CHANGES
                CS = CHANGES.split('\n')
                log.info('Changes are %s' % CS)
                HalfAChange = int(NOofChanges) / 2
                Mid_Change = CS[int(HalfAChange)]
                #print "Probable middle change : %s" %Mid_Change
                log.info('Middle Change=%s' % Mid_Change)
                status,output = commands.getstatusoutput('ls %s/visor-pxe-%s.tgz' % (BUILD_PATH,Mid_Change))
                i = 1
                j = 1
                OrderedChanges = []
                log.info('Ordering Changes')
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
                                        Append = CS[int(j)]
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
                log.info('Checking the availability of changes from the ordered list of changes')
                for i in xrange(int(NOofChanges)) :
                        status,output = commands.getstatusoutput('ls %s/visor-pxe-%s.tgz' % (BUILD_PATH,OrderedChanges[i]))
                        #print "Availability of change %s is %s" % (OrderedChanges[i],status)
                        if status == 0 :
                                print "Change %s is available" % OrderedChanges[i]
                                log.info('Change %s is available' % OrderedChanges[i])
                        else :
                                log.info('Change %s not available' % OrderedChanges[i])
                        #log.info('Availability of change %s is %s' % (OrderedChanges[i],status))
                        Change_Unavailability = 1
                        if status == 0 and OrderedChanges[i] != BEGINCS and OrderedChanges[i] != ENDCS :
                                Change_Unavailability = 0
                                DEPLOY_CHANGE = OrderedChanges[i]
                                print "Deploying build %s" % OrderedChanges[i]
                                log.info('Deploying build %s' % OrderedChanges[i])
                                os.system('/home/performance/automation/eesx/scripts/deploy-visor-pxe.sh -s %s/visor-pxe-%s.tgz -d %s/%s/ -k -r %s/devel-postboot-sh -v' % (BUILD_PATH,OrderedChanges[i],HOME,PXE_DIRECTORY,HOME))
                                os.system('sudo -u performance ssh pxeuser@suite ./PXEconfig.pl -m %s -p %s/%s/ -l %s' % (MAC,HOME,PXE_DIRECTORY,LOCATION))
                                print "Rebooting the machine"
                                print "System is about to reboot now"
                                log.info('Rebooting the Machine')
                                reboot = subprocess.call(['ssh',HOST,'reboot'])
                                time.sleep(300)
                                ssh_status = 1
                                while ssh_status > 0 :
                                        ssh_status,output = commands.getstatusoutput("ssh %s 'ls' > deleteme" % HOST)
                                log.info('Machine is UP with the build %s' % OrderedChanges[i])
                                os.system("ssh %s 'cd %s;./%s %s > deleteme;'" % (HOST,PXEBENCH_DIR,PXEBENCH_FILE,RUNLIST))
                                status,results = commands.getstatusoutput("scp -r root@%s:/vmfs/volumes/datastore1/playground/benchdata %s/tmp" % (IP,PWD))
                                print "Done with the testing"
                                print "Results displayed below"
                                os.system("cd tmp;%s > out;cd .." % (RESULT_HowTo))
                                status,output = commands.getstatusoutput("cat %s/tmp/out" % PWD)
                                output = commands.getoutput("cat %s/tmp/out | awk {'print $3'}" % PWD)
                                print output
                                log.info('Calculating the mean from the results')
                                numalone = re.findall(r'\d+\.?\d+', output)
                                print type(numalone)
                                print numalone
                                floatnums = [float(x) for x in numalone]
                                print floatnums
                                floatmean = sum(floatnums) / len(numalone)
                                break
                if Change_Unavailability == 1 :
                        print "None of the above changes are available ..SandBox Request is required"
                        log.info("No Changes available between %s and %s" % (BEGINCS,ENDCS))
                        SANDBOX_NECESSITY = 9
                        return ("Provide sandbox request for %s" % OrderedChanges[0],SANDBOX_NECESSITY)
                        sys.exit()
                log.info('Comparing the value with the LIMIT')
                print floatmean
                log.info("LIMIT in config file is %s" % floatlimit)
                log.info("Mean value from the obtained results = %s" % floatmean)
                if match :
                        if floatlimit[0] > floatmean :
                                print "Deployed change-set is a good one %s" % DEPLOY_CHANGE
                                log.info('Deployed change-set %s is good' % DEPLOY_CHANGE)
                                GOODNESS = 1
                        else :
                                print "Deployed change-set is a bad one %s" % DEPLOY_CHANGE
                                log.info('Deployed change-set %s is bad' % DEPLOY_CHANGE)
                                GOODNESS = 0
                        return (DEPLOY_CHANGE,GOODNESS)
                else :
                        if floatlimit[0] < floatmean :
                                print "Deployed change-set is a good one %s" % DEPLOY_CHANGE
                                log.info('Deployed change-set %s is good' % DEPLOY_CHANGE)
                                GOODNESS = 1
                        else :
                                print "Deployed change-set is a bad one %s" % DEPLOY_CHANGE
                                log.info('Deployed change-set %s is bad' % DEPLOY_CHANGE)
                                GOODNESS = 0
                        return (DEPLOY_CHANGE,GOODNESS)
