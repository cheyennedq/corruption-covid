import pandas as pd

df = pd.read_csv("/Users/cheyennequijano/PycharmProjects/corruption-covid/UN Comtrade Data/merged_trade_data.csv")

import pandas as pd
df = pd.read_csv("/Users/cheyennequijano/PycharmProjects/corruption-covid/UN Comtrade Data/merged_trade_data.csv")

df.columns
Index(['Classification', 'Year', 'Period', 'Period Desc.', 'Aggregate Level',
       'Is Leaf Code', 'Trade Flow Code', 'Trade Flow', 'Reporter Code',
       'Reporter', 'Reporter ISO', 'Partner Code', 'Partner', 'Partner ISO',
       '2nd Partner Code', '2nd Partner', '2nd Partner ISO',
       'Customs Proc. Code', 'Customs', 'Mode of Transport Code',
       'Mode of Transport', 'Commodity Code', 'Commodity', 'Qty Unit Code',
       'Qty Unit', 'Qty', 'Alt Qty Unit Code', 'Alt Qty Unit', 'Alt Qty',
       'Netweight (kg)', 'Gross weight (kg)', 'Trade Value (US$)',
       'CIF Trade Value (US$)', 'FOB Trade Value (US$)', 'Flag'],
      dtype='object')
df['price'] = df['Trade Value (US$)']/df['Qty']

df['Trade Flow Code']
0          1
1          1
2          1
3          1
4          1
          ..
3363155    1
3363156    1
3363157    1
3363158    1
3363159    1
Name: Trade Flow Code, Length: 3363160, dtype: int64

df['Trade Flow Code'].value_counts
0          1
1          1
2          1
3          1
4          1
          ..
3363155    1
3363156    1
3363157    1
3363158    1
3363159    1
Name: Trade Flow Code, Length: 3363160, dtype: int64>

df['Trade Flow Code'].value_counts()
0    2485293
1     476023
2     378004
3      21842
4       1998
Name: Trade Flow Code, dtype: int64

df['Trade Flow'].value_counts()
M            1255698
X             842216
Import        476023
Export        378004
DX            155675
FM            144820
RX             66065
Re-Export      21842
RM             12720
MIP             4669
Re-Import       1998
XIP             1368
MOP             1139
XOP              730
MIF              138
XIF               55
Name: Trade Flow, dtype: int64

imports = df[df['Trade Flow']=='M']
exports = df[df['Trade Flow']=='X']
exports.groupby(['Partner Code', 'Commodity Code'])
exports.groupby(['Partner Code', 'Commodity Code'])[['Qty','price']].mean()

                                      Qty  price
Partner Code Commodity Code
0            5603            4.307073e+06    inf
             9020            1.694514e+08    inf
             220710          2.281042e+07    inf
             220890          1.641161e+06    inf
             280440          5.534502e+11    inf
                                   ...    ...
899          841920          2.447857e+02    inf
             900490          2.570192e+03    inf
             901920          6.459482e+02    inf
             902000          3.757081e+02    inf
             902780          4.135603e+02    inf
[4496 rows x 2 columns]

replace function