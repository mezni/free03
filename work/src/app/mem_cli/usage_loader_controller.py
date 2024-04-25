"""Usage Loader Controller Module"""


class UsageLoaderController:
    """Create Usage Loader Controller Class"""

    def __init__(self):
        self.logger = None

    def execute(self, usage_data):
        """
        Execute the ProcessHandler

        Args:
            usage_data ([str]): list of periods
        Returns:
            None
        """
        repository = None
        presenter = None
        input_dto = None
        use_case = None
        result = None
