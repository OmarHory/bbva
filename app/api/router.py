from fastapi import APIRouter, HTTPException, Depends, Path, status
from app.models.schemas import ChatMessage, ChatResponse
from app.services.state_service import reset_user_state
from app.workflow.graph import compiled_graph
from app.auth.security import verify_token
from app.api.auth import auth_router
import logging

logger = logging.getLogger("api.router")

router = APIRouter()

router.include_router(auth_router, tags=["authentication"])

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(message: ChatMessage, authenticated: bool = Depends(verify_token)):
    try:
        logger.info(f"Received message from {message.user_id}: {message.text}")
        thread = {"configurable": {"thread_id": message.user_id}}
        state = compiled_graph.invoke({"user_query": message.text}, thread)
        if state.get("end_of_conversation", False):
            logger.info(f"Conversation ended for {message.user_id}")
            return ChatResponse(
                user_id=message.user_id,
                message=state["final_message"],
                end=True
            )
        else:
            logger.info(f"Generated response for {message.user_id}: {state['final_message']}")

            return ChatResponse(
                    user_id=message.user_id,
                    message=state["final_message"],
                    end=False
                )
    except Exception as e:
        logger.error(f"Error generating response for {message.user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate response")

@router.post("/reset/{user_id}", status_code=200)
def reset_conversation(
    user_id: str = Path(..., description="User ID to reset"),
    authenticated: bool = Depends(verify_token)
):
    logger.info(f"Resetting conversation for user: {user_id}")
    success = reset_user_state(user_id)
    
    if not success:
        logger.error(f"Failed to reset state for user: {user_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to reset conversation state")
        
    return {"status": "success", "message": f"Conversation reset for user: {user_id}"} 