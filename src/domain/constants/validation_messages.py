# src/domain/constants/validation_messages.py

ERR_SESSION_TYPE = "session must be an InterviewSession instance."
ERR_BOOL_FIELD = "{field_name} cannot be bool."
ERR_FIELD_TYPE = "{field_name} must be {expected_type}."
ERR_EMPTY = "{field_name} cannot be empty."
ERR_BOOL_ITEM = "Items in {field_name} cannot be bool."
ERR_ITEM_TYPE = "All items in {field_name} must be {item_type}."
ERR_ITEM_NUMERIC = "Items in {field_name} must be numeric."
ERR_ITEM_FINITE = "Items in {field_name} must be finite."
ERR_ITEM_MIN = "Items in {field_name} must be >= {min_value}."
ERR_ITEM_MAX = "Items in {field_name} must be <= {max_value}."
ERR_TZ_AWARE = "{field_name} must be timezone-aware."