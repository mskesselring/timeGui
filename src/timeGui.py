import PySimpleGUI as sg
import datetime
import pytz
import json
import os
import logging


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    font = ("Helvetica", 16)
    str_time = "%H:%M"
    text_color = "green"
    background_color = "black"
    justification = "center"
    update_period = 1

    # Read time zone info from config
    base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(base_path, "config", "timezone_config.json")
    try:
        if os.path.isfile(json_path):
            print("Reading from json")
            zones = []
            with open(json_path, "r") as json_file:
                zone_list = json.load(json_file)
                for zone in zone_list:
                    zones.append((zone["display_name"], zone["zone_name"]))
            print("Loaded json config")
        else:
            raise FileNotFoundError(
                    f"json config file not found at {json_path}")
    except Exception as e:
        logger.exception(e)
        print("Loading default config")
        zones = [("Pacific", "US/Pacific"),
                 ("EST", "US/Eastern"),
                 ("London", "Europe/London"),
                 ("Sydney", "Australia/Sydney")]

    # Create GUI objects
    tz_times = []
    tz_layouts = []
    tz_labels = []
    frames = []
    for title, _ in zones:
        tz_time = sg.Text("00:00", auto_size_text=True, font=font,
                          justification=justification, text_color=text_color,
                          background_color=background_color,
                          grab=True)
        tz_label = sg.Text(title, auto_size_text=True, font=font,
                           justification=justification, text_color=text_color,
                           background_color=background_color,
                           grab=True)
        z_layout = [[tz_time], [tz_label]]
        z_frame = sg.Frame(title="", layout=z_layout,
                           background_color=background_color, border_width=0,
                           element_justification=justification,
                           vertical_alignment="center")

        tz_times.append(tz_time)
        tz_layouts.append(z_layout)
        tz_labels.append(tz_label)
        frames.append(z_frame)

    # Font size buttons
    # TODO: Possibly add dynamic font size
    # font_up = sg.Button("+")
    # font_down = sg.Button("-")

    # Create the window
    center_text = sg.Text(key='-EXPAND-', font=("Helvetica", 1), pad=(0, 0),
                          background_color=background_color, grab=True)
    layout = [[center_text],
              frames]
    right_click_menu = ['&Right',
                        ['E&xit']]
    window = sg.Window("TimeZones", layout, resizable=True,
                       background_color=background_color, auto_size_text=True,
                       no_titlebar=True, return_keyboard_events=True,
                       text_justification="center",
                       element_justification="center",
                       right_click_menu=right_click_menu, grab_anywhere=True)
    window.finalize()
    # TODO: Add command line option to maximize
    # window.Maximize()
    center_text.expand(True, True, True)

    # Create an event loop
    first_loop = True
    while True:
        if first_loop:
            event, values = "__TIMEOUT__", {}
            window.finalize()
            first_loop = False
        else:
            event, values = window.read(timeout=update_period * 1000)

        font_updated = False
        # End program if user closes window
        if (event == sg.WIN_CLOSED) or (event == "\r") or (event == "Exit"):
            break
        elif event == "+":
            font = (font[0], font[1] + 1)
            font_updated = True
        elif event == "-":
            font = (font[0], font[1] - 1)
            font_updated = True
        elif event == "__TIMEOUT__":
            # If not, update times
            for frame in frames:
                frame.expand(expand_x=True)
                frame.update()
            for idx, tz_time in enumerate(tz_times):
                frame = frames[idx]
                label = tz_labels[idx]
                _, zone_name = zones[idx]
                z_datetime = datetime.datetime.now().astimezone(
                        pytz.timezone(zone_name)
                )
                tz_time.update(value=z_datetime.strftime(str_time))

    window.close()


if __name__ == "__main__":
    main()
