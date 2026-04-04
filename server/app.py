from openenv.core.env_server import create_fastapi_app

from environment import EmailTriageEnvironment
from models import EmailTriageAction, EmailTriageObservation

app = create_fastapi_app(
    EmailTriageEnvironment,
    EmailTriageAction,
    EmailTriageObservation
)
