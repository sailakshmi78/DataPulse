from apps.validation.models import ValidationRule

from algorithms.duplicate_detector import find_duplicates
from algorithms.missing_value_detector import find_missing_values
from algorithms.range_detector import find_out_of_range
from algorithms.format_detector import find_format_issues


def run_validation(dataframe):
    """
    Run all active DataPulse validation rules
    configured in the database.
    """

    results = {
        "duplicates": [],
        "missing_values": [],
        "range_issues": [],
        "format_issues": [],
        "invalid_values": []
    }

    active_rules = ValidationRule.objects.filter(
        is_active=True
    )

    for rule in active_rules:

        # ================================================
        # DUPLICATE
        # ================================================

        if rule.rule_type == "duplicate":

            columns = rule.parameters.get("columns")

            if columns:
                columns = [
                    column
                    for column in columns
                    if column in dataframe.columns
                ]

            results["duplicates"].extend(
                find_duplicates(
                    dataframe,
                    columns=columns
                )
            )

        # ================================================
        # MISSING
        # ================================================

        elif rule.rule_type == "missing":

            results["missing_values"].extend(
                find_missing_values(dataframe)
            )

        # ================================================
        # RANGE
        # ================================================

        elif rule.rule_type == "range":

            column = rule.column_name

            if not column:
                continue

            if column not in dataframe.columns:
                continue

            minimum = rule.parameters.get("minimum")
            maximum = rule.parameters.get("maximum")

            if minimum is None or maximum is None:
                continue

            results["range_issues"].extend(
                find_out_of_range(
                    dataframe,
                    column=column,
                    minimum=minimum,
                    maximum=maximum
                )
            )

        # ================================================
        # FORMAT
        # ================================================

        elif rule.rule_type == "format":

            column = rule.column_name

            if not column:
                continue

            if column not in dataframe.columns:
                continue

            pattern = rule.parameters.get("pattern")

            if not pattern:
                continue

            results["format_issues"].extend(
                find_format_issues(
                 dataframe,
                 column=column,
                 pattern=pattern
                 )
            )

    return results