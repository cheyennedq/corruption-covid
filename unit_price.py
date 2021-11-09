import merge

<<<<<<< HEAD
import numpy

import matplotlib.pyplot as plt

=======
>>>>>>> 716bda3c70f992fd4c57b6718482b0e2e6235673

def calc_price(df, row_number, product_code, total_trade_dict):
    imp_exp_dict = {}
    for i in range(row_number):
        # temporarily only include World as a partner, year 2020
        if df.iloc[i, 1] == 2020 and df.iloc[i, 12] == "World" and df.iloc[i, 21] == product_code:
            # create dictionary of import & export values per country {'country': {M: $imp, X: $exp, ...]}
            # if partner is not already in the dictionary, add it
            if df.iloc[i, 9] not in imp_exp_dict:
                # temporarily only include imports & exports
                imp_exp_dict[df.iloc[i, 9]] = {'M': 0, 'X': 0}
            # calculation of average price: avg_price_1*prop(trade_value_1/total_trade)
            #   final result is a weighted sum: avg_price_1*prop(trade_value_1/total_trade)
            #   + avg_price_2*prop(trade_value_2/total_trade) + ... + avg_price_n*prop(trade_value_n/total trade)
            average_price = (df.iloc[i, 31] / df.iloc[i, 25]) * (
                        df.iloc[i, 31] / total_trade_dict[df.iloc[i, 9]][product_code]['total'])
            # index by country, then by M or X depending on the trade flow
            if "m" in df.iloc[i, 7].lower() and "r" not in df.iloc[i, 7].lower():
                average_price = (df.iloc[i, 31] / df.iloc[i, 25]) * (df.iloc[i, 31] / total_trade_dict[df.iloc[i, 9]][product_code]['total_m'])
                imp_exp_dict[df.iloc[i, 9]]['M'] += average_price
            elif "x" in df.iloc[i, 7].lower() and "r" not in df.iloc[i, 7].lower():
                average_price = (df.iloc[i, 31] / df.iloc[i, 25]) * (df.iloc[i, 31] / total_trade_dict[df.iloc[i, 9]][product_code]['total_x'])
                imp_exp_dict[df.iloc[i, 9]]['X'] += average_price
            # price dict {'country': {'M': weighted_price_imp, 'X': weighted_price_exp}} (return)
    for key in imp_exp_dict.keys():
        imp_exp_dict[key]['D'] = imp_exp_dict[key]['X'] - imp_exp_dict[key]['M']
    return imp_exp_dict


def total_trade(df, row_number):
    """
    calculates the total amount of money traded (combining exports & imports)
    :param df: dataframe containing UN Comtrade data
    :param row_number: number of rows in the data frame
    :return: dictionary of country-product-value triplets
    """
    total_trade_dict = {}
    # {'country': {'product_1': {'total': tv_1, 'M': num, 'X': num}, 'product_2': tv_2, ...}
    for i in range(row_number):
        # country not in dict
        if df.iloc[i, 9] not in total_trade_dict:
            total_trade_dict[df.iloc[i, 9]] = {}
        # product not in subdict
        if df.iloc[i, 21] not in total_trade_dict[df.iloc[i, 9]]:
            total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]] = {'total': 0, 'total_m': 0, 'total_x': 0}
        # add the total trade value
        total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]]['total'] += df.iloc[i, 31]
        # add the import/export value
        if "m" in df.iloc[i, 7].lower() and "r" not in df.iloc[i, 7].lower():
            total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]]['total_m'] += df.iloc[i, 31]
        elif "x" in df.iloc[i, 7].lower() and "r" not in df.iloc[i, 7].lower():
            total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]]['total_x'] += df.iloc[i, 31]
    return total_trade_dict


# create dictionary of country-price pairs for histogram
<<<<<<< HEAD
def price_histogram(cp_dict, product):
    first_edge = 0
    last_edge = 0
    bins = 20
    bin_edges = numpy.linspace(start=first_edge, stop=last_edge, num=bins+1, endpoint=True)
    # import, export, difference histograms
    # bin_counter = numpy.bincount(df, range=(0, df.max*()))
    return


def price_bar(cp_dict, product):
    # bar graph
    difference = []
    exp = []
    imp = []
    plt.style.use('ggplot')
    countries = list(cp_dict.keys())
    for country in countries:
        difference.append(cp_dict[country]['D'])
        exp.append(cp_dict[country]['X'])
        imp.append(cp_dict[country]['M'])
    x_pos = [i for i, _ in enumerate(countries)]
    plt.bar(x_pos, difference, color='green')
    plt.xlabel("Country")
    plt.ylabel("Difference between export & import value")
    plt.title("Export/import price difference by country for " + str(product))

    plt.xticks(x_pos, countries)

    plt.savefig(str(product) + '_bar_graph.png', dpi=400)
    plt.show()

    # scatter plot
    plt.scatter(difference, numpy.log10(imp))
    plt.savefig(str(product) + '_scatter_imp.png', dpi=400)
    plt.show()

    plt.scatter(difference, numpy.log10(exp))
    plt.savefig(str(product) + '_scatter_exp.png', dpi=400)
    plt.show()
=======


def price_histogram(df, product):
>>>>>>> 716bda3c70f992fd4c57b6718482b0e2e6235673
    return


if __name__ == "__main__":
    product_code_list = [900490, 841920, 5603, 300215, 382200, 382100, 902780, 220710, 220890, 380894, 280440, 901920,
                         300220, 392620, 401511, 621010, 481850, 9020, 90200]
    # if in the dataframe, loop over otherwise skip
    merged_df = merge.merge_files()
    print("merged files")
    rows = len(merged_df)
    print("counted rows")
    tt_product = total_trade(merged_df, rows)
    print("constructed total trade dictionary")
    print(tt_product)
    for product in product_code_list:
        product_dict = calc_price(merged_df, rows, product, tt_product)
        print(product)
        print(product_dict)
<<<<<<< HEAD
        price_bar(product_dict, product)
        print(product + "bar chart completed")
=======
>>>>>>> 716bda3c70f992fd4c57b6718482b0e2e6235673
