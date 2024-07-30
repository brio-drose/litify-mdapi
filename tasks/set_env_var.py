import os

from cumulusci.core.tasks import BaseTask, CCIOptions
from cumulusci.utils.options import Field

class SetEnvVar(BaseTask):
    class Options(CCIOptions):
        env_var_name: str = Field(..., description="The name of the environment variable to set")
        value: str = Field(..., description="The value to set the environment variable to")

    parsed_options: Options

    def _run_task(self):
        env_var_name = self.parsed_options.env_var_name
        value = self.parsed_options.value

        os.environ[env_var_name] = value
        self.logger.info(f"Set {env_var_name} environment variable to {value}")
        
