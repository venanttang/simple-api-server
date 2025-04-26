import json
import logging
from jsonschema import SchemaError, ValidationError, validate


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

# Function to remove 'id' field recursively
def remove_id(json_obj:json):
    if isinstance(json_obj, dict):
        # Remove 'id' field if it exists
        result = {}
        for key, value in json_obj.items():
            logger.debug(f"key={key}, value={value}")
            # Recursively remove 'id' from nested objects
            if key != 'id':
                result[key] = remove_id(value)
            # else:
            #     result[key] = value
        return result
    elif isinstance(json_obj, list):
        return [remove_id(item) for item in json_obj]
    return json_obj

# Function to lookup 'id' based on 'label'
def lookup_id_by_label(json_obj: json, label: str) -> int:
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == 'label' and value == label:
                return json_obj.get('id')
            # Recursively search in nested objects
            found_id = lookup_id_by_label(value, label)
            if found_id is not None:
                return found_id
    elif isinstance(json_obj, list):
        for item in json_obj:
            found_id = lookup_id_by_label(item, label)
            if found_id is not None:
                return found_id
    return None

# Function to validate JSON against the schema
def validate_json(json_data, schema):
    if not json_data:
        logger.info("JSON data is empty or None")
        return
    if not schema:
        logger.info("Schema is empty or None")
        return
    
    try:
        # Validate the JSON data against the schema
        validate(instance=json_data, schema=schema)
        logger.info("JSON is valid!")
    except ValidationError as e:
        # Validation failed, logger.info the error
        logger.info(f"JSON validation failed: {e.message}")
    except SchemaError as e:
        # If the schema itself has an issue
        logger.info(f"Schema error: {e.message}")
    except Exception as e:
        # Catch other unexpected exceptions
        logger.info(f"An unexpected error occurred: {e}")
    return
