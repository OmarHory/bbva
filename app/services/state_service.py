from app.models.schemas import WorkflowState
from app.services.redis_service import load_user_state, save_user_state, delete_user_state_pattern
import logging
from redis import Redis
# Set up logger
logger = logging.getLogger("services.state")

def get_user_state(user_id: str, user_input: str) -> WorkflowState:
    """
    Retrieve (or initialize) a user's conversation state from Redis.
    Store the history of user inputs for better context.
    """
    state = load_user_state(user_id)
    
    if not state:
        logger.info(f"Creating new conversation state for user {user_id}")
        state = WorkflowState(user_query=user_input)
    else:
        state["user_input"] = user_input
        
        if "user_input_history" not in state:
            state["user_input_history"] = []
        
        state["user_input_history"] = (state["user_input_history"] + [user_input])[-10:]
        
        for key in ["plate_attempts", "location_attempts", "code_attempts"]:
            if key not in state:
                state[key] = []
                
        if "__result__" not in state:
            state["__result__"] = None
    
    save_user_state(user_id, state)
    
    return state

def reset_user_state(user_id: str) -> bool:
    """Reset a user's conversation state to start over."""

    # delete any key that starts with *user_id*
    try:
        delete_user_state_pattern(f"*{user_id}*")
        return True 
    except Exception as e:
        logger.error(f"Error resetting user state: {e}")
        return False 