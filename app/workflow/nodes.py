from typing import Literal, Optional, List, Union
import re
from app.models.schemas import CollectInformationSchema
from app.services.llm_service import run_agent
from app.config.settings import settings
import logging

# Set up logger
logger = logging.getLogger("workflow.nodes")


def collect_information_node(state):

    user_query = state["user_query"]




    if "user_query_history" not in state:
        state["user_query_history"] = []





    user_query_history = state["user_query_history"]
    user_query_history = "\n".join(
    f"{i+1}. {'Human' if i % 2 == 0 else 'Logistics Assistant'}: {entry}" for i, entry in enumerate(user_query_history))



    if user_query_history == "":
        user_query = f"User Query:\n{user_query}"
    else:
        user_query = f"Conversation History:\n{user_query_history}\nUser Query:\n{user_query}"





    response = run_agent(settings.prompts["collect_information"], user_query, CollectInformationSchema)


    if response.model_dump()['license_plate'] is not None:
        state["license_plate"] = response.model_dump()['license_plate']
        state["provided_license_plate"] = response.model_dump()['license_plate']
    else:
        if "provided_license_plate" in state:
            state["license_plate"] = state["provided_license_plate"]
        else:
            state["license_plate"] = None

    if response.model_dump()['location'] is not None:
        state["location"] = response.model_dump()['location']
        state["provided_location"] = response.model_dump()['location']
    else:
        if "provided_location" in state:
            state["location"] = state["provided_location"]
        else:
            state["location"] = None


    if response.model_dump()['access_code'] is not None:
        state["access_code"] = response.model_dump()['access_code']
        state["provided_access_code"] = response.model_dump()['access_code']
    else:
        if "provided_access_code" in state:
            state["access_code"] = state["provided_access_code"]
        else:
            state["access_code"] = None





    
    if state["license_plate"] is not None:
        print("license plate is provided")
    if state["location"] is not None:
        print("location is provided")

    if state["access_code"] is not None:
        print("access code is provided")






    return state
    

def final_message_node(state):

    user_query = state["user_query"]
    if "user_query_history" not in state:
        state["user_query_history"] = []

    user_query_history = state["user_query_history"]
    user_query_history = "\n".join(
    f"{i+1}. {'Human' if i % 2 == 0 else 'Logistics Assistant'}: {entry}" for i, entry in enumerate(user_query_history)
)

    if user_query_history == "":
        user_query = f"User Query:\n{user_query}\nProvided Information:\nLicense Plate: {state['license_plate']}\nLocation: {state['location']}\nAccess Code: {state['access_code']}"
    else:
        user_query = f"Conversation History:\n{user_query_history}\nUser Query:\n{user_query}\nProvided Information:\nLicense Plate: {state['license_plate']}\nLocation: {state['location']}\nAccess Code: {state['access_code']}"
    print("########\nuser query is", user_query, "\n########")
    response = run_agent(settings.prompts["final_message"], user_query)
    # del state['access_code']

    if state["license_plate"] is not None and state["location"] is not None and state["access_code"] is not None:
        state["end_of_conversation"] = True

    if "provided_license_plate" in state:
        del state['provided_license_plate']
        del state['license_plate']
    if "provided_location" in state:
        del state['provided_location']
        del state['location']
    if "provided_access_code" in state:
        del state['provided_access_code']
        del state['access_code']
    state["final_message"] = response.content


    state["user_query_history"].append(state["user_query"])
    state["user_query_history"].append(state["final_message"])


    return state
