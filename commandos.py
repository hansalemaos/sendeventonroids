import struct
import time
import shutil
import sys
import re
import random
from adbshellexecuter import UniversalADBExecutor
import struct
import base64
from cythoncubicspline import (
    get_rectangle_coordinates_surface,
    get_ellipse_coordinates_surface,
    get_polygon_coordinates_surface,
    calculate_missing_coords_and_fill_all_holes,
    get_coords_of_line,
    get_circle_coordinates,
    get_rectangle_coordinates_surface,
    get_ellipse_coordinates_surface,
    get_polygon_coordinates_surface,
)
from typing import Literal

regex_compiled_for_bin_prefix = re.compile(r"^b[\'\"]", re.I)

FORMAT = "iiHHI"  # should be "llHHI", but long is sometimes 32 bit and sometimes 64 bit, that way it works on both
COMMAND_GET_MAX_SCREEN_VALUES = """ | grep "ABS_MT_POSITION" | awk 'BEGIN{FS="max[[:space:]]+";}{print $2}' | awk 'BEGIN{FS=",";}{printf $1" "}' | xargs"""
COMMAND_GET_RESOLUTION = """wm size | awk '{print $NF}'"""
chunk_size = struct.calcsize(FORMAT)
pack_fu = struct.Struct(FORMAT).pack
unpack_fu = struct.Struct(FORMAT).unpack
modulecfg = sys.modules[__name__]
modulecfg.cache_structs_mouse_input_data = {}
modulecfg.cache_data = {}
modulecfg.cache_screen_size_dict = {}
modulecfg.cache_complex_swipe_events = {}
modulecfg.cache_simple_click_events = {}
modulecfg.cache_commands_base64 = {}
modulecfg.cache_commands_ascii = {}
modulecfg.cache_commands_concat_str_and_bytes = {}
modulecfg.cache_executable_commands = {}
modulecfg.cache_string_bytes_newlines_linux = {}
modulecfg.cache_complex_dd_swipes = {}
modulecfg.cache_split_echo_printf = {}


def get_n_coordinates_from_geoshape(
    numer_of_coordinates,
    kind: Literal["circle", "rectangle", "ellipse", "polygon"],
    **kwargs,
):
    print(kwargs)
    if kind == "circle":
        circle_coords = list(set(get_circle_coordinates(*kwargs.values())))
    if kind == "rectangle":
        circle_coords = list(set(get_rectangle_coordinates_surface(*kwargs.values())))
    if kind == "ellipse":
        circle_coords = list(set(get_ellipse_coordinates_surface(*kwargs.values())))
    if kind == "polygon":
        circle_coords = list(set(get_polygon_coordinates_surface(*kwargs.values())))
    circle_counter = 0
    circle_coords_joined = []
    for index_x0_y0, index_x1_y1 in zip(
        range(1, len(circle_coords) - 1), range(len(circle_coords))
    ):
        try:
            line_coords = get_coords_of_line(
                circle_coords[index_x0_y0][0],
                circle_coords[index_x0_y0][1],
                circle_coords[index_x1_y1][0],
                circle_coords[index_x1_y1][1],
            )
            circle_coords_joined.extend(line_coords)
            circle_counter = circle_counter + 1
            if circle_counter >= numer_of_coordinates:
                break
        except Exception as e:
            print(e)

    return circle_coords_joined


def get_n_coordinates_from_circle(
    x,
    y,
    radius,
    numer_of_coordinates=100,
):
    return get_n_coordinates_from_geoshape(
        numer_of_coordinates=numer_of_coordinates,
        kind="circle",
        x=x,
        y=y,
        r=radius,
    )


def get_n_coordinates_from_rectangle(
    x,
    y,
    width,
    height,
    numer_of_coordinates=100,
):
    return get_n_coordinates_from_geoshape(
        numer_of_coordinates=numer_of_coordinates,
        kind="rectangle",
        x=x,
        y=y,
        w=width,
        h=height,
    )


def get_n_coordinates_from_ellipse(
    x_center,
    y_center,
    rx,
    ry,
    numer_of_coordinates=100,
):
    return get_n_coordinates_from_geoshape(
        numer_of_coordinates=numer_of_coordinates,
        kind="ellipse",
        x_center=x_center,
        y_center=y_center,
        rx=rx,
        ry=ry,
    )


def get_n_coordinates_from_polygon(
    vertices,
    numer_of_coordinates=100,
):
    return get_n_coordinates_from_geoshape(
        numer_of_coordinates=numer_of_coordinates,
        kind="polygon",
        vertices=[(int(q[0]), int(q[1])) for q in vertices],
    )


def cached_struct_pack(q):
    return modulecfg.cache_structs_mouse_input_data.setdefault(q, pack_fu(*q))


def generate_mouse_input_data(
    x,
    y,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
):
    

    finaldata = b""
    if not x_max or not y_max or not screen_width or not screen_height:
        x_max, y_max, screen_width, screen_height = get_screen_data(
            device_serial, inputdev=inputdev, adb_path=adb_path
        )
    if not randomize_data:
        finaldata = modulecfg.cache_structs_mouse_input_data.get(
            (x, y, x_max, y_max, screen_width, screen_height), b""
        )
    if not finaldata:
        timestamp_likely_not_important = (
            1720908827 if not randomize_data else time.time()
        )
        alwayszero = 0
        likely_some_pressing_force = (
            60466 if not randomize_data else random.randint(1, 65439)
        )
        slowly_increasing_low_char = 4 if not randomize_data else random.randint(1, 15)
        input_event1 = 3
        input_event2 = 54
        constant_3473411 = 3473411
        ycoord = int(y * y_max / screen_height)
        xcoord = int(x * x_max / screen_width)
        constant_64539 = 64539
        constant_26258 = 26258
        maybe_time_delta = 322610 if not randomize_data else random.randint(1, 400_000)
        constant_131072 = 131072

        finaldata = b"".join(
            cached_struct_pack(q)
            for q in (
                (
                    timestamp_likely_not_important,
                    alwayszero,
                    likely_some_pressing_force,
                    slowly_increasing_low_char,
                    alwayszero,
                ),
                (
                    constant_3473411,
                    xcoord,
                    constant_64539,
                    constant_26258,
                    alwayszero,
                ),
                (
                    maybe_time_delta,
                    alwayszero,
                    input_event1,
                    input_event2,
                    ycoord,
                ),
                (
                    timestamp_likely_not_important,
                    alwayszero,
                    likely_some_pressing_force,
                    slowly_increasing_low_char,
                    alwayszero,
                ),
                (
                    constant_131072,
                    alwayszero,
                    constant_64539,
                    constant_26258,
                    alwayszero,
                ),
                (
                    maybe_time_delta,
                    alwayszero,
                    alwayszero,
                    alwayszero,
                    alwayszero,
                ),
            )
        )
        if not randomize_data:
            modulecfg.cache_structs_mouse_input_data[
                (x, y, x_max, y_max, screen_width, screen_height)
            ] = finaldata
    return finaldata


def get_finish_click_command(randomize_data=False):
    finalcmd = b""
    if not randomize_data:
        finalcmd = modulecfg.cache_structs_mouse_input_data.get(
            "get_finish_click_command", b""
        )
    if not finalcmd:
        timestamp_likely_not_important = (
            1720908827 if not randomize_data else time.time()
        )
        alwayszero = 0
        slowly_increasing_low_char = 4 if not randomize_data else random.randint(1, 15)
        constant_131072 = 131072
        constant_26258 = 26258
        constant_64539 = 64539
        maybe_time_delta = 322610 if not randomize_data else random.randint(1, 400_000)
        likely_some_pressing_force = (
            11631 if not randomize_data else random.randint(1, 65439)
        )

        finalcmd = b"".join(
            cached_struct_pack(q)
            for q in (
                (
                    timestamp_likely_not_important,
                    alwayszero,
                    likely_some_pressing_force,
                    slowly_increasing_low_char,
                    alwayszero,
                ),
                (
                    constant_131072,
                    alwayszero,
                    constant_64539,
                    constant_26258,
                    alwayszero,
                ),
                (
                    maybe_time_delta,
                    alwayszero,
                    alwayszero,
                    alwayszero,
                    alwayszero,
                ),
            )
        )
        if not randomize_data:
            modulecfg.cache_data["get_finish_click_command"] = finalcmd
    return finalcmd


def get_screen_data(device_serial, inputdev, adb_path=None):
    screendata = modulecfg.cache_screen_size_dict.get((device_serial, inputdev), {})

    if not screendata:
        if not adb_path:
            adb_path = shutil.which("adb")
        adbsh = UniversalADBExecutor(adb_path, device_serial)

        stdout, stderr, returncode = (
            adbsh.shell_with_capturing_import_stdout_and_stderr(
                f"""getevent -lp {inputdev}""" + COMMAND_GET_MAX_SCREEN_VALUES
            )
        )
        p = stdout.decode("utf-8", errors="ignore").strip()
        x_max, y_max = p.split()
        x_max = int(x_max.strip())
        y_max = int(y_max.strip())
        stdout, stderr, returncode = (
            adbsh.shell_with_capturing_import_stdout_and_stderr(COMMAND_GET_RESOLUTION)
        )
        screensize = stdout.decode("utf-8").strip().split("x")
        screen_width, screen_height = screensize
        screen_width = int(screen_width.strip())
        screen_height = int(screen_height.strip())
        modulecfg.cache_screen_size_dict[(device_serial, inputdev)] = {
            "x_max": x_max,
            "y_max": y_max,
            "screen_width": screen_width,
            "screen_height": screen_height,
        }
        return x_max, y_max, screen_width, screen_height
    return tuple(screendata.values())


def _convert_list_to_tuple(x):
    return tuple((int(y), int(y)) for y in x)


def get_raw_swipe_command_from_list_of_coordinates(
    x_y_coordinates,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
):
    if isinstance(x_y_coordinates, list) and isinstance(x_y_coordinates[0], tuple):
        x_y_coordinates = tuple(x_y_coordinates)
    iscacheable = (
        isinstance(x_y_coordinates, tuple)
        and isinstance(x_y_coordinates[0], tuple)
        and not randomize_data
    )
    fullcommand = b""
    if not x_max or not y_max or not screen_width or not screen_height:
        x_max, y_max, screen_width, screen_height = get_screen_data(
            device_serial, inputdev=inputdev, adb_path=adb_path
        )
    if iscacheable:
        fullcommand = modulecfg.cache_complex_swipe_events.get(
            (x_y_coordinates, device_serial, inputdev, number_of_finish_commands), b""
        )
    if not fullcommand:
        fullcommand = (
            b"".join(
                (
                    generate_mouse_input_data(
                        int(x),
                        int(y),
                        device_serial=device_serial,
                        inputdev=inputdev,
                        adb_path=adb_path,
                        x_max=int(x_max),
                        y_max=int(y_max),
                        screen_width=int(screen_width),
                        screen_height=int(screen_height),
                        randomize_data=randomize_data,
                    )
                )
                for x, y in x_y_coordinates
                if x >= 0 and y >= 0
            )
        ) + b"".join(
            get_finish_click_command(randomize_data=randomize_data)
            for _ in range(number_of_finish_commands)
        )
        if not iscacheable:
            return fullcommand
        modulecfg.cache_complex_swipe_events[
            (x_y_coordinates, device_serial, inputdev, number_of_finish_commands)
        ] = fullcommand
        return modulecfg.cache_complex_swipe_events[
            (x_y_coordinates, device_serial, inputdev, number_of_finish_commands)
        ]
    return fullcommand


def get_raw_swipe_command_through_a_couple_of_coordinates(
    x_y_coordinates,
    xtolerance=-2,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
):
    return get_raw_swipe_command_from_list_of_coordinates(
        x_y_coordinates=tuple(
            calculate_missing_coords_and_fill_all_holes(
                coordlist=x_y_coordinates
                if isinstance(x_y_coordinates, list)
                else list(x_y_coordinates),
                xtolerance=xtolerance,
                minvalue_x=0,
                minvalue_y=0,
                maxvalue_x=0,
                maxvalue_y=0,
                check_minvalue_x=True,
                check_maxvalue_x=False,
                check_minvalue_y=True,
                check_maxvalue_y=False,
            )
        ),
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
    )


def _get_raw_swipe_command_from_2_coordinates(
    x0,
    y0,
    x1,
    y1,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    echo_or_printf="echo -e -n",
):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    x_y_coordinates = tuple(get_coords_of_line(x0, y0, x1, y1))
    return _get_swipe_command_from_many_points(
        x_y_coordinates=x_y_coordinates,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf=echo_or_printf,
    )


def get_swipe_command_from_2_coordinates_echo_e_n(
    x0,
    y0,
    x1,
    y1,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _get_raw_swipe_command_from_2_coordinates(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf="echo -e -n",
    )


def get_swipe_command_from_2_coordinates_printf(
    x0,
    y0,
    x1,
    y1,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _get_raw_swipe_command_from_2_coordinates(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf='printf "%b"',
    )


def get_raw_click_command_from_xy_coordinates(
    x,
    y,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
):
    clickcommandbinary = b""
    if not x_max or not y_max or not screen_width or not screen_height:
        x_max, y_max, screen_width, screen_height = get_screen_data(
            device_serial, inputdev=inputdev, adb_path=adb_path
        )
    if not randomize_data:
        clickcommandbinary = modulecfg.cache_simple_click_events.get(
            (x, y, device_serial, inputdev, number_of_finish_commands), b""
        )
    if not clickcommandbinary:
        clickcommandbinary = generate_mouse_input_data(
            x=x,
            y=y,
            device_serial=device_serial,
            inputdev=inputdev,
            adb_path=adb_path,
            x_max=x_max,
            y_max=y_max,
            screen_width=screen_width,
            screen_height=screen_height,
            randomize_data=randomize_data,
        ) + b"".join(
            get_finish_click_command(randomize_data=randomize_data)
            for _ in range(number_of_finish_commands)
        )
        if not randomize_data:
            modulecfg.cache_simple_click_events[
                (x, y, device_serial, inputdev, number_of_finish_commands)
            ] = clickcommandbinary
    return clickcommandbinary


def convert_to_ascii(data):
    return modulecfg.cache_commands_ascii.setdefault(
        data,
        regex_compiled_for_bin_prefix.sub("", ascii(data)[:-1]).replace("'", "'\\''"),
    )


def convert_to_ascii_blocks(
    data,
    outputpath="/dev/input/event4",
    chunksize=128,
    echo_or_printf=b'printf "%b"',
    split_into_chunks=True,
):
    outputdata = modulecfg.cache_split_echo_printf.get(
        (data, outputpath, echo_or_printf, chunksize, split_into_chunks, "ascii"), b""
    )
    if not outputdata:
        if isinstance(echo_or_printf, str):
            echo_or_printf = echo_or_printf.encode()

        data = regex_compiled_for_bin_prefix.sub("", ascii(data)[:-1])
        if isinstance(data, str):
            data = data.encode()
        if isinstance(outputpath, str):
            outputpath = outputpath.encode()

        if split_into_chunks:
            outputdata = b"\n".join(
                [
                    (
                        echo_or_printf
                        + b" '"
                        + data[i : i + chunksize].replace(b"'", b"'\\''")
                    )
                    + b"'"
                    + (b" > " if i == 0 else b" >> ")
                    + outputpath
                    for i in range(0, len(data), chunksize)
                ]
            ).replace(b"\r\n", b"\n")
        else:
            outputdata = (
                (echo_or_printf + b" '" + data.replace(b"'", b"'\\''") + b"'")
                + b" > "
                + outputpath
            ).replace(b"\r\n", b"\n")
        modulecfg.cache_split_echo_printf[
            (data, outputpath, echo_or_printf, chunksize, split_into_chunks, "ascii")
        ] = outputdata
    return outputdata


def convert_to_base64_blocks(
    data,
    outputpath="/dev/input/event4",
    chunksize=128,
    echo_or_printf=b'printf "%b"',
    split_into_chunks=True,
):
    outputdata = modulecfg.cache_split_echo_printf.get(
        (data, outputpath, echo_or_printf, chunksize, split_into_chunks, "base64"), b""
    )
    if not outputdata:
        if isinstance(echo_or_printf, str):
            echo_or_printf = echo_or_printf.encode()
        if isinstance(data, str):
            data = data.encode()
        data = base64.b64encode(data)
        if isinstance(outputpath, str):
            outputpath = outputpath.encode()
        outputpathtmp = outputpath + b".tmp"
        if split_into_chunks:
            outputdata = b"\n".join(
                [
                    (
                        echo_or_printf
                        + b" '"
                        + (data[i : i + chunksize]).replace(b"'", b"'\\''")
                    )
                    + b"'"
                    + (b" > " if i == 0 else b" >> ")
                    + outputpathtmp
                    for i in range(0, len(data), chunksize)
                ]
            ).replace(b"\r\n", b"\n")
        else:
            outputdata = (
                (echo_or_printf + b" '" + (data).replace(b"'", b"'\\''") + b"'")
                + b" > "
                + outputpathtmp
            ).replace(b"\r\n", b"\n")
        outputdata = outputdata + b"\nbase64 -d " + outputpathtmp + b" > " + outputpath
        modulecfg.cache_split_echo_printf[
            (data, outputpath, echo_or_printf, chunksize, split_into_chunks, "base64")
        ] = outputdata
    return outputdata


def dos2unix(data):
    if isinstance(data, str):
        return modulecfg.cache_string_bytes_newlines_linux.setdefault(
            data, data.replace("\r\n", b"\n")
        )
    return modulecfg.cache_string_bytes_newlines_linux.setdefault(
        data, data.replace(b"\r\n", b"\n")
    )


def convert_to_base64(data):
    return modulecfg.cache_commands_base64.setdefault(
        data,
        base64.b64encode(
            data if isinstance(data, bytes) else dos2unix(data.encode("utf-8"))
        ),
    )


def convert_to_concat_str_and_bytes(data, sep=b""):
    if not isinstance(data, (tuple)):
        data = tuple(data)
    return modulecfg.cache_commands_concat_str_and_bytes.setdefault(
        (data, sep),
        (sep if isinstance(sep, bytes) else dos2unix(sep.encode("utf-8"))).join(
            d if isinstance(d, bytes) else dos2unix(d.encode("utf-8")) for d in data
        ),
    )


def _convert_command_to_echo_or_printf(
    binary_data, inputdev, echo_or_printf="echo -e -n", su_exe="su"
):
    return modulecfg.cache_executable_commands.setdefault(
        (echo_or_printf, binary_data, inputdev, su_exe),
        convert_to_concat_str_and_bytes(
            data=(
                f"{su_exe}\n" if su_exe else "",
                convert_to_ascii_blocks(
                    data=binary_data,
                    outputpath=inputdev,
                    chunksize=1024,
                    echo_or_printf=echo_or_printf,
                    split_into_chunks=False,
                ),
            ),
            sep=b"",
        ),
    )


def convert_command_to_echo_e_n(binary_data, inputdev, su_exe="su"):
    return _convert_command_to_echo_or_printf(
        binary_data=binary_data,
        inputdev=inputdev,
        echo_or_printf="echo -e -n",
        su_exe=su_exe,
    )


def convert_command_to_printf(binary_data, inputdev, su_exe="su"):
    return _convert_command_to_echo_or_printf(
        binary_data=binary_data,
        inputdev=inputdev,
        echo_or_printf='printf "%b"',
        su_exe=su_exe,
    )


def _convert_command_to_echo_or_printf_and_cat(
    binary_data,
    inputdev,
    output_path="/sdcard/echoen_cat.bin",
    su_exe="su",
    cat_or_cp="cat",
    echo_or_printf="echo -e -n",
):
    return modulecfg.cache_executable_commands.setdefault(
        (echo_or_printf, binary_data, inputdev, su_exe, output_path, cat_or_cp),
        (
            convert_to_concat_str_and_bytes(
                data=(
                    f"{su_exe}\n" if su_exe else "",
                    convert_to_base64_blocks(
                        data=binary_data,
                        outputpath=inputdev,
                        chunksize=1024,
                        echo_or_printf=echo_or_printf,
                        split_into_chunks=True,
                    ),
                ),
                sep=b"",
            ),
            (
                f"cat {output_path} > {inputdev}\n"
                if cat_or_cp == "cat"
                else f"cp {output_path} {inputdev}\n"
            ).encode("utf-8"),
        ),
    )


def convert_command_to_echo_e_n_and_cat(
    binary_data,
    inputdev,
    output_path="/sdcard/echoen_cat.bin",
    su_exe="su",
    cat_or_cp="cat",
):
    return _convert_command_to_echo_or_printf_and_cat(
        binary_data=binary_data,
        inputdev=inputdev,
        output_path=output_path,
        su_exe=su_exe,
        cat_or_cp=cat_or_cp,
        echo_or_printf="echo -e -n",
    )


def convert_command_to_printf_and_cat(
    binary_data,
    inputdev,
    output_path="/sdcard/printf_cat.bin",
    su_exe="su",
    cat_or_cp="cat",
):
    return _convert_command_to_echo_or_printf_and_cat(
        binary_data=binary_data,
        inputdev=inputdev,
        output_path=output_path,
        su_exe=su_exe,
        cat_or_cp=cat_or_cp,
        echo_or_printf='printf "%b"',
    )


def _convert_command_to_echo_or_printf_and_dd(
    binary_data,
    inputdev,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    echo_or_printf="echo -e -n",
):
    scriptdata, binarydata, executecommand, output_path_sh = _generate_dd_command(
        binary_data=binary_data,
        output_path=output_path,
        inputdev=inputdev,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        su_exe=su_exe,
    )
    return (
        convert_to_concat_str_and_bytes(
            data=(
                f"{su_exe}\n" if su_exe else "",
                convert_to_base64_blocks(
                    data=binarydata,
                    outputpath=output_path,
                    chunksize=1024,
                    echo_or_printf=echo_or_printf,
                    split_into_chunks=True,
                ),
                b"\n",
                convert_to_base64_blocks(
                    data=scriptdata,
                    outputpath=output_path_sh,
                    chunksize=1024,
                    echo_or_printf=echo_or_printf,
                    split_into_chunks=True,
                ),
            ),
            sep=b"",
        ),
        executecommand,
    )


def convert_command_to_echo_e_n_and_dd(
    binary_data,
    inputdev,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return modulecfg.cache_complex_dd_swipes.setdefault(
        (
            binary_data,
            inputdev,
            output_path,
            su_exe,
            blocksize,
            sleepbetweencommand,
            exec_or_eval,
            "echo -e -n",
        ),
        _convert_command_to_echo_or_printf_and_dd(
            binary_data=binary_data,
            inputdev=inputdev,
            output_path=output_path,
            su_exe=su_exe,
            blocksize=blocksize,
            sleepbetweencommand=sleepbetweencommand,
            exec_or_eval=exec_or_eval,
            echo_or_printf="echo -e -n",
        ),
    )


def convert_command_to_printf_and_dd(
    binary_data,
    inputdev,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return modulecfg.cache_complex_dd_swipes.setdefault(
        (
            binary_data,
            inputdev,
            output_path,
            su_exe,
            blocksize,
            sleepbetweencommand,
            exec_or_eval,
            'printf "%b"',
        ),
        _convert_command_to_echo_or_printf_and_dd(
            binary_data=binary_data,
            inputdev=inputdev,
            output_path=output_path,
            su_exe=su_exe,
            blocksize=blocksize,
            sleepbetweencommand=sleepbetweencommand,
            exec_or_eval=exec_or_eval,
            echo_or_printf='printf "%b"',
        ),
    )


def _get_long_click_command_from_xy_coordinates_echo_or_printf(
    x,
    y,
    duration=1,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    echo_or_printf="echo -e -n",
    su_exe="su",
):
    clickcommandbinary = generate_mouse_input_data(
        x=x,
        y=y,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
    )

    finishcommand = b"".join(
        get_finish_click_command(randomize_data=randomize_data)
        for _ in range(number_of_finish_commands)
    )
    return convert_to_concat_str_and_bytes(
        data=(
            f"{su_exe}\n" if su_exe else "",
            convert_to_ascii_blocks(
                data=clickcommandbinary,
                outputpath=inputdev,
                chunksize=1024,
                echo_or_printf=echo_or_printf,
                split_into_chunks=False,
            ),
            f"\nsleep {duration}\n",
            convert_to_ascii_blocks(
                data=finishcommand,
                outputpath=inputdev,
                chunksize=1024,
                echo_or_printf=echo_or_printf,
                split_into_chunks=False,
            ),
        ),
        sep=b"",
    )


def get_long_click_command_echo_e_n(
    x,
    y,
    duration=1,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    su_exe="su",
):
    return _get_long_click_command_from_xy_coordinates_echo_or_printf(
        x=x,
        y=y,
        duration=duration,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        echo_or_printf="echo -e -n",
        su_exe=su_exe,
    )


def get_long_click_command_printf(
    x,
    y,
    duration=1,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    su_exe="su",
):
    return _get_long_click_command_from_xy_coordinates_echo_or_printf(
        x,
        y,
        duration=duration,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        echo_or_printf='printf "%b"',
        su_exe=su_exe,
    )


def _generate_dd_command(
    binary_data,
    output_path,
    inputdev="/dev/input/event4",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    su_exe="su",
):
    lendata = len(binary_data)
    numberofloops = (lendata // blocksize) + 1
    scriptdata = _write_data_using_dd(
        path_on_device=output_path,
        lendata=lendata,
        numberofloops=numberofloops,
        inputdev=inputdev,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
    )

    return (
        (scriptdata),
        (binary_data),
        f"""su -c 'sh {output_path}.sh'""",
        (output_path + ".sh"),
    )


def _write_data_using_dd(
    path_on_device,
    lendata,
    numberofloops,
    inputdev="/dev/input/event4",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="eval",
):
    if sleepbetweencommand>0:
        sleepbetweencommand = f"sleep {sleepbetweencommand}"
    else:
        sleepbetweencommand = ""
    if exec_or_eval == "eval":
        quotes = '"'
        commandline = f"eval {quotes}dd status=none conv=sync count=1 skip=$skiphowmany bs=$blocksize if=$inputfile of=$outdevice{quotes}"
    else:
        commandline = 'dd status=none conv=sync count=1 skip="$skiphowmany" bs="$blocksize" if="$inputfile" of="$outdevice"'
    return rf"""#!/bin/sh
# su -c 'sh {path_on_device}.sh'
inputfile={path_on_device}
outdevice={inputdev}
totalchars={lendata}
blocksize={blocksize}
howmanyloops={numberofloops}
skiphowmany=0
for line in $(seq 1 $howmanyloops); do
        skiphowmany=$((line-1))
        {commandline}
        {sleepbetweencommand}
        skiphowmany=$((skiphowmany+1))
done
        """


def _get_simple_click_command_echo_or_printf(
    x,
    y,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    echo_or_printf="echo -e -n",
    su_exe="su",
):
    binaryclickcmd = get_raw_click_command_from_xy_coordinates(
        x=x,
        y=y,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
    )
    if echo_or_printf == "echo -e -n":
        command = convert_command_to_echo_e_n(binaryclickcmd, inputdev, su_exe=su_exe)
    else:
        command = convert_command_to_printf(binaryclickcmd, inputdev, su_exe=su_exe)
    return command


def get_simple_click_command_echo_e_n(
    x,
    y,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    su_exe="su",
):
    return _get_simple_click_command_echo_or_printf(
        x,
        y,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        echo_or_printf="echo -e -n",
        su_exe=su_exe,
    )


def get_simple_click_command_printf(
    x,
    y,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    su_exe="su",
):
    return _get_simple_click_command_echo_or_printf(
        x,
        y,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        echo_or_printf='printf "%b"',
        su_exe=su_exe,
    )


def _get_swipe_command_from_many_points(
    x_y_coordinates,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    echo_or_printf="echo -e -n",
):
    binary_data_swipe = get_raw_swipe_command_from_list_of_coordinates(
        x_y_coordinates=x_y_coordinates
        if isinstance(x_y_coordinates, tuple)
        else tuple(x_y_coordinates),
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
    )
    return _convert_command_to_echo_or_printf_and_dd(
        binary_data=binary_data_swipe,
        inputdev=inputdev,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf=echo_or_printf,
    )


def get_swipe_command_from_many_points_echo_e_n(
    x_y_coordinates,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _get_swipe_command_from_many_points(
        x_y_coordinates=x_y_coordinates,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf="echo -e -n",
    )


def get_swipe_command_from_many_points_printf(
    x_y_coordinates,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _get_swipe_command_from_many_points(
        x_y_coordinates=x_y_coordinates,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf='printf "%b"',
    )


def _create_swipe_path_from_list_of_coordinates(
    x_y_coordinates,
    xtolerance=-2,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    echo_or_printf="echo -e -n",
):
    binary_data_swipe = get_raw_swipe_command_through_a_couple_of_coordinates(
        x_y_coordinates=x_y_coordinates,
        xtolerance=xtolerance,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
    )
    return _convert_command_to_echo_or_printf_and_dd(
        binary_data=binary_data_swipe,
        inputdev=inputdev,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf=echo_or_printf,
    )


def get_swipe_command_from_a_couple_of_coordinates_printf(
    x_y_coordinates,
    xtolerance=-2,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _create_swipe_path_from_list_of_coordinates(
        x_y_coordinates=x_y_coordinates,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf='printf "%b"',
    )


def get_swipe_command_from_a_couple_of_coordinates_echo_e_n(
    x_y_coordinates,
    xtolerance=-2,
    device_serial=None,
    inputdev="/dev/input/event4",
    adb_path=None,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    number_of_finish_commands=2,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    echo_or_printf='echo -e -n "%b"',
):
    return _create_swipe_path_from_list_of_coordinates(
        x_y_coordinates=x_y_coordinates,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf='printf "%b"',
    )


def _get_drag_and_drop_command(
    x0,
    y0,
    x1,
    y1,
    sleep_before_drag_move=2,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    number_of_finish_commands=2,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72,
    sleepbetweencommand=0,
    exec_or_eval="exec",
    echo_or_printf="echo -e -n",
):
    clickcommandbinary = generate_mouse_input_data(
        x=x0,
        y=y0,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
    )

    (
        executable_swipe_command_get_swipe_command_from_2_coordinates_echo_e_n,
        get_swipe_command_from_2_coordinates_echo_e_n_after_copy,
    ) = _get_raw_swipe_command_from_2_coordinates(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        number_of_finish_commands=number_of_finish_commands,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf=echo_or_printf,
    )
    clickcommandbinaryfinal = b"".join(
        get_finish_click_command(randomize_data=randomize_data)
        for _ in range(number_of_finish_commands)
    )

    asciiclick = convert_to_ascii_blocks(
        data=clickcommandbinary,
        outputpath=inputdev,
        chunksize=1024,
        echo_or_printf=echo_or_printf,
        split_into_chunks=False,
    )

    asciiclickfinal = convert_to_ascii_blocks(
        data=clickcommandbinaryfinal,
        outputpath=inputdev,
        chunksize=1024,
        echo_or_printf=echo_or_printf,
        split_into_chunks=False,
    )

    commandaftercopy = convert_to_concat_str_and_bytes(
        data=(
            su_exe,
            asciiclick,
            b"sleep " + str(sleep_before_drag_move).encode("utf-8"),
            get_swipe_command_from_2_coordinates_echo_e_n_after_copy,
            asciiclickfinal,
        ),
        sep=b"\n",
    )
    return (
        executable_swipe_command_get_swipe_command_from_2_coordinates_echo_e_n,
        commandaftercopy,
    )


def get_drag_and_drop_command_echo_e_n(
    x0,
    y0,
    x1,
    y1,
    sleep_before_drag_move=2,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    number_of_finish_commands=2,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72 * 4,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _get_drag_and_drop_command(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        sleep_before_drag_move=sleep_before_drag_move,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        number_of_finish_commands=number_of_finish_commands,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf="echo -e -n",
    )


def get_drag_and_drop_command_printf(
    x0,
    y0,
    x1,
    y1,
    sleep_before_drag_move=2,
    device_serial=None,
    inputdev=None,
    adb_path=None,
    number_of_finish_commands=2,
    x_max=None,
    y_max=None,
    screen_width=None,
    screen_height=None,
    randomize_data=False,
    output_path="/sdcard/echoen_dd.bin",
    su_exe="su",
    blocksize=72 * 4,
    sleepbetweencommand=0,
    exec_or_eval="exec",
):
    return _get_drag_and_drop_command(
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        sleep_before_drag_move=sleep_before_drag_move,
        device_serial=device_serial,
        inputdev=inputdev,
        adb_path=adb_path,
        number_of_finish_commands=number_of_finish_commands,
        x_max=x_max,
        y_max=y_max,
        screen_width=screen_width,
        screen_height=screen_height,
        randomize_data=randomize_data,
        output_path=output_path,
        su_exe=su_exe,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
        echo_or_printf='printf "%b"',
    )

