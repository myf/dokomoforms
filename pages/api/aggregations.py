"""API endpoints dealing with aggregations."""
from tornado.escape import json_encode
import tornado.web

import api.aggregation
from pages.util.base import APIHandler, get_email, validation_message


class AggregationHandler(APIHandler):
    def _apply_aggregation(self, aggregation_name: str, question_id: str):
        try:
            method = getattr(api.aggregation, aggregation_name)
            return method(question_id, email=get_email(self))
        except AttributeError:
            reason = json_encode(
                validation_message('aggregation', aggregation_name, 'invalid'))
        except api.aggregation.InvalidTypeForAggregationError:
            reason = json_encode(
                validation_message('aggregation', aggregation_name, 'invalid'))
        except api.aggregation.NoSubmissionsToQuestionError:
            reason = json_encode(
                validation_message('aggregation', aggregation_name,
                                   'no_submissions'))
        raise tornado.web.HTTPError(422, reason=reason)


    def get(self, question_id: str):
        response = [self._apply_aggregation(arg, question_id) for arg in
                    self.request.arguments]
        self.write(json_encode(response))
