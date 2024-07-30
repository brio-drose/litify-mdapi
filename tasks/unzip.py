import zipfile
import os
from pathlib import Path

from cumulusci.core.tasks import BaseTask, CCIOptions
from cumulusci.utils.options import Field

class Unzip(BaseTask):
    class Options(CCIOptions):
        zip_path: Path = Field(..., description="The path to the zip file")
        extract_to: Path = Field(..., description="The directory to extract files to")
        remove_zip: bool = Field(default=False, description="Whether to remove the zip file after extraction")

    parsed_options: Options

    def _run_task(self):
        zip_path = self.parsed_options.zip_path
        extract_to = self.parsed_options.extract_to
        remove_zip = self.parsed_options.remove_zip

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            self.logger.info(f"Extracted {zip_path} to {extract_to}")

        # Conditionally remove the zip file
        if remove_zip:
            os.remove(zip_path)
            self.logger.info(f"Removed {zip_path}")
