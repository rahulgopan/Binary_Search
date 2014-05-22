import commands
import re
import sys
import subprocess
import os
import time
HOME = os.environ['HOME']
def deploy_best_available_CN(BRANCH,BEGINCS,ENDCS) :
                CONFIG_FILE = open('Binary_search.cfg','rU')
                MAC_FILE = open('mac','rU')
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
                                print HIB
                        if "NOISY" in line :
                                match = re.search('(?<=NOISY = )\d',line)
                                noisy = match.group()
                                print noisy
                        if "NOISE_RANGE" in line :
                                match = re.search('(?<=NOISE_RANGE = )\d',line)
                                NOISE_VALUE_BEGIN = match.group()
                                match = re.search('(?<=NOISE_RANGE = \d - )\d+',line)
                                NOISE_VALUE_END = match.group()
                                print "Range is %s - %s" % (NOISE_VALUE_BEGIN,NOISE_VALUE_END)
                        if "RUNLIST" in line :
                                match = re.search('(?<=RUNLIST = )\w+',line)
                                RUNLIST = match.group()
                                print RUNLIST
                        if "TEST" in line :
                                match = re.search('(?<=TEST = )[\w+\W+]+',line)
                                TEST = match.group()
                                TEST = TEST.strip()
                                print TEST
                for line in MAC_FILE :
                        if IP in line :
                                line = line.split()
                                MAC = line[2]
                                print MAC
                                LOCATION = line[5]
                                print LOCATION
                                PXE_DIRECTORY = line[4]
                                print PXE_DIRECTORY
                HOST = "root@%s" % IP

                BUILD_PATH = '/perfauto1/builds/visor/%s/release' % BRANCH
                NOofChanges = commands.getoutput('/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | wc -l' % (BRANCH,BEGINCS,ENDCS))
                print "Total Number of changes in between : %s" %NOofChanges
                CHANGES = commands.getoutput("/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | awk {'print $2'}" % (BRANCH,BEGINCS,ENDCS))
                print CHANGES
                CS = CHANGES.split('\n')
                HalfAChange = int(NOofChanges) / 2
                Mid_Change = CS[int(HalfAChange)]
                print "Probable middle change : %s" %Mid_Change
                status,output = commands.getstatusoutput('ls %s/visor-pxe-%s.tgz' % (BUILD_PATH,Mid_Change))
                i = 1
                j = 1
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
                for i in xrange(int(NOofChanges)) :
                        status,output = commands.getstatusoutput('ls %s/visor-pxe-%s.tgz' % (BUILD_PATH,OrderedChanges[i]))
                        print "Availability of change %s is %s" % (OrderedChanges[i],status)
                        Change_Unavailability = 1
                        if status == 0 and OrderedChanges[i] != BEGINCS and OrderedChanges[i] != ENDCS :
                                Change_Unavailability = 0
                                DEPLOY_CHANGE = OrderedChanges[i]
                                print "Build %s will be deployed" % OrderedChanges[i]
                                os.system('/home/performance/automation/eesx/scripts/deploy-visor-pxe.sh -s %s/visor-pxe-%s.tgz -d %s/%s/ -k -r %s/devel-postboot-sh -v' % (BUILD_PATH,OrderedChanges[i],HOME,PXE_DIRECTORY,HOME))
                                os.system('sudo -u performance ssh pxeuser@suite ./PXEconfig.pl -m %s -p %s/%s/ -l %s' % (MAC,HOME,PXE_DIRECTORY,LOCATION))
                                print "Rebooting the machine"
                                print "System is about to reboot now"
                                reboot = subprocess.call(['ssh',HOST,'reboot'])
                                time.sleep(300)
                                ssh_status = 1
                                while ssh_status > 0 :
                                        ssh_status,output = commands.getstatusoutput("ssh %s 'ls' > deleteme" % HOST)
                                os.system("ssh %s 'cd /vmfs/volumes/datastore1/playground;./%s %s > deleteme;'" % (HOST,PXE_TEST,RUNLIST))
                                status,results = commands.getstatusoutput("scp -r root@%s:/vmfs/volumes/datastore1/playground/benchdata %s/scripts/BS/tmp" % (IP,HOME))
                                print "Done with the testing"
                                print "Results displayed below"
                                if int(res_match.group()) == 1 :
                                        os.system("perl %s/get-scores.pl -i %s/scripts/BS/tmp/benchdata/boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb -n boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb -b -a > %s/scripts/BS/tmp/BStest" % (HOME,HOME,HOME))
                                        status,output = commands.getstatusoutput("cat %s/scripts/BS/tmp/BStest" % HOME)
                                else :
                                        status,output = commands.getstatusoutput("ssh root@%s 'cd /vmfs/volumes/datastore1/playground;grep -i vmqa benchdata/boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb;exit;'" % IP)
                                output = commands.getoutput("cat %s/scripts/BS/tmp/BStest | awk {'print $3'}" % HOME)
                                print output
                                numalone = re.findall(r'\d+\.?\d+', output)
                                print type(numalone)
                                print numalone
                                floatnums = [float(x) for x in numalone]
                                print floatnums
                                floatmean = sum(floatnums) / len(numalone)
                                break
                if Change_Unavailability == 1 :
                        print "None of the above changes are available ..SandBox Request is required"
                        SANDBOX_NECESSITY = 9
                        return ("Provide sandbox request for %s" % OrderedChanges[0],SANDBOX_NECESSITY)
                        sys.exit()

                print floatmean
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
