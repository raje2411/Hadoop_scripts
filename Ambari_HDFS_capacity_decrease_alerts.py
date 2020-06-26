#!/usr/bin/env python

#Libararies
import os
import urllib2
import json
import collections
import time
import calendar
import time



#Function to get Epoch time in milliseconds
def current_milli_time() :
    epoch = int(round(time.time() * 1000))
    return epoch

#Main function
def execute(configurations={}, parameters={}, host_name=None):

    #Default threshold if nothing is passed
    critical_threshold = 10
    warning_threshold = 5
    if parameters:
        critical_threshold = parameters["metric.deviation.critical.threshold"]
        warning_threshold = parameters["metric.deviation.warning.threshold"]

    #Epoch time to pass in http request
    today = current_milli_time()
    yesterday = (today - 192800000)

    #Environment details (Have to changed according to cluster)
    ams_host = "c449-node4.coelab.cloudera.com"
    ams_port = "6188"
    AMS_GET_URL = "http://" + ams_host + ":" + ams_port + "/ws/v1/timeline/metrics?metricNames=dfs.FSNamesystem.CapacityUsedGB&appId=namenode&precision=days&startTime=" + str(
        yesterday) + "&endTime=" + str(today)
    print AMS_GET_URL
    #AMS Metrics request
    try:
        metric_data = urllib2.urlopen(AMS_GET_URL,timeout=300)
    except:
        msg = 'AMS GET call timeout.  Check the following URL output:'+AMS_GET_URL
        result_code='UNKNOWN'
        return (result_code,[msg])

    #Convert to Json object
    metric_json_data = json.loads(metric_data.read())

    #extracted_collection_with_sort - will only have 2 sets ordered by epoch timestamp.
    extracted_collection_with_sort = collections.OrderedDict(sorted((metric_json_data["metrics"])[0]["metrics"].items()))
    print extracted_collection_with_sort
    #Capacity Calculation
    today_capacity = extracted_collection_with_sort.values()[1]
    yesterday_capacity = extracted_collection_with_sort.values()[0]

    # Percentage Differnce calculation
    pct_change = ((float(today_capacity) - yesterday_capacity) / abs(yesterday_capacity)) * 100.0

    #Retrun to Ambari Alerts with results_code and msg

    # Critical Alert check
    if (pct_change > critical_threshold) :
        if (today_capacity < yesterday_capacity) :
            result_code = 'CRITICAL'
            msg = 'Capacity Decreased by ' + str(pct_change) + '%'
        if (today_capacity > yesterday_capacity) :
            result_code = 'CRITICAL'
            msg = 'Capacity Increased by ' + str(pct_change) + '%'
        return result_code,[msg]

    # Warning Alert check
    if (pct_change > warning_threshold) :
        if (today_capacity < yesterday_capacity):
            result_code = 'WARNING'
            msg = 'Capacity Decreased by ' + str(pct_change) + '%'
        if (today_capacity > yesterday_capacity) :
            result_code = 'WARNING'
            msg = 'Capacity Increased by ' + str(pct_change) + '%'
        return result_code,[msg]

    # 'OK' Alert check
    if (pct_change < warning_threshold) :
        result_code = 'OK'
        msg = 'Capacity increase / decrease is less than threshold ' + str(warning_threshold)
        return result_code,[msg]
    #End of execute()

#execute({},{"metric.deviation.critical.threshold": 20.0,"metric.deviation.warning.threshold": 15.0},None)
msg = execute()
print msg
