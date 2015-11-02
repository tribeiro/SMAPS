import sys,os
import numpy as np
# import pylab as py
from astropy.table import Table
import re

def main(argv):

    path = '/Volumes/TIAGOSD2/Documents/x.py/noWDs'
    mainCatName = 'kuruczSPTypeMatchCatalog.hdf5'
    runCatName = 'unknown.lis.hdf5'

    ulist =  Table.read(os.path.join(path,runCatName),path='list')

    ures = Table.read(os.path.join(path,runCatName),path=ulist['filename'][0])

    sptypes = Table.read(os.path.join(path,mainCatName),path='sptypes')

    truePar = re.search('CK(?P<TEMP>\S+)-g(?P<LOGG>\S+)-(?P<MET>\S+).0000',
                        ulist['filename'][0]).groupdict()

    trueT = np.float(truePar['TEMP'])
    trueL = np.float(truePar['LOGG'])
    trueM = np.float(truePar['MET'])

    # bestPar = re.search('template.CK(?P<TEMP>\S+)-g(?P<LOGG>\S+)-(?P<MET>\S+).0000',
    #                     ures['tempmatch'][0]).groupdict()
    #
    # bestT = np.int(bestPar['TEMP'])
    # bestL = np.float(bestPar['LOGG'])
    # bestM = np.float(bestPar['MET'])
    #
    # print trueT,bestT
    # print trueL,bestL
    # print trueM,bestM

    bestChi2 = ures['chi2'][0]
    worstChi2 = 2*bestChi2
    worstIndex = np.where(ures['chi2'] > worstChi2)[0][1]
    print bestChi2/ures['chi2'][:worstIndex]
    resArr = np.zeros(worstIndex,dtype=[('T',np.float),
                                        ('logg',np.float),
                                        ('mm',np.float)])
    for i in range(worstIndex):
        resPar = re.search('template.CK(?P<TEMP>\S+)-g(?P<LOGG>\S+)-(?P<MET>\S+).0000',
                            ures['tempmatch'][i]).groupdict()
        resArr['T'][i] = np.float(resPar['TEMP'])
        resArr['logg'][i] = np.float(resPar['LOGG'])
        resArr['mm'][i] = np.float(resPar['MET'])

    print 'T:',trueT,np.average(resArr['T'],weights=bestChi2/ures['chi2'][:worstIndex]),np.var(resArr['T'])
    print 'logg:',trueL,np.average(resArr['logg'],weights=bestChi2/ures['chi2'][:worstIndex]),np.var(resArr['logg'])
    print 'mm:',trueM,np.average(resArr['mm'],weights=bestChi2/ures['chi2'][:worstIndex]),np.var(resArr['mm'])

    print resArr

    return 0

if __name__ == '__main__':
    main(sys.argv)
