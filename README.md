# THE WORLD — 19 November 2026

One image that sums up Thursday 19 November 2026's world news: a newspaper
front page, drawn from scratch with Pillow.

- **Lead:** the Trump–Xi–Putin trilateral in Shenzhen.
- **35 stories from 7 regions:** North America, South America, Europe,
  Middle East, Africa, Asia-Pacific, Oceania — five stories each.
- **The day in numbers:** a small box with the day's figures.

## Run

```sh
python3 draw.py        # writes entry.png (1024x1024, deterministic)
python3 main.py        # writes /output/entry.png
```

No network, no clock, no randomness: two runs write byte-identical PNGs.
The image is 1024×1024 and well under 1 MiB.

## License

MIT. See LICENSE.
