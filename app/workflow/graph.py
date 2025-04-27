from langgraph.graph import StateGraph, END

from app.workflow.checkpointer import RedisSaver
from app.models.schemas import WorkflowState
from app.workflow.nodes import collect_information_node, final_message_node

from langgraph.graph import StateGraph, END, START


def create_workflow_graph():

    graph = StateGraph(WorkflowState)

    graph.add_node("collect_information", collect_information_node)
    graph.add_node("return_response", final_message_node)




    #

    graph.add_edge(START, "collect_information")
    graph.add_edge("collect_information", "return_response")
    graph.add_edge("return_response", END)
    with RedisSaver.from_conn_info(
            host="localhost",
            port=6379,
            db=0,
        ) as checkpointer:
        graph = graph.compile(checkpointer=checkpointer)

    return graph



compiled_graph = create_workflow_graph()