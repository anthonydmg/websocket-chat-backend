from .responses import utter_responses


class DialogManagement:

    def utter_response(self, intent_name):
        return utter_responses['utter_saludo']
 
    def inference_rules(self, intent_name, entities, history=[]):
        responses = []

        if intent_name == "comenzar_dialogo":
            responses = [{"response": "utter_saludo"},
                         {"response": "utter_recuerda_escribir_ayuda"},
                         {"response": "utter_requerir_consulta"}]
                         
        elif intent_name == "saludo":
            responses = [{"response": "utter_saludo"},
                         {"response": "utter_requerir_consulta"}]

        elif intent_name == "despedida":
            responses = [{"response": "utter_despedida"}]

        elif intent_name == "denegar_mas_ayuda":
            responses = [{"response": "utter_despedida"}]

        elif intent_name == "confirmar_requerir_mas_ayuda":
            responses = [{"response": "utter_requerir_consulta"}]
        
        ## FAQ        
        elif ("utter_" + intent_name) in utter_responses.keys():
            responses = [{"response": "utter_" + intent_name},
                         {"response": "utter_requerir_mas"}]
        return responses


    def next_action(self, nlu_data):
        intent_name = nlu_data['intent_name']
        entities = nlu_data['entities']

        return self.utter_response(intent_name)
