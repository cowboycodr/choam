import numpy as np

import requests
from rich.console import Console
from rich.table import Table

recent_downloads_url = "https://pypistats.org/api/packages/choam/recent"

recent_downloads_response = requests.get(recent_downloads_url)
recent_downloads = recent_downloads_response.json()['data']

downloads_last_day = str(recent_downloads["last_day"])
downloads_last_week = str(recent_downloads["last_week"])
downloads_last_month = str(recent_downloads["last_month"])

table = Table(title="Choam downloads")

table.add_column("Today", justify="center", style="yellow")
table.add_column("This Week", justify="center", style="yellow")
table.add_column("This Month", justify="center", style="yellow")

table.add_row(downloads_last_day, 
              downloads_last_week, 
              downloads_last_month)

console = Console()
print()
console.print(table)