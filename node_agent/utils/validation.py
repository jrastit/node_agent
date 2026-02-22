import http
import jsonschema


def validation_error_inform_error(err, data, schema):
    """
    Custom validation error handler which produces 404 Bad Request
    response in case validation fails and returns the error
    """
    raise ValueError(
        {
            "status": http.HTTPStatus.BAD_REQUEST,
            "error": str(err),
            "data": data,
            "schema": schema,
        }
    )


def validate_function(data, schema):
    # print('validate: ', data)
    # print('definitions: ', schema)
    """
    if not hasattr(schema, 'properties'):
        print('Validation schema has no properties')
        raise Exception('validation schema has no properties')
    if not hasattr(schema, 'type'):
        print('Validation schema has no type')
        raise Exception('validation schema has no type')
    """
    try:
        jsonschema.validate(data, schema)
        # print('Validation ok')
    except Exception as e:  # pragma no cover
        print("Validation error", e)
        raise
