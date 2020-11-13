# -*- coding: utf-8 -*-

import sys
import time
import threading
from multiprocessing import connection

class srvPPE(object):
    def __init__(self, addr, pw, mode=1):
        self.lstnThread = threading.Thread(target = self.conStart, args=(addr, pw, mode,))
        self.lstnThread.daemon = True
        self.lstnThread.start()
        self.client = None
  
    def conStart(self, addr, pw, mode):
        lstnr = connection.Listener(addr, family='AF_PIPE', authkey=pw.encode())
        while 1:
            try:
                self.client = lstnr.accept()
                if mode == 1: thrd = threading.Thread(target = self.clientLoop, args=(self.client,))
                if mode != 2:
                    thrd.daemon = True
                    thrd.start()
            except:
                import traceback
                print(traceback.format_exc())

    def clientLoop(self, client):
        while not self.client.closed:
            try:
                msg = self.client.recv_bytes()
                self.client.send(eval(msg))       # WARNING - this metod sends data as pickle module serialized object, must be pickle deserialized on client
                #self.client.send_bytes(str(eval(msg)).encode())  # u can use more safe method, with no serialisation
                #exec compile(msg,'','exec') in sys.modules['__main__'].__dict__  # 
                #self.client.send('compiled')
            except EOFError as err: break
            except Exception as exc:
                import traceback
                self.client.send(traceback.format_exc())
                
class myIO():
    def write(self, message):
        sys.stdIO.write(message)
        
        if message:
            if edbg.client is not None:
                if not edbg.client.closed:
                    try:
                        edbg.client.send_bytes(str(message).encode('utf-8'))
                    except: pass
    def flush(self): sys.stdIO.flush()
    def close(self): pass

dataEx = srvPPE(r'\\.\pipe\dataEx', pw='xxxx'.encode(), mode=1 )
edbg = srvPPE(r'\\.\pipe\edbg', pw='xxxx'.encode(), mode=2 )

sys.stdIO = sys.stdout
sys.stdIO = sys.stderr
sys.stderr = sys.stdout = myIO()
    

