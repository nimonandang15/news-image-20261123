# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/nimonandang15/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/nimonandang15/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026 — a newspaper front page, "The World in One Day", with the six stories that defined the day.

## The day's news

1. **COP31 collapses with no deal** — The UN climate summit in Antalya, Turkey, ends Sunday with no agreement, the longest summit in history after 44+ hours of overtime. The final "Antalya Pact" draft did not mention fossil fuels once; the EU refused it and the UN chief is "deeply disappointed".
2. **Gulf war widens as tankers are hit** — Houthis strike Riyadh for a third straight day; at least 25 tankers have been hit in and around the Strait of Hormuz in a week; the Saudi-led coalition intercepts a Houthi missile.
3. **Drone hits flats near Kyiv; 14 missing** — A Russian drone strikes an apartment block in Dymer, leaving 14 people missing; the Sparta II is still burning off Finland after a drone attack.
4. **Factory fire: dozens missing** — Three people are dead after a candy factory fire in Banten province, Indonesia; rescuers are searching for 36 workers still missing.
5. **Minister quits over AI exam scandal** — South Korea's education minister resigns amid an AI-driven exam cheating scandal.
6. **BepiColombo reaches Mercury** — The Europe-Japan probe enters orbit after an eight-year journey, only the second mission ever to orbit the planet.

Also: Pentagon releases 43 more UAP files; Democrats win a historic House majority; UN talks on lethal AI weapons continue, no binding rules.

Sources: AP, Reuters, AFP, BBC, Al Jazeera, CNN, Politico — 23 Nov 2026.

`main.ts` (Node 22, standard library only) copies `entry.png` byte for byte to `/output/entry.png`, refusing anything that is not a whole PNG within the gate limits (≤ 1 MiB, ≤ 1024×1024). Both runs write the same bytes. The poster is drawn by `render.py` (PIL + DejaVu only).

## Run it

```sh
python3 render.py            # rebuild entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=cydbk12s&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
