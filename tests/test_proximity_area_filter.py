"""Tests for the proximity-area noise filter."""

import numpy as np
import pytest

from proximity_area_filter import proximity_area_filter


def _binary(shape, white):
    image = np.zeros(shape, dtype=np.uint8)
    for r, c in white:
        image[r, c] = 255
    return image


def test_output_has_same_shape_and_dtype():
    image = np.zeros((10, 15), dtype=np.uint8)
    result = proximity_area_filter(image, 5, 2)
    assert result.shape == image.shape
    assert result.dtype == np.uint8


def test_blank_image_stays_blank():
    image = np.zeros((10, 10), dtype=np.uint8)
    result = proximity_area_filter(image, 5, 2)
    assert not result.any()


def test_isolated_salt_noise_removed():
    shape = (10, 10)
    image = _binary(shape, [(3, 3), (8, 8)])
    result = proximity_area_filter(image, min_area_threshold=10, proximity_threshold=0)
    assert not result.any()


def test_solid_blob_is_kept():
    shape = (10, 10)
    white = [(r, c) for r in range(2, 7) for c in range(2, 7)]
    image = _binary(shape, white)
    result = proximity_area_filter(image, min_area_threshold=25, proximity_threshold=1)
    assert (result == 255).sum() == 25


def test_kept_blob_above_threshold():
    shape = (10, 10)
    image = _binary(shape, [(1, 1), (1, 2), (2, 1), (2, 2)])
    result = proximity_area_filter(image, min_area_threshold=4, proximity_threshold=1)
    assert (result == 255).sum() == 4


def test_removed_blob_below_threshold():
    shape = (10, 10)
    image = _binary(shape, [(1, 1), (1, 2), (2, 1), (2, 2)])
    result = proximity_area_filter(image, min_area_threshold=5, proximity_threshold=1)
    assert not result.any()


def test_proximity_stitches_gap_cluster():
    """Dots spaced just over the default 4/8-connectivity should merge once a
    wide enough proximity window is used."""
    shape = (10, 10)
    # Three dots separated by a two-pixel gap along the diagonal.
    dots = [(4, 4), (5, 5), (6, 6)]
    image = _binary(shape, dots)

    # Too small a window -> each dot is its own single-pixel component.
    strict = proximity_area_filter(image, min_area_threshold=3, proximity_threshold=0)
    assert (strict == 255).sum() == 0

    # Wide window -> the dots merge into one 3-pixel component that survives.
    merged = proximity_area_filter(image, min_area_threshold=3, proximity_threshold=2)
    assert (merged == 255).sum() == 3


def test_input_is_not_mutated():
    image = _binary((8, 8), [(1, 1), (2, 2)])
    original = image.copy()
    proximity_area_filter(image, min_area_threshold=1, proximity_threshold=2)
    np.testing.assert_array_equal(image, original)


@pytest.mark.parametrize("threshold", [1, 2, 8])
def test_single_pixel_depends_on_threshold(threshold):
    image = np.zeros((10, 10), dtype=np.uint8)
    image[0, 0] = 255
    result = proximity_area_filter(image, min_area_threshold=threshold, proximity_threshold=0)
    assert (result == 255).sum() == (1 if threshold <= 1 else 0)