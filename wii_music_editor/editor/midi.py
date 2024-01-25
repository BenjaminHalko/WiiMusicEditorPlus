import os
from math import ceil, floor
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

import mido
from pretty_midi import pretty_midi

from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.shell import run_shell


def NormalizeMidi(midi_path, save_path, default_tempo):
    mid = mido.MidiFile(midi_path)
    for track in mid.tracks:
        for num, msg in enumerate(track):
            try:
                if not msg.is_meta and msg.channel != 0:
                    track[num] = msg.copy(channel=0)
            except Exception as e:
                print("Error:", str(e))
    mid.save(save_path)
    midi_data = pretty_midi.PrettyMIDI(save_path)
    new_midi = pretty_midi.PrettyMIDI(initial_tempo=default_tempo, resolution=2000)
    for i, instrument in enumerate(midi_data.instruments):
        new_instrument = pretty_midi.Instrument(program=instrument.program, is_drum=instrument.is_drum,
                                                name="Track" + str(i))
        i += 1
        for note in instrument.notes:
            new_instrument.notes.append(pretty_midi.Note(
                velocity=note.velocity, pitch=note.pitch, start=note.start, end=note.end))
        new_midi.instruments.append(new_instrument)
    new_midi.write(save_path)
    mid = mido.MidiFile(save_path)
    mid.tracks[1] = mido.merge_tracks([mid.tracks[0], mid.tracks[1]])
    mid.tracks.remove(mid.tracks[0])
    for track in mid.tracks:
        for i in range(len(track)):
            if track[i].type == "note_on" and track[i].velocity == 0:
                track[i] = mido.Message("note_off", note=track[i].note, velocity=track[i].velocity, time=track[i].time,
                                        channel=track[i].channel)
    mid.save(save_path)


def LoadMidi(midi_path, default_tempo=-1):
    with TemporaryDirectory() as directory:
        prefix = Path(midi_path).suffix
        if prefix == '.mid':
            prefix = '.midi'
        if default_tempo == -1:
            copyfile(midi_path, directory + '/z' + prefix)
        else:
            NormalizeMidi(midi_path, directory + '/z' + prefix, default_tempo)

        if Path(directory + '/z.rseq').is_file():
            run_shell([
                str(paths.includePath / 'SequenceCmd' / 'GotaSequenceCmd'),
                'assemble', str(Path(directory) / 'z.rseq')])
        if Path(directory + '/z.brseq').is_file():
            run_shell([str(paths.includePath / 'SequenceCmd' / 'GotaSequenceCmd'),
                       'to_midi', str(Path(directory) / 'z.brseq')])
        else:
            run_shell([str(paths.includePath / 'SequenceCmd' / 'GotaSequenceCmd'),
                       'from_midi', str(Path(directory) / 'z.midi')])

        mid = mido.MidiFile(directory + "/z.midi")
        tempo = 0
        time_signature = 4
        for msg in mid.tracks[0]:
            if msg.type == 'set_tempo':
                tempo = floor(mido.tempo2bpm(msg.tempo))
            elif msg.type == 'time_signature':
                time_signature = msg.numerator
        Length = ceil(mid.length * tempo / 60)
        tempo = tempo
        with open(directory + "/z.brseq", "rb") as Brseq:
            Brseq.seek(0)
            info = Brseq.read()
        fileLength = os.stat(directory + "/z.brseq").st_size
    return [info, fileLength, tempo, Length, time_signature]
