import pytest

import tv


class TVDBApiResponse:
    def __init__(self, method, *args, **kwargs):
        self.method = method

    def raise_for_status(self):
        pass

    def json(self):
        return {}


@pytest.fixture
def mock_tvdb_client(monkeypatch):
    def mock_load(tvdb):
        pass

    def mock_query_series(tvdb, series_id, language):
        return None, []

    def mock_search(tvdb, series_name):
        return []

    monkeypatch.setattr(tv.tvdb._TVDBClient, "load", mock_load)
    monkeypatch.setattr(tv.tvdb._TVDBClient, "query_series", mock_query_series)
    monkeypatch.setattr(tv.tvdb._TVDBClient, "search", mock_search)


@pytest.fixture
def mock_data_file(monkeypatch):
    def mock_load():
        return [
            tv.data.Series(
                id=1,
                name="Moscow Noir",
                status="Continuing",
                seen="S01E01",
                category="active",
                language="en",
                episodes=[tv.data.Episode(1, 1), tv.data.Episode(1, 2)],
            ),
            tv.data.Series(
                id=1,
                name="Game of Thrones",
                status="Ended",
                seen="S08E06",
                category="archived",
                language="en",
                episodes=[tv.data.Episode(1, 1), tv.data.Episode(1, 2)],
            ),
        ]

    def mock_save(series_list):
        assert all(isinstance(s, tv.data.Series) for s in series_list)

    monkeypatch.setattr(tv.data, "load", mock_load)
    monkeypatch.setattr(tv.data, "save", mock_save)
