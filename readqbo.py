# svbfix
# A filter program to fix Silicon Valley Bank's .qbo file.
#
import sys
from lxml import etree

# Parse a .QBO file from stdin
# and generate a string containing header string
# and a parsed etree of <OFX>.
def parseInput():
    header = ''
    l = ''
    while True:
        l = sys.stdin.readline()
        if l.startswith('<OFX>'):
            break
        header += l
    sgml = l
    sgml += sys.stdin.read()

    qbo = etree.fromstring(sgml)
    return header, qbo

# output file to stdout
def output(header, qbo):
    print(header)
    print(etree.tostring(qbo, pretty_print=True).decode('utf-8'))

# make changes to a parsed <OFX>
def modify(qbo):
    # Look for all the statement transactions (STMTTRN)
    p = qbo.findall('.//STMTTRN')
    for trn in p:
        trnType = trn.find('TRNTYPE').text
        amount = trn.find('TRNAMT').text
        # The issue with Silicon Valley Bank's QBO files is that
        # the amount of debit transactions are positive numbers and it shows up as a deposit with Quickbooks.
        # So it detects a debit transaction and add a minus character in front of the amount.
        if trnType == 'Debit' and len(amount) > 0 and amount[0] != '-':
            trn.find('TRNAMT').text = '-' + amount


def process():
    header, qbo = parseInput()
    modify(qbo)
    output(header, qbo)

if __name__ == '__main__':
    process()
