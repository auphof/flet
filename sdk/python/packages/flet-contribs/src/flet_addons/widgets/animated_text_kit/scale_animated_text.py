from typing import Optional
import flet as ft

from .common import BaseAnimatedText


class ScaleAnimatedText(BaseAnimatedText):
    type_name = "Scale"

    def __init__(
        self,
        text: str,
        # text_align="start",
        text_style: Optional[ft.TextStyle] = None,
        duration: int = 2000,
        scaling_factor: float = 0.5,
        # curve="linear",
    ):
        self.text = text
        # self.text_align = text_align
        self.text_style = text_style
        self.duration = duration
        self.scaling_factor = scaling_factor

    def to_dict(self):
        return {
            "type": self.type_name,
            "text": self.text,
            "duration_ms": self.duration,
            "scaling_factor": self.scaling_factor,
        }
