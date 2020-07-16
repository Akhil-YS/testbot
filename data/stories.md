## happpy_path with_buttons
* greet
    - utter_greet
* request_emp_details
    - emp_search_method
* inform{"search_type":"by_name"}
    - emp_search_form
    - form{"name": "emp_search_form"}
    - form{"name": null}
* goodbye
    - utter_goodbye
    - action_restart

## happy_path without_buttons
* greet
    - utter_greet
* request_emp_details{"emp_name": "ravi"}
    - set_emp_search_method
    - emp_search_form
    - form{"name": "emp_search_form"}
    - form{"name": null}
* goodbye
    - utter_goodbye
    - action_restart
     
## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot


