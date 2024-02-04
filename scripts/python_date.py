""" In Python, you can format dates using the `strftime()` method from the `datetime` module. 
This method allows you to specify a format string to represent the date in a desired format. 
Here are some commonly used format codes:

- `%Y`: 4-digit year
- `%m`: 2-digit month (01-12)
- `%d`: 2-digit day (01-31)
- `%H`: 24-hour format hour (00-23)
- `%M`: 2-digit minute (00-59)
- `%S`: 2-digit second (00-59)
- `%A`: Full weekday name (e.g., Monday)
- `%B`: Full month name (e.g., January)
- `%a`: Abbreviated weekday name (e.g., Mon)
- `%b`: Abbreviated month name (e.g., Jan)
"""
# Here's an example of formatting the current date:

import datetime

x = datetime.datetime.now()

current_date = datetime.date.today()
print(current_date)  # 2022-12-27

print(x)  # 2023-08-06 09:18:19.222839
print(x.year)  # 2023
print(x.month)  # 8
print(x.day)  # 6
print(x.strftime("%m"))  # 08
print(x.strftime("%Y%m"))  # 202308

y = datetime.datetime(2020, 5, 17)
print(y)  # 2020-05-17 00:00:00
print(y.strftime("%B"))  # May


#! From string to date ========================================
from datetime import datetime

datetime_str = "09/19/22 13:55:26"

datetime_object = datetime.strptime(datetime_str, "%m/%d/%y %H:%M:%S").strftime(
    "%d %b %Y"
)
date_for_update = datetime.strptime(datetime_object, "%d %b %Y").strftime(
    "%Y-%m-%d %H:%M:%S"
)
print("Date is: ", date_for_update)
print(datetime_object)  # printed in default format
#! ========================================


from datetime import datetime

current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
# print(formatted_date)


# Output: `2023-07-13 15:30:00`

"""In this example, the format string `"%Y-%m-%d %H:%M:%S"` is used 
to represent the date and time in the format `YYYY-MM-DD HH:MM:SS`.
You can customize the format string according to your specific needs 
by combining the format codes mentioned above 
or using additional formatting options provided by the `strftime()` method.
"""
