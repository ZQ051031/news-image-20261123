# The World in One Picture — Monday 23 November 2026

A 1024×1024 PNG poster summarising the world news of Monday 23 November
2026 in six panels. Every pictogram is hand-drawn with Pillow vector shapes
— no photographs, no external images, no network access at runtime.

## The six stories

1. **Climate — COP31 collapses in Antalya.** Talks end with no pact after
   record overtime; fossil-fuel language is stripped from the text.
2. **Middle East — Tanker attacks in the Strait of Hormuz.** A sailor is
   missing after strikes on shipping; Trump warns of fresh US strikes on
   Iran after 1 January.
3. **Indonesia — Candy-factory fire in Banten.** Three dead and around 30
   people missing after a blaze sweeps a candy factory in Banten province.
4. **Peru — Magnitude 6.7 quake hits Junín.** One dead, 16 injured and
   about 93,000 homes without power after a powerful quake in central Peru.
5. **Ukraine / Baltic — Drones over Kyiv, ship ablaze off Finland.** A
   Russian drone strike leaves 14 missing in the Kyiv region, while a
   Russian cargo ship burns off Finland.
6. **Sport & Film — Liverpool 4–0 in Pochettino debut.** Liverpool thrash
   Manchester United 4–0 as Pochettino takes charge. At the Golden Horse
   Awards, Angela Yuen and Anson Kong win.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `entry.png` (1024×1024, well under 1 MiB) into the directory
given by `MAKEFUN_OUTPUT_DIR` (default `/output`).

## Determinism

The program uses only the Python standard library and Pillow. It makes no
network calls, uses no randomness and embeds no timestamps, so running it
twice produces byte-identical PNG files (verified: two runs, identical
SHA-256).

## Requirements

- Python 3
- Pillow (`pip install pillow`)
- DejaVu Sans fonts (present on most Linux systems at
  `/usr/share/fonts/truetype/dejavu/`)

## License

MIT — see `LICENSE`.
