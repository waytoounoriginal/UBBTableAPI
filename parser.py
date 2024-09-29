import json
from dataclasses import dataclass
from urllib.parse import quote_plus

import bs4.element
import requests
from bs4 import BeautifulSoup
import urllib.parse


LOCATIONS_LUT: dict[str, str] = {
    '2/I': 'Sala Nicolae Iorga, Cladirea Centrala, etaj 1 (Str. M. Kogalniceanu)',
    '243B': 'Laborator Fizica',
    '5/I': 'Sala Tiberiu Popoviciu, Cladirea Centrala, etaj 1 (Str. M. Kogalniceanu)',
    '6/II': 'Sala Gheorghe Calugareanu, Cladirea Centrala, etaj 2 (Str. M. Kogalniceanu)',
    '7/I': 'Sala D.V. Ionescu, Cladirea Centrala, etaj 1 (Str. M. Kogalniceanu)',
    '9/I': 'Cladirea Centrala, etaj 1 (Str. M. Kogalniceanu)',
    'AAM': 'Amfiteatrul Augustin Maior (Facultatea de Fizica), Cladirea Centrala, Etaj 2',
    'AVM': 'Amfiteatrul Victor Marian (Facultatea de Fizica), Cladirea Centrala, Etaj 2',
    'MOS-S15': 'S15 - Centrul de Modelare, Optimizare si Simulare (MOS)',
    'A304': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A305': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A311': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A312': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A313': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A321': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A322': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'A323': 'Cladirea Avram Iancu, etaj 3 (Str. A. Iancu)',
    'e': 'Cladirea Mathematicum, etaj 1 (str. Ploiesti)',
    'gamma': 'Cladirea Mathematica (str. Ploiesti)',
    'lambda': 'Cladirea Mathematica  (str. Ploiesti)',
    'Multimedia': 'Cladirea Mathematica (str. Ploiesti)',
    'pi': 'Cladirea Mathematica, parter (str. Ploiesti)',
    'Sala-Lectura': 'Sala Lectura, Mathematica',
    'A2': 'Amfiteatrul A2, Campus, parter (str. T. Mihali)',
    'C310': 'Campus, etaj 3 (str. T. Mihali)',
    'C335': 'Campus, etaj 3 (str. T. Mihali)',
    'C510': 'Campus, etaj 5 (str. T. Mihali)',
    'C512': 'Campus, etaj 5 (str. T. Mihali)',
    'L001': 'Campus, Subsol (str. T. Mihali)',
    'L002': 'Campus, Subsol (str. T. Mihali)',
    'L301': 'Campus, etaj 3 (str. T. Mihali)',
    'L302': 'Campus, etaj 3 (str. T. Mihali)',
    'L306': 'Campus, etaj 3 (str. T. Mihali)',
    'L307': 'Campus, etaj 3 (str. T. Mihali)',
    'L308': 'Campus, etaj 3 (str. T. Mihali)',
    'L320': 'Campus, etaj 3 (str. T. Mihali)',
    'L321': 'Campus, etaj 3 (str. T. Mihali)',
    'L336': 'Campus, etaj 3 (str. T. Mihali)',
    'L338': 'Campus, etaj 3 (str. T. Mihali)',
    'L339': 'Campus, etaj 3 (str. T. Mihali)',
    'L343': 'Campus, etaj 3 (str. T. Mihali)',
    'L402': 'Campus, etaj 4 (str. T. Mihali)',
    'L404': 'L404 IoT',
    'L439': 'Campus, etaj 4 (str. T. Mihali)',
    'Obs': 'Observatorul Astronomic (str. Ciresilor)',
    'Chimie204': 'Laborator 204 Chimie',
    'Catedra': 'Sediul unde are birou indrumatorul',
    'KulcsarTibor': 'Amfiteatrul Kulcsar Tibor',
    'neprecizat': 'Sala neprecizata',
    'Journey': 'Sala laborator Journey(NTT Data, Str. Ploiesti, et. 1)',
    'NTTSocrate': 'Amfiteatrul Socrate (NTT Data, Str. Ploiesti, parter)',
    'Saturn': 'Sala laborator Saturn (NTT Data, Str. Ploiesti, et. 1)',
    'DPPD-204': 'Departamentul Pentru Pregatirea Personalului didactic (Str. Motilor, nr.11)',
    'DPPD-205': 'Departamentul Pentru Pregatirea Personalului didactic (Str. Motilor, nr.11)',
    'DPPD-A307': 'Sala A307, Departamentul Pentru Pregatirea Personalului didactic (Str. Motilor,'
}



@dataclass
class OraOrar:
    ziua: int
    ora_start: int
    ora_end: int
    always_on: bool
    saptamana_para: bool
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
                "saptamana_para": self.saptamana_para,
                "sala": f"{self.sala}, {LOCATIONS_LUT[self.sala]}",
                "link_sala": f"https://maps.google.com/maps/search/?api=1&query={quote_plus(LOCATIONS_LUT[self.sala])}",
                "grupa": self.grupa,
                "tip": self.tip,
                "materie": self.materie,
                "profesor": self.profesor,
            }
        )

    @staticmethod
    def from_table_row(table_row: list[str]) -> 'OraOrar':

        ZILE_LUT = {
            "Luni": 1,
            "Marti": 2,
            "Miercuri": 3,
            "Joi": 4,
            "Vineri": 5
        }

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
            ziua=ZILE_LUT[zi],
            ora_start=int(start),
            ora_end=int(end),
            always_on=al_on,
            saptamana_para=para,
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