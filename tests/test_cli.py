from click.testing import CliRunner

from tv import tv


def test_search(mock_tvdb_client):
    runner = CliRunner()
    result = runner.invoke(tv.search, "foobar")
    if result.exception:
        raise result.exception
    assert result.exit_code == 0


def test_list(mock_data_file):
    runner = CliRunner()
    result = runner.invoke(tv.list)
    if result.exception:
        raise result.exception
    assert result.exit_code == 0
    assert "Moscow Noir" in result.output


def test_list_archived(mock_data_file):
    runner = CliRunner()
    result = runner.invoke(tv.list, ["-c", "archived"])
    if result.exception:
        raise result.exception
    assert result.exit_code == 0
    assert "Game of Thrones" in result.output


def test_set(mock_data_file):
    runner = CliRunner()
    result = runner.invoke(tv.set, ["-c", "default", "-s", "S01E02", "moscow", "noir"])
    if result.exception:
        raise result.exception
    assert result.exit_code == 0


def test_seen(mock_data_file):
    runner = CliRunner()
    result = runner.invoke(tv.seen, ["moscow", "noir"])
    if result.exception:
        raise result.exception
    assert result.exit_code == 0


def test_episodes(mock_data_file):
    runner = CliRunner()
    result = runner.invoke(tv.episodes, ["moscow", "noir"])
    if result.exception:
        raise result.exception
    assert result.exit_code == 0
