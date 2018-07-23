# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
from random import randint

cycle_time = 0.05

patterns = [{'count_min'   :   9,
             'count_max'   :  10,
             'high'        : 100,
             'low'         :  50,
             'beeptime_min': 0.1,
             'beeptime_max': 0.4,
             'mutetime_min': 0.1,
             'mutetime_max': 0.4,   # includes the last one
             'name':         111},
            {'count_min'   :   9,
             'count_max'   :  10,
             'high'        : 250,
             'low'         :  10,
             'beeptime_min': 0.2,
             'beeptime_max':   3,
             'mutetime_min': 0.1,
             'mutetime_max':   3,   # includes the last one
             'name':         222}]

def callback():
    # record 10 sec worth of data
    time0 = time.time()
    data = [192,136,129,169,10,0,118,175,183,15,0,138,188,212,26,0,109,164,179,121,0,12,178,181,158,0,0,141,164,155,14,0,29,184,166,42,2,37,205,184,187,0,0,133,174,186,20,0,86,181,169,104,0,0,0,0,0,2,5,0,2,0,0,0,0,0,9,0,1,4,0,0,9,0,0,0,0,9,0,1,0,1,0,0,0,3,0,9,0,0,1,0,0,0,0,13,2,0,0,0]
#    data = [110,110,110,0,40,40,60,70,240,20,220,190,30,290,120,120,150,300,200,190,60,180,60,240,130,160,10,70,220,300,110,120,290,40,70,100,20,60,10,230,270,280,140,270,140,280,260,110,230,100,160,20,30,120,120,270,40,260,190,80,300,30,0,80,180,170,220,200,270,210,160,130,230,220,40,20,230,100,0,60,40,40,10,110,170,260,200,180,140,190,210,220,110,80,280,160,50,140,300,290]
#    data = []
#    for i in range(0, 100):
#        sample = randint(0, 30) * 10
#        data.append(sample)
#        time.sleep(cycle_time)
#    print time.time() - time0
#    print data
    print analyze(data)

def analyze(timeseries):
    result = []
    for pattern in patterns:
        result_1 = analyze_one_pattern(timeseries, pattern)
        print result_1
        if compare(result_1, pattern):
            result.append(pattern['name'])
    return result

def analyze_one_pattern(timeseries, pattern):
    beeptime = []
    mutetime = []
    sample = timeseries[0]
    if sample >= pattern['high']:
        nr_of_beeps = 1
        beep = True
        beeptime.append(0)
    else:
        nr_of_beeps = 0
        beep = False
        mutetime.append(0)
    for sample in timeseries:
        if beep and (sample >= pattern['low']):
            beeptime[nr_of_beeps - 1] += cycle_time
#            print sample,
        elif not beep and (sample >= pattern['high']):
            beep = True
            nr_of_beeps += 1
            beeptime.append(cycle_time)
#            print sample
        elif beep and (sample < pattern['low']):
            beep = False
            mutetime.append(cycle_time)
#            print 'n', sample
        elif not beep and (sample < pattern['high']):
            mutetime[nr_of_beeps - 1] += cycle_time
#            print 'n', sample,
    if len(mutetime) > 1:
        mutetime = mutetime[:-1]
    return nr_of_beeps, beeptime, mutetime


def compare(found_pattern, pattern):
    if (pattern['count_min'] > found_pattern[0]) or (pattern['count_max'] < found_pattern[0]):
        return False
    else:
        b_min_true = [dauer >= pattern['beeptime_min'] for dauer in found_pattern[1]]
#        print b_min_true
        b_max_true = [dauer <= pattern['beeptime_max'] for dauer in found_pattern[1]]
#        print b_max_true
        m_min_true = [dauer >= pattern['mutetime_min'] for dauer in found_pattern[2]]
#        print m_min_true
        m_max_true = [dauer <= pattern['mutetime_max'] for dauer in found_pattern[2]]
#        print m_max_true
        if all(b_min_true) and all(b_max_true) and all(m_min_true) and all(m_max_true):
            return True
    return False

callback()