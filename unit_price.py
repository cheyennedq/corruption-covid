import merge


def calc_price(df, row_number, product_code, total_trade_dict):
    imp_exp_dict = {}
    for i in range(row_number):
        print(df.iloc[i, 9])
        # temporarily only include World as a partner, year 2020
        if df.iloc[i, 1] == 2020 & df.iloc[i, 12] == "World" & df.iloc[i, 21] == product_code:
            # create dictionary of import & export values per country {'country': {M: $imp, X: $exp, ...]}
            # if partner is not already in the dictionary, add it
            if df.iloc[i, 9] not in imp_exp_dict:
                # temporarily only include imports & exports
                imp_exp_dict[df.iloc[i, 9]] = {"M": 0, "X": 0}
            # calculation of average price: avg_price_1*prop(trade_value_1/total_trade)
            #   final result is a weighted sum: avg_price_1*prop(trade_value_1/total_trade)
            #   + avg_price_2*prop(trade_value_2/total_trade) + ... + avg_price_n*prop(trade_value_n/total trade)
            average_price = (df.iloc[i, 31] / df.iloc[i, 25]) * (
                        df.iloc[i, 31] / total_trade_dict[df.iloc[i, 9]][product_code])
            # index by country, then by M or X depending on the trade flow
            if df.iloc[i, 7].contains("M") | df.iloc[i, 7].contains("X"):
                imp_exp_dict[df.iloc[i, 9]][df.iloc[i, 7]] += average_price
            # price dict {'country': weighted_price} (return)
    return imp_exp_dict


def total_trade(df, row_number):
    """
    calculates the total amount of money traded (combining exports & imports)
    :param df: dataframe containing UN Comtrade data
    :param row_number: number of rows in the data frame
    :return: dictionary of country-product-value triplets
    """
    total_trade_dict = {}
    # {'country': {'product_1': tv_1, 'product_2': tv_2, ...}
    for i in range(row_number):
        # country not in dict
        if df.iloc[i, 9] not in total_trade_dict:
            total_trade_dict[df.iloc[i, 9]] = {}
        # product not in subdict
        if df.iloc[i, 21] not in total_trade_dict[df.iloc[i, 9]]:
            total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]] = {'total': 0, 'M': 0, 'X': 0}
        # add the trade value
        total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]]['total'] += df.iloc[i, 31]
        # increment M & X counter
        if df.iloc[i, 7].contains("M") | df.iloc[i, 7].contains("X"):
            total_trade_dict[df.iloc[i, 9]][df.iloc[i, 21]][df.loc[df.iloc[i, 7]]] += 1
    return total_trade_dict


# create dictionary of country-price pairs for histogram


def price_histogram():
    return


if __name__ == "__main__":
    product_code_list = [900490, 841920, 5603, 300215, 382200, 382100, 902780, 220710, 220890, 380894, 280440, 901920,
                         300220, 392620, 401511, 621010, 481850, 9020, 90200]
    # if in the dataframe, loop over otherwise skip
    merged_df = merge.merge_files()
    rows = len(merged_df)
    tt_product = total_trade(merged_df, rows)
    print(tt_product)
    for product in product_code_list:
        print(calc_price(merged_df, rows, product, tt_product))
        print(product)
