from abc import abstractmethod


class PipelineStep:
    def __init__(self):
        pass

    @abstractmethod
    def annotate(self, text):
        pass