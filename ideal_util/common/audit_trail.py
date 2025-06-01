#/usr/bin/env python3

from datetime import datetime
import pandas as pd

from ideal_util.common import ideal_config as config


def coversheet(tool_name, tool_url):
    
    now = datetime.now(config.US_EASTERN)

    key_list = [
        "Tool Used:",
        "Tool URL:",
        "Data Generated on:",
        "Disclaimer:"
    ]

    value_list = [
        tool_name,
        tool_url,
        now.strftime(config.DATETIME_FORMAT),
        "Please consult your ARM stakeholder(s) before using the data in a report or making any methodological decisions."
    ]
    
    key_list = [key.upper() for key in key_list]

    return pd.DataFrame({"Key":key_list, "value":value_list})
    

def parameters(param_dict):

    key_list = param_dict.keys()
    key_list = [key.upper() for key in key_list]
    value_list = param_dict.values()

    return pd.DataFrame({"Key":key_list, "value":value_list})
  

