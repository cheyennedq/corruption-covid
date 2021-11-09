import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import time


def calc_price(product_code):
    # read csv
    start_read = time.time()
    df = pd.read_csv("/Users/cheyennequijano/PycharmProjects/corruption-covid/UN Comtrade Data/merged_trade_data.csv")
    stop_read = time.time()
    print("read csv " + str(stop_read - start_read))

    # calculate price
    start_calcprice = time.time()
    df['Price'] = df['Trade Value (US$)'] / df['Qty'].notnull()
    print(df['Price'])
    stop_calcprice = time.time()
    print("created price column " + str(stop_calcprice - start_calcprice))

    # fix indices
    start_fixindex = time.time()
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'M') | (df['Trade Flow'] == 'Import'), 1, inplace=True)
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'X') | (df['Trade Flow'] == 'Export'), 2, inplace=True)
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'RX') | (df['Trade Flow'] == 'Re-Export'), 3, inplace=True)
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'RM') | (df['Trade Flow'] == 'Re-Import'), 4, inplace=True)
    stop_fixindex = time.time()
    print("indices fixed " + str(stop_fixindex - start_fixindex))

    # group data by imports or exports
    start_group = time.time()
    imports = df[(df['Partner ISO'] == 'WLD') & (df['Year'] == 2020) & ((df['Trade Flow Code'] == 1) | (df['Trade Flow Code'] == 4))]
    exports = df[(df['Partner ISO'] == 'WLD') & (df['Year'] == 2020) & ((df['Trade Flow Code'] == 2) | (df['Trade Flow Code'] == 3))]
    stop_group = time.time()
    print("grouped imports/exports " + str(stop_group - start_group))
    print(imports)
    print(exports)

    # get specific product
    start_pc = time.time()
    product_imports = imports[df['Commodity Code'] == product_code]
    product_exports = exports[df['Commodity Code'] == product_code]
    stop_pc = time.time()
    print("grouped product_imports/exports " + str(stop_pc - start_pc))
    print(product_imports)
    print(product_exports)

    # get total trade value for country
    start_iev = time.time()
    total_imp_value = product_imports.groupby(['Reporter ISO'], as_index=False)['Trade Value (US$)'].sum()
    total_exp_value = product_exports.groupby(['Reporter ISO'], as_index=False)['Trade Value (US$)'].sum()
    stop_iev = time.time()
    print("calculated total value of imports/exports " + str(stop_iev - start_iev))
    print(total_imp_value)
    print(total_exp_value)

    # assign total to product_exp/imports df
    start_assign = time.time()
    for pi in range(len(product_imports)):
        product_imports['Total Import Value (USD$)'] = total_imp_value.loc[(total_imp_value['Reporter ISO'] == product_imports.iloc[pi, 10]), 'Trade Value (US$)'].values[0]

    for pe in range(len(product_exports)):
        product_exports['Total Export Value (USD$)'] = total_exp_value.loc[(total_exp_value['Reporter ISO'] == product_exports.iloc[pi, 10]), 'Trade Value (US$)'].values[0]
    stop_assign = time.time()
    print("assigned total value of imports/exports " + str(stop_assign - start_assign))
    print(product_imports)
    print(product_exports)

    # average price
    # remove infinity & other things for price
    average_imp_price = product_imports.groupby(['Reporter ISO'],
                                                as_index=False).apply(lambda x: pd.Series({'Gap': (x['Price'] / x['Total Import Value (USD$)']).sum()}))
    average_exp_price = product_exports.groupby(['Reporter ISO'],
                                                as_index=False).apply(lambda x: pd.Series({'Gap': (x['Price'] / x['Total Export Value (USD$)']).sum()}))
    print(average_imp_price)
    print(average_exp_price)
    # print(average_gap_price)
    # test2 = product_imports.groupby(['Reporter ISO'], as_index=False).apply(lambda x: (x['Price'] * (x['Trade Value (US$)'] / x['Total Import Value (USD$)'])).sum())
    # test = product_imports['Price'] * (product_imports['Trade Value (US$)'] / product_imports['Total Import Value (USD$)']), ['Trade Value (US$)']])

    country_list = average_exp_price['Reporter ISO'].tolist()
    gap_list = []
    for country in country_list:
        if country in average_imp_price['Reporter ISO'].values:
            gap = average_exp_price.loc[(average_exp_price['Reporter ISO'] == country), 'Gap'].values[0] - average_imp_price.loc[(average_imp_price['Reporter ISO'] == country), 'Gap'].values[0]
            gap_list.append(gap)
        else:
            country_list.remove(country)
    print("created lists")

    # df_bar = pd.DataFrame({'Country': country_list, 'Export/Import Gap (USD$)': gap_list})
    # ax = df_bar.plot.bar(x='Country', y='Export/Import Gap (USD$)', rot=0)
    # ax.show()
    # ax.figure.savefig(str(product_code) + 'Export/Import Average Price Gap by Country (USD$).png')

    x_pos = [i for i, _ in enumerate(country_list)]
    plt.bar(x_pos, gap_list, color='green')
    plt.xlabel("Country")
    plt.ylabel("Export/Import Gap (USD$)")
    plt.title(str(product_code) + 'Export/Import Average Price Gap by Country (USD$)')

    plt.xticks(x_pos, country_list)

    plt.savefig(str(product_code) + ' Export_Import Average Price Gap by Country (USD$)_bar_graph.png')
    plt.show()

    return


if __name__ == "__main__":
    product_code_list = [900490, 841920, 5603, 300215, 382200, 382100, 902780, 220710, 220890, 380894, 280440, 901920,
                         300220, 392620, 401511, 621010, 481850, 9020, 90200]
    for pc in product_code_list:
        calc_price(90200)
