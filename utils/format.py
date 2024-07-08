from prettytable import PrettyTable
from datetime import datetime
import re

def format_empty_space(slot_text):
    current_date = datetime.now().strftime('%Y-%m-%d')
    split_parking_space = re.findall(r'\d{2}', slot_text)
    split_parking_space = ' '.join(split_parking_space)
    slots = split_parking_space.split()
    
    rows = [slots[i:i+2] for i in range(0, len(slots), 2)]
    
    table_str = "+--------+--------+\n"
    for row in rows:
        if len(row) < 2:
            row.append("")
        table_str += f"|  {row[0]:<6} |  {row[1]:<6} |\n"
    table_str += "+--------+--------+"

    template = (
        "------------------------------\n"
        "    주차장 빈자리 안내\n"
        f"    {current_date}\n"

        "------------------------------\n\n"
        f"{table_str}\n"
        "\n전체 자리 수: 23\n"
        "------------------------------"
    )
    
    return template

def format_predicted_space(predicted_val):
    current_date = datetime.now().strftime('%Y-%m-%d')
    data_rows = []
    for data in predicted_val:
        time = f"{data['hour']:02d}:00"
        empty_slots = str(data['empty_space'])
        data_rows.append([time, empty_slots])
    
    table = PrettyTable(["시각", "빈자리 수"])
    
    for row in data_rows:
        table.add_row(row)
    
    table_str = table.get_string()

    template = (
        "------------------------------\n"
        "    시간대별 빈자리 예측\n"
        f"    {current_date}\n"
        "------------------------------\n\n"
        f"{table_str}\n\n"
        "전체 자리 수: 23\n"
        "------------------------------"
    )
    
    return template
    
    return template
