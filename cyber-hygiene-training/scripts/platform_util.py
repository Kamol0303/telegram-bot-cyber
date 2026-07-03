"""
Platform detection — Termux, Linux, Windows, macOS.
"""

import os
import platform
import sys
from enum import Enum


class Platform(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    TERMUX = "termux"
    MACOS = "macos"
    UNKNOWN = "unknown"


def detect_platform() -> Platform:
    system = platform.system().lower()
    if os.path.isdir("/data/data/com.termux"):
        return Platform.TERMUX
    if system == "windows":
        return Platform.WINDOWS
    if system == "darwin":
        return Platform.MACOS
    if system == "linux":
        return Platform.LINUX
    return Platform.UNKNOWN


def is_windows() -> bool:
    return sys.platform == "win32"


def get_python_cmd(project_dir: str) -> str:
    """Return best Python executable (venv first)."""
    if is_windows():
        venv_py = os.path.join(project_dir, "venv", "Scripts", "python.exe")
    else:
        venv_py = os.path.join(project_dir, "venv", "bin", "python")

    if os.path.isfile(venv_py):
        return venv_py

    for cmd in (["py", "-3"] if is_windows() else []) + ["python3", "python"]:
        if isinstance(cmd, list):
            return " ".join(cmd)
        return cmd
    return "python3"


def get_pip_cmd(project_dir: str) -> list[str]:
    py = get_python_cmd(project_dir)
    if " " in py:
        return py.split() + ["-m", "pip"]
    return [py, "-m", "pip"]


def get_activate_hint(project_dir: str) -> str:
    if is_windows():
        return os.path.join(project_dir, "venv", "Scripts", "activate.bat")
    return f"source {os.path.join(project_dir, 'venv', 'bin', 'activate')}"


def get_stop_hint() -> str:
    if is_windows():
        return "stop.bat"
    return "bash stop.sh"


def get_start_hint() -> str:
    if is_windows():
        return "start.bat"
    return "bash start.sh"


def platform_label(p: Platform) -> str:
    labels = {
        Platform.WINDOWS: "Windows",
        Platform.LINUX: "Linux",
        Platform.TERMUX: "Termux (Android)",
        Platform.MACOS: "macOS",
        Platform.UNKNOWN: "Noma'lum",
    }
    return labels.get(p, "Noma'lum")
