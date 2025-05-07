from pydantic_settings import BaseSettings
class Credentials(BaseSettings):
    ado_pat: str
    class Config:
        env_file = '.env'
        fields = {
            'ado_pat': {'env': 'ADO_PAT'},
        }
creds: Credentials = Credentials()