# CourtVision 🚧

Estimates the probability an NBA player goes over a prop line, based on how streaky they actually are. *It won't tell you what to bet — it'll tell you what the numbers say, which is a different thing...* 😉 

## Why It exists

Sportsbooks post a line. You get one number to decide against — usually a season average — and that number hides the thing that actually matters.

> Two players both average 24 points. One goes 23, 25, 24, 26. The other goes 8, 40, 12, 36.
>
> Identical averages, wildly different bets. The over on the first guy at 24.5 is close to a coin flip. On the second guy there isn't even an educated guess, that's just gambling... 

Means lie all the time, it's not the better estimate for 'average' in sports, and anyone that's ever taken STATS101 knows that the median is the resistant, more reliable, measure of center. But what most people *don't know* is that **_spread_** tells you whether the over is worth taking. CourtVision runs the same question through different statistical methods so you can see how much the answer depends on which assumptions you make.

## Install:

```bash
git clone https://github.com/mohammadbutt20/CourtVision.git
cd CourtVision
pip install nba_api
```

Python 3.11+. The stats functions are standard library only — `nba_api` is just for pulling game data.

## Usage:

Give it a player's recent scoring and a line:

```python
from stats import prob_over_empirical, prob_over_normal, prob_over_monte_carlo

points = [27, 31, 18, 24, 33, 22, 29, 26]
line = 24.5

prob_over_empirical(points, line)     # 0.625
prob_over_normal(points, line)        # 0.573
prob_over_monte_carlo(points, line)   # 0.571
```

Look up a player's NBA ID by name:

```python
from nba_data import get_player_id

get_player_id("LeBron James")   # 2544
```

> [!CAUTION]
> `get_player_id` raises `PlayerNotFoundError` or `PlayerAmbiguousError`. Type in `"John Doe"` and it'll say there's no one by that name. Type something like `"Thomas"` and it'll tell you to be more specific; or if you search for players with identical legal names,  which happen to be only a handful of people, it will also raise `PlayerAmbiguousError` *(Ex: There are two Mike James, albeit both are inactive...)*

Pull a player's real game log for a season — comes back as typed `GameRow` objects, not raw API dicts:

```python
from nba_data import get_player_games

games = get_player_games(2544, "2025-26")   # LeBron, this season
games[0].points                             # 18
games[0].game_date                          # datetime.date(2026, 4, 12)
```

## How It Works:

Three methods, same question, different assumptions:

| Method | How it works | Best for | Trade-off |
|---|---|---|---|
| **Empirical** | Observational proportion. Counts number of past games that cleared the line | Establishing a basis  | Can't make predictions. Works only on past info |
| **Normal** | Fits a bell curve, reads the CDF (Cumulative Distribution Function) | High-volume stats like points | Assumes symmetry that low stats don't have |
| **Monte Carlo** | Simulates ``'n'`` games and counts the "hits" | What a formula cannot describe | Currently, samples a normal dist. Inaccurate for the moment |


## TODO:

🚧 Under Active Development. Pardon My Dust. 🚧 

- [x] Basic Statistical Methods: Empirical, Normal, & Monte Carlo
- [x] Player name → NBA ID lookup *(with error handling)*
- [x] Live game logs via `nba_api` → typed `GameRow` objects
- [x] SQLite storage for fetched games *(write path)*
- [ ] Cache-aside: freshness check + read path so repeat lookups skip the API
- [ ] CLI
- [ ] MatPlotLib tests / probability plots

<!--  
- [ ] WEBSERVER / BACKEND (FLASK)
- [ ] WEB UI (?) 
- [ ] DEPLOYMENT (VERCEL?)
-->

## Author

Built by [@mohammadbutt20](https://github.com/mohammadbutt20) — a project for understanding the statistics, the data plumbing, and building with quality :)