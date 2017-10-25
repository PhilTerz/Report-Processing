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
    '''
    Generates a map of the E1 report to Current Month

    The report is read through tabula into a dataframe. 
    We get the first two columns and clean up the number to match
    the Business Objects report. 

    @return {Dictionary} the E1 report row labels to numbers
    '''
    report = tabula.read_pdf("sanant.pdf", pages="1")
    report = report.rename(columns = {"Unnamed: 1" : "First"})
    report = report.dropna(subset = ['First']) #drop all rows that the first numbers are NaN
    row_labels = report.iloc[0:26, 0].tolist() #first column is rows
    num_strs = report.iloc[0:26, 1].tolist() #second column is current month values
    nums = []
    # Turn the strings into integers that match the BO report scale
    for strs in num_strs:
        strs = strs.replace(',','')
        strs = float(strs)
        strs = int(strs)
        nums.append(round(strs / 1000))
    report_map = dict(zip(row_labels, nums))
    # This field is not in use
    del report_map['Current Year Retained Earnings']
    return report_map

def map_e1_bo_labels(e1_map):
    ''' 
    The E1 and BO report labels don't exactly match, so we 
    have to use a dictionary to map the corresponding labels.

    @param {Dictionary} the E1 map of labels to dollar values
    @return {List} the corresponding BO labels
    '''
    bo_labels = []
    for k, v in e1_map.items():
        bo_labels.append(e1_bo_labels[k])
    
    return bo_labels

def bo_report_map(bo_labels):
    '''
    Once the E1 report is read, we know what we need to check for 
    in the BO report. 
    Find the associated column (TODO) with the E1 division and then
    create a map of the same format as the E1 map. 

    @param {List} the list of BO labels that correspond to the E1 report
    @return {Dictionary} the BO report labels to numbers
    '''
    report = tabula.read_pdf("E1.pdf", pages="2")
    # Grab only the rows that are provided in the corresponding E1 report
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
    '''
    Pseudo-main function that serves as the entry point for the script. 
        1. Get the E1 map
        2. Send the E1 map to map to corresponding BO labels
        3. Get the BO map
        4. Create a map to both report values from E1 values
        5. Get the labels and values of the fields that don't match between the reports

    @return {List} a list of mismatched tuples, E1 label -> [E1 value, BO value]
    '''
    e1_map = e1_report_map()
    bo_labels = map_e1_bo_labels(e1_map)
    bo_map = bo_report_map(bo_labels)
    #map of "[BO Label]": [BO val, E1 val]
    compares = compare_dict(e1_map, bo_map)
    mismatches = compare(compares)
    return mismatches

def compare(compares):
    '''
    Given the comparison dictionary, if the values for a label do 
    not match, store it as a mismatch

    @param {Dictionary} maps the E1 labels -> [E1 value, BO value]
    @return {List} a list of tuples for (E1 Label, [E1 value, BO value])
    '''
    mismatches = []
    for k, v in compares.items():
        if v[0] != v[1]:
            mismatches.append((k, v))
    return mismatches

def compare_dict(e1_map, bo_map):
    '''
    Compare the value of the two reports using the label map. 

    @param {Dictionary} e1_map is the E1 label -> value 
    @param {Dictionary} bo_map is the BO label -> value
    @return {Dictionary} the E1 label -> [E1 value, BO value]
    '''
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