import time
from pathlib import Path, PureWindowsPath
from random import randint, random, sample

import numpy as np
from omegaconf import DictConfig, OmegaConf
from pywinauto import keyboard, mouse
from pywinauto.application import Application


class LuminaireManager:
    def __init__(self, config):
        self.config = config
        self.luminaire_channels = [
            "violet",
            "royal_blue",
            "blue",
            "cyan",
            "lime",
            "amber",
            "deep_red",
        ]

    def init(self):
        self.luminaire_app = Application().connect(title_re=".*Luminaire Manager.*", found_index=0)
        self.luminaire_dlg = self.luminaire_app.LuminaireManager
        self.luminaire_dlg.set_focus()

    def create_lumenscript_using_thermal_target_CT(self):

        start_temperature = self.config.start_temperature
        thermal_sweep_value = self.config.thermal_sweep_value
        screenshot_dir = PureWindowsPath(self.config.screenshot_dir)

        self.luminaire_dlg.set_focus()
        self.reset_Luminaire()

        if self.luminaire_dlg["single frameCheckBox"].is_checked():
            self.luminaire_dlg["single frameCheckBox"].uncheck_by_click()
        self.luminaire_dlg["Match modeComboBox"].select("spectrum")
        self.luminaire_dlg["Frame sourceComboBox"].select("target")
        self.luminaire_dlg["Spectrum formatComboBox"].select("tab-delimited")
        self.luminaire_dlg.Button19.click_input()  # Click create lumenscript button
        self.luminaire_dlg.Button16.click_input()  # Click increase frame index button
        self.disable_UV()
        self._set_duration()
        self.luminaire_dlg.capture_as_image().save(
            str(screenshot_dir / "luminaire_app_screenshot_INITIAL_CONFIGURATION.png")
        )

        for i in range(self.config.n_lights):
            self.luminaire_dlg.Edit2.set_edit_text(self.config.frame_duration)  # Set Duration
            thermal_target = start_temperature + i * thermal_sweep_value

            # self.luminaire_dlg.Edit3.set_edit_text(thermal_target)  # Set thermal target CT
            # self.luminaire_dlg.Edit3.type_keys("{ENTER}")
            self._create_thermal_target(color_temp=thermal_target)
            time.sleep(2)
            self.luminaire_dlg.Button22.click_input()  # Click insert frame button
            self.luminaire_dlg.Button16.click_input()  # Click increase frame index button
            # Luminaire matched --> save screenshot
            self.luminaire_dlg.set_focus()
            screenshot_filename = str(screenshot_dir / f"luminaire_app_CT_{thermal_target}.png")
            self.luminaire_dlg.capture_as_image().save(screenshot_filename)

        lumenscript_filename = f"{self.config.method_create_lumenscript}_n_lights_{self.config.n_lights}_CTsweep_{self.config.thermal_sweep_value}_lumen_20220818"
        if self.config.save_lumenscript:
            self.luminaire_dlg.Button21.click_input()  # Save lumen script
            save_dialog = self.luminaire_app.window(
                title_re="Save Lumenscript", class_name="#32770"
            )
            save_dialog.Edit.set_edit_text(lumenscript_filename)
            save_dialog.Save.close_click()

    def create_lumenscript_using_channel_drive_level(self):
        screenshot_dir = PureWindowsPath(self.config.screenshot_dir)

        self.luminaire_dlg.set_focus()
        if self.luminaire_dlg["single frameCheckBox"].is_checked():
            self.luminaire_dlg["single frameCheckBox"].uncheck_by_click()

        # Reset the manager
        self.reset_Luminaire()

        self.luminaire_dlg.Button19.click_input()  # Click create lumenscript button
        self.luminaire_dlg.Button16.click_input()  # Click increase frame index button

        self.luminaire_dlg["Spectrum formatComboBox"].select("tab-delimited")

        # Create random lights
        self._reset_all_drive_level_to_0()
        self.luminaire_dlg["Frame sourceComboBox"].select("actual")
        self.luminaire_dlg["Match modeComboBox"].select("regular palette")
        for i in range(self.config.n_lights):
            self._set_duration()

            # Create light with randomly 5 to 7 channels
            self._create_a_random_SPD_using_drive_level(n_channels=randint(5, 7))

            time.sleep(1)
            self.luminaire_dlg.Button22.click_input()  # Click insert frame button
            self.luminaire_dlg.Button16.click_input()  # Click increase frame index button
            time.sleep(1)
            # Luminaire matched --> save screenshot
            self.luminaire_dlg.set_focus()
            screenshot_filename = str(screenshot_dir / f"luminaire_app_frame_{i}.png")
            self.luminaire_dlg.capture_as_image().save(screenshot_filename)

        lumenscript_filename = (
            f"{self.config.method_create_lumenscript}_n_lights_{self.config.n_lights}"
        )
        if self.config.save_lumenscript:
            self.luminaire_dlg.Button21.click_input()  # Save lumen script
            save_dialog = self.luminaire_app.window(
                title_re="Save Lumenscript", class_name="#32770"
            )
            save_dialog.Edit.set_edit_text(lumenscript_filename)
            save_dialog.Save.close_click()

    def _change_luminaire_channels_drive_level(
        self, channel_names: list = None, level: float = 0.1, time_sleep: float = 1  # Maximum 0.8
    ) -> None:
        if channel_names:
            for channel_name in channel_names:
                coords = self._get_coords_channel_drive_level(channel_name)
                mouse.move(coords=coords)
                mouse.click(button="left", coords=coords)
                keyboard.send_keys(str(level) + "{ENTER}")
                time.sleep(time_sleep)

    def _reset_all_drive_level_to_0(self):
        self._change_luminaire_channels_drive_level(
            channel_names=["UV"] + self.luminaire_channels, level=0, time_sleep=0
        )

    def _create_a_random_SPD_using_drive_level(
        self,
        n_channels: int = 6,
    ) -> None:
        # Reset all channel drive level to 0
        # self.luminaire_dlg["Edit FrameButton3"].click_input() # Should not use this button for multi frame editing
        self._reset_all_drive_level_to_0()

        for channel_name in sample(self.luminaire_channels, k=n_channels):
            level = round(random(), 6)
            self._change_luminaire_channels_drive_level([channel_name], level=level)

            status = str(self.luminaire_dlg.panel18.Static.Texts)
            if "power is too high" in status:
                # Make it smaller
                self._change_luminaire_channels_drive_level([channel_name], level=0.01)

        time.sleep(0.5)

    def _match_SPD(self):
        self.luminaire_dlg["Edit FrameButton4"].click_input()

    def reset_Luminaire(self):
        self.luminaire_dlg.set_focus()
        self.luminaire_dlg["Edit FrameButton3"].click_input()

    def disable_UV(self):
        drive_level_grid_coords = self._get_drive_level_grid_coords()
        UV_coords = (
            drive_level_grid_coords[0] - 50,
            drive_level_grid_coords[1] + 1 * round(23.75 / 2),
        )
        mouse.move(coords=UV_coords)
        mouse.click(button="left", coords=UV_coords)

    def _get_drive_level_grid_coords(self):
        control_channel_rect = self.luminaire_dlg["Control Luminaire ChannelsStatic"].rectangle()
        control_channel_coords = (control_channel_rect.left, control_channel_rect.top)
        drive_level_grid_coords = (control_channel_coords[0] + 122, control_channel_coords[1] + 99)
        return drive_level_grid_coords

    def _get_coords_channel_drive_level(
        self,
        channel_name: str,
    ):

        drive_level_grid_coords = self._get_drive_level_grid_coords()
        # Grid height is 190 with 8 channels --> 23.75 height for each
        if channel_name == "UV":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 1 * round(23.75 / 2),
            )
        elif channel_name == "violet":
            # Coords is the center of the drive level box of violet
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 3 * round(23.75 / 2),
            )
        elif channel_name == "royal_blue":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 5 * round(23.75 / 2),
            )
        elif channel_name == "blue":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 7 * round(23.75 / 2),
            )
        elif channel_name == "cyan":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 9 * round(23.75 / 2),
            )
        elif channel_name == "lime":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 11 * round(23.75 / 2),
            )
        elif channel_name == "amber":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 13 * round(23.75 / 2),
            )
        elif channel_name == "deep_red":
            return (
                drive_level_grid_coords[0] + 50,
                drive_level_grid_coords[1] + 15 * round(23.75 / 2),
            )
        else:
            raise NameError(f"There is no such channel_name {channel_name}.")

    def _create_thermal_target(self, color_temp: int = 6500, luminous: int = 2000):
        self.luminaire_dlg["Edit FrameButton1"].click_input()  # Click on the sun icon
        create_thermal_dlg = self.luminaire_app.window(
            title_re="Create thermal or daylight target", class_name="#32770"
        )
        create_thermal_dlg["Color Temperature (K):Edit"].set_edit_text(color_temp)
        create_thermal_dlg["Luminous Output (lm):Edit"].set_edit_text(luminous)
        create_thermal_dlg.CreateButton.click_input()

    def create_day_light(self):
        self.luminaire_dlg["Edit FrameButton1"].click_input()  # Click on the sun icon
        create_thermal_dlg = self.luminaire_app.window(
            title_re="Create thermal or daylight target", class_name="#32770"
        )
        create_thermal_dlg["Color Temperature (K):Edit"].set_edit_text(6500)
        create_thermal_dlg["Luminous Output (lm):Edit"].set_edit_text(2000)
        if not create_thermal_dlg["Daylight?CheckBox"].is_checked():
            create_thermal_dlg["Daylight?CheckBox"].check()
        create_thermal_dlg.CreateButton.click_input()

    def _set_duration(self):
        if self.luminaire_dlg["single frameCheckBox"].is_checked():
            self.luminaire_dlg["single frameCheckBox"].uncheck_by_click()
        self.luminaire_dlg.Edit2.set_edit_text(self.config.frame_duration)

    def load_lumenscript(self):
        self.luminaire_dlg.set_focus()
        if self.luminaire_dlg["single frameCheckBox"].is_checked():
            self.luminaire_dlg["single frameCheckBox"].uncheck_by_click()
        self.luminaire_dlg.wait("visible ready active")
        self.luminaire_dlg.Button20.click_input()  # Load lumen script
        load_dialog = self.luminaire_app.window(title_re="Load Lumenscript", class_name="#32770")
        lumenscript_dir = PureWindowsPath(self.config.lumenscript_dir)
        lumenscript_filename = lumenscript_dir / f"{self.config.lumenscript_filename}"
        load_dialog.Edit.set_edit_text(lumenscript_filename)
        load_dialog.Open.click_input()
        self.luminaire_dlg.wait("visible ready active")

    def set_match_mode(self, match_mode: str = "regular palette") -> None:
        self.luminaire_dlg["Match modeComboBox"].select(match_mode)

    def set_frame_source(self, frame_source: str = "target") -> None:
        self.luminaire_dlg["Frame sourceComboBox"].select(frame_source)

    def set_spectrum_format(self, spd_format: str = "tab-delimited") -> None:
        self.luminaire_dlg["Spectrum formatComboBox"].select(spd_format)

    def increase_lumen_frame(self):
        # Increase Lumen Frame
        self.luminaire_dlg.set_focus()
        self.luminaire_dlg.Button16.click_input()

    def go_to_frame(self, frame_id: int, time_sleep=3):
        self.luminaire_dlg.set_focus()
        self.luminaire_dlg["Frame numberEdit"].click_input()
        self.luminaire_dlg["Frame numberEdit"].set_edit_text(frame_id)
        keyboard.send_keys("{ENTER}")
        time.sleep(time_sleep)
