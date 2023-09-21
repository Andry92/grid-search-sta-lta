from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import trigger_onset
from obspy import read
import os
import copy
import datetime
import re
import sys

# ---------- CUT LEFT AND RIGHT LIMIT ----------
# remove the left and right limit time from the signal setted automatically during the cut
def cut_limit(trace):
    start_time = trace.stats.starttime + 10
    end_time = trace.stats.endtime - 10

    trace.trim(starttime=start_time, endtime=end_time, nearest_sample=True)

    return trace

# open log_file in write mode
log_filename = "testing_log_"+str(datetime.datetime.now()).replace(":", "")+".txt"
print(log_filename)
f=open("log/"+log_filename, "w")

def write_to_file(str_to_write):
    str_to_write = str(str_to_write)
    f.writelines(str_to_write)
    f.write("\n")

# extract all the raw signals
directory_raw = "data/testing_set/fifth_day_raw"
all_files_raw = []

for filename in os.listdir(directory_raw):
    all_files_raw.append(filename)

# extract all the cutted signals
directory_cutted = "data/testing_set/fifth_day_cutted"
all_files_cutted = []

for filename in os.listdir(directory_cutted):
    all_files_cutted.append(filename)

# dictionary that contains all the filenames of the EQs extracted from raw signal
cut_by_human = {}
for filename in all_files_cutted:
    p = os.path.join(directory_cutted, filename)
    cut_by_human[p] = read(p)[0]

# list with all the results (foreach sta lta window and foreach trig on trig off threshold)
qn_index_trigger_on_complete_list = []
qn_index_trigger_off_complete_list = []

# list containing all the quintuples results: sta, lta, trig_on, trig_off, qni
quintuple_list = []

# starting date and time
start_time = datetime.datetime.now()
print ("Start time = %s" % start_time)
write_to_file("Start time: %s" % start_time)

# ------------
# In this part, it is required to the user to enter the training results file name. From the quintuples,
# the quadruples with qni's value equal or greater than 0.5 are extracted and used for testing
filename = input("Insert the training results filename that you want for testing (without extension): ")
if filename == "":
    print("No file input")
    sys.exit()

# initialize the array to read all quintuples inside the file
quintuples = []

# read results from file
with open('results/'+filename+'.txt') as result_file:
    data = result_file.read()
    
    # match all the quintuples
    quintules_matched = re.findall(r'\((.*?,.*?)\)',data)

    for quintuple_match in quintules_matched:
        # match single values, and then cast to int
        matched_numbers_list = re.findall(r'[0-9.]+',quintuple_match)

        sta = int(matched_numbers_list[0])
        lta = int(matched_numbers_list[1])
        trig_on = int(matched_numbers_list[2])
        trig_off = int(matched_numbers_list[3])
        qni = float(matched_numbers_list[4])

        quintuples.append((sta, lta, trig_on, trig_off, qni))
        
# extract the quadruples from quintuples with qni's values equal or greater than 0.5
quadruples = []
for quint in quintuples:
    if(quint[4] >= 0.5):
        quadruples.append((quint[0], quint[1], quint[2], quint[3]))
# ------------
# ------------

#quadruples = [(0.5, 7, 2, 2)] # Earle and Shearer (1994)
print(quadruples)
print(len(quadruples))

for comb in quadruples:
    sta = comb[0]
    lta = comb[1]
    trig_on = comb[2]
    trig_off = comb[3]

    qn_index_trigger_on_list = []
    qn_index_trigger_off_list = []

    print("-------")
    print("STA: ", sta)
    print("LTA: ", lta)
    print("TRIG ON: ", trig_on)
    print("TRIG OFF: ", trig_off)
    print("-------")

    write_to_file("-------")
    write_to_file("STA: "+ str(sta))
    write_to_file("LTA: "+ str(lta))
    write_to_file("TRIG ON: "+ str(trig_on))
    write_to_file("TRIG OFF: "+ str(trig_off))
    write_to_file("-------")

    successful_cuts = []
    trigger_on_abs_list = []
    trigger_off_abs_list = []

    total_num_sta_lta_triggers = 0

    num_file_raw = 1

    # for every raw signal
    for file_raw in all_files_raw:
    
        print("RAW DATA:", num_file_raw, file_raw)
        write_to_file("RAW DATA:" + str(num_file_raw) +" "+ file_raw)

        file_path_raw = os.path.join(directory_raw, file_raw)

        st_raw_signal = read(file_path_raw)
        tr_raw_signal = st_raw_signal[0]

        # check if raw signal duration is greater than lta and trig_on is greater or equal than trig_off,
        # otherwise, go to the next raw signal
        trace_duration = tr_raw_signal.stats.endtime - tr_raw_signal.stats.starttime
        if trace_duration > lta and trig_on >= trig_off:

            cft = classic_sta_lta(tr_raw_signal.data, int(
                sta * tr_raw_signal.stats.sampling_rate), int(lta * tr_raw_signal.stats.sampling_rate))
        
            # calculate triggers
            triggers = trigger_onset(cft, trig_on, trig_off)
            
            # count how many triggers sta/lta returns
            total_num_sta_lta_triggers += len(triggers)
        
            # check every trigger in triggers list for that raw signal
            for trigger in triggers:
                
                # get trigger in seconds
                trigger_on_sta_lta = trigger[0]/tr_raw_signal.stats.sampling_rate
                trigger_off_sta_lta = trigger[1]/tr_raw_signal.stats.sampling_rate
        
                # check every cutted signal
                for file_cutted in all_files_cutted:
                            
                    file_path_cutted = os.path.join(directory_cutted, file_cutted)
        
                    tr_cutted_signal = copy.deepcopy(cut_by_human[file_path_cutted])
        
                    # cut the limits in explosion quakes signal
                    tr_cutted_signal = cut_limit(tr_cutted_signal)
        
                    # select cutted signals that corresponds to the same hour and the same day in raw signal
                    if(tr_raw_signal.stats.starttime.hour == tr_cutted_signal.stats.starttime.hour and tr_raw_signal.stats.starttime.day == tr_cutted_signal.stats.starttime.day):
                        second_starttime = tr_cutted_signal.stats.starttime.second + \
                            (tr_cutted_signal.stats.starttime.microsecond/1000000)
                        second_endtime = tr_cutted_signal.stats.endtime.second + \
                            (tr_cutted_signal.stats.endtime.microsecond/1000000)
        
                        trigger_on_cutted = (
                            tr_cutted_signal.stats.starttime.minute * 60) + round(second_starttime)
                        trigger_off_cutted = (
                            tr_cutted_signal.stats.endtime.minute * 60) + round(second_endtime)
                
                        # check if sta/lta cut correctly based on the operator
                        trigger_on_abs = abs(trigger_on_sta_lta - trigger_on_cutted)
                        trigger_off_abs = abs(trigger_off_sta_lta - trigger_off_cutted)
                        if trigger_on_abs <= 10 and trigger_off_abs <= 10:
                            print("Explosion Quake detected: ", trigger_on_sta_lta)
                            write_to_file("Explosion Quake detected: "+ str(trigger_on_sta_lta))

                            successful_cuts.append(
                                (trigger_on_sta_lta, trigger_off_sta_lta))
        
                            trigger_on_abs_list.append(trigger_on_abs)
                            trigger_off_abs_list.append(trigger_off_abs)
        
                            break
                    
            num_file_raw += 1
        else:
            print("trace duration < lta, day: ", tr_raw_signal.stats.starttime.day)
            print("or, trig_on trig_off: ", trig_on, trig_off)

            write_to_file("trace duration < lta, day: "+ str(tr_raw_signal.stats.starttime.day))
            write_to_file("or, trig_on trig_off: "+ str(trig_on) +" "+ str(trig_off))

            num_file_raw += 1
            
    # ----------- QUALITY (PRECISION) PART -----------
    
    if len(trigger_on_abs_list) > 0:
        mean_quality_index_trigger_on = sum(trigger_on_abs_list) / len(trigger_on_abs_list)
        
        quality_index_trigger_on = 1 - (mean_quality_index_trigger_on / 10)
    else:
        quality_index_trigger_on = -1
    
    if len(trigger_off_abs_list) > 0:
        mean_quality_index_trigger_off = sum(trigger_off_abs_list) / len(trigger_off_abs_list)
    
        quality_index_trigger_off = 1 - (mean_quality_index_trigger_off / 10)
    else:
        quality_index_trigger_off = -1    
        
    # ----------- QUALITY (PRECISION) PART ----------
    
    # ----------- NUMEROSITY PART -----------
    
    theoretical_num_eq = len(all_files_cutted)
    experimental_num_eq = total_num_sta_lta_triggers
    
    print("\nexperimental_num_eq: ", experimental_num_eq)
    print("\ntheoretical_num_eq: ", theoretical_num_eq)
    
    write_to_file("\nexperimental_num_eq: "+ str(experimental_num_eq))
    write_to_file("\ntheoretical_num_eq: "+ str(theoretical_num_eq))

    # check if experimental eq exceed theoretical eq
    if experimental_num_eq > theoretical_num_eq:
        # if experimental exceed (or equals to) twice theoretical, numerosity is 0
        if experimental_num_eq >= 2*(theoretical_num_eq):
            numerosity = 0
        else:
            # using module, we count how many experimental eq exceed the num of theoretical eq
            numerosity = (theoretical_num_eq - (experimental_num_eq % theoretical_num_eq)) / theoretical_num_eq
    else:
        numerosity = experimental_num_eq / theoretical_num_eq
        
    # ----------- NUMEROSITY PART -----------
    
    # calculate the quality*numerosity index (qn_index)
    qn_index_trigger_on = quality_index_trigger_on * numerosity
    qn_index_trigger_off = quality_index_trigger_off * numerosity
        
    qn_index_trigger_on_list.append(round(qn_index_trigger_on, 2))
    qn_index_trigger_off_list.append(round(qn_index_trigger_off, 2))

    qni = round((qn_index_trigger_on + qn_index_trigger_off)/2, 2)
    quintuple_list.append((sta, lta, trig_on, trig_off, qni))
    
    print("qni: ", qni)
    write_to_file("qni: "+ str(qni))

    qn_index_trigger_on_complete_list.append(qn_index_trigger_on_list)
    qn_index_trigger_off_complete_list.append(qn_index_trigger_off_list)

print("----------------")
print("FINAL RESULTS")
print("qn_index_trigger_on_complete_list", qn_index_trigger_on_complete_list)
print(len(qn_index_trigger_on_complete_list))
print("qn_index_trigger_off_complete_list", qn_index_trigger_off_complete_list)
print(len(qn_index_trigger_off_complete_list))

write_to_file("----------------")
write_to_file("FINAL RESULTS")
write_to_file("qn_index_trigger_on_complete_list"+ str(qn_index_trigger_on_complete_list))
write_to_file(str(len(qn_index_trigger_on_complete_list)))
write_to_file("qn_index_trigger_off_complete_list"+ str(qn_index_trigger_off_complete_list))
write_to_file(str(len(qn_index_trigger_off_complete_list)))

# calculate mean trigger on and trigger off lists
qn_index_total_list = []

for lst1, lst2 in zip(qn_index_trigger_on_complete_list, qn_index_trigger_off_complete_list):
  internal_list = []
  for qn1, qn2 in zip(lst1, lst2):
    mean_value = (qn1 + qn2) / 2
    mean_value = round(mean_value, 2)
    internal_list.append(mean_value)

  qn_index_total_list.append(internal_list)

print("----------")
print("----------")
print("Mean trigger on and trigger off lists")
print(qn_index_total_list)
print(len(qn_index_total_list))

write_to_file("----------")
write_to_file("----------")
write_to_file("Mean trigger on and trigger off lists")
write_to_file(str(qn_index_total_list))
write_to_file(str(len(qn_index_total_list)))

print("----------")
print("----------")
print("Quintuple results")
print(quintuple_list)
print(len(quintuple_list))

write_to_file("----------")
write_to_file("----------")
write_to_file("Quintuple results")
write_to_file(str(quintuple_list))
write_to_file(str(len(quintuple_list)))

# ending date and time
end_time = datetime.datetime.now()
print("\nEnd time = %s" % end_time)
write_to_file("\nEnd time: %s" % end_time)

print("\nTime elapsed: ", end_time - start_time)
write_to_file("\nTime elapsed: "+ str(end_time - start_time))

end_time_formatted = str(end_time)
end_time_formatted = end_time_formatted.replace(" ", "T")
end_time_formatted = end_time_formatted.replace("-", "")
end_time_formatted = end_time_formatted.replace(":", "")

with open("results/testing_results_"+end_time_formatted+".txt", "w") as quint_list_file:
    quint_list_file.write(str(quintuple_list))

print("\nTesting results saved inside 'results' folder, filename: testing_results_"+end_time_formatted+".txt")
print("See "+log_filename+" in log folder for the results")