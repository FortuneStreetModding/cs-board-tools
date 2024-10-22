from cs_board_tools.io import read_yaml


def test_reading_yaml():
    filename = "WiiU.yaml"
    descriptor = read_yaml(f"./tests/artifacts/{filename}")

    assert descriptor.authors[0].name == "nikkums"
    assert descriptor.background == "grid_blue"
    assert descriptor.base_salary
    assert descriptor.changelog[0].version == 2
    assert descriptor.icon == "WiiU"
    assert descriptor.rule_set == "Standard"
    assert descriptor.theme == "Mario"

    assert descriptor.tour_mode.bankruptcy_limit == 3
    assert descriptor.tour_mode.opponent_1 == "Luigi"
    assert descriptor.tour_mode.opponent_2 == "Peach"
    assert descriptor.tour_mode.opponent_3 == "Toad"

    assert descriptor.venture_cards.count == 64
