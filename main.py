1
import rtmidi
import libmapper as mpr
import datetime
import math


midiin = rtmidi.MidiIn()

def update_midi_note_sig(note_num):
    last_midi_note_sig.set_value(note_num)

def h(sig, event, id, val, timetag):
        # print(val)
        return


###### INIT Libmapper Stuff ######

dev = mpr.Device("MidiProcessor")

rate_of_notes_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "rate_of_notes_played", 1,
                        mpr.Type.INT32, None, None, None)

last_midi_note_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "last_midi_note", 1,
                        mpr.Type.INT32, None, 0, 127)

average_velocity_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "average_velocity", 1,
                        mpr.Type.INT32, None, 0, 127)

sig_in = dev.add_signal(mpr.Signal.Direction.INCOMING, "my_input", 1,
                        mpr.Type.FLOAT, "m/s", -10, 10, None, h)

        
energy_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "energy", 1, mpr.Type.INT32, None, 0, 1000) # Decide appropriate min/max values


###### END Libmapper Stuff ######

class EnergyManager():
    def __init__(self, sig, leaky_rate):
        self.leaky_rate = leaky_rate
        self.energy = 1
        
        self.sig = sig
        
        
    def add(self, value):
        self.energy += value
        
        self.update_signal()
        
    def leak(self):
        self.energy -= self.leaky_rate
        
        if self.energy < 0:
            self.energy = 0

        self.update_signal()
        

    def update_signal(self):
        self.sig.set_value(self.energy)

LAST_TIME = datetime.datetime.now() # Initialize a timestamp
LAST_TIME_FAST = datetime.datetime.now() # Initialize a timestamp
INTERVAL = 5 # Specify the interval window (in seconds)
INTERVAL_FAST = 0.1

COUNT = 0
VELOCITIES = []

em = EnergyManager(energy_sig, 10)

ports = range(midiin.get_port_count())
if ports:
    for i in ports:
        print(midiin.get_port_name(i))
    print("Opening MIDI port 0!") 
    midiin.open_port(0)

    while True:
    
        dev.poll(0)
        m = midiin.get_message() # some timeout in ms
        if m:
            # print(m)
            # Note on message
            if m[0][0] == 144:
                update_midi_note_sig(m[0][1])
                COUNT += 1 # Increment the count of notes this interval
                VELOCITIES.append(m[0][2])
                em.add(m[0][2])        
                
        # If the long interval has elapsed
        if (datetime.datetime.now() - LAST_TIME).total_seconds() > INTERVAL:
            LAST_TIME = datetime.datetime.now()
            rate_of_notes_sig.set_value(math.ceil(COUNT/INTERVAL)) # Update the rate of notes signal
            COUNT = 0
            
        # Else if the slow interval has passed
        elif (datetime.datetime.now() - LAST_TIME_FAST).total_seconds() > INTERVAL_FAST:
            LAST_TIME_FAST = datetime.datetime.now()
            em.leak()
            if len(VELOCITIES) > 0:
                VELOCITIES.pop(0)
                
            avg_vel = 0
            if len(VELOCITIES) > 0:
                avg_vel = sum(VELOCITIES)/len(VELOCITIES)
                VELOCITIES.pop(0)
            average_velocity_sig.set_value(avg_vel) # Update the avg velocity signal
            
            # VELOCITIES = []
else:
    print('NO MIDI INPUT PORTS!')