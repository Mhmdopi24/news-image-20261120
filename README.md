# The World Today — Friday, 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Mhmdopi24/news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Mhmdopi24/news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

One image that sums up the world's news of Friday, 20 November 2026, drawn as
a newspaper front page: the ICJ's historic ruling that Myanmar committed
genocide against the Rohingya; the first-ever Trump–Xi–Putin trilateral
meeting in Shenzhen; Cyclone Akvan bearing down on India's east coast; GTA VI
smashing launch records; Russian strikes damaging the Dutch and Austrian
embassies in Kyiv; and South Korea's top court clearing ex-PM Han Duck-soo —
plus the day's smaller stories in the footer.

## How it works

`main.ts` (Node 22, standard library only) copies the front page,
`entry.png` (1024×1024, drawn in code with Pillow in `tools/draw_frontpage.py`
during this session), byte for byte to `$MAKEFUN_OUTPUT_DIR/entry.png`, so
both runs produce identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
