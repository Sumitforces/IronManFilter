"""
proximity_area_filter.py
========================

The generic, reusable implementation behind the Proximity-Area Noise Filter.

Run this file directly to demo it on a synthetic image, or import the function
and call it on your own 2-D numpy arrays.
"""

import numpy as np


def proximity_area_filter(image, min_area_threshold, proximity_threshold):
    """
    Remove scattered noise from a binary image by grouping nearby pixels
    into "meta-shapes", then keeping only the shapes big enough to be real
    signal.

    Parameters
    ----------
    image : numpy.ndarray
        A 2-D array of uint8, where 255 means "signal" and anything else is
        treated as empty background.
    min_area_threshold : int
        A merged component must have at least this many pixels to be kept.
        Smaller components are dropped as noise.
    proximity_threshold : int
        Radius of the BFS search window. Instead of only touching the 4 or 8
        immediate neighbours, the flood-fill looks in a (2*proximity_threshold
        + 1) x (2*proximity_threshold + 1) square, so it can "jump" over small
        gaps and stitch separated dots into one component.

    Returns
    -------
    numpy.ndarray
        A 2-D uint8 array with 255 where signal was kept and 0 everywhere else.
        This has the same shape as the input image.
    """
    rows, cols = image.shape
    visited = np.zeros((rows, cols), dtype=bool)
    output_image = np.zeros((rows, cols), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            # Find an unvisited white pixel and start growing a component.
            if image[i, j] == 255 and not visited[i, j]:

                component_pixels = []
                queue = [(i, j)]
                visited[i, j] = True

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    component_pixels.append((curr_r, curr_c))

                    # Search within the proximity window.
                    # This is what lets the BFS "jump" gaps of up to
                    # 'proximity_threshold' pixels so nearby dots merge.
                    for dr in range(-proximity_threshold, proximity_threshold + 1):
                        for dc in range(-proximity_threshold, proximity_threshold + 1):
                            # Optional: use Euclidean distance for a circular
                            # radius instead of the square window.
                            # if (dr**2 + dc**2) ** 0.5 > proximity_threshold:
                            #     continue

                            nr, nc = curr_r + dr, curr_c + dc

                            if 0 <= nr < rows and 0 <= nc < cols:
                                if image[nr, nc] == 255 and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    queue.append((nr, nc))

                # Check if the combined "meta-shape" meets the area requirement.
                if len(component_pixels) >= min_area_threshold:
                    for r, c in component_pixels:
                        output_image[r, c] = 255

    return output_image


def _make_demo_image():
    """Build a small synthetic image: two solid blobs plus a few specks of noise."""
    image = np.zeros((40, 60), dtype=np.uint8)

    # A couple of solid blobs - these should definitely survive the filter.
    image[5:20, 5:25] = 255
    image[25:35, 40:55] = 255

    # A few isolated noise pixels scattered around - these should be removed.
    for r, c in [(30, 10), (31, 12), (3, 50), (8, 45), (18, 35)]:
        image[r, c] = 255

    return image


if __name__ == "__main__":
    test_image = _make_demo_image()
    cleaned = proximity_area_filter(test_image, min_area_threshold=20,
                                    proximity_threshold=2)

    signal_before = int((test_image == 255).sum())
    signal_after = int((cleaned == 255).sum())
    print(f"signal pixels before: {signal_before}")
    print(f"signal pixels after : {signal_after}")
    print(f"noise pixels removed: {signal_before - signal_after}")