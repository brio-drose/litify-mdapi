from cumulusci.core.tasks import BaseTask
import requests
import os
import zipfile
import shutil
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
        url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
        
        # Install to Python Scripts directory which is in PATH
        scripts_dir = Path(os.path.dirname(shutil.which("python"))) / "Scripts"
        driver_path = scripts_dir / "chromedriver.exe"

        if driver_path.exists():
            driver_path.unlink()

        self.logger.info(f"Downloading ChromeDriver {version}")
        
        # Download and extract directly to Scripts directory
        response = requests.get(url)
        response.raise_for_status()

        zip_path = scripts_dir / "chromedriver.zip"
        zip_path.write_bytes(response.content)

        with zipfile.ZipFile(zip_path) as z:
            for zip_info in z.filelist:
                if zip_info.filename.endswith("chromedriver.exe"):
                    zip_info.filename = "chromedriver.exe"
                    z.extract(zip_info, scripts_dir)
        
        zip_path.unlink()

        self.logger.info(f"ChromeDriver {version} installed to {driver_path}")