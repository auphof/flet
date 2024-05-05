from typing import Optional
import flet as ft


class BaseAnimatedText:
    def serialize(self):
        return self.to_dict()
