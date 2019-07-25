
import json
import re
import matplotlib.pyplot as plt
import os
import numpy as np

def read_time_data(series_name):
    """ Read time data from file """
    times_s = {"real": [], "user": [], "sys": []}
    matchers = {"real": re.compile(r'real\s+(\d+)m(\d+[,.]\d+)s\n'),
            "user": re.compile(r'user\s+(\d+)m(\d+[,.]\d+)s\n'),
            "sys": re.compile(r'sys\s+(\d+)m(\d+[,.]\d+)s\n')}
    filename_time = "sieve_%s_times.txt" % series_name
    with open(filename_time) as ftime:
        for line in ftime:
            for timetype in times_s.keys():
                m = matchers[timetype].match(line)
                if m:
                    mins = float(m.group(1))
                    secs = float(m.group(2).replace(',','.'))
                    times_s[timetype].append(60*mins + secs)
    return times_s

def read_memory_data(series_name):
    """ Read memory data from file """
    memory = {"mem%": [], "VSZ": [], "RSS": []}
    filename_mem = "sieve_%s_mem.txt" % series_name
    with open(filename_mem) as fmem:
        line = fmem.readline()
        fields = re.split("\s+", line)
        it_mem = None
        it_vsz = None
        it_rss = None
        for (it, field) in enumerate(fields):
            it_mem = it if field == "%MEM" else it_mem
            it_vsz = it if field == "VSZ" else it_vsz
            it_rss = it if field == "RSS" else it_rss
        if not (it_mem and it_vsz and it_rss):
            raise Exception("Could not find all expected fields in memory file")
        for line in fmem:
            fields = re.split("\s+", line)
            if fields[0] != "USER":
                memory["mem%"].append(float(fields[it_mem]))
                memory["VSZ"].append(int(fields[it_vsz]))
                memory["RSS"].append(int(fields[it_rss]))
    return memory

def read_raw_data(series_name):
    """ Read raw data from a series name and return the data """
    data_dict = {}
    data_dict["times_s"] = read_time_data(series_name)
    data_dict["memory"] = read_memory_data(series_name)
    return data_dict

def read_data_from_file(series_name):
    """ Read data from file based on the name of a series """
    datafilename = series_name + "_data.json"
    data_dict = None
    if os.path.exists(datafilename):
        with open(datafilename) as fdata:
            data_dict = json.load(fdata)
    else:
        data_dict = read_raw_data(series_name)
        with open(datafilename, 'w') as fdata:
            json.dump(data_dict, fdata)
    return data_dict

arm_data = read_data_from_file("arm")
arm_times_s = arm_data["times_s"]
arm_memory = arm_data["memory"]
qemu_data = read_data_from_file("qemu")
qemu_times_s = qemu_data["times_s"]
qemu_memory = qemu_data["memory"]
native_data = read_data_from_file("native")
native_times_s = native_data["times_s"]
native_memory = native_data["memory"]

real_time_arm = sum(arm_data["times_s"]["real"])/len(arm_data["times_s"]["real"])
real_time_qemu = sum(qemu_data["times_s"]["real"])/len(qemu_data["times_s"]["real"])
real_time_native = sum(native_data["times_s"]["real"])/len(native_data["times_s"]["real"])

time_means = [real_time_arm, real_time_qemu, real_time_native]

rss_mean_arm = float(sum(arm_data["memory"]["RSS"]))/len(arm_data["memory"]["RSS"]) * 1e-3
rss_mean_qemu = float(sum(qemu_data["memory"]["RSS"]))/len(qemu_data["memory"]["RSS"]) * 1e-3
rss_mean_native = float(sum(native_data["memory"]["RSS"]))/len(native_data["memory"]["RSS"]) * 1e-3

rss_means = [rss_mean_arm, rss_mean_qemu, rss_mean_native]

#plt.plot(native_memory["RSS"], label='Native')
#plt.plot(arm_memory["RSS"], label='Arm')
#plt.plot(qemu_memory["RSS"], label='Qemu')

#plt.plot(native_times_s["real"], label='Native')
#plt.plot(arm_times_s["real"], label='Arm')
#plt.plot(qemu_times_s["real"], label='Qemu')




fig, ax1 = plt.subplots()
index = np.arange(3)
bar_width = 0.35
opacity = 0.7

rects1 = plt.bar(index, time_means, bar_width,
alpha=opacity,
color='b',
label='Times [s]')
ax1.set_ylabel('Times [s]', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
rects2 = ax2.bar(index + bar_width, rss_means, bar_width,
alpha=opacity,
color='g',
label='Memory (RSS) [MB]')
ax2.set_ylabel('Memory (RSS) [MB]', color='g')
ax2.tick_params(axis='y', labelcolor='g')

plt.xticks(index + bar_width/2, ('Arm', 'Qemu', 'Native'))

plt.tight_layout()
plt.show()
