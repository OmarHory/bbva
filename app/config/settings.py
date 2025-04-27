import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from app.config.agent_prompts import AGENT_PROMPTS

# Load environment variables from .env file
load_dotenv()

class OpenAISettings(BaseModel):
    """Settings for OpenAI API"""
    api_key: str = Field(default=os.getenv("OPENAI_API_KEY", ""), description="OpenAI API Key")
    model: str = Field(default=os.getenv("OPENAI_MODEL", "gpt-4.1"), description="OpenAI Model to use")

class RedisSettings(BaseModel):
    """Settings for Redis"""
    url: str = Field(default=os.getenv("REDIS_URL", "redis://localhost:6379"), description="Redis URL")
    password: str = Field(default=os.getenv("REDIS_PASSWORD", ""), description="Redis password")
    prefix: str = Field(default=os.getenv("REDIS_PREFIX", "bbva_demo_access_"), description="Redis key prefix")
    db: int = Field(default=os.getenv("REDIS_DB", 0), description="Redis database")
class SecuritySettings(BaseModel):
    """Settings for API security"""
    secret_key: str = Field(
        default=os.getenv("API_SECRET_KEY"), 
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(default="HS256", description="Algorithm for JWT token")

class Settings(BaseModel):
    """Main application settings"""
    environment: str = Field(default=os.getenv("ENVIRONMENT", "development"), description="Environment (development, production)")
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"), description="Logging level")
    openai: OpenAISettings = Field(default_factory=OpenAISettings, description="OpenAI settings")
    redis: RedisSettings = Field(default_factory=RedisSettings, description="Redis settings")
    security: SecuritySettings = Field(default_factory=SecuritySettings, description="Security settings")
    prompts: dict = AGENT_PROMPTS

settings = Settings() 