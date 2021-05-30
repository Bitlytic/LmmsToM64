# Should be native modules
import sys
import re
import os
import warnings
from configparser import RawConfigParser

# Probably need to install this one though
from mido import MidiFile, MidiTrack, Message, MetaMessage

# Load config
configparser = RawConfigParser()
configFilePath = './settings.cfg'
configparser.read(configFilePath)

version = configparser.get('decomp-info', 'version')
version = version.upper()
abi_type = ''

if version == 'US':
    abi_type = 'sm64'
elif version == 'EU':
    abi_type = 'sm64eu'
else:
    abi_type = 'sm64'
    warnings.warn(f"Version selected is {version}, which I'm not sure will work, but we'll try anyways")

decomp_path = configparser.get('decomp-info', 'path')
if decomp_path[-1] != '\\':
    decomp_path += '\\'

sound_bank_path = 'sound\\sequences\\us\\'

seq_path = configparser.get('seq64-info', 'path-to-exe')

m = sys.argv[1]
out = decomp_path + sound_bank_path + sys.argv[2]

# Load input midi, this should be the one from lmms
input_midi = MidiFile('./' + m)

track_to_remove = -1

# Perform operations to update tracks to seq64 compatible, like setting channel and programs
for i, track in enumerate(input_midi.tracks):
    pitch = 0
    # We need to remove kicker track, as lmms adds this by default and breaks our .m64 file
    if track.name.upper() == 'KICKER':
        track_to_remove = i
        continue
    new_track = MidiTrack()

    # Patch is entry in instrument_list found in sound bank json files
    r1 = re.findall(r"Patch ([\-0-9]*)", track.name)

    # Pitch is for correction, certain instruments will play at different pitches in sm64,
    # so if you want to adjust pitch outside of lmms, you can add Pitch {value} to the name
    # to adjust this, otherwise it plays at default pitch
    r2 = re.findall(r"Pitch ([\-0-9]*)", track.name)
    if len(r2) != 0:
        pitch = int(r2[0])

    # Add program change message to beginning, this is missing from lmms
    new_track.append(Message('program_change', channel=i, program=int(r1[0]), time=0))

    # Add all other messages, like notes and tempo changes from midi
    for m in track: 
        if not isinstance(m, MetaMessage):
            m.channel = i
            m.note = m.note + pitch
        new_track.append(m)

    input_midi.tracks[i] = new_track

# If we found kicker track, delete that shit
if track_to_remove != -1:
    del input_midi.tracks[track_to_remove]

input_midi.save("temp.mid")

command_string = f'{seq_path} --abi={abi_type} --in=temp.mid --out={out}'
print(f"Running command: \n{command_string}")

# Run through seq64, which saves as .m64
os.system(command_string)