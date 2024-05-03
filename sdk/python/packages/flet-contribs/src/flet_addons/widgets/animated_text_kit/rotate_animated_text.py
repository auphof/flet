from typing import Optional
import flet as ft


class RotateAnimatedText:
    extra_length_for_blinks = 8  # Similar to the static const in Dart
    type_name = "Rotate"

    def __init__(
        self,
        text: str,
        # text_align="start",
        text_style: Optional[ft.TextStyle] = None,
        duration: int = 2000,
        rotate_out: bool = True,
        # curve="linear",
        # cursor="_",
    ):
        """
        Initializes a new instance of TypewriterAnimatedText.

        Args:
            text (str): The text to be animated.
            text_style (ft.TextStyle, optional): The style to apply to the text, if any.
            duration (int): The duration of the  rotation of the text, measured in milliseconds.
            rotate_out: (bool): Controls whether the text rotates in _and_ out (True), or just rotates _in_ (False)
        """
        self.text = text
        # self.text_align = text_align
        self.text_style = text_style
        self.duration = duration
        self.rotate_out = rotate_out
        # Placeholder for animation controller logic
        # self.typewriter_text = None

    def to_dict(self):
        return {
            "text_type": self.type_name,
            "text": self.text,
            "duration_ms": self.duration,
            "rotate_out": self.rotate_out,
        }
