
import rtmidi
import libmapper as mpr


midiin = rtmidi.MidiIn()

def print_message(midi):
    print(midi)
    # if midi.is_note_on():
    #     print('ON: ', midi.get_midi_note_name(midi.get_note_number()), midi.get_velocity())
    # elif midi.isNoteOff():
    #     print('OFF:', midi.get_midi_note_name(midi.get_note_number()))
    # elif midi.isController():
    #     print('CONTROLLER', midi.get_controller_number(), midi.getControllerValue())

dev = mpr.Device("MidiProcessor")


sig_out = dev.add_signal(mpr.Signal.Direction.OUTGOING, "rate_of_notes_played", 1,
                         mpr.Type.INT32, None, 0, 60)


ports = range(midiin.get_port_count())
if ports:
    for i in ports:
        print(midiin.get_port_name(i))
    print("Opening port 0!") 
    midiin.open_port(0)
    while True:
        dev.poll()
        m = midiin.get_message() # some timeout in ms
        if m:
            print_message(m)
else:
    print('NO MIDI INPUT PORTS!')