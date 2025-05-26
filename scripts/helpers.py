from typing import Dict
import pandas as pd
from collections import defaultdict
from enum import Enum

class Mode(Enum):
    number = 0
    index = 1

#{number} :: {attribute} || {number} :: {attribute} || …
def extract_from_notation(df: pd.DataFrame, col_name: str, mode: Mode = Mode.number) -> pd.DataFrame:
    output_dir = defaultdict(int)

    for cell in df[col_name]:
        if pd.isna(cell):
            continue

        for val in cell.split("||"):
            parsed = ''.join(val.split())
            if "::" in parsed:
                number_str, attribute = parsed.split("::", 1)
                try:
                    output_dir[attribute] += int(number_str) if mode is Mode.number else 1
                except ValueError:
                    pass

    return pd.DataFrame(output_dir.items(), columns=["attribute", "total"])

def parse_participants(row):
    try:
        age_dict = {int(p.split("::")[0]): int(p.split("::")[1]) for p in str(row['participant_age']).split("||") if "::" in p}
    except:
        age_dict = {}
    try:
        type_dict = {int(p.split("::")[0]): p.split("::")[1] for p in str(row['participant_type']).split("||") if "::" in p}
    except:
        type_dict = {}

    common_keys = set(age_dict.keys()) & set(type_dict.keys())
    data = [{'age': age_dict[k], 'type': type_dict[k]} for k in common_keys]
    return pd.DataFrame(data)



if __name__ == "__main__":

    #DEMO
    data = {
        'notation': [
            "3 :: speed || 2 :: strength || 5 :: agility",
            "1 :: speed || 4 :: agility",
            "2 :: strength || 1 :: agility || 3 :: speed",
            "5 :: stamina"
        ]
    }

    df = pd.DataFrame(data)

    print(extract_from_notation(df, "notation"))