#Class for online and offline rpi data tests

#for the rollmask you're testing hexaboards, if at least one rollmask doesn't work the test should fail
#if you want to know the event and the skyrock involved in the mistake, you can read the data.
#this only indicates if at least one rollmask is wrong

import common_variables
import unpacker
set_rm={3,6,12,24,48,96,192,384,768,1536,3072,6144,4097} #all possible values for rollMask
class checker():
    data_array=[]
    rollMask=[]
    curr_ev=0

    def __init__(self,da,rm):
        self.data_array=da #Style: [[0 for sca in range(15)] for ch in range(64)] for sk in range(4)]
        self.rollMask=rm #Style: =[0x0000 for sk in range(4)]
        self.curr_ev=common_variables.current_event

    def printUnusualData(self):
        print('*********** Unusual-Data *************')
        for sk in common_variables.chip_array:
            print("Event = "+str(self.curr_ev)+"\t Chip = "+str(sk)+"\t RollMask = "+str(hex(self.rollMask[sk])))
            self.check_RollMask(sk)
            for ch in range(64):
                stream="channelID = "+str(63-ch%64)+"   "
                for sca in range(9):
                    if (self.check_sca_noisy(sk,ch,sca,stream)): #print data not in sca interval
                        break
                    elif(self.check_TOA_TOT(sk,ch,stream)):#check if TOA and TOT are at 4
                        break  #jump to next channel
                for sca in range(13):
                    if self.check_sca_broken(sk,ch,sca,stream):
                        break

    ####--------- FOR ALL TESTS: SCA=SwitchCapacitorArray (0-14), SK=SkiROC (0-3), ch=Channel(0-127), i=Event number----------#####
    #for use in printUnusualData only
    def check_RollMask(self,sk):#checks rollMask for unexpected values
        if (self.rollMask[sk] not in set_rm):
            print('Rollmask Issue : impossible value (not 10..01, not 0..11..0, not 110..0, not 0..011)')

    #for use in printUnusualData only
    def check_sca_noisy(self,sk,ch,sca,stream):#checks sca and prints unusual values not in [min-sca, max-sca}
        tmp_stream=stream
        (outside_min_and_max)=((self.data_array[sk][ch][sca] < common_variables.min) or (self.data_array[sk][ch][sca] > common_variables.max))
        if (outside_min_and_max):
            for sca1 in range (15): #print whole channel, if just one value is wrong
                tmp_stream+=" "+str(self.data_array[sk][ch][sca1])
            print(tmp_stream+' (noisy)')
        return outside_min_and_max
        ######hier weiter, erkennt manhcmal nicht richtig

    def check_sca_broken(self,sk,ch,sca,stream):#checks sca and prints unusual values not in [min-sca, max-sca}
        tmp_stream=stream
        (outside_min_and_max)=((self.data_array[sk][ch][sca] < common_variables.min) or (self.data_array[sk][ch][sca] > common_variables.max))
        zero_or_four=(self.data_array[sk][ch][sca]==0)or(self.data_array[sk][ch][sca]==4)
        if zero_or_four:
            for sca1 in range (15): #print whole channel, if just one value is wrong
                tmp_stream+=" "+str(self.data_array[sk][ch][sca1])
            print(tmp_stream+' (broken)')
        return zero_or_four

    #for use in printUnusualData only
    def check_TOA_TOT(self,sk,ch,stream):#checks TOA TOT and print unusual values
        tmp_stream=stream
        if(common_variables.injection_ON):
            ch1=common_variables.inputch[0]
            At_least_one_TO_smaller_4=(self.data_array[sk][ch1][13]<=4) or (self.data_array[sk][ch1][14]<=4)
            if (At_least_one_TO_smaller_4):
                for sca1 in range (15): #print whole channel, if just one value is wrong
                    tmp_stream+=" "+str(self.data_array[sk][ch1][sca1])
                print(tmp_stream+'ToA or ToT wrong')
            return At_least_one_TO_smaller_4
        else:
            At_least_one_TO_not_4=(self.data_array[sk][ch][13]!=4) or (self.data_array[sk][ch][14]!=4)
            if (At_least_one_TO_not_4):
                for sca1 in range (15): #print whole channel, if just one value is wrong
                    tmp_stream+=" "+str(self.data_array[sk][ch][sca1])
                print(tmp_stream+' ToA or ToT wrong')
            return At_least_one_TO_not_4

######-----The following functions work independently and perform tested ONE event------#######

    def check_full_RollMask(self):
        print('*********** RollMask-TEST *************')
        rollMask_issue=[False for sk in common_variables.chip_array]
        for sk in common_variables.chip_array:
            print("Event = "+str(self.curr_ev)+"\t Chip = "+str(sk)+"\t RollMask = "+ str(hex(self.rollMask[sk])))
            if (self.rollMask[sk]not in set_rm):
                rollMask_issue[sk]=True #One rollMask wrong = full hexaboard not useful
                print('Rollmask Issue : impossible value (not 10..01, not 0..11..0, not 110..0, not 0..011)')
        return rollMask_issue

    def check_full_sca(self,chip_array=[0,1,2,3]):
        print('*********** SCA-TEST *************')
        noisy_ch_counter=0
        noisy_channels=[None for sk in chip_array]
        broken_ch_counter=0
        broken_channels=[None for sk in chip_array]
        for sk in chip_array:
            print("Event = "+str(self.curr_ev)+"\t Chip = "+str(sk)+"\t RollMask = "+ str(hex(self.rollMask[sk])))
            ch_list_1=[]
            ch_list_2=[]
            for ch in range(64):#only slow ramp tested
                ADC_saturated_counter=0 #counter for 13 SCAs per ch
                noisy_sca_counter=0
                for sca in range(13):
                    if((self.data_array[sk][ch][sca]==0)or(self.data_array[sk][ch][sca]==4)):
                        ADC_saturated_counter+=1
                    if(ADC_saturated_counter>=common_variables.th_broken_per_ch): #all 13 ch need to be broken so that the whole channel is broken
                        broken_ch_counter+=1
                        ch_list_1.append(63-ch)
                    if (sca<9): #test only first 9 sca for noise
                        not_in_min_max=((self.data_array[sk][ch][sca] < common_variables.min) or (self.data_array[sk][ch][sca] > common_variables.max))
                        if (not_in_min_max):
                            noisy_sca_counter+=1
                if noisy_sca_counter >=common_variables.th_noisy_per_ch:
                    noisy_ch_counter+=1
                    ch_list_2.append(63-ch)
            print('broken channels:' + str(ch_list_1))
            print('noisy channels:' + str(ch_list_2))
            noisy_channels[sk]=ch_list_2
            broken_channels[sk]=ch_list_1
        return(noisy_ch_counter,noisy_channels,broken_ch_counter,broken_channels)

    def check_full_TOA_TOT(self):
        print('*********** ToA/ToT-TEST *************')
        wrong_To_list=[[] for sk in common_variables.chip_array]
        if(common_variables.injection_ON):
            for sk in common_variables.chip_array:
                print("Event = "+str(self.curr_ev)+"\t Chip = "+str(sk)+"\t RollMask = "+ str(hex(self.rollMask[sk])))
                ch=common_variables.inputch[0]
                if((self.data_array[sk][ch][13]<=4) or (self.data_array[sk][ch][14]<=4)):
                    wrong_To_list[sk].append(63-ch)
            print('channels with ToA or ToT <=4: \n', wrong_To_list)
            return (None,wrong_To_list)
        else:
            less_counts_than_threshold=[True for sk in common_variables.chip_array]
            for sk in common_variables.chip_array:
                print("Event = "+str(self.curr_ev)+"\t Chip = "+str(sk)+"\t RollMask = "+ str(hex(self.rollMask[sk])))
                Unexpected_TO_counter=0#reset of unexpected_TO_counter for the next skiroc
                for ch in range(64):
                    if((self.data_array[sk][ch][13]!=4) or (self.data_array[sk][ch][14]!=4)):
                        Unexpected_TO_counter+=1
                        wrong_To_list[sk].append(63-ch)
                    if(Unexpected_TO_counter>=1):
                        less_counts_than_threshold[sk]=False
            print('channels with ToA or ToT not 4:', wrong_To_list)
            return (less_counts_than_threshold,wrong_To_list)

    def printBinaryRollMask(self): #just for debugging
        numrows = len(self.rollMask)
        numcols = len(self.rollMask[0])
        for i in range(numrows):
            stream = 'RollMask Chip'+str(i)+': '
            for j in range(numcols):
                stream=stream+str(bin(self.rollMask[i][j]))+' '
            print(stream)
