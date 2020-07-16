from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
import json

# https://youngsoft.com/ritwik_employee/details.php?func=getEmpByName&empName=Priyanka
# https://youngsoft.com/ritwik_employee/details.php?func=getEmpByExp&empExp=3
# https://youngsoft.com/ritwik_employee/details.php?func=getEmpByLoc&empLoc=Hyderabad

ENDPOINTS = {
    "base": "https://youngsoft.com/ritwik_employee/details.php",
    "emp_search": {
                    "by_name": "?func=getEmpByName&empName={}",
                    "by_experience": "?func=getEmpByExp&empExp={}",
                    "by_location": "?func=getEmpByLoc&empLoc={}"
                }
    }
# There is a specific required_slot for specific search_type
REQ_SLOTS = {                 
    "by_name": "emp_name",
    "by_location": "emp_location",
    "by_experience":"emp_experience"
}
ENTITIES = REQ_SLOTS
SORRY_MESSAGE = {
    "by_name": "Sorry, I could not find any employees by the name {}.",
    "by_location": "Sorry, I could not find any employees from {}.",
    "by_experience": "Sorry, I  could not find any employees with {} years of experience."
}
def create_path(base: Text, query: Text, value: Text):

    return (base+query).format(value)


def find_employee(search_type: Text, value: Text) -> List[Dict]:
    
    employee_list = []
    names = []
    full_path = create_path( ENDPOINTS["base"], ENDPOINTS["emp_search"][search_type], value)
    try:
        json_obj = requests.get(full_path).json()
        print(json_obj)
        data = json.dumps(json_obj)
        clean_data = json.loads(data)
        
        for i in clean_data["employees"]:
        
            employee={}
            employee["emp_name"] = i["emp_name"]
            employee["emp_code"] = i["emp_code"]
            employee["emp_email"] = i["emp_email"]
            employee["emp_phone"] = i["emp_phone"]
            employee["emp_dob"] = i["emp_dob"]
            employee["exp"] = i["exp"]
            employee["location"] = i["location"]
            employee_list.append(employee)
            names.append(i["emp_name"])
        print(employee_list)
        print(len(employee_list))
        print(names)
        return names, employee_list
    except:
        return names, employee_list

class SelectEmployeeSearchMethod(Action):
  
    def name(self) -> Text:

        return "emp_search_method"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        buttons = []
        search_type = "Find Employees by Name"
        payload = "/inform{\"search_type\":\"by_name\"}"   
        buttons.append({"title": "{}".format(search_type),
                          "payload": payload})
        search_type = "Find Employees by Experience"
        payload = "/inform{\"search_type\":\"by_experience\"}"

        buttons.append({"title": "{}".format(search_type),
                          "payload": payload})
        search_type = "Find Employees by Location"
        payload = "/inform{\"search_type\":\"by_location\"}"
        buttons.append({"title": "{}".format(search_type),
                          "payload": payload})
      
        dispatcher.utter_button_template("utter_select_search_method", buttons, tracker)
        return []

class SetEmployeeSearchMethod(Action):
  
    def name(self) -> Text:

        return "set_emp_search_method"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        ent = tracker.latest_message['entities'][0]['entity']
        
        print("ent:{}".format(ent))
        search = ""
        for search_method, entity in ENTITIES.items():  
            print("{}:{}".format(search_method,entity))
            if entity == ent:
                search = search_method
                break

        print("search:{}".format(search))

        return [SlotSet("search_type", search)]
      
class SearchEmployee(FormAction):

    def name(self) -> Text:
        
        return "emp_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        
        search_type = tracker.get_slot('search_type')
        print("search_type:{}".format(search_type))

        req_slots = [REQ_SLOTS[search_type]]
        print(req_slots)
        
        return req_slots

    def slot_mappings(self) -> Dict[Text, Any]:
        return { "emp_name": self.from_entity(entity="emp_name", intent=["request_emp_details","inform"]),
                 "emp_location": self.from_entity(entity="emp_location", intent=["request_emp_details","inform"]),
                 "emp_experience": self.from_entity(entity="emp_experience", intent=["request_emp_details","inform"])
               }

    def submit(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]
           ) -> List[Dict]:
        
        search_type = tracker.get_slot('search_type')
        search_key  = tracker.get_slot(ENTITIES[search_type])

        names, employee_list = find_employee(search_type,search_key)


        if len(names) == 0:
            message = SORRY_MESSAGE[search_type]
            dispatcher.utter_message(text = message.format(search_key))
            return []

        names_list = names[0]
        for i in range(1,len(names)):
            names_list = names_list + ", " + names[i]
        dispatcher.utter_message(text = "Found {} employees - {} and these are their details".format(len(names),names_list))
        dispatcher.utter_message()
        for i in employee_list:
             dispatcher.utter_message(text = ("Employee Name: {}" + ", " + "Employee Code: {}" + ", " + "Email: {}" + ", " + "Phone: {}" + ", " + "Date Of Birth: {}" + ", " + "Experience: {}" + ", " + "Location: {}").format(i["emp_name"], i["emp_code"],i["emp_email"], i["emp_phone"], i["emp_dob"],i["exp"],i["location"]))

             # dispatcher.utter_message()
        return []
