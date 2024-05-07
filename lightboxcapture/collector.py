import os
import pickle
import shutil
import subprocess
import time
from pathlib import Path, PureWindowsPath

import hydra
import numpy as np
import pywinauto
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

# import dotenv
from pushsafer import Client
from pywinauto import keyboard, mouse
from pywinauto.application import Application
from tqdm import tqdm

from src.constant import DEVICE_COORDS, UV_DRIVE_NAME_COORD
from src.luminaire_manager import LuminaireManager
from src.secrets import PUSHSAFER_API_KEY


class Collector:
    def __init__(self, config: DictConfig):
        self.config = config

    def get_SPD_plots_from_telelumen(self):
        screenshot_dir = PureWindowsPath(self.config.screenshot_dir)
        telelumen_plot_dir = PureWindowsPath(self.config.telelumen_plot_dir)

        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="target")
        self.luminaire_manager.set_match_mode(match_mode="spectrum")
        self.luminaire_manager.disable_UV()
        self.luminaire_manager.create_day_light()
        time.sleep(3)
        shutil.copy2(
            telelumen_plot_dir / "tmp.png",
            screenshot_dir / "frame_000_daylight_D65.png",
            follow_symlinks=False,
        )

        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.disable_UV()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="target")
        self.luminaire_manager.set_match_mode(match_mode="spectrum")
        self.luminaire_manager.load_lumenscript()
        time.sleep(2)

        # if "SFU" in self.config.lumenscript_filename:
        #     n_lights = 102
        # elif "PhotoLED" in self.config.lumenscript_filename:
        #     n_lights = 1494
        # else:
        n_lights = self.config.n_lights

        for idx in range(1, n_lights + 1):
            new_name = f"frame_{idx:04d}"
            self.luminaire_manager.increase_lumen_frame()
            time.sleep(2)
            shutil.copy2(
                telelumen_plot_dir / "tmp.png",
                screenshot_dir / f"{new_name}.png",
                follow_symlinks=False,
            )

    def loop_predefined_frames(self):
        pass

    def capture_images_with_predefined_frames(self):

        powershell = Application().connect(title_re=".*PowerShell")

        powershell_dlg = powershell.WindowPowerShell

        frames_path = Path(self.config.frames_path)
        if frames_path.suffix == ".npy":
            frames = np.load(self.config.frames_path)
        elif frames_path.suffix == ".p":
            if "All_info" in self.config.frames_path:
                with open(frames_path, "rb") as f:
                    frames_all_info = pickle.load(f)
                frames = [f"illuminant_{frame_info['id']}" for frame_info in frames_all_info]
            else:
                with open(frames_path, "rb") as f:
                    frames = pickle.load(f)
        else:
            raise Exception(f"Unknown extension {frames_path.suffix=}")

        if frames[0] == "illuminant_0000":
            self._capture_day_light(powershell_dlg)

        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.disable_UV()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="target")
        self.luminaire_manager.set_match_mode(match_mode="spectrum")
        self.luminaire_manager.load_lumenscript()
        time.sleep(3)
        for frame in frames:
            if frame != "illuminant_0000":
                frame_id = int(frame.split("_")[1]) - 1
                # Click to the frame
                self.luminaire_manager.go_to_frame(frame_id, time_sleep=2)
                # Capture image
                self._capture_image(powershell_dlg, time_sleep=4)
                print(f"{frame=}")
                time.sleep(2)

    def capture_images_SPD_data(self):

        screenshot_dir = PureWindowsPath(self.config.screenshot_dir)
        powershell = Application().connect(title_re=".*PowerShell")

        powershell_dlg = powershell.WindowPowerShell

        self._capture_day_light(powershell_dlg)
        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.disable_UV()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="target")
        self.luminaire_manager.set_match_mode(match_mode="spectrum")
        self.luminaire_manager.load_lumenscript()

        time.sleep(2)

        for _ in range(self.config.n_lights):
            # Capture image
            self._capture_image(powershell_dlg, time_sleep=3.5)

            self.luminaire_manager.increase_lumen_frame()
            time.sleep(2)

    def capture_images_SFU_data(self):
        print("CAPTURE SFU")
        screenshot_dir = PureWindowsPath(self.config.screenshot_dir)
        powershell = Application().connect(title_re=".*PowerShell")
        powershell_dlg = powershell.WindowPowerShell

        self._capture_day_light(powershell_dlg)
        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.disable_UV()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="target")
        self.luminaire_manager.set_match_mode(match_mode="spectrum")
        self.luminaire_manager.load_lumenscript()
        time.sleep(2)

        if "SFU" in self.config.lumenscript_filename:
            n_lights = 102
        elif "PhotoLED" in self.config.lumenscript_filename:
            n_lights = 1494
        else:
            n_lights = 100

        for _ in range(n_lights):
            # Capture image
            self._capture_image(powershell_dlg, time_sleep=3.5)

            self.luminaire_manager.increase_lumen_frame()
            time.sleep(2)

    def capture_images_for_using_channel_drive_level(self):
        screenshot_dir = PureWindowsPath(self.config.screenshot_dir)
        powershell = Application().connect(title_re=".*PowerShell")
        powershell_dlg = powershell.WindowPowerShell

        self._capture_day_light()
        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="actual")
        self.luminaire_manager.set_match_mode(match_mode="regular palette")
        self.luminaire_manager.load_lumenscript()
        time.sleep(2)

        for _ in range(self.config.n_lights):
            # Capture image
            self._capture_image(powershell_dlg)

            self.luminaire_manager.increase_lumen_frame()
            time.sleep(2)

    def _capture_image(self, powershell_dlg, time_sleep=5):
        # Capture image
        powershell_dlg.set_focus()
        device = self.config.device
        if device != "DSLR":
            x = DEVICE_COORDS[device]["x"]
            y = DEVICE_COORDS[device]["y"]
            powershell_dlg.type_keys(
                "adb{VK_SPACE}-s{VK_SPACE}"
                + device
                + "{VK_SPACE}shell{VK_SPACE}input{VK_SPACE}tap{VK_SPACE}"
                + str(x)
                + "{VK_SPACE}"
                + str(y)
                + "{ENTER}"
            )
        else:
            x = DEVICE_COORDS["DSLR"]["x"]
            y = DEVICE_COORDS["DSLR"]["y"]
            powershell_dlg.type_keys(
                "adb{VK_SPACE}"
                + "shell{VK_SPACE}input{VK_SPACE}tap{VK_SPACE}"
                + str(x)
                + "{VK_SPACE}"
                + str(y)
                + "{ENTER}"
            )
        time.sleep(time_sleep)

    def _capture_day_light(self, powershell_dlg):
        self.luminaire_manager.reset_Luminaire()
        self.luminaire_manager.set_spectrum_format(spd_format="tab-delimited")
        self.luminaire_manager.set_frame_source(frame_source="target")
        self.luminaire_manager.set_match_mode(match_mode="spectrum")
        self.luminaire_manager.disable_UV()
        self.luminaire_manager.create_day_light()
        time.sleep(3)
        self._capture_image(powershell_dlg)  # Capture Daylight D65

    def change_folder_name_for_using_thermal_target_CT(self):
        start_temperature = self.config.start_temperature
        thermal_sweep_value = self.config.thermal_sweep_value
        scene_dir = Path(rf"{self.config.scene_dir}")
        camera_names = [
            "SN_R3CRB0BW3KA_S2203220012",
            "SN_R3CNC02XBYR_S000000046",
            "SN_R5CRB0VX8VV_S2204260005",
        ]
        for camera_name in camera_names:
            camera_dir = scene_dir / camera_name
            for idx, folder in enumerate(sorted(list(camera_dir.iterdir()))):
                if not folder.is_dir():
                    continue
                thermal_target = start_temperature + idx * thermal_sweep_value
                new_name = f"Scene_0_frame_{idx}_CT_{thermal_target}"
                new_folder = folder.parent / new_name
                shutil.move(folder, new_folder)
            assert idx == 99

    def change_folder_name_for_using_channel_drive_level(self):
        scene_id = self.config.scene_id
        scene_dir = Path(rf"{self.config.scene_dir}")
        camera_names = [
            "SN_R3CRB0BW3KA_S2203220012",
            "SN_R3CNC02XBYR_S000000046",
            "SN_R5CRB0VX8VV_S2204260005",
        ]
        for camera_name in camera_names:
            camera_dir = scene_dir / camera_name
            if camera_dir.is_dir():
                for idx, folder in enumerate(sorted(list(camera_dir.iterdir()))):
                    if not folder.is_dir():
                        continue
                    if idx == 0:
                        new_name = f"Scene_{scene_id:02d}_frame_{idx:04d}_daylight_D65"
                    else:
                        new_name = f"Scene_{scene_id:02d}_frame_{idx:04d}"
                    new_folder = folder.parent / new_name
                    shutil.move(folder, new_folder)

    def change_folder_name_for_SFU_data(self):
        scene_id = self.config.scene_id
        scene_dir = Path(rf"{self.config.scene_dir}")
        camera_names = [
            "SN_R3CRB0BW3KA_S2203220012",
            "SN_R3CNC02XBYR_S000000046",
            "SN_R5CRB0VX8VV_S2204260005",
        ]
        for camera_name in camera_names:
            camera_dir = scene_dir / camera_name
            if camera_dir.is_dir():
                for idx, folder in enumerate(sorted(list(camera_dir.iterdir()))):
                    if not folder.is_dir():
                        continue
                    if idx == 0:
                        new_name = f"Scene_{scene_id:02d}_frame_{idx:04d}_daylight_D65"
                    else:
                        new_name = f"Scene_{scene_id:02d}_frame_{idx:04d}"
                    new_folder = folder.parent / new_name
                    shutil.move(folder, new_folder)
            # assert idx == 102

    def change_folder_name_predefined_frames(self):
        frames_path = Path(self.config.frames_path)
        if frames_path.suffix == ".npy":
            frames = np.load(self.config.frames_path)
        elif frames_path.suffix == ".p":
            if "All_info" in self.config.frames_path:
                with open(frames_path, "rb") as f:
                    frames_all_info = pickle.load(f)
                frames = [f"illuminant_{frame_info['id']}" for frame_info in frames_all_info]
            else:
                with open(frames_path, "rb") as f:
                    frames = pickle.load(f)
        else:
            raise Exception(f"Unknown extension {frames_path.suffix=}")

        input_dir = Path(rf"{self.config.input_dir}")
        root_dir = Path(rf"{self.config.root_dir}")
        scene_name = self.config.scene_name
        camera_name = self.config.camera_name  # "SN_R3CRB0BW3KA_S2203220012"
        output_root = root_dir / scene_name / camera_name
        output_jpg = output_root / "JPG"
        output_raw = output_root / "RAW"
        output_jpg.mkdir(parents=True, exist_ok=True)
        output_raw.mkdir(parents=True, exist_ok=True)
        device_type = self.config.device_type
        if device_type == "phone":
            input_dirs = sorted(list(input_dir.iterdir()))
            print(f"Input dir length: {len(input_dirs)}")
            assert len(input_dirs) == len(
                frames
            ), "Input dirs and frames should have the same length"
            for frame, input_dir in tqdm(zip(frames, input_dirs)):
                # print(f"{frame=} {input_dir}")
                jpeg_paths = list(input_dir.glob("*.jpg"))
                raw_paths = list(input_dir.glob("*.dng"))
                assert len(jpeg_paths) == 1
                assert len(raw_paths) == 1
                jpeg_path = jpeg_paths[0]
                raw_path = raw_paths[0]
                shutil.copy(jpeg_path, output_jpg / f"{frame}.jpg")
                shutil.copy(raw_path, output_raw / f"{frame}.dng")
        elif device_type == "DSLR":
            jpeg_paths = sorted(list((input_dir / "JPG").glob("*.jpg")))
            raw_paths = sorted(list((input_dir / "RAW").glob("*.dng")))

            assert len(raw_paths) == len(jpeg_paths), "raw and jpeg should have the same length"
            assert len(frames) == len(
                jpeg_paths
            ), "Input dirs and frames should have the same length"
            for frame, jpeg_path, raw_path in tqdm(zip(frames, jpeg_paths, raw_paths)):
                shutil.copy(jpeg_path, output_jpg / f"{frame}.jpg")
                shutil.copy(raw_path, output_raw / f"{frame}.dng")

    def _load_luminaire_manager(self):
        self.luminaire_manager = LuminaireManager(self.config)
        self.luminaire_manager.init()
        time.sleep(5)

    def _send_push_notification(self):
        # Send push notification
        client = Client(PUSHSAFER_API_KEY)
        resp = client.send_message(f"It's done! {self.config.lumenscript_filename}")
        print(resp)

    def notify(self):
        cmd1 = "netsh wlan disconnect"
        cmd_list_networks = "netsh wlan show networks"
        cmd_connect_network = "netsh wlan connect name=AirYorkPLUS"
        subprocess.check_output(cmd1.split())
        wifi = subprocess.check_output(cmd_list_networks.split())
        data = wifi.decode("utf-8")
        if "AirYorkPLUS" in data:
            subprocess.check_output(cmd_connect_network.split())
            time.sleep(20)
            self._send_push_notification()
        else:
            powershell = Application().connect(title_re=".*PowerShell")
            powershell_dlg = powershell.WindowPowerShell
            powershell_dlg.type_keys("netsh{VK_SPACE}wlan{VK_SPACE}disconnect{ENTER}")
            powershell_dlg.type_keys("netsh{VK_SPACE}wlan{VK_SPACE}show{VK_SPACE}networks{ENTER}")
            powershell_dlg.type_keys(
                "netsh{VK_SPACE}wlan{VK_SPACE}connect{VK_SPACE}name=AirYorkPLUS{ENTER}"
            )
            time.sleep(20)
            self._send_push_notification()

    def run(self):
        start_experiment = time.time()
        waiting_before_capture = (
            self.config.waiting_before_capture if self.config.is_capture_image else 1
        )
        time.sleep(waiting_before_capture)
        try:
            if self.config.is_loop_through_frames:
                self._load_luminaire_manager()
                self.loop_predefined_frames()

            if self.config.is_create_lumenscript:
                self._load_luminaire_manager()
                if self.config.method_create_lumenscript == "using_thermal_target_CT":
                    self.luminaire_manager.create_lumenscript_using_thermal_target_CT()
                elif self.config.method_create_lumenscript == "using_channel_drive_level":
                    self.luminaire_manager.create_lumenscript_using_channel_drive_level()

            if self.config.is_capture_image:
                self._load_luminaire_manager()
                if self.config.method_create_lumenscript == "using_channel_drive_level":
                    self.capture_images_for_using_channel_drive_level()
                elif self.config.method_create_lumenscript == "using_SFU_data":
                    self.capture_images_SFU_data()
                elif self.config.method_create_lumenscript == "using_SPD":
                    print("Capture SPD")
                    self.capture_images_SPD_data()
                elif self.config.method_create_lumenscript == "predefined_frames":
                    self.capture_images_with_predefined_frames()

            # Change folder name
            if self.config.is_change_folder_name:
                if self.config.method_create_lumenscript == "using_thermal_target_CT":
                    self.change_folder_name_for_using_thermal_target_CT()
                elif self.config.method_create_lumenscript == "using_channel_drive_level":
                    self.change_folder_name_for_using_channel_drive_level()
                elif self.config.method_create_lumenscript == "using_SFU_data":
                    self.change_folder_name_for_SFU_data()
                elif self.config.method_create_lumenscript == "predefined_frames":
                    self.change_folder_name_predefined_frames()

            if self.config.is_get_SPD_plot:
                self._load_luminaire_manager()
                self.get_SPD_plots_from_telelumen()
        except Exception as e:
            print(f"Something went wrong. {e}")
        finally:
            if self.config.is_notify:
                self.notify()

            end_experiment = time.time()
            duration = round((end_experiment - start_experiment) / 60, 2)
            print(f"----- FINISHED in {duration} mins -----")
        # digiCamControl_app = Application().connect(path=r"C:\Program Files (x86)\digiCamControl\CameraControl.exe")
        # digiCamControl_app = Application().connect(title_re=".*qDslrDashboard.*")
        # digiCamControl_dlg = digiCamControl_app.qDslrDashboard
        # digiCamControl_dlg.set_focus()
        # digiCamControl_dlg.print_control_identifiers()
        # mouse.move(coords=(30, 100))
        # mouse.click(coords=(35, 100), button='left')
        # digiCamControl_dlg.button3.click()
        # digiCamControl_dlg.child_window(title="button3").print_control_identifiers()
        # self._load_luminaire_manager()
        # # self.luminaire_manager.luminaire_dlg.print_control_identifiers()
        # self.luminaire_manager.luminaire_dlg['Frame numberEdit'].set_edit_text(2)
        # keyboard.send_keys("{ENTER}")
        # anaconda_prompt = Application().connect(title_re="Anaconda.*")

        # anaconda_prompt_dlg = anaconda_prompt['Anaconda Prompt (Miniconda3)']
        # anaconda_prompt_dlg.set_focus()
        # anaconda_prompt_dlg.print_control_identifiers()
