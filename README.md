<div align="center">

# Proximity–Area Noise Filter

Cleans salt-scattered noise from a binary image by grouping nearby pixels into
**meta-shapes**, then keeping only the shapes big enough to be real signal —
via a BFS flood-fill with a configurable **proximity window** and an
**area threshold**.

[![Python version](https://img.shields.io/pypi/pyversions/ironmanfilter)](https://pypi.org/project/ironmanfilter/)
[![CI](https://github.com/Sumitforces/IronManFilter/actions/workflows/ci.yml/badge.svg)](https://github.com/Sumitforces/IronManFilter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## Overview

Salt noise is scattered, isolated pixels that are easy to confuse with genuine
signal — unless a real object contains only a handful of pixels. The filter
solves this in two steps:

1. **Merge nearby signal** with a BFS flood-fill whose neighbourhood is a
   `(2·proximity + 1)²` **proximity window** instead of the usual 4/8-connectivity.
   Components effectively *jump gaps* up to the configured radius and stitch
   separated dots into a single shape.
2. **Threshold by area** — every merged component survives **only if its pixel
   count meets `min_area_threshold`**. Anything smaller is dropped as noise.

The repo ships the algorithm twice:

| Artifact | What it is |
| --- | --- |
| `proximity_area_filter.py` | The generic, reusable engine (dependency: `numpy`). Pip-installable, fully tested. |
| `proximity_noise_filter_demo.html` | Interactive canvas demo: runs the *same* algorithm live, step by step, so you can watch components grow, merge, and get accepted or rejected. |
| `proximity_noise_filter_final_version.html` | Final polished recording-ready variant of the demo (narrative captions + live instrumented run) used as the on-screen deliverable for the walkthrough video. |

## Installation

Python 3.8+.

```bash
pip install ironmanfilter        # from PyPI (once published)
# or install from source:
git clone https://github.com/Sumitforces/IronManFilter.git
cd IronManFilter
pip install -e .                # editable install
```

For development, install with test tooling:

```bash
pip install -e ".[dev]"         # adds pytest
```

## Usage

```python
import numpy as np
from proximity_area_filter import proximity_area_filter

cleaned = proximity_area_filter(
    image,
    min_area_threshold=30,
    proximity_threshold=3,
)
```

- `image` — a 2-D `numpy.ndarray` of `uint8`: `255` = signal, otherwise background.
- Returns a `uint8` array of the same shape, `255` where signal was kept.

Run the bundled self-test demo directly:

```bash
python proximity_area_filter.py
```

## Algorithm parameters

| Parameter | Default | Effect |
| --- | --- | --- |
| `min_area_threshold` | 30 | Minimum pixel count for a merged component to be kept; smaller components are dropped as noise. |
| `proximity_threshold` | 3 | Radius of the flood-fill search window `(2·proximity+1)²`. Larger values stitch together more distant dots. `1` ≈ 8-connectivity. |

## Interactive demo

Two browser-deliverable HTML files are included. Open either in any browser —
they are single, dependency-free files:

- `proximity_noise_filter_demo.html` — the working interactive sandbox.
- `proximity_noise_filter_final_version.html` — the **recording-ready** variant
  used for the live walkthrough. It opens on a narrative caption, then animates
  the instrumented BFS sweep in real time for screen capture.

Both generate a synthetic `62 × 38` image from solid blobs, gap clusters, and
salt noise, then animate the sweep:

- **Run / Pause** — play or pause the sweep.
- **Step** — advance one event at a time.
- **Skip to end** — immediately apply all remaining events.
- **Restart pass** — re-run the algorithm on the current image (honours slider changes).
- **New image** — generate a fresh random test image.

Pixels are colour-coded live: unprocessed `#eef7f1`, growing component by hue,
`#9b86ff` probe window, **green** kept, **amber** removed. A **Pass Summary**
reports signal pixels, components found, and kept/removed totals.

### Recording the live demo

The final version is designed to be screen-captured end to end:

1. Open `proximity_noise_filter_final_version.html` full-screen.
2. Hit **Run** and let the instrumented sweep play through (use **Step**/*speed*
   controls to pace it for the narration).
3. Capture with OBS, a browser recorder, or Windows **Win+G**.
4. Publish the resulting video under `videos/` (see below).

Deliverables recorded live from these files live in the `videos/` folder.

## Development

```bash
pip install -e ".[dev]"
pytest                           # run the test suite (also runs on CI)
```

GitHub Actions runs the tests on Python 3.9–3.12 for every push and pull request
(see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## Project layout

```
.
├── proximity_area_filter.py          # the generic algorithm (+ importable engine)
├── proximity_noise_filter_demo.html  # interactive visualization
├── proximity_noise_filter_final_version.html  # recording-ready demo deliverable
├── videos/                           # recorded live-demo deliverables (.mp4 placeholder)
├── tests/                            # pytest suite
├── pyproject.toml                    # packaging & tooling config
├── requirements.txt                  # runtime deps (numpy)
├── requirements-dev.txt              # dev deps (pytest)
└── .github/workflows/ci.yml          # CI pipeline
```

## License

[MIT](LICENSE) © Sumit Kundu.