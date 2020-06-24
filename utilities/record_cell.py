from ij import measure
from ij.plugin.filter import Analyzer

column = 'string'
row = 0
value = 100

table = Analyzer.getResultsTable()

table.setValue(column, row, value)
table.show('the results')