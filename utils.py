import os
import pygame
from config import *
from collections.abc import MutableMapping
from core.game_object import Game_object


class Lazy_assets(MutableMapping):
    """Lightweight lazy loader to build Game objects on first access."""

    def __init__(self, meta, scale:tuple|None=None):
        self._meta = dict(meta)
        self._cache = {}
        self._scale = scale

    def _build(self, key):
        if key not in self._meta:
            raise KeyError(key)
        
        if key in self._cache:
            return self._cache[key]

        try:
            full_path = self._meta[key]
            img = pygame.image.load(full_path)

            x_scale, y_scale = None, None
            if self._scale is not None:
                x_scale, y_scale = self._scale
            else:
                x_scale, y_scale = img.get_size()
            object = Game_object(img, x_scale, y_scale)
            self._cache[key] = object
            return object
        
        except Exception:
            print(f"Failed to load asset '{full_path}', skipping.")
            raise(Exception)

    def __getitem__(self, key) -> Game_object: # from MutableMapping class
        return self._build(key)

    def __setitem__(self, key, value): # from MutableMapping class
        self._cache[key] = value
        self._meta.pop(key, None)

    def __delitem__(self, key): # from MutableMapping class
        self._meta.pop(key, None)
        self._cache.pop(key, None)

    def __iter__(self): # from MutableMapping class
        seen = set(self._meta.keys()) | set(self._cache.keys())
        for k in sorted(seen):
            yield k

    def __len__(self) -> int: # from MutableMapping class
        seen = set(self._meta.keys()) | set(self._cache.keys())
        return len(seen)

    def is_loaded(self, key) -> bool:
        return key in self._cache

    def load_all(self):
        for k in list(self._meta.keys()):
            self._build(k)

    def cache_as_dict(self):
        self.load_all()
        return dict(self._cache)



def get_meta(base_path=BASE_IMAGE_PATH, allowed_exts=ALLOWED_IMAGE_EXTS) -> dict:
    if not os.path.isabs(base_path):
        base_abs = os.path.abspath(os.path.join(os.path.dirname(__file__), base_path))
    else:
        base_abs = base_path

    if not os.path.isdir(base_abs):
        print(f"Warning: asset directory not found: {base_abs}")
        return {}

    meta = {}
    for root, _, files in os.walk(base_abs):
        for file in files:
            if file.lower().endswith(allowed_exts):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_abs).replace("\\", "/")
                key = rel_path.rsplit(".", 1)[0]  # e.g. 'minions/buzzing_vermin'
                meta[key] = full_path
    return meta