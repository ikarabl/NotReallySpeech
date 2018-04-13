from src.step import PipelineStep
import texterra
import re


class CharacterDetector(PipelineStep):
    def __init__(self):
        super().__init__()
        self.t = texterra.API("c41d9b98960e6f6bdfb3452f6b174e5a6554f992")

    def annotate(self, text):
        said_, author_ = self.__get_speech_from_text(text)
        for i in author_:
            nes = self.t.named_entities(i, language='ru')
            for j in list(nes):
                if j != []:
                    print(j, i)
        return text

    def __get_speech_from_text(self, text):
        said_ = re.findall("<speech>(.+?)</speech>", text)
        author_ = re.findall("<speech>(.+?)</speech>", text)
        # said_ = re.findall("<said>(.+?)</said>", text)
        # author_ = re.findall("<author_comment>(.+?)</author_comment>", text)
        return said_, author_
