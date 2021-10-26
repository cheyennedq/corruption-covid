import glob
import os

import pandas


def merge_files():
    path = '/Users/cheyennequijano/PycharmProjects/corruption-covid/UN Comtrade Data'
    files = glob.glob(os.path.join(path, "*.csv"))

    df = (pandas.read_csv(file, dtype={"Qty Unit": "string", "Alt Qty Unit": "string"}) for file in files)
    df_merge = pandas.concat(df, ignore_index=True)
    return df_merge


def df_to_csv(df):
    col_titles = ("Classification","Year","Period","Period Desc.","Aggregate Level","Is Leaf Code","Trade Flow Code",
                  "Trade Flow","Reporter Code","Reporter","Reporter ISO","Partner Code","Partner","Partner ISO",
                  "2nd Partner Code","2nd Partner","2nd Partner ISO","Customs Proc. Code","Customs",
                  "Mode of Transport Code","Mode of Transport","Commodity Code","Commodity","Qty Unit Code","Qty Unit",
                  "Qty","Alt Qty Unit Code","Alt Qty Unit","Alt Qty","Netweight (kg)","Gross weight (kg)",
                  "Trade Value (US$)","CIF Trade Value (US$)","FOB Trade Value (US$)","Flag")
    pandas.DataFrame(df, columns=col_titles).to_csv('merged_trade_data.csv', index=False)


if __name__ == "__main__":
    merged_df = merge_files()
    df_to_csv(merged_df)
