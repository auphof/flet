from typing import Any, Optional, Union

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
        "get_doc": "Returns the current text of the control.",
        "set_doc": "Sets the text displayed by the control.",
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
        "get_doc": "Gets the current speed of the text animation.",
        "set_doc": "Sets the speed of the text animation in milliseconds.",
    },
    "total_repeat_count": {"default": 4, "type": "int"},
    "repeat_forever": {
        "default": True,
        "type": "bool",
        "get_doc": "Checks if the animation repeats indefinitely.",
        "set_doc": "Enables or disables indefinite repetition of the animation.",
    },
    "is_repeating_animation": {"default": True, "type": "bool"},
    "stop_pause_on_tap": {"default": False, "type": "bool"},
    "display_full_text_on_tap": {"default": False, "type": "bool"},
    # Additional properties can be defined here
}

# Define event metadata similar to property metadata
flutter_control_events = {
    "on_tap": {
        "default": None,
        "get_doc": "Returns the event handler attached to 'tap' events.",
        "set_doc": "Sets the event handler for 'tap' events. Activates the control to respond to tap interactions.",
    },
    "on_finished": {
        "default": None,
        "get_doc": "Gets the event handler for the 'finished' event when the animation sequence completes.",
        "set_doc": "Sets the event handler that is called when the animation sequence completes.",
    },
    "on_next": {
        "default": None,
        "get_doc": "Gets the event handler for the 'next' event when moving to the next text.",
        "set_doc": "Sets the event handler that is triggered when moving to the next text in the animation.",
    },
    "on_next_before_pause": {
        "default": None,
        "get_doc": "Gets the event handler for the 'next_before_pause' event, triggered just before a pause.",
        "set_doc": "Sets the event handler that is called right before a pause is initiated in the animation.",
    },
}


def property_generator(properties, events):
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
                    f"on{event_name.capitalize()}",
                    True if handler is not None else None,
                )

            event_prop = property(event_getter, event_setter)
            event_prop.__doc__ = (
                event_docstring  # Set the docstring for the event property
            )
            setattr(cls, event_name, event_prop)

        return cls

    return decorator


# Apply the property_generator with both properties and events
@property_generator(flutter_control_properties, flutter_control_events)
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
        self.text = text
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

    def _get_control_name(self):
        return "animated_text_kit"

    # # src
    # @property
    # def src(self):
    #     return self._get_attr("src")

    # @src.setter
    # def src(self, value):
    #     self._set_attr("src", value)

    # # src_base64
    # @property
    # def src_base64(self):
    #     return self._get_attr("srcBase64")

    # @src_base64.setter
    # def src_base64(self, value):
    #     self._set_attr("srcBase64", value)

    # # text
    # @property
    # def text(self):
    #     return self._get_attr("text", def_value="", data_type="str")

    # @text.setter
    # def text(self, value):
    #     self._set_attr("text", value)

    # # text_size
    # @property
    # def text_size(self) -> OptionalNumber:
    #     return self._get_attr("textSize")

    # @text_size.setter
    # def text_size(self, value: OptionalNumber):
    #     self._set_attr("textSize", value)

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value

    # # @property
    # # def text_style(self) -> Optional[TextStyle]:
    # #     return self._get_attr("textStyle")

    # # @text_style.setter
    # # def text_style(self, value: Optional[TextStyle]):
    # #     self._set_attr("textStyle", value)

    # # repeatForever
    # @property
    # def repeat_forever(self):
    #     return self._get_attr("repeat_forever", def_value=True, data_type="bool")

    # @repeat_forever.setter
    # def repeat_forever(self, value):
    #     self._set_attr("repeat_forever", value)

    # # speed
    # @property
    # def speed(self):
    #     return self._get_attr("speed", def_value=250, data_type="int")

    # @speed.setter
    # def speed(self, value):
    #     self._set_attr("speed", value)

    # # speed
    # @property
    # def pause(self):
    #     """
    #     Gets or sets the duration of the pause between texts in milliseconds.
    #     By default, it is set to 1000 milliseconds unless specified.
    #     """
    #     return self._get_attr("pause", def_value=1000, data_type="int")

    # @pause.setter
    # def pause(self, value):
    #     """
    #     Sets the duration of the pause between texts in milliseconds.
    #     This controls how long the system waits before transitioning to the next text animation.
    #     """
    #     self._set_attr("pause", value)

    # @property
    # def display_full_text_on_tap(self):
    #     """Gets whether tapping the animation rushes it to completion."""
    #     return self._get_attr(
    #         "display_full_text_on_tap", def_value=False, data_type="bool"
    #     )

    # @display_full_text_on_tap.setter
    # def display_full_text_on_tap(self, value):
    #     """Sets whether tapping the animation should rush it to completion."""
    #     self._set_attr("display_full_text_on_tap", value)

    # @property
    # def stop_pause_on_tap(self):
    #     """
    #     Gets whether tapping during a pause stops the pause and starts the next text animation.
    #     If true, tapping during a pause will stop it and immediately start the next text animation.
    #     """
    #     return self._get_attr("stop_pause_on_tap", def_value=False, data_type="bool")

    # @stop_pause_on_tap.setter
    # def stop_pause_on_tap(self, value):
    #     """
    #     Sets whether tapping during a pause should stop the pause and start the next text animation.
    #     If true, a tap during a pause will stop the pause and trigger the start of the next text animation.
    #     """
    #     self._set_attr("stop_pause_on_tap", value)

    # @property
    # def is_repeating_animation(self):
    #     """Gets whether the animation is set to repeat."""
    #     return self._get_attr(
    #         "is_repeating_animation", def_value=True, data_type="bool"
    #     )

    # @is_repeating_animation.setter
    # def is_repeating_animation(self, value):
    #     """Sets whether the animation should repeat."""
    #     self._set_attr("is_repeating_animation", value)

    # @property
    # def total_repeat_count(self):
    #     """Gets the total number of times the animation should repeat."""
    #     return self._get_attr("total_repeat_count", def_value=0, data_type="int")

    # @total_repeat_count.setter
    # def total_repeat_count(self, value):
    #     """Sets the number of times the animation should repeat when not set to repeat forever."""
    #     self._set_attr("total_repeat_count", value)

    # # on_tap
    # @property
    # def on_tap(self):
    #     return self._get_event_handler("on_tap")

    # @on_tap.setter
    # def on_tap(self, handler):
    #     self._add_event_handler("on_tap", handler)
    #     self._set_attr("onTap", True if handler is not None else None)

    # # on_finished
    # @property
    # def on_finished(self):
    #     """
    #     Gets the event handler for the 'finished' event.
    #     This event is triggered when the text animation sequence has completed.
    #     """
    #     return self._get_event_handler("on_finished")

    # @on_finished.setter
    # def on_finished(self, handler):
    #     """
    #     Sets the event handler for the 'finished' event.
    #     Registers a function to be called when the text animation sequence completes.
    #     """
    #     self._add_event_handler("on_finished", handler)
    #     self._set_attr("onFinished", True if handler is not None else None)

    # # on_next
    # @property
    # def on_next(self):
    #     """
    #     Gets the event handler for the 'next' event.
    #     This event is triggered when moving to the next text in the sequence.
    #     """
    #     return self._get_event_handler("on_next")

    # @on_next.setter
    # def on_next(self, handler):
    #     """
    #     Sets the event handler for the 'next' event.
    #     Registers a function to be called when transitioning to the next text in the animation.
    #     """
    #     self._add_event_handler("on_next", handler)
    #     self._set_attr("onNext", True if handler is not None else None)

    # # on_next_before_pause
    # @property
    # def on_next_before_pause(self):
    #     """
    #     Gets the event handler for the 'next_before_pause' event.
    #     This event is triggered just before a pause is initiated after a text has been displayed.
    #     """
    #     return self._get_event_handler("on_next_before_pause")

    # @on_next_before_pause.setter
    # def on_next_before_pause(self, handler):
    #     """
    #     Sets the event handler for the 'next_before_pause' event.
    #     Registers a function to be called right before a pause is initiated in the animation cycle.
    #     """
    #     self._add_event_handler("on_next_before_pause", handler)
    #     self._set_attr("onNextBeforePause", True if handler is not None else None)

    # # animate
    # @property
    # def animate(self):
    #     return self._get_attr("animate", def_value=True, data_type="bool")

    # @animate.setter
    # def animate(self, value):
    #     self._set_attr("animate", value)

    # # reverse
    # @property
    # def reverse(self):
    #     return self._get_attr("reverse", def_value=False, data_type="bool")

    # @reverse.setter
    # def reverse(self, value):
    #     self._set_attr("reverse", value)

    # # filter_quality
    # @property
    # def filter_quality(self) -> Optional[FilterQuality]:
    #     return self.__filter_quality

    # @filter_quality.setter
    # def filter_quality(self, value: Optional[FilterQuality]):
    #     self.__filter_quality = value
    #     self._set_attr(
    #         "filterQuality", value.value if isinstance(value, FilterQuality) else value
    #     )

    # # fit
    # @property
    # def fit(self) -> Optional[ImageFit]:
    #     return self.__fit

    # @fit.setter
    # def fit(self, value: Optional[ImageFit]):
    #     self.__fit = value
    #     self._set_attr("fit", value.value if isinstance(value, ImageFit) else value)

    # # background_loading
    # @property
    # def background_loading(self):
    #     return self._get_attr("backgroundLoading", data_type="bool")

    # @background_loading.setter
    # def background_loading(self, value):
    #     self._set_attr("backgroundLoading", value)

    # # on_error
    # @property
    # def on_error(self):
    #     return self._get_event_handler("error")

    # @on_error.setter
    # def on_error(self, handler):
    #     self._add_event_handler("error", handler)
    #     self._set_attr("onError", True if handler is not None else None)
