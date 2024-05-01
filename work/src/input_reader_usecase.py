class InputReaderUseCase:
    def __init__(self, input_reader):
        self.input_reader = input_reader
        self.batch = None

    def execute(self, source_path):
        # batch
        # load
        #
        return self.input_reader.read_source(source_path)
