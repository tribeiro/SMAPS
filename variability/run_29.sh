#PBS -S /bin/bash
#PBS -e runmcsim_29.e.log
#PBS -o runmcsim_29.o.log
# execute program 
cd /sto/home/tribeiro/rdata/variability2/
/sto/home/william/local/bin/python2.7 /sto/home/tribeiro/bin/variability/runMCSIM_P.py 29
