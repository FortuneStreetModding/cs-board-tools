from cs_board_tools.io import read_zip
from cs_board_tools.validation import validate_bundle


def test_validation():
    filename = "WiiU.zip"
    bundles = read_zip(
        f"./tests/artifacts/{filename}",
        temp_dir_path="./tests/artifacts"
    )
    result = validate_bundle(bundles)

    for b in result.boards:
        assert b.board_configuration.status == "OK"
        assert b.consistency.status == "OK"
        assert b.icon.status == "OK"
        assert b.max_paths.status == "OK"
        assert b.screenshots.status == "OK"
        assert b.venture.status == "OK"
        assert result.issue_count == 0
