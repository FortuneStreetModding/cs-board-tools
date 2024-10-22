"""All the classes that make up Map Descriptors -- including
the MapDescriptor class itself -- live in this module.
"""
from dataclasses import dataclass, field
from cs_board_tools.schema.validation import CheckResult
from cs_board_tools.utilities import (
    load_yaml,
    load_yaml_schema,
)
from ruamel.yaml import YAML
yaml = YAML()

@dataclass
class AuthorInfo:
    """A dataclass holding an author's name
    and homepage information."""
    name: str = field(default="")
    url: str = field(default="")


@dataclass
class ChangeLogEntry:
    """A dataclass holding the changelog information.
    Each entry will have a version, as well as messages
    describing what has been added, changed, or removed."""
    version: int = field(default="")
    added: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)


@dataclass
class CustomMusic:
    """A dataclass holding the board's music information.
    There are strings or lists for every possible configuration
    option, including download links, multiple map themes, and
    themes for specific events."""
    # download url(s)
    download: list[str] = field(default_factory=list)

    # primary theme
    map: list[str] = field(default_factory=list)

    # secondary themes
    auction: str = field(default="")
    stock: str = field(default="")
    venture_cards: str = field(default="")

    # guests
    guest_appear: str = field(default="")
    guest_leave: str = field(default="")

    # promotions
    promotion_mii: str = field(default="")
    promotion_mario: str = field(default="")
    promotion_dragon_quest: str = field(default="")

    # game events
    bad_venture_card: str = field(default="")
    bankruptcy: str = field(default="")
    domination: str = field(default="")
    forced_buyout: str = field(default="")
    take_a_break: str = field(default="")
    target_met: str = field(default="")
    win: str = field(default="")

    # minigames
    dart_of_gold: str = field(default="")
    memory_block: str = field(default="")
    round_the_blocks: str = field(default="")
    round_the_blocks_win: str = field(default="")
    round_the_blocks_777: str = field(default="")
    slurpodrome_select: str = field(default="")
    slurpodrome_start: str = field(default="")
    slurpodrome_race: str = field(default="")
    slurpodrome_win: str = field(default="")


@dataclass
class Description:
    """A dataclass holding description information.
    Like the Name class, there are separate attributes
    here for each language."""
    en: str = field(default="")
    de: str = field(default="")
    fr: str = field(default="")
    it: str = field(default="")
    jp: str = field(default="")
    es: str = field(default="")


@dataclass
class DistrictNames:
    """A dataclass holding District Name information.

    There are separate attributes per language, each lists of strings.
    """
    en: list[str] = field(default_factory=list)
    de: list[str] = field(default_factory=list)
    fr: list[str] = field(default_factory=list)
    it: list[str] = field(default_factory=list)
    jp: list[str] = field(default_factory=list)
    es: list[str] = field(default_factory=list)


@dataclass
class LoopingInfo:
    """A dataclass holding Looping configuration.

    This determines whether the board abides by Galaxy-style gravity and
    presentation or not. There are separate attributes for mode, radius,
    horizontal padding, and vertical square count.
    """
    mode: str = field(default="None")
    radius: int = 0
    horizontal_padding: int = 0
    vertical_square_count: int = 0


@dataclass
class Name:
    """A dataclass holding board's Name information.

    Like the Description class, there are separate attributes here for
    each language.
    """
    en: str = field(default="")
    de: str = field(default="")
    fr: str = field(default="")
    it: str = field(default="")
    jp: str = field(default="")
    es: str = field(default="")


@dataclass
class ShopNames:
    """A dataclass holding Shop Name information. There are separate
    attributes per language, each lists of strings.
    """
    en: list[str] = field(default_factory=list)
    de: list[str] = field(default_factory=list)
    fr: list[str] = field(default_factory=list)
    it: list[str] = field(default_factory=list)
    jp: list[str] = field(default_factory=list)
    es: list[str] = field(default_factory=list)


@dataclass
class SwitchRotationOriginPoints:
    """A dataclass holding information relating to the Switch's
    Rotation Origin Points.

    Effectively, if you want your districts to rotate like they
    do in the Colossus board, set these to the center of the points
    they should rotate around.

    This class holds only one coordinate, but the MapDescriptor object
    holds list[SwitchRotationOriginPoints]. (Think about how Colossus
    rotates both on the left side and the right side -- it has two
    switch rotation origin points.)
    """
    x: int = 0
    y: int = 0


@dataclass
class TourModeInfo:
    """A dataclass holding information relating to the board's
    Tour Mode settings.

    These include the three designated opponents, the initial
    cash and bankruptcy limit settings, as well as the clear rank.
    """
    bankruptcy_limit: int = 1
    clear_rank: int = 1
    opponent_1: str = field(default="Mario")
    opponent_2: str = field(default="Luigi")
    opponent_3: str = field(default="Toad")


@dataclass
class VentureCardInfo:
    """A dataclass holding Venture Card information.

    numbers is a list containing every enabled Venture Card,
    and count is the number of enabled cards.
    """
    count: int = 0
    numbers: list[int] = field(default_factory=list)


@dataclass
class MapDescriptor:
    """This class represents the .yaml object, the Map
    Descriptor.

    It contains extended-level preferences for game boards,
    such as which Background to use, custom music entries,
    which Venture Cards should be enabled, and more. This is
    the main returnable when loading just a .yaml file, but
    when loading a full Board Bundle, this is returned as an
    element in the larger bundle -- bundle.descriptor.
    """
    # name and description in the various languages
    name: Name = field(default_factory=Name)
    description: Description = field(default_factory=Description)
    rule_set: str = field(default="")
    theme: str = field(default="")
    initial_cash: str = field(default="")
    target_amount: str = field(default="")
    base_salary: str = field(default="")
    salary_increment: str = field(default="")
    max_dice_roll: str = field(default="")
    frbs: list[str] = field(default_factory=list)
    background: str = field(default="")
    switch_rotation_origin_points: list[SwitchRotationOriginPoints] = field(
        default_factory=list
    )
    icon: str = field(default="")
    music: CustomMusic = field(default_factory=CustomMusic)
    looping: LoopingInfo = field(default_factory=LoopingInfo)
    tour_mode: TourModeInfo = field(default_factory=TourModeInfo)
    changelog: list[ChangeLogEntry] = field(default_factory=list)
    authors: list[AuthorInfo] = field(default_factory=list)
    venture_cards: VentureCardInfo = field(default_factory=VentureCardInfo)

    # District and Shop Names
    district_names: DistrictNames = field(default_factory=DistrictNames)
    shop_names: ShopNames = field(default_factory=ShopNames)

    # Extra Info
    notes: str = field(default="")
    tags: list[str] = field(default_factory=list)
    yaml_validation_results: CheckResult = field(default_factory=CheckResult)


def build_map_descriptor_object(yaml_filename) -> MapDescriptor:
    """
    This function takes in the filename of a .yaml Map Descriptor
    file and returns a MapDescriptor object with all of the data
    easily accessible as Pythonic attributes.

    :param yaml_filename: A filename for a .yaml Map Descriptor
        file. (For example, WiiU.yaml)
    :type yaml_filename: str
    :return: Returns a MapDescriptor object containing all of the
        data from the .yaml file.
    :rtype: MapDescriptor
    """
    yaml_schema = load_yaml_schema()
    results = load_yaml(yaml_filename, yaml_schema)
    d = MapDescriptor()
    yaml = results[0]
    if not yaml:
        d.yaml_validation_results = results[1]
        return d
    d.yaml_validation_results = results[1]
    if "authors" in yaml:
        for a in yaml["authors"]:
            if "name" in a:
                a_info = AuthorInfo()
                a_info.name = a["name"]
                if "url" in a:
                    a_info.url
                d.authors.append(a_info)
            else:
                a_info = AuthorInfo()
                a_info.name = a
                d.authors.append(a_info)

    d.background = yaml["background"]
    d.base_salary = yaml["baseSalary"]

    if "changelog" in yaml:
        entries = []
        for c in yaml["changelog"]:
            entry = ChangeLogEntry()
            entry.added = c.get("added")
            entry.changed = c.get("changed")
            entry.removed = c.get("removed")
            entry.version = c.get("version")
            entries.append(entry)
        d.changelog = entries

    if "desc" in yaml:
        desc = Description()
        desc.en = yaml["desc"].get("en")
        desc.de = yaml["desc"].get("de")
        desc.fr = yaml["desc"].get("fr")
        desc.it = yaml["desc"].get("it")
        desc.jp = yaml["desc"].get("jp")
        desc.es = yaml["desc"].get("es")
        d.description = desc

    frbs = []
    if "frbFile1" in yaml:
        frbs.append(yaml["frbFile1"])
    if "frbFile2" in yaml:
        frbs.append(yaml["frbFile2"])
    if "frbFile3" in yaml:
        frbs.append(yaml["frbFile3"])
    if "frbFile4" in yaml:
        frbs.append(yaml["frbFile4"])

    if "frbFiles" in yaml:
        frbs = yaml["frbFiles"]
    d.frbs = frbs

    d.icon = yaml.get("mapIcon")
    d.initial_cash = yaml.get("initialCash")

    if "looping" in yaml:
        d.looping = LoopingInfo()
        d.looping.horizontal_padding = (
            yaml["looping"].get("horizontalPadding")
        )
        d.looping.mode = yaml["looping"].get("mode")
        d.looping.radius = yaml["looping"].get("radius")
        d.looping.vertical_square_count = (
            yaml["looping"].get("verticalSquareCount")
        )

    d.max_dice_roll = yaml["maxDiceRoll"]

    music = CustomMusic()
    if "music" in yaml:
        music.download = []
        music.map = []
        # things that could either be a string or a list
        if "download" in yaml["music"] and \
           yaml["music"].get("download") is not None:
            if isinstance(yaml["music"]["download"], str):
                music.download.append(yaml["music"].get("download"))
            else:
                music.download.extend(yaml["music"].get("download"))

        if "map" in yaml["music"] and \
           yaml["music"].get("map") is not None:
            if isinstance(yaml["music"]["map"], str):
                music.map.append(yaml["music"].get("map"))
            else:  # ...or if it's a list, use extend instead.
                music.map.extend(yaml["music"].get("map"))

        # now back to our regularly scheduled strings
        music.auction = yaml["music"].get("auction")
        music.stock = yaml["music"].get("stock")
        music.venture_cards = yaml["music"].get("ventureCards")

        music.guest_appear = yaml["music"].get("guestAppear")
        music.guest_leave = yaml["music"].get("guestLeave")

        music.promotion_dragon_quest = (
            yaml["music"].get("promotionDragonQuest")
        )
        music.promotion_mario = yaml["music"].get("promotionMario")
        music.promotion_mii = yaml["music"].get("promotionMii")

        music.bad_venture_card = yaml["music"].get("badVentureCard")
        music.bankruptcy = yaml["music"].get("bankruptcy")
        music.domination = yaml["music"].get("domination")
        music.forced_buyout = yaml["music"].get("forcedBuyout")
        music.take_a_break = yaml["music"].get("takeAbreak")
        music.target_met = yaml["music"].get("targetMet")
        music.win = yaml["music"].get("win")

        music.dart_of_gold = yaml["music"].get("dartOfGold")
        music.memory_block = yaml["music"].get("memoryBlock")
        music.round_the_blocks = yaml["music"].get("roundTheBlocks")
        music.round_the_blocks_777 = yaml["music"].get("roundTheBlocks777")
        music.round_the_blocks_win = yaml["music"].get("roundTheBlocksWin")
        music.slurpodrome_race = yaml["music"].get("slurpodromeRace")
        music.slurpodrome_select = yaml["music"].get("slurpodromeSelect")
        music.slurpodrome_start = yaml["music"].get("slurpodromeStart")
        music.slurpodrome_win = yaml["music"].get("slurpodromeWin")
    d.music = music

    if "name" in yaml:
        name = Name()
        name.en = yaml["name"].get("en")
        name.de = yaml["name"].get("de")
        name.fr = yaml["name"].get("fr")
        name.it = yaml["name"].get("it")
        name.jp = yaml["name"].get("jp")
        name.es = yaml["name"].get("es")
        d.name = name

    d.notes = yaml.get("notes")
    d.rule_set = yaml.get("ruleSet")
    d.salary_increment = yaml.get("salaryIncrement")

    if "shopNames" in yaml:
        shop_names = ShopNames()
        shop_names.en = yaml["shopNames"].get("en")
        shop_names.de = yaml["shopNames"].get("de")
        shop_names.fr = yaml["shopNames"].get("fr")
        shop_names.it = yaml["shopNames"].get("it")
        shop_names.jp = yaml["shopNames"].get("jp")
        shop_names.es = yaml["shopNames"].get("es")
        d.shop_names = shop_names

    if "SwitchRotationOriginPoints" in yaml:
        points = SwitchRotationOriginPoints()
        points.x = yaml["SwitchRotationOriginPoints"].get("x")
        points.y = yaml["SwitchRotationOriginPoints"].get("y")
        d.switch_rotation_origin_points = points

    if "tags" in yaml:
        d.tags.extend(yaml["tags"])

    d.target_amount = yaml["targetAmount"]
    d.theme = yaml["theme"]

    if "tourMode" in yaml:
        tour_mode = TourModeInfo()
        tour_mode.bankruptcy_limit = yaml["tourMode"].get("bankruptcyLimit")
        tour_mode.clear_rank = yaml["tourMode"].get("clearRank")
        tour_mode.opponent_1 = yaml["tourMode"].get("opponent1")
        tour_mode.opponent_2 = yaml["tourMode"].get("opponent2")
        tour_mode.opponent_3 = yaml["tourMode"].get("opponent3")
        d.tour_mode = tour_mode

    if "ventureCards" in yaml:
        cards = VentureCardInfo()
        for i, card in enumerate(yaml["ventureCards"]):
            cards.count += card
            if card == 1:
                cards.numbers.append(i + 1)
        d.venture_cards = cards

    return d
