import json
import tabula
import pprint

def e1_report_json():
    # Read pdf into json using tabula
    report = tabula.read_pdf("E1.pdf", output_format="json", pages="1")
    report_clean = []
    # @data: an array of arrays representings rows of the pdf
    # @obj: the object representations of each element in a row
    # Get rid of all the spaces created from tabula, noted where height = 0
    # Report is inconsistent, so standardize all '-' to '0' (they are equivalent in meaning)
    for j, row in enumerate(report[0]['data']):
        row_clean = []

        for index, obj in enumerate(row):
            is_firstCol = False
            if obj['height'] != 0.0:
                if index == 0 and j > 0:
                    is_firstCol = True
                    row_name = obj['text'].rsplit(' ', 1)[0]
                    row_first_num = obj['text'].rsplit(' ', 1)[1]
                    row_clean.extend([row_name, row_first_num])
                else: 
                    row_clean.append(obj['text'])
    
        report_clean.append(row_clean)

        if j == 3: 
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(report_clean)
            return
    

def e1_to_file(report_clean):
    with open('tabtest.txt', 'w+') as outfile:
        json.dump(report_clean, outfile, sort_keys=True, indent=2, separators=(',', ': '))

e1_report_json()