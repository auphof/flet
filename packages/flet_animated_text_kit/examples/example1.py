import flet as ft
from flet_addons.widgets import animated_text_kit as ftatk
from datetime import datetime

# Update the page to reflect the new item in the list


def main(page: ft.Page):
    # Create a ListView to hold event messages
    event_list = ft.ListView(auto_scroll=True, height=200, reverse=True)

    # def add_event_to_list(message):
    #     # This function adds a new Text widget to the ListView
    #     event_list.controls.append(ft.Text(message))
    #     page.update()

    def add_event_to_list(message):
        # This function adds a new Text widget to the ListView with a timestamp
        now = datetime.now()  # Get the current datetime
        timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # Format the time as HH:mm:ss.xxx
        formatted_message = (
            f"{timestamp} {message}"  # Create the message with timestamp
        )
        event_list.controls.append(ft.Text(formatted_message))  # Add to the ListView
        page.update()

    def atk_error(e):
        add_event_to_list(f"on_error received! e:{e}")

    def atk_tapped(e):
        add_event_to_list(f"on_tap received! e.target:{e.target}")

    def atk_finished(e):
        add_event_to_list(f"on_finished received! e.target:{e.target}")

    def atk_next(e):
        add_event_to_list(f"on_next received! e.target:{e.target}")

    def atk_on_next_before_pause(e):
        add_event_to_list(f"on_next_before_pause received! e.target:{e.target}")

    # # Example usage:
    # animations = [
    #     ftatk.AnimatedText("Typewriter", "Hello World", 500),
    #     ftatk.AnimatedText("Rotate", "Goodbye World", 1700, rotation=15),
    # ]

    # animated_texts = ftatk.AnimatedTexts()
    # animated_texts.append(ftatk.AnimatedText("Typewriter", "Hello World", 500))
    # animated_texts.append(
    #     ftatk.AnimatedText("Rotate", "Goodbye World", 1700, rotation=15)
    # )

    # # Serializing for transmission
    # serialized_animations = [animation.serialize() for animation in animations]

    def example_typewriter(bgcolor=ft.colors.GREEN):
        animated_texts = ftatk.AnimatedTexts()
        # animated_texts.append(ftatk.AnimatedText("Typewriter", "Hello FLET World", 50))
        # animated_texts.append(
        #     ftatk.AnimatedText("Typewriter", "FLET to all devices", 50)
        # )
        animated_texts.append(
            ftatk.TypewriterAnimatedText(text="Hello FLET World", speed=30)
        )
        animated_texts.append(
            ftatk.TypewriterAnimatedText(text="FLET to all devices", speed=30)
        )
        return ft.Container(
            ftatk.AnimatedTextKit(
                # text="This is the Animated Text Kit - typewriter, there is more to come",
                # animated_texts=serialized_animations,
                animated_texts=animated_texts.serialize_all(),
                text_style=ft.TextStyle(
                    italic=True,
                    size=50,
                    color=ft.colors.GREEN,
                    # bgcolor=ft.colors.BLUE_800,
                ),
                pause=2000,
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
                speed=300,
                display_full_text_on_tap=True,
                stop_pause_on_tap=True,
                on_tap=atk_tapped,
                on_error=atk_error,
                on_next=atk_next,
                on_next_before_pause=atk_on_next_before_pause,
            ),
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(10),
        )

    def example_rotate(bgcolor=ft.colors.ORANGE):
        animated_texts = ftatk.AnimatedTexts()
        # animated_texts.append(
        #     ftatk.AnimatedText("Rotate", "Goodbye World", 1700, rotation=15)
        # )
        animated_texts.append(
            ftatk.RotateAnimatedText(
                text="Goodbye World",
                duration=1700,
                rotate_out=False,
                #  rotation=15
            )
        )
        return ft.Container(
            ftatk.AnimatedTextKit(
                # text="This is the Animated Text Kit - typewriter, there is more to come",
                # animated_texts=serialized_animations,
                animated_texts=animated_texts.serialize_all(),
                text_style=ft.TextStyle(
                    italic=True,
                    size=50,
                    color=ft.colors.GREEN,
                    # bgcolor=ft.colors.BLUE_800,
                ),
                repeat_forever=False,
                pause=5000,
                total_repeat_count=4,
                speed=100,
                display_full_text_on_tap=True,
                stop_pause_on_tap=True,
                on_tap=atk_tapped,
                on_finished=atk_finished,
                on_next=atk_next,
                on_next_before_pause=atk_on_next_before_pause,
            ),
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(10),
        )

    images = ft.GridView(
        height=400,
        width=400,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    images.controls.append(example_typewriter())
    images.controls.append(example_rotate())
    # for i in range(0, 60):
    #     images.controls.append(
    #         ft.Image(
    #             src=f"https://picsum.photos/150/150?{i}",
    #             fit=ft.ImageFit.NONE,
    #             repeat=ft.ImageRepeat.NO_REPEAT,
    #             border_radius=ft.border_radius.all(10),
    #         )
    #     )
    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    images,
                    ft.Text(
                        "Following Typing in blue is from Flutter Animated Text Kit",
                        size=30,
                        weight="bold",
                    ),
                    ft.Text(
                        "Flet-Lottie used as a template 💪",
                    ),
                    ft.Container(
                        ft.Text(
                            "⚠️ extending implementation  , adding extra animation types!",
                            size=20,
                        ),
                        bgcolor=ft.colors.YELLOW_100,
                    ),
                    ft.Container(
                        ft.Text(
                            "📝 TODO: -------------------------------------------",
                            size=20,
                        ),
                        bgcolor=ft.colors.YELLOW_100,
                    ),
                    ft.Container(
                        ft.Text(
                            "    1.  Classes for the different types of animation ",
                            size=20,
                        ),
                        bgcolor=ft.colors.YELLOW_100,
                    ),
                    ft.Container(
                        ft.Text("    2. ......", size=20),
                        bgcolor=ft.colors.YELLOW_100,
                    ),
                    # ft.Container(
                    #     ftatk.AnimatedTextKit(
                    #         # text="This is the Animated Text Kit - typewriter, there is more to come",
                    #         # animated_texts=serialized_animations,
                    #         animated_texts=animated_texts.serialize_all(),
                    #         text_style=ft.TextStyle(
                    #             italic=True,
                    #             size=50,
                    #             color=ft.colors.GREEN,
                    #             # bgcolor=ft.colors.BLUE_800,
                    #         ),
                    #         repeat_forever=False,
                    #         pause=5000,
                    #         total_repeat_count=4,
                    #         speed=100,
                    #         display_full_text_on_tap=True,
                    #         stop_pause_on_tap=True,
                    #         on_tap=atk_tapped,
                    #         on_finished=atk_finished,
                    #         on_next=atk_next,
                    #         on_next_before_pause=atk_on_next_before_pause,
                    #     ),
                    #     # bgcolor=ft.colors.BLUE_100,
                    # ),
                    event_list,  # Add the ListView to the Column
                ]
            )
        )
    )


# def main(page: ft.Page):
#     print("QQQQQQQQQQQQQQQQQQQQQQ 1")
#     page.add(ft.SafeArea(ft.Text("Hello, World of Flet!")))


ft.app(main)
