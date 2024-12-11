from cumulusci.core.tasks import BaseTask
import requests
import os
import zipfile
import shutil
import platform
from pathlib import Path

class InstallChromeDriver(BaseTask):
    task_options = {
        "version": {
            "description": "Specific Chrome/ChromeDriver version to install (default: 131.0.6778.87)",
            "required": False,
        }
    }

    def _init_options(self, kwargs):
        super()._init_options(kwargs)
        self.options["version"] = kwargs.get("version", "131.0.6778.87")

    def _run_task(self):
        version = self.options["version"]
        
        # Determine OS and architecture
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Map architecture
        arch = "win64" if system == "windows" else "linux64" if system == "linux" else "mac-x64"
        if system == "darwin" and ("arm" in machine or "aarch64" in machine):
            arch = "mac-arm64"
            
        url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/{arch}/chromedriver-{arch}.zip"
        
        # Determine installation directory
        if system == "windows":
            scripts_dir = Path(os.path.dirname(shutil.which("python"))) / "Scripts"
        else:
            scripts_dir = Path("/usr/local/bin")
            
        driver_name = "chromedriver.exe" if system == "windows" else "chromedriver"
        driver_path = scripts_dir / driver_name

        if driver_path.exists():
            if system != "windows":
                os.chmod(driver_path, 0o755)  # Ensure we can delete on Unix
            driver_path.unlink()

        self.logger.info(f"Downloading ChromeDriver {version} for {arch}")
        
        response = requests.get(url)
        response.raise_for_status()

        zip_path = scripts_dir / "chromedriver.zip"
        zip_path.write_bytes(response.content)

        with zipfile.ZipFile(zip_path) as z:
            for zip_info in z.filelist:
                if zip_info.filename.endswith(driver_name):
                    zip_info.filename = driver_name
                    z.extract(zip_info, scripts_dir)
        
        zip_path.unlink()
        
        if system != "windows":
            os.chmod(driver_path, 0o755)  # Make executable on Unix

        self.logger.info(f"ChromeDriver {version} installed to {driver_path}")