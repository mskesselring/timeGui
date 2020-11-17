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
    justification = "left"

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
            raise FileNotFoundError(f"json config file not found at {json_path}")
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
                          background_color=background_color)
        tz_label = sg.Text(title, auto_size_text=True, font=font,
                           justification=justification, text_color=text_color,
                           background_color=background_color)
        z_layout = [[tz_time], [tz_label]]
        z_frame = sg.Frame(title="", layout=z_layout,
                           background_color=background_color, border_width=0,
                           element_justification=justification)

        tz_times.append(tz_time)
        tz_layouts.append(z_layout)
        tz_labels.append(tz_label)
        frames.append(z_frame)

    # Font size buttons
    # TODO: Possibly add dynamic font size
    # font_up = sg.Button("+")
    # font_down = sg.Button("-")

    # Create the window
    layout = [frames]
    window = sg.Window("TimeZones", layout, resizable=True,
                       background_color=background_color)

    # Create an event loop
    while True:
        event, values = window.read(timeout=1000)
        font_updated = False
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break
        elif event == "+":
            font = (font[0], font[1] + 1)
            font_updated = True
        elif event == "-":
            font = (font[0], font[1] - 1)
            font_updated = True

        # If not, update times
        for idx, tz_time in enumerate(tz_times):
            _, zone_name = zones[idx]
            z_datetime = datetime.datetime.now().astimezone(
                    pytz.timezone(zone_name)
            )
            tz_time.update(value=z_datetime.strftime(str_time))

        window.finalize()

    window.close()


if __name__ == "__main__":
    main()
