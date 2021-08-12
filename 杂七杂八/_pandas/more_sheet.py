import pandas as pd

read_path = 'import_data_test.xlsx'
write_path = 'res.xlsx'

data = pd.read_excel(read_path)
data1 = pd.ExcelWriter(write_path)

for i in range(5):
    df = pd.DataFrame(data)
    df.to_excel(data1, sheet_name=f'{i}')

data1.save()
