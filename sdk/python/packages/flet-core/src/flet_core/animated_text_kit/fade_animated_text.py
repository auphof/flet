from typing import Optional
import flet as ft

from .common import BaseAnimatedText


class FadeAnimatedText(BaseAnimatedText):
    type_name = "Fade"

    def __init__(
        self,
        text: str,
        # text_align="start",
        text_style: Optional[ft.TextStyle] = None,
        duration: int = 2000,
        fade_in_end: float = 0.5,
        fade_out_begin: float = 0.8,
        # curve="linear",
    ):
        self.text = text
        # self.text_align = text_align
        self.text_style = text_style
        self.duration = duration
        self.fade_in_end = fade_in_end
        self.fade_out_begin = fade_out_begin

    def to_dict(self):
        return {
            "type": self.type_name,
            "text": self.text,
            "duration_ms": self.duration,
            "fade_in_end": self.fade_in_end,
            "fade_out_begin": self.fade_out_begin,
        }
