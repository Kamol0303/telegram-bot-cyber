"""
Cross-platform tunnel manager (zphisher port-forwarding logic).
Works on Termux, Linux, and Windows.
"""

import json
import os
import re
import shutil
import socket
import subprocess
import time
import urllib.request
from pathlib import Path

APP_PORT = int(os.getenv("APP_PORT", "8000"))


class TunnelManager:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.data_dir = project_dir / "data"
        self.bin_dir = project_dir / "bin"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.public_url_file = self.data_dir / "public_url.txt"
        self.tunnel_type_file = self.data_dir / "tunnel_type.txt"
        self.tunnel_pid_file = self.data_dir / "tunnel.pid"
        self.tunnel_log = self.data_dir / "tunnel.log"
        self.link_file = self.data_dir / "tunnel_link.tmp"
        self._processes: list[subprocess.Popen] = []

    def save_public_url(self, url: str, tunnel_type: str) -> None:
        url = url.rstrip("/")
        self.public_url_file.write_text(url + "\n", encoding="utf-8")
        self.tunnel_type_file.write_text(tunnel_type + "\n", encoding="utf-8")
        self._update_env_base_url(url)
        try:
            import sys
            sys.path.insert(0, str(self.project_dir))
            from backend.services.url_service import set_public_url
            set_public_url(url, tunnel_type)
        except Exception:
            pass
        print(f"[TUNNEL] Ommaviy havola: {url} ({tunnel_type})")

    def _update_env_base_url(self, url: str) -> None:
        env_path = self.project_dir / ".env"
        if not env_path.exists():
            return
        lines = env_path.read_text(encoding="utf-8").splitlines()
        found = False
        new_lines = []
        for line in lines:
            if line.startswith("BASE_URL="):
                new_lines.append(f"BASE_URL={url}")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"BASE_URL={url}")
        env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    def get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except OSError:
            return "127.0.0.1"

    def stop(self) -> None:
        if self.tunnel_pid_file.exists():
            try:
                pid = int(self.tunnel_pid_file.read_text().strip())
                self._kill_pid(pid)
            except (ValueError, OSError):
                pass
            self.tunnel_pid_file.unlink(missing_ok=True)

        for proc in self._processes:
            try:
                proc.terminate()
            except OSError:
                pass

        self._pkill_pattern("ngrok")
        self._pkill_pattern("serveo.net")
        self._pkill_pattern("localhost.run")
        self.link_file.unlink(missing_ok=True)

    def _kill_pid(self, pid: int) -> None:
        import sys
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
        else:
            try:
                os.kill(pid, 15)
            except OSError:
                pass

    def _pkill_pattern(self, pattern: str) -> None:
        import sys
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/FI", f"IMAGENAME eq ngrok.exe"],
                capture_output=True,
            ) if "ngrok" in pattern else None
        else:
            subprocess.run(["pkill", "-f", pattern], capture_output=True)

    def _popen_bg(self, cmd: list[str], log_file: Path | None = None) -> subprocess.Popen:
        import sys
        kwargs: dict = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        else:
            kwargs["start_new_session"] = True

        stdout = open(log_file, "w", encoding="utf-8") if log_file else subprocess.DEVNULL
        stderr = subprocess.STDOUT if log_file else subprocess.DEVNULL
        proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, **kwargs)
        self._processes.append(proc)
        if log_file:
            self.tunnel_pid_file.write_text(str(proc.pid), encoding="utf-8")
        return proc

    def start_local(self) -> str:
        ip = self.get_local_ip()
        url = f"http://{ip}:{APP_PORT}"
        self.save_public_url(url, "localhost")
        return url

    def start_none(self) -> str:
        url = f"http://127.0.0.1:{APP_PORT}"
        self.save_public_url(url, "none")
        return url

    def _find_ngrok(self) -> str | None:
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        local_ngrok = self.bin_dir / ("ngrok.exe" if os.name == "nt" else "ngrok")
        if local_ngrok.is_file():
            return str(local_ngrok)
        path = shutil.which("ngrok")
        return path

    def _install_ngrok(self) -> str | None:
        import platform as plat
        import sys
        import zipfile

        self.bin_dir.mkdir(parents=True, exist_ok=True)
        machine = plat.machine().lower()
        system = sys.platform

        urls = {
            ("linux", "aarch64"): "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip",
            ("linux", "arm"): "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip",
            ("linux", "x86_64"): "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip",
            ("linux", "i386"): "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip",
            ("win32", "amd64"): "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip",
            ("win32", "x86"): "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-386.zip",
        }

        key = (system if system != "linux" else "linux", machine)
        url = urls.get(key) or urls.get(("linux", "x86_64"))
        if not url:
            return None

        zip_path = self.bin_dir / "ngrok.zip"
        try:
            print(f"[TUNNEL] Ngrok yuklab olinmoqda...")
            urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(self.bin_dir)
            zip_path.unlink(missing_ok=True)
            ngrok_bin = self.bin_dir / ("ngrok.exe" if os.name == "nt" else "ngrok")
            if ngrok_bin.is_file() and os.name != "nt":
                ngrok_bin.chmod(0o755)
            return str(ngrok_bin) if ngrok_bin.is_file() else None
        except Exception as e:
            print(f"[TUNNEL] Ngrok yuklab olinmadi: {e}")
            return None

    def _get_ngrok_authtoken(self) -> str:
        env_path = self.project_dir / ".env"
        if not env_path.exists():
            return ""
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("NGROK_AUTHTOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
        return os.getenv("NGROK_AUTHTOKEN", "")

    def start_ngrok(self) -> str:
        ngrok = self._find_ngrok() or self._install_ngrok()
        if not ngrok:
            raise RuntimeError(
                "Ngrok topilmadi. O'rnating: https://ngrok.com/download "
                "yoki .env ga NGROK_AUTHTOKEN qo'shing"
            )

        token = self._get_ngrok_authtoken()
        if token:
            subprocess.run([ngrok, "config", "add-authtoken", token], capture_output=True)
            subprocess.run([ngrok, "authtoken", token], capture_output=True)

        self._popen_bg([ngrok, "http", str(APP_PORT)], self.tunnel_log)
        time.sleep(4)

        for _ in range(15):
            try:
                with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    for tunnel in data.get("tunnels", []):
                        url = tunnel.get("public_url", "")
                        if url.startswith("https://"):
                            self.save_public_url(url, "ngrok")
                            return url
            except Exception:
                pass
            time.sleep(2)

        raise RuntimeError("Ngrok havolasi olinmadi. NGROK_AUTHTOKEN ni tekshiring.")

    def start_serveo(self) -> str:
        ssh = shutil.which("ssh")
        if not ssh:
            raise RuntimeError("SSH topilmadi. Windows: OpenSSH o'rnating. Termux: pkg install openssh")

        self.link_file.unlink(missing_ok=True)
        cmd = [
            ssh, "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=60",
            "-R", f"80:localhost:{APP_PORT}",
            "serveo.net",
        ]
        self._popen_bg(cmd, self.link_file)
        time.sleep(12)

        if self.link_file.exists():
            text = self.link_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"https://[0-9a-zA-Z.-]+\.serveo\.net", text)
            if not match:
                match = re.search(r"https://[^\s]+", text)
            if match:
                url = match.group(0)
                self.save_public_url(url, "serveo")
                return url

        raise RuntimeError("Serveo havolasi olinmadi. Qayta urinib ko'ring.")

    def start_localhostrun(self) -> str:
        ssh = shutil.which("ssh")
        if not ssh:
            raise RuntimeError("SSH topilmadi.")

        self.link_file.unlink(missing_ok=True)
        cmd = [
            ssh, "-o", "StrictHostKeyChecking=no",
            "-R", f"80:localhost:{APP_PORT}",
            "ssh.localhost.run",
        ]
        proc = self._popen_bg(cmd, self.link_file)
        time.sleep(14)

        if self.link_file.exists():
            text = self.link_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"https://[0-9a-zA-Z.-]+\.localhost\.run", text)
            if not match:
                match = re.search(r"https://[^\s]+\.localhost\.run", text)
            if match:
                url = match.group(0)
                self.save_public_url(url, "localhostrun")
                return url

        try:
            proc.terminate()
        except OSError:
            pass
        raise RuntimeError("Localhost.run havolasi olinmadi.")

    def start_tunnel(self, choice: str) -> str:
        self.stop()
        handlers = {
            "1": self.start_local,
            "2": self.start_ngrok,
            "3": self.start_serveo,
            "4": self.start_localhostrun,
            "5": self.start_none,
        }
        handler = handlers.get(choice)
        if not handler:
            raise ValueError(f"Noto'g'ri tunnel tanlovi: {choice}")
        return handler()
