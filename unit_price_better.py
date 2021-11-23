import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import time


def calc_price(product_code, product_name):
    # read csv
    start_read = time.time()
    df = pd.read_csv("/Users/cheyennequijano/PycharmProjects/corruption-covid/UN Comtrade Data/merged_trade_data.csv")
    stop_read = time.time()
    print("read csv " + str(stop_read - start_read))

    # calculate price
    start_calcprice = time.time()
    df['Price'] = df['Trade Value (US$)'] / df['Qty']
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
    imports = df[(df['Partner ISO'] == 'WLD') & (df['Year'] == 2020) & (df['Trade Flow Code'] == 1)]
    exports = df[(df['Partner ISO'] == 'WLD') & (df['Year'] == 2020) & (df['Trade Flow Code'] == 2)]
    stop_group = time.time()
    print("grouped imports/exports " + str(stop_group - start_group))

    # get specific product
    start_pc = time.time()
    product_imports = imports[df['Commodity Code'] == product_code]
    product_exports = exports[df['Commodity Code'] == product_code]
    product_imports.reset_index(drop=True, inplace=True)
    product_exports.reset_index(drop=True, inplace=True)
    stop_pc = time.time()
    print("grouped product_imports/exports " + str(stop_pc - start_pc))

    # get total trade value for country
    start_iev = time.time()
    total_imp_value = product_imports.groupby(['Reporter ISO'], as_index=False)['Trade Value (US$)'].sum()
    total_exp_value = product_exports.groupby(['Reporter ISO'], as_index=False)['Trade Value (US$)'].sum()
    stop_iev = time.time()
    print("calculated total value of imports/exports " + str(stop_iev - start_iev))

    # assign total to product_exp/imports df
    start_assign = time.time()
    for pi in range(len(product_imports)):
        product_imports.loc[pi, 'Total Import Value (USD$)'] = total_imp_value.loc[total_imp_value['Reporter ISO'] == product_imports.iloc[pi, 10], 'Trade Value (US$)'].values[0]
    for pe in range(len(product_exports)):
        product_exports.loc[pe, 'Total Export Value (USD$)'] = total_exp_value.loc[total_exp_value['Reporter ISO'] == product_exports.iloc[pe, 10], 'Trade Value (US$)'].values[0]
    stop_assign = time.time()
    print("assigned total value of imports/exports " + str(stop_assign - start_assign))

    # average price normalized
    start_normal = time.time()
    product_imports['Average Import Price (USD$)'] = product_imports['Price'] / product_imports['Total Import Value (USD$)']
    product_exports['Average Export Price (USD$)'] = product_exports['Price'] / product_exports['Total Export Value (USD$)']
    stop_normal = time.time()
    print("normalized average price " + str(stop_normal - start_normal))

    # create country + gap lists for graphs
    start_lists = time.time()
    orig_exp_country_list = product_exports['Reporter ISO'].tolist()
    orig_imp_country_list = product_imports['Reporter ISO'].tolist()
    country_list = orig_exp_country_list
    gap_list = []
    for country in country_list:
        if country in product_imports['Reporter ISO'].values:
            gap = product_exports.loc[(product_exports['Reporter ISO'] == country), 'Average Export Price (USD$)'].values[0] - product_imports.loc[(product_imports['Reporter ISO'] == country), 'Average Import Price (USD$)'].values[0]
            gap_list.append(gap)
        else:
            country_list.remove(country)
    # remove inf values
    for gap in gap_list:
        if gap > 90000 or gap < -90000:
            remove_i = gap_list.index(gap)
            gap_list = gap_list[:remove_i] + gap_list[remove_i + 1:]
            country_list = country_list[:remove_i] + country_list[remove_i + 1:]
    stop_lists = time.time()
    print("created lists " + str(stop_lists - start_lists))

    # bar graph
    x_pos = [i for i, _ in enumerate(country_list)]
    plt.bar(x_pos, gap_list, color='green')
    plt.xlabel("Country")
    plt.ylabel("Export/Import Gap (USD$)")
    plt.title(str(product_name) + ' Export/Import Average Price Gap by Country (USD$)', fontsize=9)

    plt.xticks(x_pos, country_list, rotation='vertical')

    plt.savefig(str(product_code) + ' Export_Import Average Price Gap by Country (USD$)_bar_graph.png')

    # tables for analysis
    print(orig_exp_country_list)
    print(orig_imp_country_list)
    print(country_list)
    print(gap_list)
    print("completed " + str(product_code))

    return


if __name__ == "__main__":
    product_code_list = [900490, 841920, 5603, 300215, 382200, 382100, 902780, 220710, 220890, 380894, 280440, 901920,
                         300220, 392620, 401511, 621010, 481850, 9020, 90200]
    product_name_list = ["Safety Goggles", "Medical, surgical, laboratory sterilizers",
                         "Non-woven textiles (used for bandages, diapers, etc.)",
                         "Medical test kits (immunological reactions)",
                         "Medical test kits (PCR)", "Swab & viral transport",
                         "Medical diagnostic test instruments & apparatus",
                         "Alcohol solution (80% or more ethyl alcohol", "Alcohol solution (75% ethyl alcohol)",
                         "Hand sanitizer", "Medical oxygen", "Medical ventilators (CPAP, BiPap); Oxygen concentrators",
                         "Human vaccines", "Gloves, face & eye protection, protective garments", "Surgical gloves",
                         "Protective garments for surgical/medical use", "Disposable masks & garments",
                         "Breathing appliances excluding filters",
                         "Gas masks, filters against biological agents, masks with eye protection, face shields"]

    for product_index in range(len(product_code_list)):
        calc_price(product_code_list[product_index], product_name_list[product_index])
