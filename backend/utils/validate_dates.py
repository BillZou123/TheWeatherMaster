from datetime import datetime

def validate_dates(start_date_str, end_date_str):

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

    if start_date > end_date:
        raise ValueError("start_date must be before end_date")

    return start_date, end_date