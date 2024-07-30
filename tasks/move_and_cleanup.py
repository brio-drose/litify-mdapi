import shutil
import os
from pathlib import Path

from cumulusci.core.tasks import BaseTask, CCIOptions
from cumulusci.utils.options import Field

class MoveAndCleanup(BaseTask):
    class Options(CCIOptions):
        source_path: Path = Field(..., description="The source directory to move")
        destination_path: Path = Field(..., description="The destination directory")
        cleanup_path: Path = Field(..., description="The directory to remove after moving")
        remove_cleanup: bool = Field(default=True, description="Whether to remove the cleanup directory after moving")
        overwrite: bool = Field(default=True, description="Whether to overwrite the destination directory if it exists")

    parsed_options: Options

    def _run_task(self):
        source_path = self.parsed_options.source_path
        destination_path = self.parsed_options.destination_path
        cleanup_path = self.parsed_options.cleanup_path
        remove_cleanup = self.parsed_options.remove_cleanup
        overwrite = self.parsed_options.overwrite

        if destination_path.exists() and overwrite:
            shutil.rmtree(str(destination_path))
            self.logger.info(f"Removed existing destination directory {destination_path}")

        # Move the directory
        shutil.move(str(source_path), str(destination_path))
        self.logger.info(f"Moved {source_path} to {destination_path}")

        # Conditionally remove the cleanup directory
        if remove_cleanup:
            shutil.rmtree(str(cleanup_path))
            self.logger.info(f"Removed {cleanup_path}")
