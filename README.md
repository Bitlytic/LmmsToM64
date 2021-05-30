# What is this
This tool is for use with LMMS to make sm64 romhack music easier to create. Hopefully it does this for you and you never need to manually edit midi tracks again.

# Installation
## Clone this repo
Clone this repo onto your machine, preferably put it somewhere you'll remember it so you can save midis to the folder
> git clone https://github.com/Bitlytic/LmmsToM64.git

## SEQ64
This uses SEQ64 to convert our processed .mid file to a .m64 which can be played by sm64, you can download SEQ64 from [Here](https://github.com/sauraen/seq64)

## SM64 Soundfont by Pablo's Corner
This is kinda optional, as it's only for playing sound through LMMS, but I'd highly recommend getting it from [Here](https://www.smwcentral.net/?p=viewthread&t=88116)

## Python
It's made in python3, so you're probably gonna want that from [Here](https://www.python.org/)

### Modules
Most modules should come with your python installation, except for mido, which you can install by running
> pip install mido

If there are missing modules, here's a list of the ones it uses
- os
- system
- re
- warnings
- configparser
- mido

## LMMS
This tool might work with other DAWs, but LMMS is the one it was designed for, which you can pick up and install for free from [Here](https://lmms.io/)

## Decomp
This might also work with ROM Manager, or other ways to hack sm64, but it was only specifically made for decomp

# Usage
## Settings
After everything is installed, you will need to set up your settings.cfg, the decomp path will point to the base directory of your decomp (which has folders like actors, sound, src), the version can be upper or lowercase from the set of (US, EU, JP, SH), but it was only specifically made for US and EU, so JP and SH might not work, the seq64 exe path points directly to the seq64_console.exe

## Actually using the damn thing
### LMMS Sound Stuff
This will be a bit complicated, but once you've used it a couple times, it should be a pretty straightforward process.

First in LMMS, you should remove any tracks from the default project, so you only have either the sample or soundfont that you are playing.

Inside of LMMS, if you have the soundfont, you can play it by adding an SF2 Player from the Instrument Plugins list, and load the SM64 Soundfont from earlier

Alternatively, you can load the .aiff files from the decomp directly into the AudioFileProcessor plugin, but these usually sound a bit off from what's actually in game

Find the sound you want to use and begin creating music with it.

### SM64 Sound Stuff
Now here's the crazy stuff, you need to find the sound bank the level you are saving over uses, you can find this by opening the sequences.json from the 
sound/sequences folder. (For example, Bob-Omb Battlefield plays 03_level_Grass, which loads sound bank 22) Then, open the corresponding sound bank file from 
sound/sound_banks (Since BOB uses bank 22, I'll open 22.json). In here, you can see a list of all instruments used in this level, for example, BOB looks like 
```
    "instruments": {
        "inst0": {
            "release_rate": 208,
            "envelope": "envelope0",
            "sound": "19_brass"
        },
        "inst1": {
            "release_rate": 208,
            "envelope": "envelope1",
            "sound": "1A_slap_bass"
        },
        "inst2": {
            "release_rate": 128,
            "envelope": "envelope2",
            "sound": "1B_organ_2"
        },
        "inst3": {
            "release_rate": 208,
            "envelope": "envelope3",
            "sound": "1C"
        },
        "percussion": [
            // bunch of stuff in here
        ],
        "inst4": {
            "release_rate": 10,
            "normal_range_lo": 24,
            "envelope": "envelope5",
            "sound_lo": "0E_hihat_closed",
            "sound": "0F_hihat_open"
        },
        "inst5": {
            "release_rate": 10,
            "normal_range_lo": 28,
            "normal_range_hi": 28,
            "envelope": "envelope6",
            "sound_lo": "10_cymbal_bell",
            "sound": "11_splash_cymbal",
            "sound_hi": "10_cymbal_bell"
        }
    },
    "instrument_list": [
        "inst0",
        null,
        null,
        null,
        null,
        null,
        "inst1",
        "inst2",
        "inst3",
        null,
        "inst4",
        "inst5"
    ]
```
The main things we care about are finding the instruments we use, so if we use a trumpet, inst0 is the one we want, if it's a hihat, inst4 is what we want, etc. 
Then, look for that instrument in the instrument_list, and take note of the index. For inst0, that's index 0, but inst4 is index 11.

Back in LMMS, rename the track of your midi, and add a (Patch {value}) where {value} is the same index as your instrument. inst0 was 0, so the track 
that used trumpets could be named Trumpets (Patch 0) for instance, and there could also be a track called Hihat (Patch 11). 

After all of these have been renamed, we can now export to midi by doing File -> Export Midi..., and saving in the same folder as LmmsToM64.

### LmmsToM64
Finally, open a terminal in the folder of this tool, and run
> python -u main.py {your_midi.mid} {output_file.m64}

For example, if I was editing BOB's theme, I would run
> python -u main.py bob_theme.mid 03_level_grass.m64

This automatically patches it into your decomp folder from settings.cfg, so all you have to do is rebuild your decomp.

