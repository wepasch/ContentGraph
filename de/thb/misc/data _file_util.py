import pandas as pd
import json

from de.thb.content_graph.graph.constants import KEY_DURATION_MIN, KEY_ACTIVITIES, KEY_UID
from de.thb.misc.util import get_resource

SRC_PATH: str = 'graphs/template_v004_Psymeon 21112024.json'
DUR_PATH: str = 'graphs/Activities durations.xlsx'
DST_PAH: str = 'graphs/template_v004_Psymeon 23112024.json'


def add_duration(src_path: str, duration_path: str, dst_path: str) -> None:
    """
    Add durations from excel sheet to activities into a new file.
    """
    with open(get_resource(src_path), 'r') as src_file:
        raw = json.load(src_file)

    with open(get_resource(duration_path), 'rb') as dur_file:
        raw_excel = pd.read_excel(dur_file, sheet_name='Sheet1')
    nof_row: int = raw_excel.shape[0]
    i: int
    for i in range(nof_row):
        uid: str = raw_excel.iloc[i]['Activity ID']
        duration: int = int(raw_excel.iloc[i]['Duration in Minutes'])
        for a in raw[KEY_ACTIVITIES]:
            if a[KEY_UID] == uid:
                a[KEY_DURATION_MIN] = duration
                continue
    with open(get_resource(dst_path), 'w') as src_file:
        json.dump(raw, src_file)


add_duration(SRC_PATH, DUR_PATH, DST_PAH)
