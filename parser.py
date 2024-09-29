import json
from dataclasses import dataclass

import bs4.element
import requests
from bs4 import BeautifulSoup

@dataclass
class OraOrar:
    ziua: str
    ora_start: int
    ora_end: int
    always_on: bool
    saptaana_para: bool
    sala: str
    grupa: str
    tip: str
    materie: str
    profesor: str


    def to_json(self):
        return json.dumps(
            {
                "ziua": self.ziua,
                "start": self.ora_start,
                "end": self.ora_end,
                "fiecare_saptamana": self.always_on,
                "saptamana_para": self.saptaana_para,
                "sala": self.sala,
                "groupa": self.grupa,
                "tip": self.tip,
                "materie": self.materie,
                "profesor": self.profesor,
            }
        )

    @staticmethod
    def from_table_row(table_row: list[str]) -> 'OraOrar':

        zi = table_row[0]
        ore = table_row[1]
        start = ore.split('-')[0]
        end = ore.split('-')[-1]

        al_on: bool = True
        para = False
        if len(table_row[2]) != 0:
            al_on = False
            para = int(table_row[2].split(' ')[-1]) % 2 == 0

        sala, grupa, tip, materie, prof = table_row[3:]

        return OraOrar(
            ziua=zi,
            ora_start=int(start),
            ora_end=int(end),
            always_on=al_on,
            saptaana_para=para,
            sala=sala,
            grupa=grupa,
            tip=tip,
            materie=materie,
            profesor=prof
        )


def get_page_source(an: int, semestru: int, specializare: str, an_specializare: int) -> str | None:
    url: str = f"https://www.cs.ubbcluj.ro/files/orar/{an}-{semestru}/tabelar/{specializare}{an_specializare}.html"
    req = requests.get(url)
    if req.status_code != 200:
        return None
    return req.text

def get_table_grupa(source_code: str, grupa: str) -> bs4.element.Tag | None:
    soup = BeautifulSoup(source_code, "html.parser")

    # find the table
    el = soup.find("h1", text=f"Grupa {grupa}")
    if el and (table := el.find_next('table')):
        return table
    return None

def parse_table(table: bs4.element.Tag) -> list[OraOrar]:
    orar_raw: list[OraOrar] = []

    rows = table.find_all('tr')

    for row in rows[1:]:
        cols: list[bs4.element.Tag] = row.find_all('td')
        cols: list[str] = [ele.text.strip() for ele in cols]
        orar_raw.append(OraOrar.from_table_row(cols))

    return orar_raw