from prettytable import PrettyTable


def print_table(headers: list, results: list, align: str = None) -> None:
    x = PrettyTable()
    x.field_names = headers

    for data_row in results:
        x.add_row(data_row)

    if align:
        for i, align_char in enumerate(align):
            x.align[headers[i]] = align_char
    print(x)
