import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import time


def calc_price(product_code, product_name, year):
    # read csv
    start_read = time.time()
    df = pd.read_csv("/Users/cheyennequijano/PycharmProjects/corruption-covid/UN Comtrade Data/merged_trade_data.csv")
    stop_read = time.time()
    print("read csv " + str(stop_read - start_read))

    # fix indices
    start_fix_index = time.time()
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'M') | (df['Trade Flow'] == 'Import'), 1, inplace=True)
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'X') | (df['Trade Flow'] == 'Export'), 2, inplace=True)
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'RX') | (df['Trade Flow'] == 'Re-Export'), 3, inplace=True)
    df['Trade Flow Code'].mask((df['Trade Flow'] == 'RM') | (df['Trade Flow'] == 'Re-Import'), 4, inplace=True)
    stop_fix_index = time.time()
    print("indices fixed " + str(stop_fix_index - start_fix_index))

    # find total imports/exports
    start_find_totals = time.time()
    imports = df[(df['Partner ISO'] != 'WLD') & (df['Trade Flow Code'] == 1)]
    exports = df[(df['Partner ISO'] != 'WLD') & (df['Trade Flow Code'] == 2)]
    total_imp_value = imports.groupby(['Year', 'Reporter ISO',
                                       'Commodity Code'])[['Trade Value (US$)']].sum().reset_index()
    total_imp_value.rename(columns={'Year': 'Year', 'Reporter ISO': 'Country ISO', 'Commodity Code': 'Commodity Code',
                                    'Trade Value (US$)': 'Calculated Trade Value (US$)'}, inplace=True)
    total_exp_value = exports.groupby(['Year', 'Partner ISO',
                                       'Commodity Code'])[['Trade Value (US$)']].sum().reset_index()
    total_exp_value.rename(columns={'Year': 'Year', 'Partner ISO': 'Country ISO', 'Commodity Code': 'Commodity Code',
                                    'Trade Value (US$)': 'Export Trade Value (US$)'}, inplace=True)
    # compare
    world_imports = df[(df['Partner ISO'] == 'WLD') & (df['Trade Flow Code'] == 1)]
    total_world_imp = world_imports[['Year', 'Reporter ISO', 'Commodity Code', 'Trade Value (US$)']]
    total_world_imp.rename(columns={'Year': 'Year', 'Reporter ISO': 'Country ISO', 'Commodity Code': 'Commodity Code',
                                    'Trade Value (US$)': 'World Trade Value (US$)'}, inplace=True)
    stop_find_totals = time.time()
    print("found totals " + str(stop_find_totals - start_find_totals))

    # export csvs
    start_export_orig_csvs = time.time()
    total_imp_value.to_csv(str(year) + " " + str(product_code) + " " + 'total_imports.csv', index=False)
    total_world_imp.to_csv(str(year) + " " + str(product_code) + " " + 'total_world_imports.csv', index=False)
    total_exp_value.to_csv(str(year) + " " + str(product_code) + " " + 'total_exports.csv', index=False)

    merge_world_imports = total_world_imp.merge(total_imp_value, on=['Year', 'Country ISO', 'Commodity Code'])
    merge_world_imports['Difference'] = merge_world_imports['World Trade Value (US$)'] - merge_world_imports['Calculated Trade Value (US$)']
    merge_world_imports.to_csv('merge_calc_world.csv', index=False)
    total_imp_value.rename(columns={'Year': 'Year', 'Reporter ISO': 'Country ISO', 'Commodity Code': 'Commodity Code',
                                    'Calculated Trade Value (US$)': 'Import Trade Value (US$)'}, inplace=True)
    stop_export_orig_csvs = time.time()
    print("exported original csvs " + str(stop_export_orig_csvs - start_export_orig_csvs))

    # calculate normalized net exports
    start_normal_net = time.time()
    # merge imp/exp value files
    merge_imp_exp = total_imp_value.merge(total_exp_value, on=['Year', 'Country ISO', 'Commodity Code'], how='outer')
    merge_imp_exp['Difference'] = merge_imp_exp['Export Trade Value (US$)'] - merge_imp_exp['Import Trade Value (US$)']
    merge_imp_exp['Normalized Difference (Imp)'] = merge_imp_exp['Difference'] / merge_imp_exp['Import Trade Value (US$)']
    merge_imp_exp['Normalized Difference (Exp)'] = merge_imp_exp['Difference'] / merge_imp_exp['Export Trade Value (US$)']
    merge_imp_exp.to_csv('merged_imports_exports.csv', index=False)
    stop_normal_net = time.time()
    print("created normal nx column " + str(stop_normal_net - start_normal_net))

    # choose relevant data
    start_lists = time.time()
    sep_by_country = merge_imp_exp.groupby(['Year', 'Commodity Code'])['Country ISO'].apply(list)
    sep_by_imp_value = merge_imp_exp.groupby(['Year', 'Commodity Code'])['Normalized Difference (Imp)'].apply(list)
    sep_by_exp_value = merge_imp_exp.groupby(['Year', 'Commodity Code'])['Normalized Difference (Exp)'].apply(list)
    gb_country = sep_by_country[year][product_code]
    gb_value = sep_by_imp_value[year][product_code]
    #count by year, so we can say 20 expoort 10 import in addition to list of countries
    stop_lists = time.time()
    print("created lists " + str(stop_lists - start_lists))

    # drop zeroes & nans
    start_drop = time.time()
    # orig_exp_country_list = product_exports['Reporter ISO'].tolist()
    # orig_imp_country_list = product_imports['Reporter ISO'].tolist()
    # country_list = orig_exp_country_list
    # gap_list = []
    df_gb_orig_country = pd.DataFrame({'Country': gb_country, 'Normalized Export/Import Value (USD$)': gb_value})
    df_gb_orig_country_sorted = df_gb_orig_country.sort_values(by=['Normalized Export/Import Value (USD$)'], ascending=False)
    df_gb_orig_country_sorted.to_csv(str(year) + " " + str(product_code) + " " + 'Original_Country_ExportImport_Values.csv', index=False, encoding='utf-8')
    dropped = 0
    for i in range(len(gb_country)):
        true_index = i + dropped
        if gb_value[true_index] == 0:
            gb_country = gb_country[:true_index] + gb_country[true_index+1:]
            gb_value = gb_value[:true_index] + gb_value[true_index+1:]
            dropped -= 1
        elif pd.isna(gb_value[true_index]):
            gb_country = gb_country[:true_index] + gb_country[true_index+1:]
            gb_value = gb_value[:true_index] + gb_value[true_index+1:]
            dropped -= 1
    df_gb_country = pd.DataFrame({'Country': gb_country, 'Normalized Export/Import Value (USD$)': gb_value})
    df_gb_country_sorted = df_gb_country.sort_values(by=['Normalized Export/Import Value (USD$)'], ascending=False)
    df_gb_country_sorted.to_csv(str(year) + " " + str(product_code) + " " + 'Country_ExportImport_Values.csv', index=False,
                              encoding='utf-8')
    stop_drop = time.time()
    print("drop zeroes " + str(stop_drop - start_drop))

    # bar graph
    start_graph = time.time()

    df_bar_graph = pd.DataFrame({'Country': gb_country, 'Normalized (imp) Export/Import Gap (USD$)': gb_value})
    plt.figure(figsize=(20, 10))
    df_sorted = df_bar_graph.sort_values(by=['Normalized (imp) Export/Import Gap (USD$)'], ascending=False)
    sorted_country_list = df_sorted['Country']
    plt.bar('Country', 'Normalized (imp) Export/Import Gap (USD$)', data=df_sorted)

    x_pos = [i for i, _ in enumerate(sorted_country_list)]
    plt.xlabel("Country")
    plt.ylabel("Normalized (imp) Export/Import Gap (USD$)")
    plt.title(str(product_name) + ' Normalized Export/Import Gap by Country (USD$)', fontsize=7)

    plt.xticks(x_pos, sorted_country_list, rotation='vertical', fontsize=7)

    plt.savefig(str(year) + " " + str(product_code) + ' Normalized Export_Import Gap by Country (USD$)_bar_graph.png')
    stop_graph = time.time()
    print("created graphs " + str(stop_graph - start_graph))
    print("completed " + str(product_code))

    return


if __name__ == "__main__":
    product_code_list = [300215, 392620]
    product_name_list = ["Medical test kits (immunological reactions)", "Gloves, face & eye protection, protective garments"]
    years = [2020]

    for year in years:
        for product_index in range(len(product_code_list)):
            calc_price(product_code_list[product_index], product_name_list[product_index], year)
