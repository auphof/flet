from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ImageFit,
)
from flet_core.video import FilterQuality


class AnimatedTextKit(ConstrainedControl):
    """
    Displays lottie animations.


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
        animate: Optional[bool] = None,
        background_loading: Optional[bool] = None,
        filter_quality: Optional[FilterQuality] = None,
        fit: Optional[ImageFit] = None,
        on_error=None,
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

        self.text = text
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

    # text
    @property
    def text(self):
        return self._get_attr("text", def_value="", data_type="str")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # repeatForever
    @property
    def repeat_forever(self):
        return self._get_attr("repeat_forever", def_value=True, data_type="bool")

    @repeat_forever.setter
    def repeat_forever(self, value):
        self._set_attr("repeat_forever", value)

    # speed
    @property
    def speed(self):
        return self._get_attr("speed", def_value=250, data_type="int")

    @speed.setter
    def speed(self, value):
        self._set_attr("speed", value)

    # speed
    @property
    def pause(self):
        """
        Gets or sets the duration of the pause between texts in milliseconds.
        By default, it is set to 1000 milliseconds unless specified.
        """
        return self._get_attr("pause", def_value=1000, data_type="int")

    @pause.setter
    def pause(self, value):
        """
        Sets the duration of the pause between texts in milliseconds.
        This controls how long the system waits before transitioning to the next text animation.
        """
        self._set_attr("pause", value)

    @property
    def display_full_text_on_tap(self):
        """Gets whether tapping the animation rushes it to completion."""
        return self._get_attr(
            "display_full_text_on_tap", def_value=False, data_type="bool"
        )

    @display_full_text_on_tap.setter
    def display_full_text_on_tap(self, value):
        """Sets whether tapping the animation should rush it to completion."""
        self._set_attr("display_full_text_on_tap", value)

    @property
    def stop_pause_on_tap(self):
        """
        Gets whether tapping during a pause stops the pause and starts the next text animation.
        If true, tapping during a pause will stop it and immediately start the next text animation.
        """
        return self._get_attr("stop_pause_on_tap", def_value=False, data_type="bool")

    @stop_pause_on_tap.setter
    def stop_pause_on_tap(self, value):
        """
        Sets whether tapping during a pause should stop the pause and start the next text animation.
        If true, a tap during a pause will stop the pause and trigger the start of the next text animation.
        """
        self._set_attr("stop_pause_on_tap", value)

    @property
    def is_repeating_animation(self):
        """Gets whether the animation is set to repeat."""
        return self._get_attr(
            "is_repeating_animation", def_value=True, data_type="bool"
        )

    @is_repeating_animation.setter
    def is_repeating_animation(self, value):
        """Sets whether the animation should repeat."""
        self._set_attr("is_repeating_animation", value)

    @property
    def total_repeat_count(self):
        """Gets the total number of times the animation should repeat."""
        return self._get_attr("total_repeat_count", def_value=0, data_type="int")

    @total_repeat_count.setter
    def total_repeat_count(self, value):
        """Sets the number of times the animation should repeat when not set to repeat forever."""
        self._set_attr("total_repeat_count", value)

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
