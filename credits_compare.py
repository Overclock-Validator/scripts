from datadog import initialize, statsd
import re
import time
import subprocess

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

initialize(**options)

def get_metrics_from_line(l):
    x = re.findall("\s*(\d+)\s+",l)
    if len(x) == 0:
        return
    rank=x[0]
#    print("rank:%s"%(x[0]))
    x = re.findall("[\%|-]\s+(\d+)\s+",l)
    credits = x[-1]
#    print("credits:%s"%(x[-1]))
    x = re.findall("\s*(\w+)\s+",l)
    identity = x[1]
#    print("identity:%s"%(x[1]))
    return(identity,rank,credits)

def get_credits():
    cmd = subprocess.run("solana validators --sort=credits -r -n | grep -e C1ocKDYMCm2ooWptMMnpd5VEB2Nx4UMJgRuYofysyzcA -e FxhKTay63tcYR8WuXwRvWJCmAV239fXizqRXNMMMqhjB -e DSYrGghVvGYt2VXytFdaFxh2MuLiESStM1WtubMuuTMD -e LA1NEzryoih6CQW3gwQqJQffK2mKgnXcjSQZSRpM3wc -e 3ajcUoKkL1VsGi4SNkm9tbZR9C23ph763AkXy2pyr5eJ -e juigBT2qetpYpf1iwgjaiWTjryKkY3uUTVAnRFKkqY6 -e PUmpKiNnSVAZ3w4KaFX6jKSjXUNHFShGkXbERo54xjb -e CMPSSdrTnRQBiBGTyFpdCc3VMNuLWYWaSkE8Zh5z6gbd -e Dsx767ApcHX689ViFHTUMeJ7V6vLaNH29JSk8jv6Q5mS -e Df8inLU7AzpYMPUZXVdU6Vuy29cuWBuqv3kevNQsn9zu",shell=True, capture_output=True)
    lines = cmd.stdout.decode("ascii","ignore").split("\n")
    credit_info = []
    for l in lines:
        credit_info.append(get_metrics_from_line(l))
    return credit_info

while(1):
    clist = get_credits()
    for c in clist:
        if c is None:
            continue
        statsd.gauge('voting.rank', c[1], tags=["validator:%s"%(c[0])])
        statsd.gauge('voting.credits', c[2], tags=["validator:%s"%(c[0])])
        time.sleep(60)
