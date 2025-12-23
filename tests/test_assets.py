from utils import load_assets
import pygame


def test_load_assets_returns_dict_and_nonempty():
    assets = load_assets()
    assert isinstance(assets, dict)
    assert assets, "load_assets returned an empty dict — check BASE_IMAGE_PATH"


def test_assets_are_surfaces_and_have_size():
    assets = load_assets()
    sample = list(assets.items())[:50]  # sample at most 50 to keep test fast
    assert sample, "No assets available to test"
    for key, surf in sample:
        assert hasattr(surf, "get_width") and hasattr(surf, "get_height")
        assert surf.get_width() > 0 and surf.get_height() > 0


def test_blit_sample_assets():
    assets = load_assets()
    screen = pygame.Surface((128, 128))
    for surf in list(assets.values())[:20]:
        # Blit should not raise
        screen.blit(surf, (0, 0))
