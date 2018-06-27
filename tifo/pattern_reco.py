# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
from random import randint

cycle_time = 0.05

patterns = [{'repeat'  :  9,
               'high'    : 250,
               'low'     :  10,
               'beeptime_min':  0.2,
               'beeptime_max':  3,
               'mutetime_min':  0.1,
               'mutetime_max':  3,   # includes the last one
               'name': 100},
            {'repeat'  :  11,
               'high'    : 250,
               'low'     :  50,
               'beeptime_min':  0.1,
               'beeptime_max':  2,
               'mutetime_min':  0.1,
               'mutetime_max':  2,
               'name': 200}]

def callback():
    # record 10 sec worth of data
    time0 = time.time()
    data = []
    for i in range(0, 100):
        sample = randint(0, 30)
        data.append(sample)
        time.sleep(cycle_time)
    print time.time() - time0
    print data
    print analyze(data)

def analyze(timeseries):
    for pattern in patterns:
        result_1 = analyze_one_pattern(timeseries, pattern)
        print result_1
        result = []
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
    return nr_of_beeps, beeptime, mutetime


def compare(found_pattern, pattern):
    if pattern['repeat'] <> found_pattern[0]:
        return False
    else:
        b_min_true = [dauer >= pattern['beeptime_min'] for dauer in found_pattern[1]]
        b_max_true = [dauer <= pattern['beeptime_max'] for dauer in found_pattern[1]]
        m_min_true = [dauer >= pattern['mutetime_min'] for dauer in found_pattern[2]]
        m_max_true = [dauer <= pattern['mutetime_max'] for dauer in found_pattern[2]]
        if all(b_min_true) and all(b_max_true) and all(m_min_true) and all(m_max_true):
            return True
    return False

callback()