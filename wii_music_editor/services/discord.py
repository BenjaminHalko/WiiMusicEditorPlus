import time

from pypresence import Presence, DiscordNotFound

from wii_music_editor.utils.save import load_setting
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


def DiscordUpdate(state: int):
    if using_discord:
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
            tr("Discord", "Importing Changes")]
        try:
            discord_presence.update(state=state_list[state], large_image="logo", start=start_time)
        except Exception as e:
            print("Error updating discord presence:", e)


start_time = int(time.time())
discord_presence = Presence("932356297704226817")
using_discord = load_setting("Settings", "Discord", True)
if using_discord:
    try:
        discord_presence.connect()
        DiscordUpdate(DiscordState.ModdingWiiMusic)
    except DiscordNotFound:
        using_discord = False
