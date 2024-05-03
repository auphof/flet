from typing import Any, Optional, Union, List
import json
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ImageFit,
)
from flet_core.video import FilterQuality

flutter_control_properties = {
    "text": {
        "default": "",
        "type": "str",
        "get_doc": "Retrieves the text currently being displayed by the control.",
        "set_doc": "Updates the text displayed by the control.",
    },
    "text_size": {
        "default": None,
        "type": "OptionalNumber",
        "get_doc": "Returns the size of the text.",
        "set_doc": "Sets the size of the text displayed.",
    },
    # following `text_style` manually is implemented in the class as it requires json conversion
    # TODO TD extend generator to handle structures like text_style properties
    # "text_style": {"default": None, "type": "Optional[TextStyle]"},
    "speed": {
        "default": 250,
        "type": "int",
        "get_doc": "Returns the size of the text.",
        "set_doc": "Sets the size of the text displayed.",
    },
    "pause": {
        "default": 1000,
        "type": "int",
        "get_doc": "Retrieves the duration of the pause between texts, in milliseconds.",
        "set_doc": "Sets the duration of the pause between texts, in milliseconds.",
    },
    "display_full_text_on_tap": {
        "default": False,
        "type": "bool",
        "get_doc": "Determines whether tapping on the animation displays the full text immediately.",
        "set_doc": "Configures the control to display the full text immediately upon tapping.",
    },
    "stop_pause_on_tap": {
        "default": False,
        "type": "bool",
        "get_doc": "Checks if a tap on the control stops the current pause between texts.",
        "set_doc": "Enables or disables stopping the current pause between texts when the control is tapped.",
    },
    "is_repeating_animation": {
        "default": True,
        "type": "bool",
        "get_doc": "Checks if the animation is set to repeat.",
        "set_doc": "Enables or disables the repeating of the animation.",
    },
    "repeat_forever": {
        "default": False,
        "type": "bool",
        "get_doc": "Determines if the animation repeats indefinitely, ignoring the total repeat count.",
        "set_doc": "Enables or disables infinite repetition of the animation. When set, `totalRepeatCount` is ignored.",
    },
    "total_repeat_count": {
        "default": 3,
        "type": "int",
        "get_doc": "Gets the number of times the animation should repeat.",
        "set_doc": "Sets the number of times the animation is to repeat.",
    },
}

flutter_control_events = {
    "on_tap": {
        "default": None,
        "get_doc": "Retrieves the callback function executed on tapping the animated widget.",
        "set_doc": "Sets a callback to be executed when the animated widget is tapped.",
    },
    "on_finished": {
        "default": None,
        "get_doc": "Retrieves the callback function executed when the animation sequence completes and is not set to repeat.",
        "set_doc": "Assigns a callback to be executed upon the completion of the animation sequence, only if it is not repeating.",
    },
    "on_next": {
        "default": None,
        "get_doc": "Retrieves the callback function executed before transitioning to the next text in the sequence.",
        "set_doc": "Sets a callback to be executed right before moving to the next text after the pause.",
    },
    "on_next_before_pause": {
        "default": None,
        "get_doc": "Retrieves the callback function executed just before initiating a pause at the end of the current text animation.",
        "set_doc": "Sets a callback to be executed right before a pause is initiated after displaying a text.",
    },
}


def snake_case_to_camel_case(snake_str):
    # Split the snake_case string based on underscore
    components = snake_str.split("_")
    # Return the first component lowercased, join it with capitalized subsequent components
    return components[0].lower() + "".join(x.title() for x in components[1:])


def property_and_event_generator(properties, events):
    def decorator(cls):
        cls._flet_control_property_info = properties  # Store property metadata
        cls._flet_control_event_info = events  # Store event handler metadata

        # Generate properties with docstrings
        for prop_name, prop_settings in properties.items():
            prop_docstring = (
                f"Gets or sets the {prop_name}. Default is {prop_settings['default']}."
            )

            def getter(
                self,
                prop_name=prop_name,
                def_value=prop_settings["default"],
                data_type=prop_settings["type"],
            ):
                """Generated getter for property."""
                return self._get_attr(prop_name, def_value, data_type)

            def setter(self, value, prop_name=prop_name):
                """Generated setter for property."""
                self._set_attr(prop_name, value)

            prop = property(getter, setter)
            prop.__doc__ = prop_docstring  # Set the docstring for the property
            setattr(cls, prop_name, prop)

        # Generate event handlers with docstrings
        for event_name, default in events.items():
            event_docstring = (
                f"Event handler for when {event_name.replace('_', ' ')} occurs."
            )

            def event_getter(self, event_name=event_name):
                """Generated getter for event handler."""
                return self._get_event_handler(event_name)

            def event_setter(self, handler, event_name=event_name):
                """Generated setter for event handler."""
                self._add_event_handler(event_name, handler)
                self._set_attr(
                    f"{snake_case_to_camel_case(event_name)}",
                    True if handler is not None else None,
                )

            event_prop = property(event_getter, event_setter)
            event_prop.__doc__ = (
                event_docstring  # Set the docstring for the event property
            )
            setattr(cls, event_name, event_prop)

        return cls

    return decorator


class AnimatedText:
    def __init__(self, text_type, text, duration_ms, **kwargs):
        self.config = {
            "type": text_type,
            "text": text,
            "duration_ms": duration_ms,
            **kwargs,
        }

    def serialize(self):
        # TODO TD tidy this up we are using json to string and back, does force it to be good json but is not great code
        json_string = json.dumps(self.config)
        # print(f"AnimatedText serializedd json_string: {json_string}")
        return json.loads(json_string)


class AnimatedTexts(list):  # Subclass from list directly
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def serialize_all(self):
        # Serialize all contained AnimatedText objects to JSON-compatible dictionaries
        return [item.serialize() for item in self]

    def to_json(self):
        # Convert all entries to JSON string if needed to transmit
        return json.dumps(self.serialize_all())


# # Example usage:
# animations = [
#     AnimatedText("Typewriter", "Hello World", 500),
#     AnimatedText("Rotate", "Goodbye World", 700, rotation=15),
# ]

# # Serializing for transmission
# serialized_animations = [animation.serialize() for animation in animations]


# Apply the property_generator with both properties and events
@property_and_event_generator(flutter_control_properties, flutter_control_events)
class AnimatedTextKit(ConstrainedControl):
    """
    Displays AnimatedTextKit animations.


    Displays animated texts with various customizable properties including speed, repeat, and pause durations.

    Online docs: https://flet.dev/docs/controls/lottie
    -----
    Attributes:
        text (str): The text to animate.
        speed (OptionalNumber): The speed of the text animation in milliseconds.
        repeat (Optional[bool]): If True, the animation will repeat.
        reverse (Optional[bool]): If True, the animation will reverse at each iteration.
        animate (Optional[bool]): If True, the animation is active.
        background_loading (Optional[bool]): If True, loads the animation in the background.
        filter_quality (Optional[FilterQuality]): The quality of the animation filtering.
        fit (Optional[ImageFit]): How the animation fits into the assigned space.
        on_error (callable): Handler for error events.
        pause (OptionalNumber): Duration of the pause between texts in milliseconds.
        displayFullTextOnTap (Optional[bool]): If True, tapping the animation will rush it to completion.
        isRepeatingAnimation (Optional[bool]): Controls whether the animation repeats.
        totalRepeatCount (Optional[int]): Number of times the animation should repeat.

    """

    def __init__(
        self,
        text: str = None,
        animated_texts: List[AnimatedText] = [],
        speed: OptionalNumber = None,
        pause: OptionalNumber = None,
        repeat_forever: Optional[bool] = None,
        display_full_text_on_tap: Optional[bool] = None,
        stop_pause_on_tap: Optional[bool] = None,
        is_repeating_animation: Optional[bool] = None,
        total_repeat_count: Optional[int] = None,
        reverse: Optional[bool] = None,
        text_size: OptionalNumber = None,
        text_style: Optional[TextStyle] = None,
        animate: Optional[bool] = None,
        # TODO: check what can be removed
        background_loading: Optional[bool] = None,
        filter_quality: Optional[FilterQuality] = None,
        fit: Optional[ImageFit] = None,
        on_error=None,
        on_tap=None,
        on_finished=None,
        on_next=None,
        on_next_before_pause=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
    ):
        """
        Initializes a new instance of the AnimatedTextKit control.

        Parameters:
            text (str, optional): The text to animate.
            speed (int, optional): The speed of the text animation in milliseconds.
            repeat_forever (bool, optional): If True, the animation will repeat forever.
            reverse (bool, optional): If True, the animation will reverse at each iteration.
            animate (bool, optional): If True, the animation is active.
            background_loading (bool, optional): If True, loads the animation in the background.
            filter_quality (FilterQuality, optional): The quality of the animation filtering.
            fit (ImageFit, optional): How the animation fits into the assigned space.
            on_error (callable, optional): Handler for error events.
            pause (int, optional): Duration of the pause between texts in milliseconds.
            displayFullTextOnTap (Optional[bool]): If True, tapping the animation will rush it to completion.
            stopPauseOnTap ( Optional[bool] :If true, tapping during a pause will stop it and start the next text animation
            isRepeatingAnimation (Optional[bool]): Controls whether the animation repeats.
            totalRepeatCount (Optional[int]): Number of times the animation should repeat.

        """

        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )
        # Control properties
        # self.text = text
        self.animated_texts = animated_texts
        self.text_size = text_size
        self.text_style = text_style
        self.speed = speed
        self.repeat_forever = repeat_forever
        self.pause = (
            pause if pause is not None else 1000
        )  # Set the pause attribute with a default of 1000 milliseconds if not provided
        self.display_full_text_on_tap = display_full_text_on_tap
        self.stop_pause_on_tap = stop_pause_on_tap
        self.is_repeating_animation = is_repeating_animation
        self.total_repeat_count = total_repeat_count
        self.reverse = reverse
        self.animate = animate
        self.filter_quality = filter_quality
        self.fit = fit
        self.background_loading = background_loading
        self.on_error = on_error
        self.on_tap = on_tap
        self.on_finished = on_finished
        self.on_next = on_next
        self.on_next_before_pause = on_next_before_pause

    def before_update(self):
        super().before_update()
        self._set_attr_json("textStyle", self.__text_style)
        self._set_attr_json("animatedTexts", self.__animated_texts)

    def _get_control_name(self):
        return "animated_text_kit"

    # animated_texts
    @property
    def animated_texts(self) -> List[AnimatedText]:
        return self.__animated_texts

    @animated_texts.setter
    def animated_texts(self, value: List[AnimatedText]):
        self.__animated_texts = value

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value
