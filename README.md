UBBTableAPI
--------------

A simple graphical interface to access BBU FMI's timetables for undergraduate courses.

The repo includes a parser for the timetables.

It can be very easily integrated into any calendar application with support for the iCalendar format.

## Self-hosting
While the tool is readily available [here](https://ubbtableapi.onrender.com), one can very easily self-host it.

First step is to install the requirements
```bash
pip install -r requirements.txt
```
Afterwards you can run the tool by using FastAPI
```bash
fastapi dev main.py
```