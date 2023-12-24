from cs_board_tools.io import read_zip
from cs_board_tools.validation import validate_bundle


def test_validation():
    filename = "WiiU.zip"
    bundles = read_zip(
        f"./tests/artifacts/{filename}",
        temp_dir_path="./tests/artifacts"
    )
    result = validate_bundle(bundles)

    assert result.boards[0].door.status == "OK"
    assert result.boards[0].consistency.status == "OK"
    assert result.boards[0].venture.status == "OK"
    assert result.boards[0].max_paths.status == "OK"
    assert result.boards[0].screenshots.status == "OK"
    assert result.issue_count == 0
