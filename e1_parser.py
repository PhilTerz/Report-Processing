import json
import tabula
import pandas as pd
import pprint

def e1_report_map():
    labels_index = [0, 5, 7, 8, 9, 10, 12, 13, 15, 17, 4, 19, 24, 25, 28, 29, 30, 36, 37, 40, 45, 47, 48]
    report = tabula.read_pdf("E1.pdf", pages="2")
    row_nums = report.iloc[0:49, 15]
    row_labels = report.iloc[0:49, 0]
    row_labels_corr = [row_labels[i] for i in labels_index]
    row_nums_indexed = [row_nums[i] for i in labels_index]
    row_nums_corr = []
    for str in row_nums_indexed:
        str = str.replace(',', '')
        str = str.replace('$', '')
        str = float(str)
        row_nums_corr.append( int(str))
    report_map = dict(zip(row_labels_corr, row_nums_corr))

    return report_map


def biz_report_map():
    report = tabula.read_pdf("Biz.pdf", pages="1")
    row_labels = report.iloc[0:26, 0].tolist()
    del row_labels[14]
    del row_labels[20] #hard coding deleting the rows of just [label]:nan
    del row_labels[21]
    num_strs = report.iloc[0:26, 1].tolist()
    num_strs = [w for w in num_strs if str(w) != 'nan']
    nums = []
    for strs in num_strs:
        strs = strs.replace(',','')
        strs = float(strs)
        strs = int(strs)
        nums.append(round(strs / 1000))
    del nums[21]
    report_map = dict(zip(row_labels, nums))

    return report_map
 

def e1_to_file(report_clean):
    with open('tabtest.txt', 'w+') as outfile:
        json.dump(report_clean, outfile, sort_keys=True, indent=2, separators=(',', ': '))


def compare_reports():
    e1_map = e1_report_map()
    biz_map = biz_report_map()
    e1_nums = list(e1_map.values())
    biz_nums = list(biz_map.values())
    notsame = []
    x = 0

    for k, v in e1_map.items():
        if (v ^ int(biz_nums[x])) != 0:
            notsame.append(k)
        x += 1
    for i in notsame:
        print(i, e1_map[i])

compare_reports()
