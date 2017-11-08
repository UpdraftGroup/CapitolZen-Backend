from datetime import datetime
from pytz import UTC

from capitolzen.document_analysis.summarize import summarize_text

from capitolzen.meta.states import AVAILABLE_STATES


def iterate_states(manager, manager_task):
    for state in AVAILABLE_STATES:
        if not manager(state.name).is_updating():
            manager_task.delay(state.name)
    return True


def time_convert(time):
    if isinstance(time, str):
        return UTC.localize(datetime.strptime(time, '%Y-%m-%d %I:%M:%S'))
    try:
        return UTC.localize(time)
    except ValueError:
        # Already a non-naive datetime
        return time


def summarize(content):
    if content is None:
        return ""
    return summarize_text(content)


def normalize_data(wrapper_list):
    """
    Take a list of wrappers and standardize data for output purposes
    returns a flattened dict of data for wrappers
    :param wrapper_list:
    :return dict:
    """
    output = []
    for w in wrapper_list:
        data = {
            "state_id": w.bill.state_id,
            "state": w.bill.state,
            "id": str(w.id),
            "sponsor": w.display_sponsor,
            "summary": w.display_summary,
            "current_committee": w.bill.current_committee,
            "status": w.bill.remote_status,
            "position": w.position,
            "position_detail": w.position_detail,
            "last_action_date": w.bill.last_action_date,
            "remote_url": w.bill.remote_url
        }

        output.append(data)
    return output
