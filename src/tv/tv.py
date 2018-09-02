import logging
import sys

from tabulate import tabulate
import requests

from . import data, tvdb


logger = logging.getLogger(__name__)


def print_table(series):
    print(tabulate(
        [[s.id, s.name, s.seen, s.find_available(), s.next_on_air(), s.status, s.category] for s in series],
        headers=["TVDB ID", "Series", "Last seen", "Available", "Next on air", "Status", "Category"]
    ))


def main():
    if len(sys.argv) == 1:
        command = None
    else:
        command = sys.argv[1]

    if command == 'search':
        series_name = ' '.join(sys.argv[2:])
        for result in tvdb.search(series_name):
            print(f"{result['id']}: {result['seriesName']} ({result['status']})")
            print(f"  {result['overview']}")
            print()

    elif command == 'list':
        series = data.load()
        try:
            series = [s for s in series if s.category == sys.argv[2]]
        except IndexError:
            pass
        print_table(series)

    elif command == 'sync':
        series_list = data.load()

        try:
            series_id = int(sys.argv[2])
            for series in series_list:
                if series.id == series_id:
                    print(f"Synchronizing {series.name}")
                    series.synchronize()
        except ValueError:
            category = sys.argv[2]
            print(f"Filtering by category '{category}'")
            filtered_series = [s for s in series_list if s.category == category]
            for i, series in enumerate(filtered_series, 1):
                print(f"Synchronizing: {series.name} ({i}/{len(filtered_series)})")
                series.synchronize()
        except IndexError:
            for i, series in enumerate(series_list, 1):
                print(f"Synchronizing: {series.name} ({i}/{len(series_list)})")
                series.synchronize()

        data.save(series_list)

    elif command == 'add':
        series_id = int(sys.argv[2])
        print(f"Adding series by id {series_id}")

        series_list = data.load()
        if any(s.id == series_id for s in series_list):
            print(f"Series {series_id} is already being tracked")
            exit()

        series = data.Series.new(series_id)
        series_list.append(series)
        data.save(series_list)
        print(f"Added series '{series.name}' with default category 'active'")

    elif command == 'seen':
        series_id = int(sys.argv[2])
        seen_episode_number = sys.argv[3].upper()
        seen_episode = data.Episode(*data.parse_episode(seen_episode_number))
        series_list = data.load()
        series = [s for s in series_list if s.id == series_id][0]
        if not any([seen_episode == e for e in series.episodes]):
            print(f"{series.name} does not have an episode {seen_episode}")
            exit()
        series.seen = str(seen_episode)
        data.save(series_list)
        print_table([series])

    elif command == 'category':
        series_id = int(sys.argv[2])
        category = sys.argv[3]

        series_list = data.load()
        series = [s for s in series_list if s.id == series_id][0]
        series.category = category
        data.save(series_list)
        print_table([series])

    else:
        print("""usage: tv [command]

    tv sync [category|id]        - sync episode data from thetvdb api
    tv list [category]           - list tracked series
    tv search <query>            - search for series by name in thetvdb
    tv add <id>                  - add series to json by tvdb id
    tv seen <id> <episode>       - set last seen episode on the given series id
    tv category <id> <category>  - set category on the given series id""")


if __name__ == '__main__':
    main()
