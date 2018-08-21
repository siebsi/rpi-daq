#Common Inputs
n_ev=None
current_event=None
DuT_name='a very descriptive string'
Type_of_hardware='something in hexagonal shape'
Manufacturer='unknown'
injection_ON=False
acquisitionType='const_inj' #"standard","sweep","fixed","const_inj","instrumental_trigger","external_trigger"
injectionDAC=1
pulse_delay=1
inputch=[]

#Final output
DUT_result='None'
chip_results=['not tested'  for sk in range(4)]

#Tests ON/OFF
RollMask_full_ON=False
ToT_ToA_full_ON=False
SCA_full_ON=False
printUnusualData_ON=False

""" ****** All the following Variables are considered as 'global', meaning they are updated
after each event and take into account the result of all events done so far, NOT the current test output ******"""
chip_array=[0,1,2,3] #chips to check

#variables for SCA test
min=210 #minimum SCA value to pass the test
max=270 #maximum SCA value to pass the test
th_noisy_per_ch=1 #number of sca-values in a single channel (in a single event) to consider if noisy (1-13)
th_broken_per_ch=13 #number of sca-values in a single channel (in a single event) to consider if broken (1-13)
th_n_ev_broken=0.10 #n_current_event*th_n_ev_broken=limit for number of events a channel has to be broken to be considered as broken globally. Overwritten after each event. (percentage (0-1))
th_n_ev_noisy=0.10 #n_current_event*th_n_ev_noisy=limit for number of events a channel has to be noisy to be considered as noisy globally. Overwritten after each event. (percentage (0-1))
broken_ch_list=[[]for sk in chip_array] #list of channels considered broken (globally). Overwritten after each event.
noisy_ch_list=[[]for sk in chip_array] #list of channels considered noisy (globally). Overwritten after each event.
th_noisy_ch_chip=20 #number of channels which have to be noisy to consider the chip as noisy (1-64)
th_broken_ch_chip=1 #number of channels which have to be broken to consider the chip as broken (1-64)
n_noisy_ch_chip=[0 for sk in chip_array] #number of noisy channels per chip (globally). Overwritten after each event.
n_broken_ch_chip=[0 for sk in chip_array] #number of broken channels per chip (globally). Overwritten after each event.
chip_broken=[False for sk in chip_array] #list of results for broken-SCA test. Overwritten after each event.
chip_noisy=[False for sk in chip_array] #list of results for noisy-SCA test. Overwritten after each event.
hexaboard_noisy=False #HB noisy if 1 chip is noisy.
hexaboard_broken=False #HB broken if 1 chip is broken.

#variables for RM test
rollMask_issue=[False for sk in chip_array] #list of results for RollMask test

#variables for ToA/ToT test
th_n_ev_to_issue=0.10 #n_current_event*th_n_ev_to_issue=limit for number of events a channel has to have a TO issue to be considered as having a TO issue globally. Overwritten after each event. (percentage (0-1))
to_issue_ch_list=[[]for sk in chip_array] #list of channels considered to have a TO issue (globally). Overwritten after each event.
th_to_ch_issue_chip=10 #number of channels which have to have a TO issue to consider the chip has a TO issue (1-64)
n_to_issues_chip=[0 for sk in chip_array] #number of channels per chip which have a TO issue (globally). Overwritten after each event.
chip_to_issue=[False for sk in chip_array] #list of results for TO test. Overwritten after each event.
hexaboard_to_issue=False #HB has a TO issue if 1 chip has a TO issue.
