from pathlib import Path
import os
import xml.etree.ElementTree as ET

from cumulusci.core.tasks import BaseTask, CCIOptions
from cumulusci.utils.options import Field

class ExtractConsumerKeyAndSetEnv(BaseTask):
    class Options(CCIOptions):
        mypath: Path = Field(..., description="A filepath to be used by the task")

    parsed_options: Options

    def _run_task(self):
        file = self.parsed_options.mypath

        # Parse the XML content
        tree = ET.parse(file)
        root = tree.getroot()

        # Use XML ElementTree to extract consumerKey value
        namespace = {'md': 'http://soap.sforce.com/2006/04/metadata'}
        consumer_key_element = root.find(".//md:oauthConfig/md:consumerKey", namespace)
        if consumer_key_element is not None:
            consumer_key = consumer_key_element.text
            os.environ["CONSUMER_KEY"] = consumer_key
            self.logger.info(f"Set CONSUMER_KEY environment variable to {consumer_key}")
        else:
            self.logger.error("Failed to extract consumerKey from the provided file.")
