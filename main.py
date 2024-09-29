from datetime import datetime, date, timedelta

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from parser import (
    get_page_source,
    get_table_grupa,
    parse_table,
    OraOrar
)

# Def curr an
CURR_YR = 2024
CURR_SEM = 1
DATA_INCEPERE_AN = date(year=2024, month=9, day=30)


app = FastAPI()
api_route = FastAPI(root_path="/api/v1")

app.mount("/api/v1", api_route)
app.mount("/", StaticFiles(directory="static", html=True))

# Create the api
@api_route.get("/getweek/{specializare}/{an}/{grupa}")
async def get_week_timetable(specializare: str, an: int, grupa: str):
    page = get_page_source(CURR_YR, CURR_SEM, specializare, an)
    tbl = get_table_grupa(page, grupa)
    orar_raw = parse_table(tbl)

    # Will have to fix it on the start of the week
    now = date.today()
    mon = now - timedelta(now.weekday() % 7)

    week_dict: dict = {}
    orar_index = 0
    last_index = 0

    diff = (now - DATA_INCEPERE_AN).days
    is_saptamana_para = False if diff < 0 else ((diff + 1) // 7 + 1) % 2 == 0

    while mon.weekday() < 5:

        while orar_index < len(orar_raw) and orar_raw[orar_index].ziua == mon.weekday() + 1:
            orar_index += 1

        week_dict[mon.strftime("%d-%m-%Y")] = [ora.to_json() for ora in orar_raw[last_index:orar_index] if ora.always_on or ora.saptamana_para == is_saptamana_para]
        mon += timedelta(days=1)
        last_index = orar_index

    return week_dict



if __name__ == "__main__":
    pagina = get_page_source(
        2024,
        1,
        "IE",
        1
    )

    if pagina is None:
        print("Ayaye")
        exit(-1)

    table = get_table_grupa(pagina, "917")

    if table is None:
        print("Ayaye x2")
        exit(-1)

    orar = parse_table(table)
    print(orar)