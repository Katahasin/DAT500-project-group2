#!/bin/bash
HOSTS="dnode1 dnode2 dnode3 dnode4 dnode5 dnode6"
SCRIPT="sudo pip3 install pandas; sudo pip3 install numpy; sudo pip3 install nltk; sudo pip3 install collections; sudo pip3 install scipy; sudo pip3 install random; sudo pip3 install matplotlib; sudo pip3 install nltk; sudo pip3 install copy;"
for HOSTNAME in ${HOSTS} ; do
    ssh ${HOSTNAME} "${SCRIPT}"
done

