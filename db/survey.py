"""Allow access to the survey table."""
import re
from sqlalchemy import Table, MetaData

from sqlalchemy.engine import RowProxy, ResultProxy
from sqlalchemy.sql import Insert

from db import engine
from db.auth_user import auth_user_table


survey_table = Table('survey', MetaData(bind=engine), autoload=True)

# TODO: more than one user
AUTH_USER_ID = auth_user_table.select().execute().first().auth_user_id


# TODO: remove hardcoded user
def survey_insert(*, auth_user_id=AUTH_USER_ID, title: str) -> Insert:
    """
    Insert a record into the survey table.

    :param auth_user_id: The UUID of the user.
    :param title: The survey's title
    :return: The Insert object. Execute this!
    """
    return survey_table.insert().values(title=title, auth_user_id=auth_user_id)


def survey_select(survey_id: str) -> RowProxy:
    """
    Get a record from the survey table.

    :param survey_id: the UUID of the survey
    :return: the corresponding record
    :raise SurveyDoesNotExistError: if the UUID is not in the table
    """
    survey = survey_table.select().where(
        survey_table.c.survey_id == survey_id).execute().first()
    if survey is None:
        raise SurveyDoesNotExistError(survey_id)
    return survey


def _conflicting(title: str, surveys: ResultProxy) -> int:
    """
    Get the highest number conflict of the titles in the survey table.

    :param title: the survey title in question
    :param surveys: the surveys from the table
    :return: the highest number conflict
    """
    for survey in surveys:
        pattern = r'{}\((\d+)\)'.format(title)
        match = re.match(pattern, survey.title)
        if match:
            yield int(match.groups()[0])


def get_free_title(title: str) -> str:
    """
    Get a good version of the title to be inserted into the survey table. If
    the title as given already exists, this function will append a number.
    For example, when the title is "survey":
    1. "survey" not in table -> "survey"
    2. "survey" in table -> "survey(1)"
    3. "survey(1)" in table -> "survey(2)"

    :param title: the survey title
    :return: a title that can be inserted safely
    """
    cond = survey_table.c.title.like(title + '%')
    similar_surveys = survey_table.select().where(cond).execute().fetchall()
    if not len(similar_surveys):
        return title
    conflicts = list(_conflicting(title, similar_surveys))
    free_number = max(conflicts) + 1 if len(conflicts) else 1
    return title + '({})'.format(free_number)


class SurveyDoesNotExistError(Exception):
    pass


class SurveyAlreadyExistsError(Exception):
    pass
