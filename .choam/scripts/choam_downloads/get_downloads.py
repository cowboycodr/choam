import numpy as np

import requests
from pathlib import Path
from rich.console import Console
from rich.table import Table

download_history_text = Path("download_history.txt") \
                        .read_text(encoding="utf-8")
                    
download_history = {}                    
for section in download_history_text.split("\n"):
  name, value = section.split(":")
  
  download_history[name] = int(value)

recent_downloads_url = "https://pypistats.org/api/packages/choam/recent"

recent_downloads_response = requests.get(recent_downloads_url)
recent_downloads = recent_downloads_response.json()['data']

downloads_last_day = recent_downloads["last_day"]
downloads_last_week = recent_downloads["last_week"]
downloads_last_month = recent_downloads["last_month"]

downloads_difference = {
  "DAY": str(int(downloads_last_day) - download_history["DAY"]),
  "WEEK": str(int(downloads_last_week) - download_history["WEEK"]),
  "MONTH": str(int(downloads_last_month) - download_history["MONTH"])
}

for _type, diff in downloads_difference.items():
  if int(diff) > 0:
    downloads_difference[_type] = "+" + diff
  else:
    downloads_difference[_type] = "-" + diff

table = Table(title="Choam downloads")

table.add_column("Today", justify="center", style="yellow")
table.add_column("This Week", justify="center", style="yellow")
table.add_column("This Month", justify="center", style="yellow")

table.add_row(str(downloads_last_day), 
              str(downloads_last_week), 
              str(downloads_last_month))

difference_row_style = "red" if downloads_difference["DAY"].startswith("-") else "green"
table.add_row(str(downloads_difference["DAY"]),
              str(downloads_difference["WEEK"]),
              str(downloads_difference["MONTH"]), style=difference_row_style)

console = Console()
print()
console.print(table)

with open("download_history.txt", "w") as file:
  result = ""
  
  result += f"DAY:{downloads_last_day}"
  result += f"\nWEEK:{downloads_last_week}"
  result += f"\nMONTH:{downloads_last_month}"
  
  file.write(result)