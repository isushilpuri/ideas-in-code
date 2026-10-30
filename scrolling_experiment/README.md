# Why you can't stop scrolling

If two feeds pay out the same average reward, why would one keep you scrolling
longer than the other?

Three toy feeds, each a function that returns the reward of the next post:

- **`predictable_feed`** — every post is worth `STEADY_REWARD = 1.0`.
- **`unpredictable_feed`** — 1 post in 5 (`JACKPOT_CHANCE = 0.2`) is worth
  `JACKPOT_REWARD = 5.0`; the rest are worth 0. Same average: 1.0 per post.
- **`empty_feed`** — always 0. Just disappointment with a Wi-Fi connection.

One toy user, one rule (`scroller.py`): after every swipe,
`temptation += reward - BOREDOM`, and the chance of swiping again is
`continue_probability(temptation)`, a sigmoid. A rewarding post makes another
swipe more tempting; a boring one makes stopping more likely.

`experiment.py` simulates 5,000 users per feed with NumPy, and
`scrolling_experiment.py` prints how long they scrolled and plots the share
still scrolling at each swipe with Matplotlib.

```bash
uv run pytest -q                      # 7 tests
uv run python scrolling_experiment.py # the experiment + still_scrolling.png
```

Output (seed 42):

```
5,000 simulated users per feed
feed            average   longest 10%
predictable       9.8        18 swipes
unpredictable    19.6        40 swipes
empty             2.8         4 swipes
saved still_scrolling.png
Done. Just one more swipe. Obviously.
```

## Important: this is a toy model

The behaviour is programmed. Every number that shapes it is an assumption we
chose: `START_TEMPTATION = 3.0` and `BOREDOM = 1.1` in `scroller.py`, and
`STEADY_REWARD`, `JACKPOT_CHANCE` and `JACKPOT_REWARD` in `feeds.py`. They were
tuned so the effect is easy to see; change them and the result changes with
them.

Also worth knowing: the unpredictable feed's longer *average* comes from a long
tail. Its typical (median) user actually stops sooner than the predictable
feed's — a few lucky streaks keep a minority scrolling for a very long time.

This is **not** a measurement of real users, real feeds, dopamine or
addiction. Real behaviour involves habit, emotions, social pressure, boredom
and much more. It illustrates one idea: under these assumptions, unpredictable
rewards can produce longer sessions — you keep scrolling because the next post
*might* be good.

## Files

| File | What it does |
|---|---|
| `feeds.py` | The three feeds and their reward constants |
| `scroller.py` | The one rule: temptation, the sigmoid, and a scrolling session |
| `experiment.py` | 5,000 simulated sessions per feed, and the still-scrolling curve |
| `scrolling_experiment.py` | Prints the results and saves the chart |
| `tests/test_scrolling.py` | Checks the feeds, the rule and the experiment |
