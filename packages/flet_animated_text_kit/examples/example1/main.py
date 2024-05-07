import flet as ft

print("TESTING TESTING 123 --------------------------------------------------------")
from flet_addons.widgets import animated_text_kit as ftatk

# from flet_core import animated_text_kit as ftatk
from datetime import datetime


TYPEWRITER_TANKA = """FLET on Flutter's grace,
iOS, web, Android meet.
Desktop, seamless too,
Everywhere, FLET takes its stance—
Unity in every glance."""


ROTATE_HIKU = """FLET runs everywhere,
FLET on iOS, Android, web,
FLET in every tap"""

FADING_LIMERICK = """FLET's a clever tool that's quite neat,
On every device, it's elite.
It runs on all screens,
Efficiency it means,
Ensuring success in each FLET.
"""
SCALE_WORDS = """FLET
FLET on iOS
FLET on Android
FLET on Web
FLET on Desktop Windows
FLET on Desktop Linux
where do you FLET ?"""


def main(page: ft.Page):
    page.window_height = 1000
    page.window_width = 900
    # Fonts to support  the examples, saved in assests folder
    page.fonts = {
        # UNCOMMENT if using local assets
        "Agne": "fonts/Agne.otf",
        "Horizon": "fonts/Horizon.otf",
        "Canterbury": "fonts/Canterbury.ttf",
        # "Agne": "https://github.com/aagarwal1012/Animated-Text-Kit/raw/master/example/assets/Agne.otf",
        # "Horizon": "https://github.com/aagarwal1012/Animated-Text-Kit/raw/master/example/assets/Horizon.otf",
        # "Canterbury": "https://github.com/aagarwal1012/Animated-Text-Kit/raw/master/example/assets/Canterbury.ttf",
    }

    # Create a ListView to hold event messages
    eventlog_list = ft.ListView(auto_scroll=True, height=300, reverse=True)

    def add_to_eventlog(message):
        # This function adds a new Text widget to the ListView with a timestamp
        now = datetime.now()  # Get the current datetime
        timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # Format the time as HH:mm:ss.xxx
        formatted_message = (
            f"{timestamp} {message}"  # Create the message with timestamp
        )
        eventlog_list.controls.append(ft.Text(formatted_message))  # Add to the ListView
        page.update()

    def atk_error(e):
        add_to_eventlog(f"on_error received! e:{e}")

    def atk_tapped(e):
        add_to_eventlog(f"on_tap received! e.target:{e.target}")

    def atk_finished(e):
        add_to_eventlog(f"on_finished received! e.target:{e.target}")

    def atk_next(e):
        add_to_eventlog(f"on_next received! e.target:{e.target}")

    def atk_on_next_before_pause(e):
        add_to_eventlog(f"on_next_before_pause received! e.target:{e.target}")

    # Example usage:
    def example_typewriter(bgcolor=ft.colors.TEAL_700):
        animated_texts = ftatk.AnimatedTexts()

        # Split the string into lines and append to a list
        for line in TYPEWRITER_TANKA.split("\n"):
            animated_texts.append(ftatk.TypewriterAnimatedText(text=line, speed=60))

        return ft.Container(
            ftatk.AnimatedTextKit(
                animated_texts=animated_texts,
                text_style=ft.TextStyle(
                    # italic=True,
                    size=20,
                    font_family="Agne",
                    color=ft.colors.WHITE,
                ),
                pause=1500,
                # ---Repeating -------------------
                # repeat_forever=True,
                # is_repeating_animation=True,
                # on_finished=None,
                # -------- Non Repeating
                repeat_forever=False,
                is_repeating_animation=True,
                on_finished=atk_finished,
                total_repeat_count=4,
                # - Other properties and events
                # TODO TD - Speed needs implementing, seems to have no effect at the moment
                # speed=600,
                display_full_text_on_tap=True,
                stop_pause_on_tap=True,
                on_tap=atk_tapped,
                on_error=atk_error,
                on_next=atk_next,
                on_next_before_pause=atk_on_next_before_pause,
            ),
            margin=5,
            padding=5,
            alignment=ft.alignment.center_left,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(10),
        )

    def example_rotate(bgcolor=ft.colors.ORANGE_800):
        animated_texts = ftatk.AnimatedTexts()

        #  Split the string into lines, remove the first word and space, then append to a list
        # The first word is shown Statically
        for line in ROTATE_HIKU.split("\n"):
            animated_texts.append(
                ftatk.RotateAnimatedText(
                    text=" ".join(line.split(" ")[1:]),
                    duration=1700,
                    rotate_out=True,
                )
            )
        return ft.Container(
            ft.Row(
                controls=[
                    ft.Text("FLET", style=ft.TextStyle(size=30, color=ft.colors.WHITE)),
                    ft.Container(
                        ftatk.AnimatedTextKit(
                            animated_texts=animated_texts,
                            text_style=ft.TextStyle(
                                # italic=True,
                                size=30,
                                font_family="Horizon",
                                color=ft.colors.WHITE,
                            ),
                            repeat_forever=False,
                            pause=500,
                            total_repeat_count=12,
                            speed=100,
                            display_full_text_on_tap=True,
                            stop_pause_on_tap=True,
                            on_tap=atk_tapped,
                            on_finished=atk_finished,
                            on_next=atk_next,
                            on_next_before_pause=atk_on_next_before_pause,
                        ),
                        alignment=ft.alignment.center,
                        # height=300,
                    ),
                ],
                height=300,
            ),
            margin=5,
            padding=5,
            alignment=ft.alignment.center,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(10),
        )

    def example_fade(bgcolor=ft.colors.BROWN_600):
        animated_texts = ftatk.AnimatedTexts()

        #  Split the limerick into lines,
        for line in FADING_LIMERICK.split("\n"):
            animated_texts.append(
                ftatk.FadeAnimatedText(
                    text=line,
                    duration=1700,
                )
            )
        return ft.Container(
            ftatk.AnimatedTextKit(
                animated_texts=animated_texts,
                text_style=ft.TextStyle(
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                ),
                repeat_forever=False,
                pause=500,
                total_repeat_count=4,
                speed=100,
                display_full_text_on_tap=True,
                stop_pause_on_tap=True,
                on_tap=atk_tapped,
                on_finished=atk_finished,
                on_next=atk_next,
                on_next_before_pause=atk_on_next_before_pause,
            ),
            margin=5,
            padding=5,
            alignment=ft.alignment.center,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(10),
        )

    def example_scale(bgcolor=ft.colors.BLUE_700):
        animated_texts = ftatk.AnimatedTexts()

        #  Split the limerick into lines,
        for line in SCALE_WORDS.split("\n"):
            animated_texts.append(
                ftatk.ScaleAnimatedText(text=line, duration=2500, scaling_factor=4.0)
            )
        return ft.Container(
            ftatk.AnimatedTextKit(
                animated_texts=animated_texts,
                text_style=ft.TextStyle(
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    # font_family="Canterbury",
                    color=ft.colors.WHITE,
                ),
                repeat_forever=False,
                pause=500,
                total_repeat_count=4,
                speed=100,
                display_full_text_on_tap=True,
                stop_pause_on_tap=True,
                on_tap=atk_tapped,
                on_finished=atk_finished,
                on_next=atk_next,
                on_next_before_pause=atk_on_next_before_pause,
            ),
            margin=5,
            padding=5,
            alignment=ft.alignment.center,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(10),
        )

    text_animations = ft.GridView(
        height=500,
        width=1000,
        runs_count=2,
        max_extent=590,
        child_aspect_ratio=2,
        spacing=5,
        run_spacing=5,
    )

    text_animations.controls.append(example_typewriter())
    text_animations.controls.append(example_rotate())
    text_animations.controls.append(example_fade())
    text_animations.controls.append(example_scale())
    page.add(
        ft.SafeArea(
            ft.Column(
                controls=[
                    ft.Markdown(
                        """
# FLET Animated Text Kit 
from flutter Animated Text Kit                                 
https://pub.dev/packages/animated_text_kit
                                """,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        selectable=True,
                        auto_follow_links=True,
                        auto_follow_links_target="_blank",
                    ),
                    text_animations,
                    ft.Divider(),
                    ft.Text("Event log....."),
                    eventlog_list,  # Add the ListView to the Column
                ],
                expand=True,
            )
        )
    )


ft.app(main)
