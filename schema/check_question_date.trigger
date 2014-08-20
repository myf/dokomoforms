-- Function: check_question_date_function()

-- DROP FUNCTION check_question_date_function();

CREATE OR REPLACE FUNCTION check_question_date_function()
  RETURNS trigger AS
$BODY$
DECLARE
    the_question_type text;
begin
  SELECT question_type
    into the_question_type
  FROM question
  WHERE question.id = NEW.question_id;
  IF the_question_type != 'date' THEN
    raise exception 'date questions must have answer_date answers';
  end if;
RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION check_question_date_function()
  OWNER TO postgres;

-- Trigger: check_question_date_trigger on answer_date

-- DROP TRIGGER check_question_date_trigger ON answer_date;

CREATE TRIGGER check_question_date_trigger
  BEFORE INSERT OR UPDATE
  ON answer_date
  FOR EACH ROW
  EXECUTE PROCEDURE check_question_date_function();

