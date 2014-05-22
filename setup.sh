#!/bin/bash
limit=`cat BS.cfg | grep LIMIT | sed -n '2p' | awk {'print $3'}`
#echo $limit

machine=`cat BS.cfg | grep MACHINE_IP | awk {'print $3'}`
#echo $machine

mac=`cat /mts/home3/gopakumarr/mac | grep $machine | awk {'print $3'}`
#echo $mac

location=`cat $HOME/mac | grep $machine | awk {'print $5'}`
#echo $location

EXIS_MAC=`cat deploy_module.py | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'`
#echo $EXIS_MAC
sed -i "s/$EXIS_MAC/$mac/g" deploy_module.py
#if [ $? == 0 ];
#then
#       echo "Made Changes"
#fi

EXIS_LOC=`cat deploy_module.py | grep pxeuser@suite | awk {'print $12'} | rev | cut -c 2- | rev`
#echo $EXIS_LOC
sed -i "s/$EXIS_LOC/$location/g" deploy_module.py

runlist=`cat BS.cfg | grep RUNLIST | awk {'print $3'}`
#echo $runlist
EXIS_RUNLIST=`cat deploy_module.py | grep "> deleteme;" | awk {'print $5'}`
sed -i "s+$EXIS_RUNLIST+$runlist+g" deploy_module.py

test=`cat BS.cfg | grep TEST | awk {'print $3'}`
#echo $test

EXIS_TEST=`cat deploy_module.py | grep "ssh root@%s 'cd /vmfs/volumes/datastore1/playground;grep -i vmqa" | awk {'print $9'} | cut -d '/' -f2 | cut -d ';' -f1`
#echo $EXIS_TEST
sed -i "s+$EXIS_TEST+$test+g" deploy_module.py


pxe_dir=`cat BS.cfg | grep PXE_DIRECTORY | awk {'print $3'}`

EXIS_PXE_DIR=`cat deploy_module.py | grep "/home/performance/automation/eesx/scripts/deploy-visor-pxe.sh" | awk {'print $5'} | cut -d '/' -f2`

sed -i "s/$EXIS_PXE_DIR/$pxe_dir/g" deploy_module.py



echo "Setup.sh Succeeded"
