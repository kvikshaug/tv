# tv

tv is a lightweight CLI application that helps you manage your favorite TV series.

By utilizing the exhaustive TV series database at [thetvdb.com](https://www.thetvdb.com/), the client lets you manage and categorize a list of your favorite tv series, keep track of which episodes you've seen, and see when the next episode is airing.

## Getting started

Install the package from pypi:

```
$ pip install tv-series
```

Run `init` to initialize the application. You will be asked for an API key which you can generate on [thetvdb.com](https://www.thetvdb.com/).

```
$ tv init
```

To add your first series, first use `search` to find your series by its name.

```
$ tv search dexter
79349: Dexter (Ended)
  Dexter Morgan is a Miami-based blood splatter expert who doesn't just solve murders; he commits them too. In fact, he's a serial killer -- but he only murders the guilty, so he feels justified with his lifestyle choices. His policewoman sister and his cop co-workers have no idea Dexter lives a double life; however, adoptive father Harry knows his secret, and does, in fact, help Dexter hone his "skills." It's a unique brand of justice for which charming Dexter feels a psychological hunger.

356343: Dexter: Early Cuts (Ended)
  Animated web series providing background and depth to Dexter's character and relationships.
```

Use the numeric ID to `add` the series you were looking for.

```
$ tv add 79349
Looking up series by id 79349
Added series Dexter with default category default
```

Now you can see your series using `list`. It shows that there are 96 episodes available to watch.

```
$ tv list -c default
  TVDB ID  Series    Last seen    Available          Next on air    Status
---------  --------  -----------  -----------------  -------------  --------
    79349  Dexter                 S01E01 (96 total)  -              Ended
```

Let's show a different example. Below, you can see that:

* You've seen the first season of The Orville, but there is one more season available with 14 episodes
* You've seen all of Fool Us, but the next episode will be available June 24th
* You've finished The Wire and there will be no more episodes

```
$ tv list -a
  TVDB ID  Series                   Last seen    Available            Next on air          Status
---------  -----------------------  -----------  -------------------  -------------------  ----------
   328487  The Orville              S01E12       S02E01 (14 total)    -                    Continuing
   239851  Penn & Teller: Fool Us   S06E01       -                    S06E02 (2019-06-24)  Continuing
    79126  The Wire                 S05E10       -                    -                    Ended
```

To read more about the available features, try `tv --help`.

### Files

Data and configuration is stored according to the [XDG base dir spec](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html), which usually means `~/.local/share/tv.series.json` and `~/.config/tv.config.json`, respectively.

## Development

Prerequisites: Python 3 and pip. To install development tools, include the `dev` extras:

```
$ pip install -e ".[dev]"
```

### Testing

```
$ pytest
```

### Code style

The source code must adhere to the rules of [Black](https://black.readthedocs.io/en/stable/), [flake8](https://gitlab.com/pycqa/flake8) and [isort](https://github.com/timothycrosley/isort).

```
$ black --check src tests
$ flake8 src tests
$ isort --recursive --check-only src tests
```
