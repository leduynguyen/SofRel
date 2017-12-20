from threading import *
from OpenOPC import *
import util


'''
    OPCThread Class 
'''

class OpcThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global prev
        global response

        while util.is_running:
            util.lock.acquire()
            try:
                if util.is_connected and util.time_stamp != prev:
                    prev = util.time_stamp
                    out_path = util.res['settings']['DEST_DIR'] + '\\' + \
                               util.res['settings']['FILE_NAME'] + \
                               util.time_stamp + '.txt'
                    res = read_tags()
                    if res:
                        with open(out_path, 'w') as out_fd:
                            out_fd.writelines(response)

            finally:
                util.lock.release()
            time.sleep(1)
            # DEBUGGING
            # print 'is_running : ' + str(util.is_running)

prev = ''
response = []

'''
    read_tag function
'''

def read_tags():
    global response

    del response[:]
    try:
        opc = client()
        opc.connect(util.res['settings']['SERVER'])
    except:
        print ("Can NOT connect")
        util.cur_status = util.res['naming']['ERR_CONNECT']
        return False

	# Print Reading Data
    for tag in util.sorted_tags:
        #Read raw data
        res = opc.read(tag['tag'])
        
        # Process data quality into status
        if res[1] == "Error":
            status = "02"
        elif res[1] == "Good":
            status = "01"
        else:
            status = "00"
            
        # Convert the float data with 2 number
        if(type(res[0]) is float):
            res_val = round(res[0],2)            
        else:
            res_val = res[0]
       
        line = util.res['settings']['LINE'] + tag['name'] + '\t' + \
               str(res_val) + '\t' + \
               tag['unit'] + '\t' + \
               util.time_stamp + '\t' + \
               status + '\n'
        # print line
        line = line.encode('utf-8')
        response.append(line)
    opc.close()
    return True

''' 
================================================================================
                                END OF FILE
================================================================================
'''
