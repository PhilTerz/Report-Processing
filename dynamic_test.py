import numpy as np
import pandas as pd
import tabula
import pprint

    # This map isn't final, there are still rows not shown in E1 reports
    # except for in Total Corporate or similar. Low priority, that can 
    # be done later
e1_bo_labels = {
        'Accounts Payable': 'Accounts Payable',
        'Accounts/Loans Receivable': 'Receivables, Net',
        'Accrued liabilities': 'Accrued Liabilities',
        'Assets': 'Total Assets',
        'Buyer Deposits': 'Home Sale Deposits',
        "Cap'd Construction Overhead": 'Capitalized Construction Costs',
        'Cash and Cash Equivalents': 'Cash and Cash Equivalents',
        'Common Costs': 'Common Costs',
        'Construction in Prog - Presold': 'Construction in Progress -',
        'Current Year Retained Earnings': '', #may have to remove this
        'Deferred Tax Liability': 'Deferred Tax Liabilities',
        'Deferred Tax Asset': 'Deferred Tax Asset',
        'Deposits-Opts & Prosp. Proj.': 'Deposits, Options and Earnest',
        'Equity': 'Total Stockholders Equity',
        'Finished Lot Inventory': 'Finished Lot Inventory',
        'Intercompany': 'Intercompany',
        'Inv. in Unconsol. Entities': 'Investment in Unconsolidated',
        'Liabilities': 'Total Liabilities',
        'Loans Payable Lots/Land': 'Lots and Land',
        'Lot and Land Under Developmt': 'Lots and Land Under',
        'Model Homes': 'Model Homes',
        'PY Retained Earnings/Capital': 'Retained Earnings',
        'Prepaid Expenses & Other Assets': 'Other Assets',
        'Property, Plant and Equipment': 'Property and Equipment, Net',
        'Spec Homes': 'Spec Homes',
        'Total Liabilities & Equity': 'Total Liabilities and Equity'
    }

def e1_report_map():
    report = tabula.read_pdf("sanant.pdf", pages="1")
    report = report.rename(columns = {"Unnamed: 1" : "First"})
    report = report.dropna(subset = ['First'])
    row_labels = report.iloc[0:26, 0].tolist()
    num_strs = report.iloc[0:26, 1].tolist()
    nums = []
    for strs in num_strs:
        strs = strs.replace(',','')
        strs = float(strs)
        strs = int(strs)
        nums.append(round(strs / 1000))
    report_map = dict(zip(row_labels, nums))
    del report_map['Current Year Retained Earnings']
    return report_map

def map_e1_bo_labels(e1_map):
    bo_labels = []
    for k, v in e1_map.items():
        bo_labels.append(e1_bo_labels[k])
    
    return bo_labels

def bo_report_map(bo_labels):
    report = tabula.read_pdf("E1.pdf", pages="2")
    report = report[report['Assets'].isin(bo_labels)]
    nums_labels = len(bo_labels)
    row_nums = report.iloc[0:nums_labels, 13] #will need to change '15' here to dymanic column num
    row_labels = report.iloc[0:nums_labels, 0]
    row_nums_corr = []
    for strs in row_nums:
        strs = strs.replace(',', '')
        strs = strs.replace('$', '')
        strs = float(strs)
        row_nums_corr.append( int(strs))
    report_map = dict(zip(row_labels, row_nums_corr))

    return report_map

def main_func():
    e1_map = e1_report_map()
    bo_labels = map_e1_bo_labels(e1_map)
    bo_map = bo_report_map(bo_labels)
    #map of "[BO Label]": [BO val, E1 val]
    compares = compare_dict(e1_map, bo_map)
    mismatches = compare(compares)
    return mismatches

def compare(compares):
    mismatches = []
    for k, v in compares.items():
        if v[0] != v[1]:
            mismatches.append((k, v))
    return mismatches

def compare_dict(e1_map, bo_map):
    compares = {}
    for k, v in e1_map.items():
        vals = []
        vals.append(v)
        bv = bo_map[e1_bo_labels[k]]
        vals.append(bv)
        compares[k] = vals

    return compares


pp = pprint.PrettyPrinter(indent=2)
pp.pprint(main_func())