# BBVA Demo Code API

A conversational API that handles requests by extracting license plate, location, and access code information from user inputs. The system is designed to work like a phone call interface, allowing for natural dialogue with multiple messages about the same entity.

## Project Structure

```
.
├── app/
│   ├── api/             # API endpoints
│   │   └── router.py    # FastAPI router for chat endpoint
│   ├── config/          # Configuration files
│   │   ├── agent_prompts.py  # LLM prompt templates
│   │   └── settings.py  # Environment settings
│   ├── models/          # Data models
│   │   └── schemas.py   # Pydantic models
│   ├── services/        # Business logic
│   │   ├── llm_service.py    # LLM integration
│   │   ├── redis_service.py  # Redis integration
│   │   └── state_service.py  # State management
│   ├── utils/           # Utility functions
│   │   └── test_redis.py     # Redis connection test
│   └── workflow/        # Conversation workflows
│       ├── graph.py     # LangGraph workflow definition
│       └── nodes.py     # State machine nodes
├── .env                 # Environment variables (not committed to git)
└── main.py              # Application entry point
```

## Conversation Features

The API is designed for phone call-like interfaces and includes:

1. **Robust Entity Extraction**:
   - Can handle multiple similar inputs about the same entity
   - Uses pattern matching as a fallback when LLM extraction fails
   - Extracts the most likely value when multiple possibilities are mentioned

2. **Conversation History**:
   - Tracks conversation history for better context
   - Maintains multiple attempts for each entity extraction

3. **State Management**:
   - Persistent state using Redis
   - Checkpointing for the conversation workflow

4. **Quality Assurance**:
   - Multiple extraction attempts are reconciled to find the most likely value
   - Fallback mechanisms ensure the conversation continues

## Configuration

The application is configured using environment variables that can be set in a `.env` file:

```
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_PREFIX=bbva_demo_access_

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Prerequisites

- Python 3.8+
- Redis server running locally or accessible via network

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Create a `.env` file with your configuration
4. Start Redis server:
   ```bash
   redis-server
   ```
5. Test Redis connection:
   ```bash
   python -m app.utils.test_redis
   ```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

- **POST /api/chat**: Process a chat message
  - Request body: `{ "user_id": "user123", "text": "My message" }`
  - Returns: Response with next message and updated state

- **POST /api/reset/{user_id}**: Reset a conversation
  - Reset all state for a user to start over
  - Returns: `{ "status": "success", "message": "Conversation reset for user: user123" }`

- **GET /health**: Health check endpoint
  - Returns: `{ "status": "healthy", "environment": "development" }`

## Example Conversation Flow

1. **License Plate Extraction**:
   - System: "Please provide your license plate."
   - User: "3456AMB"
   - System: "The license plate of your is: 3456AMB. Can you tell me your location?"

2. **Location Extraction**:
   - User: "I'm at the Madrid port, loading zone 3"
   - System: "Your location is: Madrid. Please provide your access code."

3. **Access Code Extraction**:
   - User: "My access code is sunrise"
   - System: "Access code 'sunrise' received. Finalizing your request..."
   - System: "This is just a demo — your access code is sunrise. Thanks for calling, and have a great day!"

## Technologies Used

- FastAPI - API framework
- Pydantic - Data validation
- LangChain - LLM framework
- LangGraph - Conversation workflow management
- OpenAI's GPT models - Natural language processing
- Redis - State management and graph checkpointing
