class unpacker:
    compressedRawData=True
    sk2cms_data=[]
    rollMask=[0x0,0x0,0x0,0x0]

    def __init__(self,compressedRawData=True):
        self.compressedRawData=compressedRawData
        self.sk2cms_data=[[[0 for sca in range(15)] for ch in range(128)] for sk in range(4)]

    def grayToBinary(self,gray):
        binary = gray & (1 << 11)
        binary |= (gray ^ (binary >> 1)) & (1 << 10)
        binary |= (gray ^ (binary >> 1)) & (1 << 9)
        binary |= (gray ^ (binary >> 1)) & (1 << 8)
        binary |= (gray ^ (binary >> 1)) & (1 << 7)
        binary |= (gray ^ (binary >> 1)) & (1 << 6)
        binary |= (gray ^ (binary >> 1)) & (1 << 5)
        binary |= (gray ^ (binary >> 1)) & (1 << 4)
        binary |= (gray ^ (binary >> 1)) & (1 << 3)
        binary |= (gray ^ (binary >> 1)) & (1 << 2)
        binary |= (gray ^ (binary >> 1)) & (1 << 1)
        binary |= (gray ^ (binary >> 1)) & (1 << 0)
        return binary;

    def unpack(self,rawdata): #decode raw data :
        ev=[ [0 for i in range(1924)] for sk in range(4) ]
        if self.compressedRawData==False:
            for i in range(1924):
                for j in range(16):
                    x = rawdata[i*16 + j]
                    x = x&0xf
                    for sk in range(4):
                        ev[sk][i] = ev[sk][i] | (((x >> (3-sk) ) & 1) << (15 - j))

        else:
            for i in range(1924):
                for j in range(8):
                    x = rawdata[i*8 + j]
                    y = (x >> 4) & 0xf
                    x = x & 0xf
                    for sk in range(4):
                        ev[sk][i] = ev[sk][i] | (((x >> (3 - sk) ) & 1) << (14 - j*2))
                        ev[sk][i] = ev[sk][i] | (((y >> (3 - sk) ) & 1) << (15 - j*2))

        for sk in range(4):
            for i in range(128*15):
                ev[sk][i] = self.grayToBinary(ev[sk][i] & 0x0FFF)
            self.rollMask[sk]=ev[sk][1920]
        self.sk2cms_data=[[[0 for sca in range(15)] for ch in range(128)] for sk in range(4)]
        for sk in range(4):
            firstBit=self.getFirstBitFromRollMask(sk)
            for ch in range(128):
                for sca in range(0,15):
                    self.sk2cms_data[sk][ch][sca] = ev[sk][sca*128+ch]
                self.sk2cms_data[sk][ch][::]=self.sk2cms_data[sk][ch][::-1]#reverses sca array
                tmpArray=self.sk2cms_data[sk][ch][::]
                self.sk2cms_data[sk][ch][13]=tmpArray[1]#move TOA and TOT back to the end
                self.sk2cms_data[sk][ch][14]=tmpArray[0]
                for i in range(13):#arrange sca in time
                    if (firstBit+i+2)<15:
                        self.sk2cms_data[sk][ch][i]=tmpArray[firstBit+i+2]
                    else:
                        self.sk2cms_data[sk][ch][i]=tmpArray[firstBit+i+2-13]
        #self.sk2cms_data[3][127][14]=5 #for debugging the TOA TOT tests
        '''for sk in range(4): #testing...
            for ch in range(128):
                for sca in range(13):
                    self.sk2cms_data[sk][ch][sca]=250
        for sk in range(4):
            for ch in range(128):
                for sca in range(14,15):
                    self.sk2cms_data[sk][ch][sca]=4
        for sk in range(4):
            for ch in range(128):
                for sca in range(5,6):
                    self.sk2cms_data[sk][ch][sca]=400'''

    def showData(self,eventID): #use only for debugging, prints FULL data!
        for sk in range(4):
            print("Event = "+str(eventID)+"\t Chip = "+str(sk)+"\t RollMask = "+hex(self.rollMask[sk]))
            for ch in range(64):
                stream="channelID = "+str(63-ch%64)+"   "
                for sca in range(15):
                    stream=stream+" "+str(self.sk2cms_data[sk][ch][sca])
                print(stream)

    def getFirstBitFromRollMask(self,sk):
        l=0
        if self.rollMask[sk]==4097:
            l=1
        elif self.rollMask[sk]==6144:
            l=2
        elif self.rollMask[sk]==3072:
            l=3
        elif self.rollMask[sk]==1536:
            l=4
        elif self.rollMask[sk]==768:
            l=5
        elif self.rollMask[sk]==384:
            l=6
        elif self.rollMask[sk]==192:
            l=7
        elif self.rollMask[sk]==96:
            l=8
        elif self.rollMask[sk]==48:
            l=9
        elif self.rollMask[sk]==24:
            l=10
        elif self.rollMask[sk]==12:
            l=11
        elif self.rollMask[sk]==6:
            l=12
        return l
