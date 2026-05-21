from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    tcgplayer_public_key: str
    tcgplayer_private_key: str
    anthropic_api_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    twilio_to_number: str
    polling_interval_seconds: int = 900 # 15 minute default, change in .env if needed
    
    class Config:
        env_file = ".env"

settings = Settings()