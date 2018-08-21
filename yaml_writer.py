import yaml, sys
import ruamel.yaml#library for writing yaml logfile
from ruamel.yaml.util import load_yaml_guess_indent#library for writing yaml logfile
from time import gmtime, strftime#library for the timestamp of yaml logfile
import common_variables

class yaml_data:
    yaml_opt=yaml.YAMLObject()

    def __init__(self,fname="data_form.yaml"):
        Default_data = dict(
            DUT = dict(                           #for one DUT you have all events and chip number to pass (->dictionary)
                Timestamp = 'Put date and hour here', #for each timestamp there'll be one DUT (->not a dictionary)
                DUT_ID = 'Put dut ID here',
                Type_of_hardware = 'Put Hardware type here',
                Manufacturer = 'Manufacturer',
                DUT_result = 'Put DUT result here (PASS or FAIL or NOISY)',
                Number_of_events = 'Put number of events here',
                Noisy_flag = 'Put noisy flag here',
                Broken_flag = 'Put broken flag here',
                ToA_ToT_Issue_flag = 'Put ToA/ToT Issue flag here',
                Done_tests= dict(
                    Rollmask_ON='If RM test is selected',
                    SCA_ON='If SCA test is selected',
                    ToA_ToT_ON='If ToA/ToT test is selected',
                    ),
                Chip0 = dict(
                    Rm_Issue = 'Put rm issues here',
                    Result = 'Put result here (PASS or FAIL or PASS -NOISY or PASS -NOISY -TO ISSUE or PASS -TO ISSUE)',
                    SCA=dict(
                        th_noisy_per_ch='common_variables.th_noisy_per_ch', #number of sca-values in a single channel (in a single event) to consider if noisy (1-13)
                        th_broken_per_ch='common_variables.th_broken_per_ch', #number of sca-values in a single channel (in a single event) to consider if broken (1-13)
                        th_n_ev_broken='common_variables.th_n_ev_broken', #n_current_event*th_n_ev_broken=limit for number of events a channel has to be broken to be considered as broken globally. Overwritten after each event. (percentage (0-1))
                        th_n_ev_noisy='common_variables.th_n_ev_noisy', #n_current_event*th_n_ev_noisy=limit for number of events a channel has to be noisy to be considered as noisy globally. Overwritten after each event. (percentage (0-1))
                        broken_ch_list='common_variables.broken_ch_list', #list of channels considered broken (globally). Overwritten after each event.
                        noisy_ch_list ='common_variables.noisy_ch_list', #list of channels considered noisy (globally). Overwritten after each event.
                        th_noisy_ch_chip='common_variables.th_noisy_ch_chip', #number of channels which have to be noisy to consider the chip as noisy (1-64)
                        th_broken_ch_chip ='common_variables.th_broken_ch_chip', #number of channels which have to be broken to consider the chip as broken (1-64)
                        n_noisy_ch_chip='common_variables.n_noisy_ch_chip', #number of noisy channels per chip (globally). Overwritten after each event.
                        n_broken_ch_chip ='common_variables.n_broken_ch_chip', #number of broken channels per chip (globally). Overwritten after each event.
                        chip_broken='common_variables.chip_broken', #list of results for broken-SCA test. Overwritten after each event.
                        chip_noisy='common_variables.chip_noisy',#list of results for noisy-SCA test. Overwritten after each event.
                        ),
                    ToA_ToT=dict(
                        th_n_ev_to_issue='common_variables.th_n_ev_to_issue',#n_current_event*th_n_ev_to_issue=limit for number of events a channel has to have a TO issue to be considered as having a TO issue globally. Overwritten after each event. (percentage (0-1))
                        to_issue_ch_list='common_variables.to_issue_ch_list',#list of channels considered to have a TO issue (globally). Overwritten after each event.
                        th_to_ch_issue_chip='common_variables.th_to_ch_issue_chip', #number of channels which have to have a TO issue to consider the chip has a TO issue (1-64)
                        n_to_issues_chip='common_variables.n_to_issues_chip',#number of channels per chip which have a TO issue (globally). Overwritten after each event.
                        chip_to_issue='common_variables.chip_to_issue',#list of results for TO test. Overwritten after each event.
                        ),
                    ),
                Chip1 = dict(
                    Rm_Issue = 'Put rm issues here',
                    Result = 'Put result here (PASS or FAIL or PASS -NOISY or PASS -NOISY -TO ISSUE or PASS -TO ISSUE)',
                    SCA=dict(
                        th_noisy_per_ch='common_variables.th_noisy_per_ch', #number of sca-values in a single channel (in a single event) to consider if noisy (1-13)
                        th_broken_per_ch='common_variables.th_broken_per_ch', #number of sca-values in a single channel (in a single event) to consider if broken (1-13)
                        th_n_ev_broken='common_variables.th_n_ev_broken', #n_current_event*th_n_ev_broken=limit for number of events a channel has to be broken to be considered as broken globally. Overwritten after each event. (percentage (0-1))
                        th_n_ev_noisy='common_variables.th_n_ev_noisy', #n_current_event*th_n_ev_noisy=limit for number of events a channel has to be noisy to be considered as noisy globally. Overwritten after each event. (percentage (0-1))
                        broken_ch_list='common_variables.broken_ch_list', #list of channels considered broken (globally). Overwritten after each event.
                        noisy_ch_list ='common_variables.noisy_ch_list', #list of channels considered noisy (globally). Overwritten after each event.
                        th_noisy_ch_chip='common_variables.th_noisy_ch_chip', #number of channels which have to be noisy to consider the chip as noisy (1-64)
                        th_broken_ch_chip ='common_variables.th_broken_ch_chip', #number of channels which have to be broken to consider the chip as broken (1-64)
                        n_noisy_ch_chip='common_variables.n_noisy_ch_chip', #number of noisy channels per chip (globally). Overwritten after each event.
                        n_broken_ch_chip ='common_variables.n_broken_ch_chip', #number of broken channels per chip (globally). Overwritten after each event.
                        chip_broken='common_variables.chip_broken', #list of results for broken-SCA test. Overwritten after each event.
                        chip_noisy='common_variables.chip_noisy',#list of results for noisy-SCA test. Overwritten after each event.
                        ),
                    ToA_ToT=dict(
                        th_n_ev_to_issue='common_variables.th_n_ev_to_issue',#n_current_event*th_n_ev_to_issue=limit for number of events a channel has to have a TO issue to be considered as having a TO issue globally. Overwritten after each event. (percentage (0-1))
                        to_issue_ch_list='common_variables.to_issue_ch_list',#list of channels considered to have a TO issue (globally). Overwritten after each event.
                        th_to_ch_issue_chip='common_variables.th_to_ch_issue_chip', #number of channels which have to have a TO issue to consider the chip has a TO issue (1-64)
                        n_to_issues_chip='common_variables.n_to_issues_chip',#number of channels per chip which have a TO issue (globally). Overwritten after each event.
                        chip_to_issue='common_variables.chip_to_issue',#list of results for TO test. Overwritten after each event.
                        ),
                ),
                Chip2 = dict(
                    Rm_Issue = 'Put rm issues here',
                    Result = 'Put result here (PASS or FAIL or PASS -NOISY or PASS -NOISY -TO ISSUE or PASS -TO ISSUE)',
                    SCA=dict(
                        th_noisy_per_ch='common_variables.th_noisy_per_ch', #number of sca-values in a single channel (in a single event) to consider if noisy (1-13)
                        th_broken_per_ch='common_variables.th_broken_per_ch', #number of sca-values in a single channel (in a single event) to consider if broken (1-13)
                        th_n_ev_broken='common_variables.th_n_ev_broken', #n_current_event*th_n_ev_broken=limit for number of events a channel has to be broken to be considered as broken globally. Overwritten after each event. (percentage (0-1))
                        th_n_ev_noisy='common_variables.th_n_ev_noisy', #n_current_event*th_n_ev_noisy=limit for number of events a channel has to be noisy to be considered as noisy globally. Overwritten after each event. (percentage (0-1))
                        broken_ch_list='common_variables.broken_ch_list', #list of channels considered broken (globally). Overwritten after each event.
                        noisy_ch_list ='common_variables.noisy_ch_list', #list of channels considered noisy (globally). Overwritten after each event.
                        th_noisy_ch_chip='common_variables.th_noisy_ch_chip', #number of channels which have to be noisy to consider the chip as noisy (1-64)
                        th_broken_ch_chip ='common_variables.th_broken_ch_chip', #number of channels which have to be broken to consider the chip as broken (1-64)
                        n_noisy_ch_chip='common_variables.n_noisy_ch_chip', #number of noisy channels per chip (globally). Overwritten after each event.
                        n_broken_ch_chip ='common_variables.n_broken_ch_chip', #number of broken channels per chip (globally). Overwritten after each event.
                        chip_broken='common_variables.chip_broken', #list of results for broken-SCA test. Overwritten after each event.
                        chip_noisy='common_variables.chip_noisy',#list of results for noisy-SCA test. Overwritten after each event.
                        ),
                    ToA_ToT=dict(
                        th_n_ev_to_issue='common_variables.th_n_ev_to_issue',#n_current_event*th_n_ev_to_issue=limit for number of events a channel has to have a TO issue to be considered as having a TO issue globally. Overwritten after each event. (percentage (0-1))
                        to_issue_ch_list='common_variables.to_issue_ch_list',#list of channels considered to have a TO issue (globally). Overwritten after each event.
                        th_to_ch_issue_chip='common_variables.th_to_ch_issue_chip', #number of channels which have to have a TO issue to consider the chip has a TO issue (1-64)
                        n_to_issues_chip='common_variables.n_to_issues_chip',#number of channels per chip which have a TO issue (globally). Overwritten after each event.
                        chip_to_issue='common_variables.chip_to_issue',#list of results for TO test. Overwritten after each event.
                        ),
                ),
                Chip3 = dict(
                    Rm_Issue = 'Put rm issues here',
                    Result = 'Put result here (PASS or FAIL or PASS -NOISY or PASS -NOISY -TO ISSUE or PASS -TO ISSUE)',
                    SCA=dict(
                        th_noisy_per_ch='common_variables.th_noisy_per_ch', #number of sca-values in a single channel (in a single event) to consider if noisy (1-13)
                        th_broken_per_ch='common_variables.th_broken_per_ch', #number of sca-values in a single channel (in a single event) to consider if broken (1-13)
                        th_n_ev_broken='common_variables.th_n_ev_broken', #n_current_event*th_n_ev_broken=limit for number of events a channel has to be broken to be considered as broken globally. Overwritten after each event. (percentage (0-1))
                        th_n_ev_noisy='common_variables.th_n_ev_noisy', #n_current_event*th_n_ev_noisy=limit for number of events a channel has to be noisy to be considered as noisy globally. Overwritten after each event. (percentage (0-1))
                        broken_ch_list='common_variables.broken_ch_list', #list of channels considered broken (globally). Overwritten after each event.
                        noisy_ch_list ='common_variables.noisy_ch_list', #list of channels considered noisy (globally). Overwritten after each event.
                        th_noisy_ch_chip='common_variables.th_noisy_ch_chip', #number of channels which have to be noisy to consider the chip as noisy (1-64)
                        th_broken_ch_chip ='common_variables.th_broken_ch_chip', #number of channels which have to be broken to consider the chip as broken (1-64)
                        n_noisy_ch_chip='common_variables.n_noisy_ch_chip', #number of noisy channels per chip (globally). Overwritten after each event.
                        n_broken_ch_chip ='common_variables.n_broken_ch_chip', #number of broken channels per chip (globally). Overwritten after each event.
                        chip_broken='common_variables.chip_broken', #list of results for broken-SCA test. Overwritten after each event.
                        chip_noisy='common_variables.chip_noisy',#list of results for noisy-SCA test. Overwritten after each event.
                        ),
                    ToA_ToT=dict(
                        th_n_ev_to_issue='common_variables.th_n_ev_to_issue',#n_current_event*th_n_ev_to_issue=limit for number of events a channel has to have a TO issue to be considered as having a TO issue globally. Overwritten after each event. (percentage (0-1))
                        to_issue_ch_list='common_variables.to_issue_ch_list',#list of channels considered to have a TO issue (globally). Overwritten after each event.
                        th_to_ch_issue_chip='common_variables.th_to_ch_issue_chip', #number of channels which have to have a TO issue to consider the chip has a TO issue (1-64)
                        n_to_issues_chip='common_variables.n_to_issues_chip',#number of channels per chip which have a TO issue (globally). Overwritten after each event.
                        chip_to_issue='common_variables.chip_to_issue',#list of results for TO test. Overwritten after each event.
                        ),
                )
            )
        )

        with open(fname,'w') as outfile:
            yaml.dump(Default_data,outfile)
        with open(fname,'r') as fin:
            self.yaml_opt=yaml.safe_load(fin)

    def dump(self):
        return yaml.dump(self.yaml_opt)

    def dumpToYaml(self,fname):
        with open(fname,'w') as fout:
            yaml.dump(self.yaml_opt,fout)


def writeLogfile():
    new_yaml=yaml_data()

    #Creation of the logfile
    file_name='data_form.yaml'
    config=ruamel.yaml.round_trip_load(open(file_name))
    DUT = config['DUT']
    DUT['DUT_ID']=common_variables.DuT_name#get it from user input in the GUI and make sure if the user types enter it uses default values (try with the structure of yaml file if it doesn't work)
    DUT['Manufacturer']=common_variables.Manufacturer#get it from user input in the GUI and make sure if the user types enter it uses default values (try with the structure of yaml file if it doesn't work)
    DUT['Number_of_events']=common_variables.n_ev#get it from user input in the GUI and make sure if the user types enter it uses default values (try with the structure of yaml file if it doesn't work)
    DUT['Type_of_hardware']=common_variables.Type_of_hardware#get it from user input in the GUI and make sure if the user types enter it uses default values (try with the structure of yaml file if it doesn't work)
    DUT['Done_tests']['Rollmask_ON']=common_variables.RollMask_full_ON
    DUT['Done_tests']['SCA_ON']=common_variables.SCA_full_ON
    DUT['Done_tests']['ToA_ToT_ON']=common_variables.ToT_ToA_full_ON
    for sk in common_variables.chip_array:
        chip_name='Chip'+str(sk)
        DUT[chip_name]['ToA_ToT']['th_n_ev_to_issue']=common_variables.th_n_ev_to_issue#n_current_event*th_n_ev_to_issue=limit for number of events a channel has to have a TO issue to be considered as having a TO issue globally. Overwritten after each event. (percentage (0-1))
        DUT[chip_name]['ToA_ToT']['to_issue_ch_list']=common_variables.to_issue_ch_list[sk] #list of channels considered to have a TO issue (globally). Overwritten after each event.
        DUT[chip_name]['ToA_ToT']['th_to_ch_issue_chip']=common_variables.th_to_ch_issue_chip #number of channels which have to have a TO issue to consider the chip has a TO issue (1-64)
        DUT[chip_name]['ToA_ToT']['n_to_issues_chip']=common_variables.n_to_issues_chip[sk]#number of channels per chip which have a TO issue (globally). Overwritten after each event.
        DUT[chip_name]['ToA_ToT']['chip_to_issue']=common_variables.chip_to_issue[sk]#list of results for TO test. Overwritten after each event.        DUT[chip_name][SCA]['th_noisy_per_ch']=common_variables.th_noisy_per_ch #number of sca-values in a single channel (in a single event) to consider if noisy (1-13)
        DUT[chip_name]['SCA']['th_broken_per_ch']=common_variables.th_broken_per_ch #number of sca-values in a single channel (in a single event) to consider if broken (1-13)
        DUT[chip_name]['SCA']['th_n_ev_broken']=common_variables.th_n_ev_broken #n_current_event*th_n_ev_broken=limit for number of events a channel has to be broken to be considered as broken globally. Overwritten after each event. (percentage (0-1))
        DUT[chip_name]['SCA']['th_n_ev_noisy']=common_variables.th_n_ev_noisy #n_current_event*th_n_ev_noisy=limit for number of events a channel has to be noisy to be considered as noisy globally. Overwritten after each event. (percentage (0-1))
        DUT[chip_name]['SCA']['broken_ch_list']=common_variables.broken_ch_list[sk] #list of channels considered broken (globally). Overwritten after each event.
        DUT[chip_name]['SCA']['noisy_ch_list']=common_variables.noisy_ch_list[sk] #list of channels considered noisy (globally). Overwritten after each event.
        DUT[chip_name]['SCA']['th_noisy_ch_chip']=common_variables.th_noisy_ch_chip #number of channels which have to be noisy to consider the chip as noisy (1-64)
        DUT[chip_name]['SCA']['th_broken_ch_chip'] =common_variables.th_broken_ch_chip #number of channels which have to be broken to consider the chip as broken (1-64)
        DUT[chip_name]['SCA']['n_noisy_ch_chip']=common_variables.n_noisy_ch_chip[sk] #number of noisy channels per chip (globally). Overwritten after each event.
        DUT[chip_name]['SCA']['n_broken_ch_chip'] =common_variables.n_broken_ch_chip[sk] #number of broken channels per chip (globally). Overwritten after each event.
        DUT[chip_name]['SCA']['chip_broken']=common_variables.chip_broken[sk] #list of results for broken-SCA test. Overwritten after each event.
        DUT[chip_name]['SCA']['chip_noisy']=common_variables.chip_noisy[sk]#list of results for noisy-SCA test. Overwritten after each event.
        DUT[chip_name]['SCA']['th_noisy_per_ch']=common_variables.th_noisy_per_ch
        DUT[chip_name]['Result']=common_variables.chip_results[sk]
        DUT[chip_name]['Rm_Issue']=common_variables.rollMask_issue[sk]
    DUT['DUT_result']=common_variables.DUT_result
    DUT['Timestamp']=strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    DUT['Broken_flag']=common_variables.hexaboard_broken
    DUT['Noisy_flag']=common_variables.hexaboard_noisy
    DUT['ToA_ToT_Issue_flag']=common_variables.hexaboard_to_issue

    name_of_logfile='log_'+'DUT_number_'+str(DUT['DUT_ID'])+'_'+str(DUT['Timestamp'])+'.yaml'

    print(name_of_logfile)
    config_path='./LOG/'+name_of_logfile
    ruamel.yaml.round_trip_dump(config,stream=open(config_path, 'w'))
