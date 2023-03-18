from datetime import datetime

from tgbot.keyboards.calendar import calendar_callback


year = datetime.now().year,
month = datetime.now().month
calendar_callback.new("DAY", year, month, "day")
print(dict(calendar_callback))
