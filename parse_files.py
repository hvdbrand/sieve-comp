
import re
import matplotlib.pyplot as plt

config = "native"
file_time = "sieve_%s_times.txt" % config
file_mem = "sieve_%s_mem.txt" % config

times_s = {"real": [], "user": [], "sys": []}
matchers = {"real": re.compile(r'real\s+(\d+)m(\d+[,.]\d+)s\n'),
            "user": re.compile(r'user\s+(\d+)m(\d+[,.]\d+)s\n'),
            "sys": re.compile(r'sys\s+(\d+)m(\d+[,.]\d+)s\n')}


with open(file_time) as ftime:
    for line in ftime:
        for timetype in times_s.keys():
            m = matchers[timetype].match(line)
            if m:
                mins = float(m.group(1))
                secs = float(m.group(2).replace(',','.'))
                times_s[timetype].append(60*mins + secs)

            
plt.plot(times_s["real"])
plt.plot(times_s["user"])
plt.plot(times_s["sys"])
plt.show()
