import itertools
import matplotlib.pyplot as plt
import re
import sys

filename = input("Insert the results filename to show the plot (without extension): ")
if filename == "":
    print("No file input")
    sys.exit()

quintuples = []

# read results from file
with open('results/'+filename+'.txt') as result_file:
    data = result_file.read()
    
    # match all the quintuples
    quintules_matched = re.findall(r'\((.*?,.*?)\)',data)
    #print(quintules_matched)

    for quintuple_match in quintules_matched:
        # match single values, and then cast to int
        matched_numbers_list = re.findall(r'[0-9.]+',quintuple_match)
        #print(matched_numbers_list)

        sta = int(matched_numbers_list[0])
        lta = int(matched_numbers_list[1])
        trig_on = int(matched_numbers_list[2])
        trig_off = int(matched_numbers_list[3])
        qni = float(matched_numbers_list[4])

        quintuples.append((sta, lta, trig_on, trig_off, qni))

# remove redundances from list
quintuples = list(dict.fromkeys(quintuples))

# extract list values for the 4 parameters
sta_list = []
lta_list = []
trig_on_list = []
trig_off_list = []

for quint in quintuples:
    if quint[0] not in sta_list:
        sta_list.append(quint[0])

    if quint[1] not in lta_list:
        lta_list.append(quint[1])

    if quint[2] not in trig_on_list:
        trig_on_list.append(quint[2])

    if quint[3] not in trig_off_list:
        trig_off_list.append(quint[3])

print("sta_list", sta_list)
print("lta_list", lta_list)

trig_on_list.sort()
print("trig_on_list", trig_on_list)
print("trig_off_list", trig_off_list)

# Create a list with only QNI values selected (fullfilled with zeros)
c = list(itertools.product(sta_list, lta_list))

qni_list = []

for comb in c:
    sta = comb[0]
    lta = comb[1]

    c_trig = list(itertools.product(trig_on_list, trig_off_list))

    for comb_trig in c_trig:
        trig_on = comb_trig[0]
        trig_off = comb_trig[1]

        qni_found_in_list = 0

        for quintuple in quintuples:
            if quintuple[0] == sta and quintuple[1] == lta and quintuple[2] == trig_on and quintuple[3] == trig_off:
                qni_list.append(quintuple[4])
                qni_found_in_list = 1

        if qni_found_in_list == 0:
            qni_list.append(0)

# multiply every qni * 100
qni_list = [qni*100 for qni in qni_list]

# divide list len(trig_on_list)*len(trig_off_list) times for grid
cont = 1
new_results = []
trig_comb = []
for qni in qni_list:
    if cont <= len(trig_on_list)*len(trig_off_list):
        trig_comb.append(qni)
        cont += 1
    else:
        new_results.append(trig_comb)
        trig_comb = [qni]
        cont = 2

new_results.append(trig_comb) # including last list

# PLOT PART
trig_on_comb = []
trig_off_comb = []

for comb_trig in c_trig:
       trig_on_comb.append(comb_trig[0])
       trig_off_comb.append(comb_trig[1])

fig = plt.figure(figsize=(20,18))

i_th_list = 0
for i in range(len(sta_list)):
    for j in range(len(lta_list)):
            ax = plt.subplot2grid((len(sta_list),len(lta_list)), (i,j))

            ax.scatter(trig_on_comb, trig_off_comb, new_results[i_th_list], new_results[i_th_list], cmap='viridis_r', vmin=0, vmax=100)
            plt.xlabel("trigger on")
            plt.ylabel("trigger off")

            i_th_list+=1

# get the last axes
im = plt.gca().get_children()[0]
# set colorbar scale
#im.set_clim(0,100)
# position of the figures
cax = fig.add_axes([0.93,0.1,0.03,0.8])
# set colorbar for figure
cb = fig.colorbar(im, cax=cax)
# set colorbar title
cb.ax.set_title('QNI')
# to invert colorbar
cb.ax.invert_yaxis()
# change fontsize text colorbar
cb.ax.tick_params(labelsize=14)

#fig.text(0.08, 0.84, '2', va='center', fontsize = 13)
#fig.text(0.08, 0.74, '4', va='center', fontsize = 13)
fig.text(0.07, 0.76, '6', va='center', fontsize = 13)
fig.text(0.07, 0.50, '8', va='center', fontsize = 13)
fig.text(0.07, 0.23, '10', va='center', fontsize = 13)
#fig.text(0.08, 0.35, '12', va='center', fontsize = 13)
#fig.text(0.08, 0.25, '14', va='center', fontsize = 13)
#fig.text(0.08, 0.15, '16', va='center', fontsize = 13)

#fig.text(0.15, 0.05, '20', va='center', fontsize = 13)
#fig.text(0.22, 0.05, '40', va='center', fontsize = 13)
#fig.text(0.29, 0.05, '60', va='center', fontsize = 13)
fig.text(0.23, 0.03, '80', va='center', fontsize = 13)
fig.text(0.51, 0.03, '100', va='center', fontsize = 13)
fig.text(0.78, 0.03, '120', va='center', fontsize = 13)
#fig.text(0.58, 0.05, '140', va='center', fontsize = 13)
#fig.text(0.65, 0.05, '160', va='center', fontsize = 13)
#fig.text(0.72, 0.05, '180', va='center', fontsize = 13)
#fig.text(0.79, 0.05, '200', va='center', fontsize = 13)
#fig.text(0.86, 0.05, '220', va='center', fontsize = 13)

fig.text(0.51, 0.001, 'LTA (s)', ha='center', fontsize = 15)
fig.text(0.04, 0.5, 'STA (s)', va='center', rotation='vertical', fontsize = 15)

#fig.text(0.41, 0.93, 'STA / LTA EXPERIMENTS RESULTS', va='center', style = 'italic', fontsize = 15)

fig.suptitle("Results of: "+ filename, fontsize=16)
plt.show()