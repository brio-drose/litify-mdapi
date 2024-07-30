import re
from pathlib import Path

from cumulusci.core.tasks import BaseTask, CCIOptions
from cumulusci.utils.options import Field

class ExtractValueFromXML(BaseTask):
    class Options(CCIOptions):
        xml_file_path: Path = Field(..., description="The path to the XML file containing the value")
        tag: str = Field(..., description="The XML tag to extract the value from")

    parsed_options: Options

    def _run_task(self):
        xml_file_path = self.parsed_options.xml_file_path
        tag = self.parsed_options.tag

        if not xml_file_path.exists():
            self.logger.error(f"The file {xml_file_path} does not exist.")
            return

        with open(xml_file_path, 'r') as file:
            content = file.read()

        # Use regex to extract the value within the specified tag
        tag_pattern = f'<{tag}>([^<]+)</{tag}>'
        match = re.search(tag_pattern, content)
        if match:
            value = match.group(1)
            self._set_return_values(value)
            self.logger.info(f"Extracted value: {value}")
        else:
            self.logger.error(f"Failed to extract value for tag <{tag}> from the provided file.")
    
    def _set_return_values(self, value):
        self.return_values = {
            "extracted_value": value,
        }
