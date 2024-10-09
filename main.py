from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

exel_data = pd.read_excel('/home/arachnemaster/Downloads/data.xlsx')

df = pd.DataFrame(exel_data,
                  columns=['client_id', 'sum', 'status', 'sale', 'new/current', 'document', 'receiving_date'])
pre_sort = df.query("receiving_date != '-'").dropna(subset='receiving_date')


def slice_frame_for_interval(frame: pd.DataFrame, sep1: Optional[str], sep2: Optional[str] = None):
    if sep2 and sep1:
        ind1 = frame[frame['status'].astype(str).str.contains(sep1, na=False)].index[0]
        ind2 = frame[frame['status'].astype(str).str.contains(sep2, na=False)].index[0]
        return frame.iloc[ind1:ind2]
    elif sep2:
        ind2 = frame[frame['status'].astype(str).str.contains(sep2, na=False)].index[0]
        return frame.iloc[:ind2]
    else:
        ind1 = frame[frame['status'].astype(str).str.contains(sep1, na=False)].index[0]
        return frame.iloc[ind1:]


july_2021 = slice_frame_for_interval(df, 'Июль 2021', 'Август 2021')

sum_by_july_2021 = july_2021.query('status != "ПРОСРОЧЕНО"')['sum'].sum()  # 859896.4699999996

july_2021 = july_2021.sort_values(axis=0, by='receiving_date').dropna(subset='receiving_date')


def create_graph_sales_date(subset: pd.DataFrame):
    plt.plot(subset['receiving_date'], subset['sum'])
    plt.ylabel('Sales')
    plt.xlabel('Date')
    plt.show()


sept_2021 = slice_frame_for_interval(df, 'Сентябрь 2021', 'Октябрь 2021')

top_manager = sept_2021.groupby('sale')['sum'].sum()  # Смирнов 221525.70

oct_2021 = slice_frame_for_interval(df, 'Октябрь 2021')

top_sale_type = oct_2021['new/current'].value_counts().idxmax()  # текущая

june_2021 = slice_frame_for_interval(df, 'Июнь 2021', 'Июль 2021')

contracts_from_may = june_2021[
    june_2021['receiving_date'].between(pd.to_datetime('2021-04'), pd.to_datetime('2021-06'))]
amount_of_contracts = contracts_from_may.count()  # 1


def count_marge_per_manager(row):
    if row['new/current'] == 'новая' and row['status'] == 'ОПЛАЧЕНО' and row['document'] == 'оригинал':
        return row['sum'] * 0.07
    elif row['new/current'] == 'текущая' and row['status'] != 'ПРОСРОЧЕНО' and row['document'] == 'оригинал':
        return row['sum'] * 0.05 if row['sum'] > 10000 else row['sum'] * 0.03
    else:
        return 0


by_july_01 = slice_frame_for_interval(df, sep1=None, sep2='Июль 2021').copy()
by_july_01['bonus'] = by_july_01.apply(count_marge_per_manager, axis=1)
manager_bonuses = by_july_01.groupby('sale')['bonus'].sum()

# Андреев        8744.0334
# Васильев       1376.2800
# Иванов         8495.2910
# Кузнецова      7101.6217
# Петрова       17799.5494
# Селиванов      5651.0120
# Смирнов       10508.9890
# Соколов         269.2110
# Филимонова     2727.6409
