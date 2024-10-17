# Libmapper Midi Processor

This utility script reads incoming MIDI messages and provide statistics about that information as outgoing [libmapper signals](https://github.com/libmapper/libmapper) .

## Avaliable Signals

- Last MIDI Note Played
- Count of notes played in a given interval of time
- Average velocity of notes played in a given interval of time

## Usage

To run the script, ensure the relevant packages are installed and then run the command:

```python main.py```

Open up a [webmapper](https://github.com/libmapper/webmapper) session and you should see your signals ready to map from!