rawfname = 'data/Modulea_very_descriptive_string_2-7-2018_18-33.raw'
rawfname = 'data/Modulea_very_descriptive_string_2-7-2018_18-29.raw'
#rawfname = 'data/Modulea_very_descriptive_string_2-7-2018_18-26.raw'
#rawfname = 'data/Modulea_very_descriptive_string_23-7-2018_12-30.raw'
raw = open(rawfname,'rb')
dataArray=[]

#ch=channel(0-63),roc=readoutchip(0-3), w=word -> (0-12=sca, 13=ToT, 14=ToA)
#event_length=ch*roc*w*2(high+low gain)*16(bits per word)/8(bytes)

'''------------- CHECK DATASIZE --------------'''
import os.path as osp
rawdata_sz = osp.getsize(rawfname) #filesize of raw data file

# Length of the SK2CMS configuration: 96 bit/ROC * 4 ROC/HB * 1/8 byte/bit
conf_sz = 96 *4 //8

# https://cms-docdb.cern.ch/cgi-bin/DocDB/RetrieveFile?docid=12963&filename=SK2a_MemoryMapping_v2a.pdf&version=3
# 16 bit/word * 1924 word/ROC * 4 ROC/HB * 1/8 byte/bit
#1924 = (13+2)*64 +4 =bits per channel * channels + header in front (4 bits)
ev_sz = 16 *1924 *4 // 8    +2    #+2 bytes (injected voltage is added)

evdata_sz = rawdata_sz - conf_sz

remainder = evdata_sz%ev_sz # check if correct lenght readed
if remainder:
    print("BAD: Event data does not match event size boundary by %d bytes"% remainder)



''' ------------- SHOW CONFIG + UNPACK --------------'''
n_ev = 5 #number of events to check
#n_ev=evdata_sz/ev_sz #check full data

''' print configuration'''

import bitarray as ba
conf = ba.bitarray() #full raw-file as bitarray
conf.fromfile(raw, conf_sz) #reads config_bits
print("Configuration string:")
print(conf)


'''unpack data'''
from unpacker import unpacker
up = unpacker() #create upacker object and storage arrays for eventData and rollMask
eventArray=[[[[0 for ev in range(n_ev) ] for sca in range(15)] for ch in range(128)] for sk in range(4)]
rollMaskArray=[[0x0 for ev in range (n_ev)] for sk in range(4)]

for ev in range(n_ev):
    print("Reading event %d"%ev)
    rawdata = raw.read(ev_sz) #read raw data (returns string with 0s and 1s)
    bytedata = bytearray(rawdata) # reads 8 bits and returns byte-value
    up.unpack(bytedata)
    for sk in range(4):
        rollMaskArray[sk][ev] = up.rollMask[sk] #unpack and store rollMask
        for ch in range(128):
            for sca in range(15):
                eventArray[sk][ch][sca][ev] = up.sk2cms_data[sk][ch][sca] #unpack and store eventData
    #up.showData(ev) #only for debugging!
raw.close()

''' ------------- DATA CHECKS --------------'''
from rpi_data_tests import * #look at pri_data_tests.py for details
check = checker(eventArray,n_ev,rollMaskArray)

#check.printUnusualData()#full test
#check.check_full_TOA_TOT(3)#Argument= Threshold for maximum acceptable number of wrong TO - values
#print(rollMaskArray) #print in decimal dataArray
check.printBinaryRollMask()
#check.check_full_sca(200,270)#Arguments=interval for allowed SCA values
#check.check_full_RollMask()
