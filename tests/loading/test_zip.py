from cs_board_tools.io import read_zip
from cs_board_tools.schema.frb import LoopingMode, SquareType


def test_reading_zip_file():
    filename = "WiiU.zip"
    bundles = read_zip(
        f"./tests/artifacts/{filename}",
        temp_dir_path="./tests/artifacts"
    )
    board_bundle = bundles[0]
    # General Map Bundle properties
    # General Map Bundle properties
    assert board_bundle.name.en == "Wii U"
    assert board_bundle.description.en == (
        "The Wii U had a plethora of wonderful games. Its eShop finally "
        "went offline on March 27th, 2023, giving it a lifespan of over "
        "10 years."
    )
    assert board_bundle.description.es == (
        "La Wii U tenía una plétora de juegos maravillosos. Su eShop "
        "finalmente se desconectó el 27 de marzo de 2023, lo que le dio "
        "una vida útil de más de 10 años."
    )
    assert board_bundle.description.de == (
        "Die Wii U hatte eine Fülle wunderbarer Spiele. Sein eShop ging "
        "schließlich am 27. März 2023 offline, was ihm eine Lebensdauer "
        "von über 10 Jahren verleiht."
    )
    assert board_bundle.description.fr == (
        "La Wii U avait une pléthore de jeux merveilleux. Son eShop "
        "s'est finalement déconnecté le 27 mars 2023, lui donnant une "
        "durée de vie de plus de 10 ans."
    )
    assert board_bundle.description.jp == (
        "Wii Uには素晴らしいゲームがたくさんありました。 その eShop は 2023 年 "
        "3 月 27 日についにオフラインになり、10 年以上の寿命を迎えました。"
    )
    assert board_bundle.authors[0].name == "nikkums"
    assert board_bundle.background == "grid_blue"
    assert board_bundle.screenshots[0] == "./tests/artifacts/WiiU/WiiU.webp"
    # Map Descriptor values
    assert board_bundle.descriptor.authors[0].name == "nikkums"
    assert board_bundle.descriptor.background == "grid_blue"
    assert board_bundle.descriptor.base_salary == 350
    assert board_bundle.descriptor.changelog[0].version == 2
    assert board_bundle.descriptor.icon == "WiiU"
    assert board_bundle.descriptor.rule_set == "Standard"
    assert board_bundle.descriptor.theme == "Mario"
    assert board_bundle.descriptor.tour_mode.bankruptcy_limit == 3
    assert board_bundle.descriptor.tour_mode.opponent_1 == "Luigi"
    assert board_bundle.descriptor.tour_mode.opponent_2 == "Peach"
    assert board_bundle.descriptor.tour_mode.opponent_3 == "Toad"
    assert board_bundle.descriptor.venture_cards.count == 64
    # Specific square's values
    assert board_bundle.frbs[0].squares[0].square_type == SquareType.Bank
    # Square 43, picked at random
    assert board_bundle.frbs[0].squares[43].district_destination_id == 4
    assert board_bundle.frbs[0].squares[43].price == 36
    assert board_bundle.frbs[0].squares[43].shop_model == 21
    assert board_bundle.frbs[0].squares[43].square_type == SquareType.Property
    assert board_bundle.frbs[0].squares[43].value == 210
    assert board_bundle.frbs[0].squares[43].positionX == 448
    assert board_bundle.frbs[0].squares[43].positionY == 80
    # .frb board info
    assert board_bundle.frbs[0].board_info.base_salary == 350
    assert board_bundle.frbs[0].board_info.galaxy_status == LoopingMode.NONE
    assert board_bundle.frbs[0].board_info.max_dice_roll == 8
    assert board_bundle.frbs[0].board_info.salary_increment == 200
    assert board_bundle.frbs[0].board_info.version_flag == 3
    # .frb number of squares
    assert len(board_bundle.frbs[0].squares) == 55
    # .frb filenames
    assert board_bundle.frb_filenames[0] == "./tests/artifacts/WiiU/WiiU.frb"
    # Music filenames
    assert board_bundle.music.auction == "WiiUeShopMay2019.85"
    assert board_bundle.music.bad_venture_card == "Mario3DWorldMiss.75"
    assert board_bundle.music.dart_of_gold == (
        "A_NintendolandMarioChaseSlideHill.75"
    )
    assert board_bundle.music.domination == "WiiUMiiverseJingle.75"
    assert board_bundle.music.download[0] == (
        "https://nikkums.io/cswt/BGM/WiiU.music.zip"
    )
    assert board_bundle.music.download[1] == (
        "https://drive.google.com/u/0/uc?id=1k1fRXR2gTyD35G93W3bA"
        "NxKB4UTQv__6&export=download"
    )
    assert board_bundle.music.map[0] == "WiiUeShopApr2014.70"
    assert board_bundle.music.memory_block == "A_Mario3DWorldAthletic.75"
    assert board_bundle.music.round_the_blocks == (
        "A_Mario3DWorldSuperBellHill.75"
    )
    assert board_bundle.music.round_the_blocks_777 == (
        "Mario3DWorldWorldClear.75"
    )
    assert board_bundle.music.round_the_blocks_win == (
        "Mario3DWorldCourseClear.75"
    )
    assert board_bundle.music.slurpodrome_race == (
        "Mario3DWorldMountMustDash.75"
    )
    assert board_bundle.music.slurpodrome_select == (
        "A_Mario3DWorldSlotMachine.75"
    )
    assert board_bundle.music.slurpodrome_start == (
        "Mario3DWorldMountMustDashIntro.75"
    )
    assert board_bundle.music.slurpodrome_win == (
        "MarioKart8FirstPlaceFinishFanfare.85"
    )
    assert board_bundle.music.stock == "WiiUeShopJan2014.75"
    assert board_bundle.music.take_a_break == (
        "WiiUChatDisconnecting.75"
    )
    assert board_bundle.music.target_met == "WiiUeShopSept2015.75"
    assert board_bundle.music.venture_cards == "WiiUeShopJan2015.75"
    assert board_bundle.music.win == (
        "WiiUChatConnectingAndAmiiboSettings.75"
    )
