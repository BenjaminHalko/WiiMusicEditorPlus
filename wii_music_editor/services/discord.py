import time

from pypresence import Presence, DiscordNotFound

from wii_music_editor.utils.preferences import preferences
from wii_music_editor.ui.widgets.translate import tr


class DiscordState:
    Settings = 0
    ModdingWiiMusic = 1
    EditingSongs = 2
    EditingStyles = 3
    EditingText = 4
    EditingDefaultStyles = 5
    RemovingSongs = 6
    EditingSounds = 7
    CreatingRiivolutionPatch = 8
    RevertingChanges = 9
    PackingRom = 10
    ImportingChanges = 11


class DiscordPresence:
    state: int = DiscordState.ModdingWiiMusic
    __start_time: int
    __discord_presence: Presence
    __active = False

    def __init__(self):
        self.__start_time = int(time.time())
        self.__discord_presence = Presence("932356297704226817")
        if preferences.using_discord:
            self.connect()

    def connect(self):
        try:
            self.__discord_presence.connect()
            self.update(DiscordState.ModdingWiiMusic)
            self.__active = True
        except DiscordNotFound:
            pass

    def disconnect(self):
        self.__active = False
        self.__discord_presence.close()

    def update(self, state: int):
        self.state = state
        if self.__active:
            state_list = [
                tr("Discord", "Changing Settings"),
                tr("Discord", "Modding Wii Music"),
                tr("Discord", "Editing Songs"),
                tr("Discord", "Editing Styles"),
                tr("Discord", "Editing Text"),
                tr("Discord", "Editing Default Styles"),
                tr("Discord", "Removing Songs"),
                tr("Discord", "Editing Sounds"),
                tr("Discord", "Creating Riivolution Patch"),
                tr("Discord", "Reverting Changes"),
                tr("Discord", "Packing Rom"),
                tr("Discord", "Importing Changes")
            ]
            try:
                self.__discord_presence.update(state=state_list[state], large_image="logo", start=self.__start_time)
            except Exception as e:
                print("Error updating discord presence:", e)


discord_presence = DiscordPresence()