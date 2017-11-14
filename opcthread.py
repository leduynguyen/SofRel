from threading import *
from OpenOPC import *

import util

# import resources as res

'''
    OPCThread Class 
    ...
    ...
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
                    out_path = util.res['settings']['DEST_DIR'] + \
                               '\\' + util.res['settings']['STT_NAME'] + \
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

    # Start of file
    line = '[Data] \n'.encode('utf-8')
    response.append(line)
    line = 'Tagname;TimeStamp;Value;DataQuality \n'.encode('utf-8')
    response.append(line)	
	
	# Print reading data
    for tag in util.sorted_tags:
        res = opc.read(tag['tag'])
        line = 'ThepMienNam--slave.' + tag['name'] + ';' + \
			   util.time_stamp_ + ';' + \
               str(res[0]) + ';' + \
               str(res[1]) + '\n'
        # print line
        line = line.encode('utf-8')
        response.append(line)
    opc.close()
    return True

''' 
================================================================================
                                End of file
================================================================================
'''