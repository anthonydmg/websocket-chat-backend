from .nlu import NLU
from .dialog_manager import DialogManagement

class Pipeline:
    def __init__(self) -> None:
        self.nlu = NLU()
        self.dm = DialogManagement()

    def preprocessing(self, text):
        text = text.lower()
        text = text.strip()
        return text

    def run(self, message):
        ## Prepocesing text
        print("Message Pipeline: ", message)
        clean_message = self.preprocessing(message)
        ## Nlu Inference
        nlu_data = self.nlu.inference(clean_message)
        ## Dialoque Managment
        responses = self.dm.next_action(nlu_data)

        return responses