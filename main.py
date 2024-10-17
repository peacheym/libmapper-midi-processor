
import rtmidi
import libmapper as mpr
import datetime
import math


midiin = rtmidi.MidiIn()

def update_midi_note_sig(note_num):
    last_midi_note_sig.set_value(note_num)

def h(sig, event, id, val, timetag):
        print(val)

dev = mpr.Device("MidiProcessor")

rate_of_notes_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "rate_of_notes_played", 1,
                        mpr.Type.INT32, None, None, None)

last_midi_note_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "last_midi_note", 1,
                        mpr.Type.INT32, None, 0, 127)

average_velocity_sig = dev.add_signal(mpr.Signal.Direction.OUTGOING, "average_velocity", 1,
                        mpr.Type.INT32, None, 0, 127)

sig_in = dev.add_signal(mpr.Signal.Direction.INCOMING, "my_input", 1,
                        mpr.Type.FLOAT, "m/s", -10, 10, None, h)


LAST_TIME = datetime.datetime.now() # Initialize a timestamp
INTERVAL = 5 # Specify the interval window (in seconds)

COUNT = 0
VELOCITIES = []

ports = range(midiin.get_port_count())
if ports:
    for i in ports:
        print(midiin.get_port_name(i))
    print("Opening MIDI port 0!") 
    midiin.open_port(0)

    while True:
    
        dev.poll()
        m = midiin.get_message() # some timeout in ms
        if m:

            # Note on message
            if m[0][0] == 144:
                update_midi_note_sig(m[0][1])
                COUNT += 1 # Increment the count of notes this interval
                VELOCITIES.append(m[0][2])

        # If the interval has elapsed
        if (datetime.datetime.now() - LAST_TIME).total_seconds() > INTERVAL:

            LAST_TIME = datetime.datetime.now()
            rate_of_notes_sig.set_value(math.ceil(COUNT/INTERVAL)) # Update the rate of notes signal
            
            avg_vel = 0
            if len(VELOCITIES) > 0:
                avg_vel = sum(VELOCITIES)/len(VELOCITIES)
            average_velocity_sig.set_value(avg_vel) # Update the avg velocity signal
            
            VELOCITIES = []
            COUNT = 0
else:
    print('NO MIDI INPUT PORTS!')