Binary_Search
=============

Python script to automate binary search 

Usage : python Binary_search.py <branch> <Lower_bound> <Upper_bound>
Configuration file : Binary_search.cfg

How to use the script 
=====================

1. Make sure all your entries are correct in configuration file i.e Binary_search.cfg (Go to line number to see the config file entries)
2. Make sure you have the files setup.sh,deploy_module.py in the same location where you have the main script Binary_search.py
3. Run the scrpt like ./Binary_search.py <branch> <Lower_bound> <Upper_bound>

Configuration file : Entries
============================

LIMIT = 42 ### Specify your limit value which will be used by the script to check whether the deployed change is good or bad

HIGHER_IS_BETTER = false ### Entry must be either "true" or "false"

PXEBENCH_SCRIPT = pxebench.sh ### Specify the script used to test the change

RESULT_HowTo = 1 ### Entry must be either 1 or 2. If its 1 then script uses get-scores.pl to get the results and if its 2 then it uses "grep -i vmqa" to get the results

NOISY = 1 ### In case if the test is noisy specify here as 1 else specify as 0

NOISE_RANGE = 8 - 10 ### Specify the noise range here

MACHINE_IP = 10.133.208.15 ### Sepcify the testbed machine IP address

RUNLIST = boothalt ### Specify the runlist that you use to test the change here

TEST = boothalt_rhel6.1server_64_hwexec_swmmu_32vcpu_256gb ### Here you need to specify the test which will be used by the script while getting the result

PXE_DIRECTORY = nehlcurrentCS ### Directory where all your builds will be deployed for pxe booting







