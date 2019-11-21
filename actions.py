# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import weather


# class ActionCurrentWeather(Action):

#     def name(self) -> Text:
#         return "action_current_weather"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         location = "Karlstad"

#         w = weather.Weather()
#         weather_report = w.get_current_weather(location)

#         dispatcher.utter_message(w.format_weather(weather_report,
#                                                   location))

#         return []


class CurrentWeatherForm(FormAction):

    def name(self) -> Text:
        return "current_weather_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """
        A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked
        """
        print("----In slot_mappings")
        return {
            "location": self.from_entity(entity="location")
            }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        print("----In submit")
        location = tracker.get_slot("location")
        w = weather.Weather()
        weather_report = w.get_current_weather(location)
        dispatcher.utter_message(w.format_weather(weather_report,
                                                  location))
        dispatcher.utter_template("utter_submit", tracker)
