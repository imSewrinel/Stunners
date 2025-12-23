import os
import pygame
from config import *

ALLOWED_IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')

def load_assets(base_path=BASE_IMAGE_PATH, scale=None, allowed_exts=ALLOWED_IMAGE_EXTS):
    # Resolve absolute base path relative to project root
    if not os.path.isabs(base_path):
        base_abs = os.path.abspath(os.path.join(os.path.dirname(__file__), base_path))
    else:
        base_abs = base_path

    if not os.path.isdir(base_abs):
        print(f"Warning: asset directory not found: {base_abs}")
        return {}

    assets = {}
    for root, _, files in os.walk(base_abs):
        for file in files:
            if file.lower().endswith(allowed_exts):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_abs).replace("\\", "/")
                key = rel_path.rsplit(".", 1)[0]  # e.g. 'minions/buzzing_vermin'
                try:
                    img = pygame.image.load(full_path).convert_alpha()
                    if scale is not None:
                        img = pygame.transform.smoothscale(img, scale)
                    assets[key] = img
                except Exception as e:
                    print(f"Failed to load asset {full_path}: {e}")
    return assets