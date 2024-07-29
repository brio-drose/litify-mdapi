from pathlib import Path

from cumulusci.core.tasks import BaseTask, CCIOptions
from cumulusci.utils.options import Field


class WriteFileCustomTask(BaseTask):
    class Options(CCIOptions):
        mypath: Path = Field(..., description="A filepath to be used by the task")
        mystring: str = Field("Hello", description="A string to be used by the task")

    parsed_options: Options

    def _run_task(self):
        file = self.parsed_options.mypath
        data = self.parsed_options.mystring
        file.write_text(data)
        self.logger.info(f"Wrote {data} to {file}")
