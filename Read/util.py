import collections
import threading
import json
import operator

# GLOBAL VARIABLE
is_connected = True
is_running = True

comm_state = 0
time_stamp = ''
time_stamp_ = ''

cur_status = ''

lock = threading.Lock()

# lst_command = collections.OrderedDict()

# REGEX
JSON_REGEX = r"([\w ]+)_([\d]+)(\.json)"

res = None
with open('config.json') as json_data_file:
    res = json.load(json_data_file)

sorted_tags = sorted(res['OPC'].values(), key=lambda x: int(x['index']))
''' 
================================================================================
								END OF FILE
================================================================================
''' 