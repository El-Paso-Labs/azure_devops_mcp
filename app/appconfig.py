from pydantic_settings import BaseSettings
class Credentials(BaseSettings):
    ado_token: str
    class Config:
        env_file = '.env'
        fields = {
            'ado_token': {'env': 'ADO_TOKEN'},
        }
creds: Credentials = Credentials()