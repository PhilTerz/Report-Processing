import json
import tabula

def e1_report_json:
    # Read pdf into json using tabula
    report = tabula.read_pdf("E1.pdf", output_format="json", pages="1")
    report_clean = []

    # @data: an array of arrays representings rows of the pdf
    # @obj: the object representations of each element in a row
    # Get rid of all the spaces created from tabula, noted where height = 0
    # Report is inconsistent, so standardize all '-' to '0' (they are equivalent in meaning)
    for row in report[0]['data']:
        for obj in row:
            if obj['height'] != 0.0:
                if obj['text'] == '-':
                    obj['text'] = "0"
                row_clean = []
                row_clean.append(obj)
                report_clean.append(row_clean)
    e1_to_file(report_clean)

def e1_to_file(report_clean):
    with open('tabtest.txt', 'w+') as outfile:
        json.dump(report_clean, outfile, sort_keys=True, indent=2, separators=(',', ': '))
