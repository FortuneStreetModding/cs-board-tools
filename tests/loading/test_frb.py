from cs_board_tools.io import read_frb
from cs_board_tools.schema.frb import LoopingMode, SquareType


def test_reading_frb():
    filename = "WiiU.frb"
    frb = read_frb(f"./tests/artifacts/{filename}")

    assert len(frb.squares) == 55

    assert frb.squares[0].square_type == SquareType.Bank

    assert frb.squares[43].district_destination_id == 4
    assert frb.squares[43].price == 36
    assert frb.squares[43].shop_model == 21
    assert frb.squares[43].square_type == SquareType.Property
    assert frb.squares[43].value == 210
    assert frb.squares[43].positionX == 448
    assert frb.squares[43].positionY == 80

    assert frb.board_info.base_salary == 350
    assert frb.board_info.galaxy_status == LoopingMode.NONE
    assert frb.board_info.max_dice_roll == 7
    assert frb.board_info.salary_increment == 200
    assert frb.board_info.version_flag == 3
