#PBS -S /bin/bash
#PBS -e runmcsim_43.e.log
#PBS -o runmcsim_43.o.log
# execute program 
cd /sto/home/tribeiro/rdata/variability3/
/sto/home/william/local/bin/python2.7 /sto/home/tribeiro/bin/variability/runMCSIM_PP.py 43
