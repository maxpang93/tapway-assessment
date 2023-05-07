import json
from jsonschema import validators, Draft202012Validator
import base64
from datetime import datetime

"""
1. Extends latest validator with 'base64' and 'datetime' types
2. 'datetime' type only check '%Y-%m-%d %H:%M:%S.%f' format
3. validator return list of error message if any
"""

def is_base64(checker, instance):
    try:
        base64.b64decode(instance,validate=True)
        return True
    except:
        return False

def is_datetime(checker, instance):
    try:
        datetime.strptime(instance, "%Y-%m-%d %H:%M:%S.%f")
        return True
    except:
        return False

with open("schema.json") as f:
    schema = json.load(f)

type_checker = Draft202012Validator.TYPE_CHECKER.redefine_many({
    "base64": is_base64,
    "datetime": is_datetime
})

CustomValidator = validators.extend(
    Draft202012Validator,
    type_checker=type_checker
)
# CustomValidator.check_schema(schema) # No need to check_schema(). See validators.extend(): Extended validator's META_SCHEMA is not updated.
validator = CustomValidator(schema)

def validate_data(instance, show_full_error=True):
    if show_full_error:
        return [str(err) for err in validator.iter_errors(instance)]
    else:
        return [err.message for err in validator.iter_errors(instance)]
