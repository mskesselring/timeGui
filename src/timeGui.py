import PySimpleGUI as sg
import datetime
import pytz


def main():
    font = ("Helvetica", 16)
    str_time = "%H:%M"
    text_color = "green"
    background_color = "black"

    zones = [("Pacific", "US/Pacific"),
             ("EST", "US/Eastern"),
             ("London", "Europe/London"),
             ("Sydney", "Australia/Sydney")]

    tz_times = []
    tz_layouts = []
    tz_labels = []
    frames = []
    for title, _ in zones:
        tz_time = sg.Text("00:00  ", auto_size_text=True, font=font,
                          justification="CENTER", text_color=text_color,
                          background_color=background_color)
        tz_label = sg.Text(title, auto_size_text=True, font=font,
                           justification="CENTER", text_color=text_color,
                           background_color=background_color)
        z_layout = [[tz_time], [tz_label]]
        z_frame = sg.Frame(title="", layout=z_layout,
                           background_color=background_color, border_width=0)

        tz_times.append(tz_time)
        tz_layouts.append(z_layout)
        tz_labels.append(tz_label)
        frames.append(z_frame)

    # Create the window
    layout = [frames]
    window = sg.Window("TimeZones", layout, resizable=True,
                       background_color=background_color)

    # Create an event loop
    while True:
        event, values = window.read(timeout=1000)
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

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
