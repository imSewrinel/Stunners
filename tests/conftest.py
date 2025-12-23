import os
import pytest
import pygame

@pytest.fixture(scope="session", autouse=True)
def pygame_headless():
    # Use the dummy video driver so tests can run in CI or headless environments
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    pygame.display.init()
    # Create a tiny display so convert()/convert_alpha() work
    pygame.display.set_mode((1, 1))
    yield
    try:
        pygame.display.quit()
    except Exception:
        pass
    pygame.quit()
