class RegionType:
    US = 0
    Europe = 1
    Japan = 2
    Korea = 3


class LanguageType:
    English = 0
    French = 1
    Spanish = 2
    German = 3
    Italian = 4
    Japanese = 5
    Korean = 6


region_messages = (
    ("US", "FU", "SU"),
    ("EN", "FR", "SP", "GE", "IT"),
    "JP",
    "KR"
)


def get_message_type(region: int, language: int) -> str:
    if region >= 2:
        return region_messages[region]
    language = min(language, len(region_messages[region]) - 1)
    return region_messages[region][language]


game_ids = [
    "R64E01",
    "R64P01",
    "R64J01",
    "R64K01"
]

dolphin_save_ids = [
    "52363445",
    "52363450",
    "5236344a",
    "5236344b"
]
