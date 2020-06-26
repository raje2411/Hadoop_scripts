#!/usr/bin/env python

# Libraries
import calendar
import collections
import json
import time
import urllib2

# Function to get Epoch time in milliseconds
def epoch_time():
    epoch = calendar.timegm(time.gmtime())
    return epoch

# Main function
def execute(configurations={}, parameters={}, host_name=None):
    # Default threshold if nothing is passed
    critical_threshold = 10
    warning_threshold = 5
    if parameters:
        critical_threshold = int(parameters["metric.deviation.critical.threshold"])
        warning_threshold = int(parameters["metric.deviation.warning.threshold"])

    # Epoch time to pass in http request
    today = epoch_time()
    yesterday = today - (84000)

    # Environment details (Have to changed according to cluster)
    ams_host = "c449-node4.coelab.cloudera.com"
    ams_port = "6188"
    AMS_GET_URL = "http://" + ams_host + ":" + ams_port + "/ws/v1/timeline/metrics?metricNames=dfs.FSNamesystem.CapacityUsedGB&appId=namenode&precision=minutes&startTime=" + str(
        yesterday) + "&endTime=" + str(today)

    #AMS Metrics request
    try:
        metric_data = urllib2.urlopen(AMS_GET_URL, timeout=300)
    except:
        msg = 'AMS GET call timeout.  Check the following URL output:' + AMS_GET_URL
        result_code = 'UNKNOWN'
        return (result_code, [msg])

    # Convert to Json object
    metric_json_data = json.loads(metric_data.read())

    # extracted_collection_with_sort - will only have 2 sets ordered by epoch timestamp.
    extracted_collection_with_sort = collections.OrderedDict(
        sorted((metric_json_data["metrics"])[0]["metrics"].items()))

    # Capacity Calculation
    today_capacity = extracted_collection_with_sort[max(extracted_collection_with_sort)]
    yesterday_capacity = extracted_collection_with_sort[min(extracted_collection_with_sort)]

    # Percentage Difference calculation
    pct_change = abs(((float(today_capacity) - yesterday_capacity) / abs(yesterday_capacity)) * 100.0)

    # Retrun results_code and msg to Ambari Alerts
    # Critical Alert check
    if (pct_change > critical_threshold) :
        if (today_capacity > yesterday_capacity) :
            result_code = 'OK'
            msg = 'Capacity decreased by 0%'
        if (today_capacity < yesterday_capacity) :
            result_code = 'CRITICAL'
            msg = 'Capacity Decreased by ' + str(pct_change) + '%'
        return result_code, [msg]

    # Warning Alert check
    if (pct_change > warning_threshold) :
        if (today_capacity > yesterday_capacity) :
            result_code = 'OK'
            msg = 'Capacity decreased by 0%'
        if (today_capacity < yesterday_capacity) :
            result_code = 'WARNING'
            msg = 'Capacity Decreased by ' + str(pct_change) + '%'
        return result_code, [msg]

    # 'OK' Alert check
    if (pct_change < warning_threshold) :
        if (today_capacity > yesterday_capacity) :
            result_code = 'OK'
            msg = 'Capacity decreased 0%'
        if (today_capacity <= yesterday_capacity) :
            result_code = 'OK'
            msg = 'Capacity Decreased by ' + str(pct_change) + '%'
        return result_code, [msg]
    # End of execute()

#Call main function
# execute({},{"metric.deviation.critical.threshold": 20.0,"metric.deviation.warning.threshold": 15.0},None)
execute()
