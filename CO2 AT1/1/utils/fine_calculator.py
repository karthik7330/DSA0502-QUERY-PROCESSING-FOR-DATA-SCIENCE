from datetime import datetime

def calculate_fine(issue_date, return_date):

    issue = datetime.strptime(issue_date,"%Y-%m-%d")
    ret = datetime.strptime(return_date,"%Y-%m-%d")

    days = (ret-issue).days

    if days<=7:
        return 0

    return (days-7)*10