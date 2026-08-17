# Proximity–Area Noise Filter

An interactive, instrumented visualization of a **proximity–area signal filter** for cleaning salt-scattered noise from a binary pixel grid. It runs the real BFS flood-fill algorithm live on a canvas and lets you watch each component grow, merge, and get accepted or rejected.

## What it does

The filter processes a synthetic `62 × 38` binary image made of:

- **Solid content blobs** — real signal, always kept.
- **Gap clusters** — tiny dot groups spaced apart that only clear the threshold once the *proximity gap-jump* stitches them together.
- **Salt noise** — scattered isolated pixels, the intended removal target.

The algorithm performs a connected-component analysis using a **BFS flood-fill** whose neighbourhood is a `(2·proximity + 1)²` square **proximity window** instead of the usual 4/8-connectivity. Components effectively "jump gaps" up to the configured proximity radius and are merged. Each finished component then survives **only if its merged pixel count meets the `min_area_threshold`**.

## Key parameters

| Parameter | Default | Effect |
| --- | --- | --- |
| `min_area_threshold` | 30 | Minimum pixel count for a merged component to be kept; anything smaller is dropped as noise. |
| `proximity_threshold` | 3 | Radius of the flood-fill probe window (odd square `(2·proximity+1)²`). Larger values stitch together more distant dots. |
| playback speed | 40 | Events/second for the animated sweep. |

## Controls

- **Run / Pause** — play or pause the sweep.
- **Step** — advance one event at a time.
- **Skip to end** — immediately apply every remaining event.
- **Restart pass** — re-apply the algorithm to the current image (picks up slider changes).
- **New image** — generate a fresh random test image.

## How to run

### Interactive visualization

The HTML demo is entirely self-contained — a single file with zero build step or dependencies. Just open it in any browser:

```
proximity_noise_filter_demo.html
```

### Generic Python implementation

`proximity_area_filter.py` holds the reusable, dependency-light version of the same filter. It only needs `numpy`:

```
pip install numpy
python proximity_area_filter.py      # runs a self-test on a synthetic image
```

Or import it and use it on your own binary images:

```python
import numpy as np
from proximity_area_filter import proximity_area_filter

cleaned = proximity_area_filter(image, min_area_threshold=30, proximity_threshold=3)
```

The function signature matches the parameters in the HTML demo: `proximity_area_filter(image, min_area_threshold, proximity_threshold)`.

## Output / "Scope" readouts

A live frame buffer shows pixels colour-coded by status:

- `#eef7f1` — unprocessed signal (255)
- `hsl(…)` — growing / active component (hue per component id)
- `#9b86ff` — proximity probe window
- green — **kept** (area ≥ threshold)
- amber — **removed** (area < threshold)

The side panel tracks the current component's size against the threshold, and a **Pass Summary** reports signal pixels, components found, and kept/removed component & pixel counts — so you can see exactly how much noise the filter removed.