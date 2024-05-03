from typing import Optional
import flet as ft


class TypewriterAnimatedText:
    extra_length_for_blinks = 8  # Similar to the static const in Dart
    type_name = "Typewriter"

    def __init__(
        self,
        text: str,
        # text_align="start",
        text_style: Optional[ft.TextStyle] = None,
        speed: int = 30,
        # curve="linear",
        # cursor="_",
    ):
        """
        Initializes a new instance of TypewriterAnimatedText.

        Args:
            text (str): The text to be animated.
            text_style (ft.TextStyle, optional): The style to apply to the text, if any.
            speed (int): The duration of the delay between the appearance of each character, measured in milliseconds.
        """
        # """
        # Initializes a new instance of TypewriterAnimatedText.
        # :param text: The text to be animated.
        # :param text_align: The alignment of the text (default is 'start').
        # :param text_style: The style to apply to the text, if any.
        # :param speed: The duration of the delay between the appearance of each character, in milliseconds.
        # :param curve: The curve of the rate of change of animation over time.
        # :param cursor: The cursor text, defaults to underscore.
        # """
        self.text = text
        # self.text_align = text_align
        self.text_style = text_style
        self.speed = speed
        # self.curve = curve
        # self.cursor = cursor
        self.duration = self.speed * (len(text) + self.extra_length_for_blinks)

        # Placeholder for animation controller logic
        # self.typewriter_text = None

    def to_dict(self):
        return {
            "text_type": self.type_name,
            "text": self.text,
            "duration_ms": self.duration,
        }
