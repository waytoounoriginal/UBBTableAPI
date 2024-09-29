from parser import (
    get_page_source,
    get_table_grupa,
    parse_table,
    OraOrar
)


ORAR: dict[str, str, OraOrar] = {}


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