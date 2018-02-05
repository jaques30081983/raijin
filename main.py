from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
#from packet import E131Packet
from source import DMXSource
import threading
import time
from random import randint
from kivy.clock import Clock, mainthread
##########e131########
data = [0] * 512

import socket
import struct

# 239.256.0.1:5568
UDP_IP = "239.255.0.1"
# UDP_IP = "127.0.0.1"
UDP_PORT = 5568
multicast_group = ("239.255.0.1", 5568)

clouds = 12
cloud_chan = 9

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)


sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

# sent = sock.sendto(p.packet, (UDP_IP, UDP_PORT))
src = DMXSource()
import time

######Audio#######
#import pyaudio
#import numpy as np

CHUNK = 2**11
RATE = 44100



#######GUIL########
class RootWidget(FloatLayout):
    stop = threading.Event()
    speed = 0
    random_running = 0
    #for i in range(500):
        #src.send_data(data)
        #time.sleep(0.1)
    def cloud(self,chan, action, *args):
        if (action == 0):
            value = randint(3, 15)
        else:
            value = 0
        data[chan] = value
        src.send_data(data)
        print chan, action
        print data
    def set_intensity(self,value, *args):
        j = 0
        for i in range(clouds):       
            data[j] = int(value)
            
            j = j + cloud_chan
        src.send_data(data)

    def set_red(self,value, *args):
        j = 1
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
        src.send_data(data)
    def set_green(self,value, *args):
        j = 2
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
        src.send_data(data)
    def set_blue(self,value, *args):
        j = 3
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
        src.send_data(data)
    def set_lightning_r(self,value, *args):
        j = 4
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
        src.send_data(data)
    def set_lightning_g(self,value, *args):
        j = 5
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
        src.send_data(data)
    def set_lightning_b(self,value, *args):
        j = 6
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
        src.send_data(data)
    def set_lightning_kind(self,value, *args):
        j = 7
        for i in range(clouds):       
            data[j] = int(value)
            j = j + cloud_chan
            print data
        src.send_data(data)
    def set_lightning_energy(self,value, *args):
        
        for i in range(clouds):       
            data[8+i] = int(value)
        print data
        src.send_data(data)

    def set_speed(self,value, *args):
        self.speed = value
        if self.random_running == 1:
            Clock.unschedule(self.my_callback)
            Clock.schedule_interval(self.my_callback,self.speed/60) 

    def my_callback(self,dt):
        self.cloud(randint(8, 19),randint(0, 1))
        

    def set_random(self, checkbox, value):

        if value:
            Clock.schedule_interval(self.my_callback,self.speed/60)         
            self.random_running = 1

        else:
            Clock.unschedule(self.my_callback)
            self.random_running = 0


    def start_pitch_thread(self):
        threading.Thread(target=self.get_pitch, args=('NIX',)).start()
        
    def get_pitch(self,*args):
        p=pyaudio.PyAudio()
        stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

        for i in range(int(10*44100/1024)): #go for a few seconds
            data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
            peak=np.average(np.abs(data))*2
            bars="#"*int(50*peak/2**16)
            print("%04d %05d %s"%(i,int(50*peak/2**16),bars))
            self.update_level(int(50*peak/2**16))
        stream.stop_stream()
        stream.close()
        p.terminate()

                

    @mainthread
    def update_level(self, value):
        self.ids.level.value = int(value)
        self.set_lightning_energy(int(value))

class MainApp(App):
    def build(self):
        return RootWidget()
    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass
    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

if __name__ == '__main__':
    MainApp().run()
