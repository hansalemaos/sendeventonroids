from .commandos import (
    modulecfg,
    get_simple_click_command_echo_e_n,
    UniversalADBExecutor,
    get_simple_click_command_printf,
    get_long_click_command_echo_e_n,
    get_long_click_command_printf,
    get_swipe_command_from_many_points_printf,
    get_swipe_command_from_many_points_echo_e_n,
    get_n_coordinates_from_circle,
    get_n_coordinates_from_rectangle,
    get_n_coordinates_from_ellipse,
    get_n_coordinates_from_polygon,
    get_n_coordinates_from_circle,
    get_swipe_command_from_2_coordinates_echo_e_n,
    get_swipe_command_from_2_coordinates_printf,
    get_swipe_command_from_a_couple_of_coordinates_printf,
    get_swipe_command_from_a_couple_of_coordinates_echo_e_n,
    get_drag_and_drop_command_printf,
    get_drag_and_drop_command_echo_e_n,
)
from typing import Literal


class CodeExec:
    def __init__(
        self,
        executer,
        init_cmd,
        main_cmd,
    ) -> None:
        self.init_cmd = init_cmd
        self.main_cmd = main_cmd
        self.init_cmd_str = (
            init_cmd.decode("utf-8", "backslashreplace")
            if init_cmd and isinstance(init_cmd, bytes)
            else init_cmd
            if isinstance(init_cmd, str)
            else "intital command not needed"
        )[:300] + "..."
        self.main_cmd_str = (
            main_cmd.decode("utf-8", "backslashreplace")
            if main_cmd and isinstance(main_cmd, bytes)
            else main_cmd
            if isinstance(main_cmd, str)
            else "intital command not needed"
        )[:300]
        self.executer = executer
        if not init_cmd:
            self.inital_command_success = True
        else:
            self.inital_command_success = False

    def __repr__(self) -> str:
        return f"INITAL COMMAND:\n{self.init_cmd_str}\n\n\nMAIN COMMAND:\n{self.main_cmd_str}"

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self, **kwargs):
        if not self.inital_command_success:
            self.run_init_command()
        self.run_main_command()
        return self

    def run_init_command(self, **kwargs):
        self.executer.shell_without_capturing_stdout_and_stderr(self.init_cmd, **kwargs)
        self.inital_command_success = True
        return self

    def run_main_command(self, **kwargs):
        self.executer.shell_without_capturing_stdout_and_stderr(self.main_cmd, **kwargs)
        return self


class SendEventOnRoids:
    r"""
    This module provides tools for handling advanced commands for simulating user inputs on Android devices.
    It includes two main classes:

    1. CodeExec: Executes shell commands on the Android device via adb.
    2. SendEventOnRoids: Handles advanced gestures and command sequences such as taps, swipes, and drags using adb commands.

    Classes:
        CodeExec: Manages and executes a single adb command.
        SendEventOnRoids: Facilitates the creation of complex adb command sequences.


    """

    def __init__(
        self,
        adb_path=None,
        device_serial=None,
        input_device="/dev/input/event4",
        x_max=None,
        y_max=None,
        screen_width=None,
        screen_height=None,
        number_of_finish_commands=2,
        su_exe="su",
        blocksize=72,
        prefered_execution: Literal["exec", "eval"] = "exec",
        chunk_size=1024,
    ) -> None:
        r"""
        Initializes an instance of SendEventOnRoids, setting up the Android Debug Bridge (ADB) environment
        for executing touch and swipe commands on a connected Android device.

        Args:
            adb_path (str, optional): The full path to the adb executable. If None, it will assume adb is in the system path.
            device_serial (str, optional): The serial number of the target Android device. If None, ADB commands will target the only connected device.
            input_device (str, optional): The device file for the input device in the Android filesystem. Defaults to '/dev/input/event4', commonly used for touchscreen inputs.
            x_max (int, optional): The maximum x-coordinate for the device's touchscreen. Needed for coordinate scaling.
            y_max (int, optional): The maximum y-coordinate for the device's touchscreen. Needed for coordinate scaling.
            screen_width (int, optional): The actual screen width in pixels of the Android device.
            screen_height (int, optional): The actual screen height in pixels of the Android device.
            number_of_finish_commands (int, optional): The number of 'finish' commands (zero bytes) to send after executing touch or swipe actions. This helps ensure that all actions are registered correctly on the device.
            su_exe (str, optional): The command to execute 'superuser' actions, always needed. Defaults to 'su'.
            blocksize (int, optional): The size of each block of data sent in a command, this controls the speed of the command, ajust it in steps of 72.
            prefered_execution (str, optional): Preferred method of executing the ADB commands, can be 'exec' (default) or 'eval' (slower) for evaluating expressions.
            chunk_size (int, optional): The size of data chunks processed at one time during execution, relevant when handling large sets of commands or data (swipes).

        Example:
            start_on_device = False
            if start_on_device:  # you can do that if you installed python as root on your device -> https://github.com/hansalemaos/termuxfree
                device_serial = None
                input_device = "/dev/input/event4"
                adb_path = None
                android_automation = SendEventOnRoids(
                    adb_path=adb_path,
                    device_serial=device_serial,
                    input_device=input_device,
                    x_max=32767,
                    y_max=32767,
                    screen_width=900,
                    screen_height=1600,
                    number_of_finish_commands=2,
                    su_exe="/system/xbin/su",
                    blocksize=72,
                    prefered_execution="exec",
                    chunk_size=1024,
                )

            else:  # via adb
                adb_path = shutil.which("adb")
                device_serial = "127.0.0.1:5645"
                input_device = "/dev/input/event4"
                android_automation = SendEventOnRoids(
                    adb_path=adb_path,
                    device_serial=device_serial,
                    input_device=input_device,
                    x_max=None,
                    y_max=None,
                    screen_width=None,
                    screen_height=None,
                    number_of_finish_commands=2,
                    su_exe="/system/xbin/su",
                    blocksize=72,
                    prefered_execution="exec",
                    chunk_size=1024,
                )
        """
        self.adb_path = adb_path
        self.device_serial = device_serial
        self.input_device = input_device
        self.x_max = x_max
        self.y_max = y_max
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.randomize_data = False
        self.number_of_finish_commands = number_of_finish_commands
        self.su_exe = su_exe
        self.blocksize = blocksize
        self.prefered_execution = prefered_execution
        self.chunk_size = chunk_size
        if all(
            [device_serial, input_device, x_max, y_max, screen_width, screen_height]
        ):
            modulecfg.cache_screen_size_dict[(device_serial, input_device)] = {
                "x_max": x_max,
                "y_max": y_max,
                "screen_width": screen_width,
                "screen_height": screen_height,
            }
        self.adb_shell = UniversalADBExecutor(self.adb_path, self.device_serial)

    def echo_input_tap(self, x, y, input_device=None, number_of_finish_commands=2):
        r"""
        Simulates a tap on the Android device at a specified (x, y) coordinate using echo commands

        Args:
            x (int): X-coordinate where the tap will occur.
            y (int): Y-coordinate where the tap will occur.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): How many times the command should finalize (sending zero bytes). Defaults to 2.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            input_tap_echo = self.echo_input_tap(
                x=300,
                y=400,
                input_device=None,
                number_of_finish_commands=2,
            )
            input_tap_echo()
        """
        clickcmd = get_simple_click_command_echo_e_n(
            x=int(x),
            y=int(y),
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            su_exe=self.su_exe,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=b"",
            main_cmd=clickcmd,
        )

    def printf_input_tap(self, x, y, input_device=None, number_of_finish_commands=2):
        r"""
        Simulates a tap on the Android device at a specified (x, y) coordinate using printf commands.

        Args:
            x (int): X-coordinate where the tap will occur.
            y (int): Y-coordinate where the tap will occur.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): How many times the command should finalize (sending zero bytes). Defaults to 2.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            input_tap_printf = self.printf_input_tap(
                x=600,
                y=200,
                input_device=None,
                number_of_finish_commands=2,
            )
            input_tap_printf()
        """
        clickcmd = get_simple_click_command_printf(
            x=int(x),
            y=int(y),
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            su_exe=self.su_exe,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=b"",
            main_cmd=clickcmd,
        )

    def echo_long_input_tap(
        self,
        x,
        y,
        duration=2,
        input_device=None,
        number_of_finish_commands=2,
    ):
        r"""
        Simulates a long tap on the Android device at a specified (x, y) coordinate using echo commands

        Args:
            x (int): X-coordinate where the long tap will occur.
            y (int): Y-coordinate where the long tap will occur.
            duration (int): Duration of the long tap in seconds. Defaults to 2 seconds.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): How many times the command should finalize (sending zero bytes). Defaults to 2.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            long_input_tap_echo = self.echo_long_input_tap(
                x=100,
                y=400,
                duration=2,
                input_device=None,
                number_of_finish_commands=2,
            )
            long_input_tap_echo()
        """
        clickcmd = get_long_click_command_echo_e_n(
            x=int(x),
            y=int(y),
            duration=duration,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            su_exe=self.su_exe,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=b"",
            main_cmd=clickcmd,
        )

    def printf_long_input_tap(
        self,
        x,
        y,
        duration=2,
        input_device=None,
        number_of_finish_commands=2,
    ):
        r"""
        Simulates a long tap on the Android device at a specified (x, y) coordinate using printf commands via adb.

        Args:
            x (int): X-coordinate where the long tap will occur.
            y (int): Y-coordinate where the long tap will occur.
            duration (int): Duration of the long tap in seconds. Defaults to 2 seconds.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): How many times the command should finalize (sending zero bytes). Defaults to 2.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            long_input_tap_printf = self.printf_long_input_tap(
                x=600,
                y=600,
                duration=2,
                input_device=None,
                number_of_finish_commands=2,
            )
            long_input_tap_printf()
        """
        clickcmd = get_long_click_command_printf(
            x=int(x),
            y=int(y),
            duration=duration,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            su_exe=self.su_exe,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=b"",
            main_cmd=clickcmd,
        )

    def printf_swipe_through_continuous_coordinates(
        self,
        coordinates,
        output_path="/sdcard/printf_swipe_through_continuous_coordinates.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Executes a swipe through a sequence of continuous coordinates using printf commands.

        Args:
            coordinates (list of tuple): List of (x, y) coordinates to swipe through.
            output_path (str): Path on the device to store the swipe command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each swipe. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            printf_swipe_through_continuous_coordinates = (
                self.printf_swipe_through_continuous_coordinates(
                    coordinates=circle_coords,
                    output_path="/sdcard/printf_swipe_through_continuous_coordinates.bin",
                    input_device=None,
                    number_of_finish_commands=2,
                    blocksize=72 * 10,
                    exec_or_eval=None,
                    sleep_between_each_pixel=0,
                )
            )
            printf_swipe_through_continuous_coordinates()
        """
        (
            executable_swipe_command_with_printf,
            executable_swipe_command_with_printf_after_copy,
        ) = get_swipe_command_from_many_points_printf(
            x_y_coordinates=coordinates,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_with_printf,
            main_cmd=executable_swipe_command_with_printf_after_copy,
        )

    def echo_swipe_through_continuous_coordinates(
        self,
        coordinates,
        output_path="/sdcard/echo_swipe_through_continuous_coordinates.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Executes a swipe through a sequence of continuous coordinates using echo commands.

        Args:
            coordinates (list of tuple): List of (x, y) coordinates to swipe through.
            output_path (str): Path on the device to store the swipe command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each swipe. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            echo_swipe_through_continuous_coordinates = (
                self.echo_swipe_through_continuous_coordinates(
                    coordinates=circle_coords,
                    output_path="/sdcard/echo_swipe_through_continuous_coordinates.bin",
                    input_device=None,
                    number_of_finish_commands=2,
                    blocksize=72 * 10,
                    exec_or_eval=None,
                    sleep_between_each_pixel=0,
                )
            )
            echo_swipe_through_continuous_coordinates()
        """
        (
            executable_swipe_command_with_echo,
            executable_swipe_command_with_echo_after_copy,
        ) = get_swipe_command_from_many_points_echo_e_n(
            x_y_coordinates=coordinates,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_with_echo,
            main_cmd=executable_swipe_command_with_echo_after_copy,
        )

    def echo_brute_force_swipe_rectangle_area(
        self,
        x,
        y,
        width,
        height,
        numer_of_coordinates=100,
        output_path="/sdcard/echo_brute_force_swipe_rectangle_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe across a rectangular area, generating numerous coordinates within the rectangle and executing echo commands for each.

        Args:
            x, y (int): Top-left corner of the rectangle.
            width, height (int): Dimensions of the rectangle.
            numer_of_coordinates (int): Number of coordinates to generate within the rectangle for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.echo_brute_force_swipe_rectangle_area(
                x=20,
                y=20,
                width=100,
                height=300,
                numer_of_coordinates=30,
                output_path="/sdcard/echo_brute_force_swipe_rectangle_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_rectangle(
            x=int(x),
            y=int(y),
            width=int(width),
            height=int(height),
            numer_of_coordinates=int(numer_of_coordinates),
        )

        return self.echo_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def printf_brute_force_swipe_rectangle_area(
        self,
        x,
        y,
        width,
        height,
        numer_of_coordinates=100,
        output_path="/sdcard/printf_brute_force_swipe_rectangle_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe across a rectangular area, generating numerous coordinates within the rectangle and executing printf commands for each.

        Args:
            x, y (int): Top-left corner of the rectangle.
            width, height (int): Dimensions of the rectangle.
            numer_of_coordinates (int): Number of coordinates to generate within the rectangle for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.printf_brute_force_swipe_rectangle_area(
                x=20,
                y=20,
                width=100,
                height=300,
                numer_of_coordinates=30,
                output_path="/sdcard/printf_brute_force_swipe_rectangle_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_rectangle(
            x=int(x),
            y=int(y),
            width=int(width),
            height=int(height),
            numer_of_coordinates=int(numer_of_coordinates),
        )
        return self.printf_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def echo_brute_force_swipe_ellipse_area(
        self,
        x_center,
        y_center,
        rx,
        ry,
        numer_of_coordinates=100,
        output_path="/sdcard/echo_brute_force_swipe_ellipse_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe across an elliptical area by generating numerous coordinates within the ellipse and executing echo commands for each.

        Args:
            x_center, y_center (int): Center coordinates of the ellipse.
            rx, ry (int): Radii of the ellipse along the x and y axes.
            numer_of_coordinates (int): Number of coordinates to generate within the ellipse for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.echo_brute_force_swipe_ellipse_area(
                x_center=200,
                y_center=400,
                rx=100,
                ry=50,
                numer_of_coordinates=30,
                output_path="/sdcard/echo_brute_force_swipe_ellipse_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_ellipse(
            x_center=int(x_center),
            y_center=int(y_center),
            rx=int(rx),
            ry=int(ry),
            numer_of_coordinates=int(numer_of_coordinates),
        )

        return self.echo_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def printf_brute_force_swipe_ellipse_area(
        self,
        x_center,
        y_center,
        rx,
        ry,
        numer_of_coordinates=100,
        output_path="/sdcard/printf_brute_force_swipe_ellipse_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe across an elliptical area by generating numerous coordinates within the ellipse and executing printf commands for each.

        Args:
            x_center, y_center (int): Center coordinates of the ellipse.
            rx, ry (int): Radii of the ellipse along the x and y axes.
            numer_of_coordinates (int): Number of coordinates to generate within the ellipse for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.printf_brute_force_swipe_ellipse_area(
                x_center=200,
                y_center=400,
                rx=100,
                ry=50,
                numer_of_coordinates=30,
                output_path="/sdcard/printf_brute_force_swipe_ellipse_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_ellipse(
            x_center=int(x_center),
            y_center=int(y_center),
            rx=int(rx),
            ry=int(ry),
            numer_of_coordinates=int(numer_of_coordinates),
        )
        return self.printf_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def echo_brute_force_swipe_polygon_area(
        self,
        vertices,
        numer_of_coordinates=100,
        output_path="/sdcard/echo_brute_force_swipe_polygon_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe over a polygonal area by generating multiple coordinates along the edges defined by the given vertices using echo commands.

        Args:
            vertices (list of tuple): List of (x, y) tuples defining the vertices of the polygon.
            numer_of_coordinates (int): Number of coordinates to generate along the polygon for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.echo_brute_force_swipe_polygon_area(
                vertices=[
                    (350, 100),
                    (450, 450),
                    (150, 400),
                    (100, 200),
                    (350, 100),
                    (200, 300),
                    (350, 350),
                    (300, 200),
                    (200, 300),
                ],
                numer_of_coordinates=30,
                output_path="/sdcard/echo_brute_force_swipe_polygon_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_polygon(
            vertices=vertices,
            numer_of_coordinates=numer_of_coordinates,
        )

        return self.echo_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def printf_brute_force_swipe_polygon_area(
        self,
        vertices,
        numer_of_coordinates=100,
        output_path="/sdcard/printf_brute_force_swipe_polygon_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe over a polygonal area by generating multiple coordinates along the edges defined by the given vertices using printf commands.

        Args:
            vertices (list of tuple): List of (x, y) tuples defining the vertices of the polygon.
            numer_of_coordinates (int): Number of coordinates to generate along the polygon for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.printf_brute_force_swipe_polygon_area(
                vertices=[
                    (350, 100),
                    (450, 450),
                    (150, 400),
                    (100, 200),
                    (350, 100),
                    (200, 300),
                    (350, 350),
                    (300, 200),
                    (200, 300),
                ],
                numer_of_coordinates=30,
                output_path="/sdcard/printf_brute_force_swipe_polygon_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_polygon(
            vertices=vertices,
            numer_of_coordinates=int(numer_of_coordinates),
        )
        return self.printf_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def echo_brute_force_swipe_circle_area(
        self,
        x,
        y,
        radius,
        numer_of_coordinates=100,
        output_path="/sdcard/echo_brute_force_swipe_circle_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe over a circular area by generating multiple coordinates along the circumference of the circle using echo commands.

        Args:
            x, y (int): Center coordinates of the circle.
            radius (int): Radius of the circle.
            numer_of_coordinates (int): Number of coordinates to generate along the circle for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.echo_brute_force_swipe_circle_area(
                x=500,
                y=500,
                radius=150,
                numer_of_coordinates=30,
                output_path="/sdcard/echo_brute_force_swipe_circle_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_circle(
            x=int(x),
            y=int(y),
            radius=int(radius),
            numer_of_coordinates=numer_of_coordinates,
        )

        return self.echo_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def printf_brute_force_swipe_circle_area(
        self,
        x,
        y,
        radius,
        numer_of_coordinates=100,
        output_path="/sdcard/printf_brute_force_swipe_circle_area.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a swipe over a circular area by generating multiple coordinates along the circumference of the circle using printf commands.

        Args:
            x, y (int): Center coordinates of the circle.
            radius (int): Radius of the circle.
            numer_of_coordinates (int): Number of coordinates to generate along the circle for swiping.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            exampledata = self.printf_brute_force_swipe_circle_area(
                x=500,
                y=500,
                radius=150,
                numer_of_coordinates=30,
                output_path="/sdcard/printf_brute_force_swipe_circle_area.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=72 * 8,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            exampledata()
        """
        line_coords = get_n_coordinates_from_circle(
            x=int(x),
            y=int(y),
            radius=int(radius),
            numer_of_coordinates=numer_of_coordinates,
        )
        return self.printf_swipe_through_continuous_coordinates(
            coordinates=line_coords,
            output_path=output_path,
            input_device=input_device,
            number_of_finish_commands=number_of_finish_commands,
            blocksize=blocksize,
            exec_or_eval=exec_or_eval,
            sleep_between_each_pixel=sleep_between_each_pixel,
        )

    def echo_swipe_from_one_coordinate_to_another(
        self,
        x0,
        y0,
        x1,
        y1,
        output_path="/sdcard/echo_swipe_from_one_coordinate_to_another.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Executes a swipe action from one coordinate (x0, y0) to another (x1, y1) using echo commands.

        Args:
            x0, y0 (int): Starting coordinates of the swipe.
            x1, y1 (int): Ending coordinates of the swipe.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            swipecmd = self.echo_swipe_from_one_coordinate_to_another(
                x0=10,
                y0=50,
                x1=200,
                y1=300,
                output_path="/sdcard/echo_swipe_from_one_coordinate_to_another.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=None,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            swipecmd()

        """
        (
            executable_swipe_command_get_swipe_command_from_2_coordinates_echo_e_n,
            get_swipe_command_from_2_coordinates_echo_e_n_after_copy,
        ) = get_swipe_command_from_2_coordinates_echo_e_n(
            x0=int(x0),
            y0=int(y0),
            x1=int(x1),
            y1=int(y1),
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_get_swipe_command_from_2_coordinates_echo_e_n,
            main_cmd=get_swipe_command_from_2_coordinates_echo_e_n_after_copy,
        )

    def echo_swipe_from_one_coordinate_to_another(
        self,
        x0,
        y0,
        x1,
        y1,
        output_path="/sdcard/echo_swipe_from_one_coordinate_to_another.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        (
            executable_swipe_command_get_swipe_command_from_2_coordinates_echo_e_n,
            get_swipe_command_from_2_coordinates_echo_e_n_after_copy,
        ) = get_swipe_command_from_2_coordinates_echo_e_n(
            x0=int(x0),
            y0=int(y0),
            x1=int(x1),
            y1=int(y1),
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_get_swipe_command_from_2_coordinates_echo_e_n,
            main_cmd=get_swipe_command_from_2_coordinates_echo_e_n_after_copy,
        )

    def printf_swipe_from_one_coordinate_to_another(
        self,
        x0,
        y0,
        x1,
        y1,
        output_path="/sdcard/printf_swipe_from_one_coordinate_to_another.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Executes a swipe action from one coordinate (x0, y0) to another (x1, y1) using printf commands.

        Args:
            x0, y0 (int): Starting coordinates of the swipe.
            x1, y1 (int): Ending coordinates of the swipe.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            swipecmd = self.printf_swipe_from_one_coordinate_to_another(
                x0=100,
                y0=500,
                x1=200,
                y1=700,
                output_path="/sdcard/printf_swipe_from_one_coordinate_to_another.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=None,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            swipecmd()
        """
        (
            executable_swipe_command_get_swipe_command_from_2_coordinates_printf,
            executable_swipe_command_get_swipe_command_from_2_coordinates_printf_after_copy,
        ) = get_swipe_command_from_2_coordinates_printf(
            x0=int(x0),
            y0=int(y0),
            x1=int(x1),
            y1=int(y1),
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_get_swipe_command_from_2_coordinates_printf,
            main_cmd=executable_swipe_command_get_swipe_command_from_2_coordinates_printf_after_copy,
        )

    def printf_swipe_through_a_couple_of_coordinates(
        self,
        coordinates,
        output_path="/sdcard/printf_swipe_through_a_couple_of_coordinates.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Executes a swipe through a set of specified coordinates using printf commands, allowing for precise control over swipe paths on the device screen.

        Args:
            coordinates (list of tuple): List of (x, y) coordinates to swipe through.
            output_path (str): Path on the device to store the swipe command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each swipe. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            printf_swipe_through_a_couple_of_coordinates = (
                self.printf_swipe_through_a_couple_of_coordinates(
                    coordinates=[
                        (150, 150),
                        (550, 450),
                        (650, 350),
                        (750, 1200),
                        (250, 200),
                    ],
                    output_path="/sdcard/printf_swipe_through_a_couple_of_coordinates.bin",
                    input_device=None,
                    number_of_finish_commands=2,
                    blocksize=10 * 72,
                    exec_or_eval=None,
                    sleep_between_each_pixel=0,
                )
            )
            printf_swipe_through_a_couple_of_coordinates()
        """
        (
            executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_printf,
            executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_printf_after_copy,
        ) = get_swipe_command_from_a_couple_of_coordinates_printf(
            x_y_coordinates=coordinates,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_printf,
            main_cmd=executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_printf_after_copy,
        )

    def echo_swipe_through_a_couple_of_coordinates(
        self,
        coordinates,
        output_path="/sdcard/echo_swipe_through_a_couple_of_coordinates.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Executes a swipe through a set of specified coordinates using echo commands, suitable for drawing arbitrary paths on the device screen.

        Args:
            coordinates (list of tuple): List of (x, y) coordinates to swipe through.
            output_path (str): Path on the device to store the swipe command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each swipe. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between swipe actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            echo_swipe_through_a_couple_of_coordinates = (
                self.echo_swipe_through_a_couple_of_coordinates(
                    coordinates=[
                        (10, 11),
                        (100, 100),
                        (500, 300),
                        (600, 200),
                        (700, 1100),
                        (200, 100),
                    ],
                    output_path="/sdcard/echo_swipe_through_a_couple_of_coordinates.bin",
                    input_device=None,
                    number_of_finish_commands=2,
                    blocksize=10 * 72,
                    exec_or_eval=None,
                    sleep_between_each_pixel=0,
                )
            )
            echo_swipe_through_a_couple_of_coordinates()
        """
        (
            executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_echo_e_n,
            executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_echo_e_n_after_copy,
        ) = get_swipe_command_from_a_couple_of_coordinates_echo_e_n(
            x_y_coordinates=coordinates,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )
        return CodeExec(
            executer=self.adb_shell,
            init_cmd=executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_echo_e_n,
            main_cmd=executable_swipe_command_get_swipe_command_from_a_couple_of_coordinates_echo_e_n_after_copy,
        )

    def echo_drag_and_drop(
        self,
        x0,
        y0,
        x1,
        y1,
        sleep_before_drag_move=2,
        output_path="/sdcard/echo_drag_and_drop.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a drag-and-drop action from one coordinate to another using echo commands.

        Args:
            x0, y0 (int): Starting coordinates of the drag.
            x1, y1 (int): Ending coordinates of the drag.
            sleep_before_drag_move (int): Sleep duration in seconds before starting the drag move.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between drag actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            echo_drag_and_drop = self.echo_drag_and_drop(
                x0=100,
                y0=500,
                x1=800,
                y1=700,
                sleep_before_drag_move=2,
                output_path="/sdcard/echo_drag_and_drop.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=4 * 72,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            echo_drag_and_drop()
        """
        dragcopycmd1, commandaftercopy1 = get_drag_and_drop_command_echo_e_n(
            x0=int(x0),
            y0=int(y0),
            x1=int(x1),
            y1=int(y1),
            sleep_before_drag_move=sleep_before_drag_move,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )

        return CodeExec(
            executer=self.adb_shell,
            init_cmd=dragcopycmd1,
            main_cmd=commandaftercopy1,
        )

    def printf_drag_and_drop(
        self,
        x0,
        y0,
        x1,
        y1,
        sleep_before_drag_move=2,
        output_path="/sdcard/printf_drag_and_drop.bin",
        input_device=None,
        number_of_finish_commands=2,
        blocksize=None,
        exec_or_eval=None,
        sleep_between_each_pixel=0,
    ):
        r"""
        Simulates a drag-and-drop action from one coordinate to another using printf commands.

        Args:
            x0, y0 (int): Starting coordinates of the drag.
            x1, y1 (int): Ending coordinates of the drag.
            sleep_before_drag_move (int): Sleep duration in seconds before starting the drag move.
            output_path (str): Path on the device to store the command data.
            input_device (str, optional): The input device path in the Android system. Defaults to class attribute.
            number_of_finish_commands (int): Number of times to finalize the command.
            blocksize (int, optional): Size of data blocks to write in each action. Defaults to class attribute.
            exec_or_eval (str, optional): Execution method, can be 'exec' or 'eval'. Defaults to class attribute.
            sleep_between_each_pixel (int, optional): Sleep duration in seconds between drag actions.

        Returns:
            CodeExec: An executable command object ready to be executed.

        Example:
            printf_drag_and_drop = self.printf_drag_and_drop(
                x0=100,
                y0=500,
                x1=800,
                y1=700,
                sleep_before_drag_move=2,
                output_path="/sdcard/printf_drag_and_drop.bin",
                input_device=None,
                number_of_finish_commands=2,
                blocksize=4 * 72,
                exec_or_eval=None,
                sleep_between_each_pixel=0,
            )
            printf_drag_and_drop()
        """
        dragcopycmd1, commandaftercopy1 = get_drag_and_drop_command_printf(
            x0=int(x0),
            y0=int(y0),
            x1=int(x1),
            y1=int(y1),
            sleep_before_drag_move=sleep_before_drag_move,
            device_serial=self.device_serial,
            inputdev=input_device or self.input_device,
            adb_path=self.adb_path,
            x_max=self.x_max,
            y_max=self.y_max,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            randomize_data=False,
            number_of_finish_commands=number_of_finish_commands,
            output_path=output_path,
            su_exe=self.su_exe,
            blocksize=blocksize or self.blocksize,
            sleepbetweencommand=sleep_between_each_pixel,
            exec_or_eval=exec_or_eval or self.prefered_execution,
        )

        return CodeExec(
            executer=self.adb_shell,
            init_cmd=dragcopycmd1,
            main_cmd=commandaftercopy1,
        )
