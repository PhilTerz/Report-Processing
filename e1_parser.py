import json
import tabula
import pprint

def e1_report_json():
    # Read pdf into json using tabula
    report = tabula.read_pdf("E1.pdf", output_format="json", pages="1")
    report_clean = []
    spillout_rows = {7, 12, 17, 19, 28, 34, 40, 43}
    spillout_texts = []
    # @data: an array of arrays representings rows of the pdf
    # @obj: the object representations of each element in a row
    # Get rid of all the spaces created from tabula, noted where height = 0
    # Report is inconsistent, so standardize all '-' to '0' (they are equivalent in meaning)
    for j, row in enumerate(report[0]['data']):
        row_clean = []

        for index, obj in enumerate(row):
            is_firstCol = False
            if obj['height'] != 0.0:
                if j in spillout_rows:
                    spillout_texts.append( (obj['text'], len(report_clean) - 1) )
                    break
                if index == 0 and j > 0 and j != 27 and j != 42:
                    is_firstCol = True
                    row_name = obj['text'].rsplit(' ', 1)[0]
                    row_first_num = '0' if obj['text'].rsplit(' ', 1)[1] == '-' else obj['text'].rsplit(' ', 1)[1]
                    row_clean.extend([row_name, row_first_num])
                else:
                    obj_text = '0' if obj['text'] == '-' else obj['text'] 
                    row_clean.append(obj_text)
        #after each row is processed, append the row to the cleaned up matrix
        if j not in spillout_rows:
            report_clean.append(row_clean)

    #after all rows processed, append spillout to previous column label
    labels1 = ["Assets", "Total Corporate", "Corporate", "Carefree Title", "Total Carefree Title", "Tucson", "Active Adult", "Phoenix", "West Region", "Total Arizona", "Northern California", "Southern California"]
    labels2 = ["Liabilities", "Total Corporate", "Corporate", "Carefree Title", "Total Carefree Title", "Tucson", "Active Adult", "Phoenix", "West Region", "Total Arizona", "Northern California", "Southern California"]
    labels3 = ["Stockholders Equity", "Corporate", "Total Corporate", "Carefree Title", "Total Carefree Title", "Tucson", "Active Adult", "Phoenix", "West Region", "Total Arizona", "Northern California", "Southern California"]
    
    for txt, row_num in spillout_texts:
        report_clean[row_num][0] = report_clean[row_num][0] + ' ' + txt
    report_clean[0] = labels1
    report_clean[23] = labels2
    report_clean[35] = labels3
    
    #return report_clean
    tst_index = report_clean[0].index('Phoenix')
    phx_col = [rowz[tst_index] for rowz in report_clean]
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(phx_col)

    return report_clean

# @report_clean is the matrix structure generated from e1_report_json()
# @region is a string, denoting the column label for the region, ex) 'Houston'
# We need to isolate the column that belongs to this and return the data from 
# the three tables, Assets, Liabilities, and Stockholders Equity
def region_map(report_clean, region):
    region_index = report_clean[0]['data'][0][0].index(region)
    #map represents the three tables found in the report
    reg_map = {
        'Assets': [],
        'Liabilities': [],
        'Stockholders Equity': []
    }
    # Do I need this?
    # ON HOLD for now


def e1_to_file(report_clean):
    with open('tabtest.txt', 'w+') as outfile:
        json.dump(report_clean, outfile, sort_keys=True, indent=2, separators=(',', ': '))

e1_report_json()
