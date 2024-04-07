import logging
from math import ceil, floor
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

import mido
from pretty_midi import pretty_midi

from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.shell import run_shell


class Midi:
    midi_path: Path
    suffix: str
    data: bytearray
    length: int
    tempo: int = 0
    time_signature: int = 4

    def __init__(self, path: Path or None):
        if path is not None:
            self.midi_path = path
            self.suffix = self.midi_path.suffix
            if self.suffix == '.mid':
                self.suffix = '.midi'
            with TemporaryDirectory() as directory:
                copyfile(self.midi_path, directory + '/z' + self.suffix)
                self.convert(directory)
        else:
            self.data = bytearray()

    def convert(self, directory: str):
        if Path(directory + '/z.rseq').is_file():
            run_shell([
                paths.include / 'sequence_cmd' / 'GotaSequenceCmd',
                'assemble', Path(directory) / 'z.rseq'
            ])
        if Path(directory + '/z.brseq').is_file():
            run_shell([
                paths.include / 'sequence_cmd' / 'GotaSequenceCmd',
                'to_midi', Path(directory) / 'z.brseq'
            ])
        else:
            run_shell([
                paths.include / 'sequence_cmd' / 'GotaSequenceCmd',
                'from_midi', Path(directory) / 'z.midi'
            ])

        mid = mido.MidiFile(directory + "/z.midi")
        for msg in mid.tracks[0]:
            if msg.type == 'set_tempo':
                self.tempo = floor(mido.tempo2bpm(msg.tempo))
            elif msg.type == 'time_signature':
                self.time_signature = msg.numerator
        self.length = ceil(mid.length * self.tempo / 60)
        with open(directory + "/z.brseq", "rb") as Brseq:
            self.data = bytearray(Brseq.read())

    def normalize(self):
        with TemporaryDirectory() as directory:
            save_path = directory + "/z.midi"
            mid = mido.MidiFile(self.midi_path)
            for track in mid.tracks:
                for num, msg in enumerate(track):
                    try:
                        if not msg.is_meta and msg.channel != 0:
                            track[num] = msg.copy(channel=0)
                    except Exception as e:
                        print("Error:", str(e))
            mid.save(save_path)
            midi_data = pretty_midi.PrettyMIDI(save_path)
            new_midi = pretty_midi.PrettyMIDI(initial_tempo=self.tempo, resolution=2000)
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
                        track[i] = mido.Message("note_off", note=track[i].note, velocity=track[i].velocity,
                                                time=track[i].time,
                                                channel=track[i].channel)
            mid.save(save_path)
            self.convert(directory)
