from boto3 import client
from sanic import Sanic

from application.shared.redis import Redis
from application.shared.clients.decyphr.client import DecyphrNlpClient
from .cache import ProcessorPubSub
from .controllers import bp as ProcessingController
from .manager import ProcessorManager
from .repository import ProcessorRepository
from .processors.aws.processor import AWSComprehendProcessor
from .processors.decyphr.processor import DecyphrNlpProcessor
from .processors.decyphr.normaliser import DecyphrNlpNormaliser


def register_processor_blueprint(app: Sanic, redis: Redis) -> None:
    aws_processor = AWSComprehendProcessor(
        client=client(
            "comprehend",
            "eu-west-1",
            aws_access_key_id=app.config["aws"]["aws_access_key"],
            aws_secret_access_key=app.config["aws"]["aws_secret_key"],
        )
    )
    decyphr_processor = DecyphrNlpProcessor(DecyphrNlpNormaliser())
    processor_pubsub = ProcessorPubSub(redis)
    processor_manager = ProcessorManager(
        aws_processor=aws_processor,
        decyphr_processor=decyphr_processor,
        pubsub=processor_pubsub,
        repository=ProcessorRepository(),
        decyphr_client=DecyphrNlpClient(app.config["nlp"]["url"]),
    )

    app.blueprint(ProcessingController)
    app.ext.dependency(processor_manager, "processor_manager")
