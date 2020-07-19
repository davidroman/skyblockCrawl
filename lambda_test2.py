import time
import boto3
import json
from boto3.dynamodb.conditions import Key
import logging

from ask_sdk_core.skill_builder import SkillBuilder

from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# launch request
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to Sky Block shopping, you can retrieve pricing details for items on Sky Block"
        # handler_input.response_builder.speak(speech_text).set_card(SimpleCard("sky block shop", speech_text)).set_should_end_session(False)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)

        return handler_input.response_builder.response

# Shop Intent Handlers
class ShopHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("shop")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In shopHandler")

        # get localization data
        ## nah - data = handler_input.attributes_manager.request_attributes["_"]

        # type: (HandlerInput) -> Response
        speech_text = "You can shop Sky Block by stating an item to learn prices"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("SkyBlock Shop", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can request price details for SkyBlock items nearing Auction ending time"
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("SkyBlock Shop", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Thank you, Goodbye"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("SkyBlock Shop", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Add logging - logger.info("In SessionEndedRequestHandler")

        ## more logging logger.info("Session ended reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Add logging logger.info("In CatchAllExceptionHandler")
        # more logging logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ShopHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
