import logging

import click
from tabulate import tabulate

from . import data, tvdb

logger = logging.getLogger(__name__)


def print_table(series):
    print(
        tabulate(
            [
                [
                    s.id,
                    s.name,
                    s.seen,
                    s.find_available(),
                    s.next_on_air(),
                    s.status,
                    s.category,
                ]
                for s in series
            ],
            headers=[
                "TVDB ID",
                "Series",
                "Last seen",
                "Available",
                "Next on air",
                "Status",
                "Category",
            ],
        )
    )


def identify_series(query, series_list):
    try:
        return [s for s in series_list if s.id == int(query)][0]
    except ValueError:
        return [s for s in series_list if query.lower() in s.name.lower()][0]


@click.group()
def cli():
    pass


@cli.command(help="search for series by name in thetvdb")
@click.argument("query", nargs=-1)
def search(query):
    for result in tvdb.search(query):
        print(f"{result['id']}: {result['seriesName']} ({result['status']})")
        print(f"  {result['overview']}")
        print()


@cli.command(help="list tracked series")
@click.option("-a", "--all", is_flag=True, help="ignore filters")
@click.option(
    "-c", "--category", default="active", help="filter by category (default: active)"
)
@click.option("-n", "--name", help="filter by series name")
@click.option("-i", "--id", type=int, help="filter by tvdb id")
def list(all, category, name, id):
    series = data.load()
    if not all and category:
        series = [s for s in series if s.category.lower() == category.lower()]
    if not all and name:
        series = [s for s in series if name.lower() in s.name.lower()]
    if not all and id:
        series = [s for s in series if s.id == id]
    print_table(series)


@cli.command(help="sync episode data from thetvdb api")
@click.option("-c", "--category", help="filter by category")
@click.option("-n", "--name", help="filter by series name")
@click.option("-i", "--id", type=int, help="filter by tvdb id")
def sync(category, name, id):
    series_list = data.load()
    series_filtered = series_list.copy()

    if category:
        series_filtered = [
            s for s in series_filtered if s.category.lower() == category.lower()
        ]
    if name:
        series_filtered = [s for s in series_filtered if name.lower() in s.name.lower()]
    if id:
        series_filtered = [s for s in series_filtered if s.id == id]

    for i, series in enumerate(series_filtered, 1):
        print(f"{series.name} ({i}/{len(series_filtered)})")
        series.synchronize()

    data.save(series_list)


@cli.command(help="add new series")
@click.argument("series_id", type=int)
def add(series_id):
    print(f"Looking up series by id {series_id}")

    series_list = data.load()
    if any(s.id == series_id for s in series_list):
        print(f"Series {series_id} is already being tracked")
        exit()

    series = data.Series.new(series_id)
    series_list.append(series)
    data.save(series_list)
    print(f"Added series {series.name} with default category {series.category}")


@cli.command(help="set last seen episode for given series")
@click.argument("series", nargs=-1)
@click.argument("episode")
def seen(series, episode):
    series_list = data.load()
    series = identify_series(" ".join(series), series_list)

    if episode.lower() == "next":
        if not series.seen:
            seen_episode = data.Episode(1, 1)
        else:
            seen_episode = data.Episode(*data.parse_episode(series.seen))
            index = series.episodes.index(seen_episode)
            try:
                seen_episode = series.episodes[index + 1]
            except IndexError:
                print(f"{seen_episode} is the last episode in {series.name}")
                exit()
    else:
        seen_episode = data.Episode(*data.parse_episode(episode.upper()))

    if not any([seen_episode == e for e in series.episodes]):
        print(f"{series.name} does not have an episode {seen_episode}")
        exit()

    series.seen = str(seen_episode)
    data.save(series_list)
    print_table([series])


@cli.command(help="set category for given series")
@click.argument("series", nargs=-1)
@click.argument("category")
def category(series, category):
    series_list = data.load()
    series = identify_series(" ".join(series), series_list)
    series.category = category
    data.save(series_list)
    print_table([series])


@cli.command(help="list available episodes for given series")
@click.argument("series", nargs=-1)
def episodes(series):
    series = identify_series(" ".join(series), data.load())

    height = max(e.episode for e in series.episodes)
    width = max(e.season for e in series.episodes)
    table = [[""] * width for _ in range(height)]
    for episode in series.episodes:
        description = f"{episode} ({episode.aired})"
        if str(episode) == series.seen:
            description = f"{description} *seen*"
        table[episode.episode - 1][episode.season - 1] = description

    print(tabulate(table, headers=[f"Season {n + 1}" for n in range(len(table))]))
