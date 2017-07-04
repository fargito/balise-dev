import pandas

df = pandas.read_excel(open('test_import.xls','rb'), sheetname=0)
print(df)
