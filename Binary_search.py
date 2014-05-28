#!/usr/local/bin/python2.7

import os
import sys
import commands
from array import *
import subprocess
import re
from deploy_module import deploy_best_available_CN
from color import colored
import log
def Sandbox(Change) :
        #/exit14/home/performance/src/automation/bin/sandbox-bld-req -T server -b vmcore-main -n Change -t release -N
        print "Done with sandbox request"

TOTAL_ARGV = len(sys.argv)
interrupt = 0
if TOTAL_ARGV > 3 :
        LASTGOOD = sys.argv[2]
        LASTBAD = sys.argv[3]
        result = deploy_best_available_CN(sys.argv[1],LASTGOOD,LASTBAD)
        while interrupt == 0:
                if result[1] == 9:
                        print "Sandbox function called"
                        Sandbox(result[0])
                        sys.exit()
                elif result[1] == 1:
                        LASTGOOD = result[0]
                        No_of_changes = commands.getoutput('/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | wc -l' % (sys.argv[1],LASTGOOD,LASTBAD))
                        if int(No_of_changes) > 2:
                                result = deploy_best_available_CN(sys.argv[1],LASTGOOD,LASTBAD)
                                print result
                        else:
                                print "Not enough changes in between"
                                log.info('No changes in between the Good %s and Bad number %s' % (LASTGOOD,LASTBAD))
                                print colored('The problem Change-set might be %s','red') % LASTBAD
                                log.info('The problem Change-set might be %s' % LASTBAD)
                                sys.exit()
                else:
                        LASTBAD = result[0]
                        No_of_changes = commands.getoutput('/exit14/home/performance/src/automation/bin/p4range -b %s -B %s -E %s | wc -l' % (sys.argv[1],LASTGOOD,LASTBAD))
                        if int(No_of_changes) > 2:
                                result = deploy_best_available_CN(sys.argv[1],LASTGOOD,LASTBAD)
                                print result
                        else:
                                print "Not enough changes in between"
                                log.info('No changes in between the Good %s and Bad number %s' % (LASTGOOD,LASTBAD))
                                print colored('The problem Change-set might be %s','red') % LASTBAD
                                log.info('The problem Change-set might be %s' % LASTBAD)
                                sys.exit()
else :
        print "Usage : python Binary_Search.py <branch_name> <BeginCS> <EndCS> "
