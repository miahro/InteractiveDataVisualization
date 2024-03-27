"""Main program to run the data cleaning and visualization."""

from data_cleaning import read_data, drop_column, drop_row, \
    count_non_zero, explore_data, convert_age_to_categorical, drop_rows
from plots import plot_bar_charts_mult, plot_polar_barplots, plot_barplots_two
from config import FREQUENCY_THRESHOLD


def main():
    """main function to run the data cleaning and visualization."""
    data = read_data()
    explore_data(data)
    print(
        f'Non-zero values for Capital gain {count_non_zero(data, "Capital gain")}')
    print(
        f'Non-zero values for Capital loss {count_non_zero(data, "Capital loss")}')
    data = drop_column(data, 'Capital gain')
    data = drop_column(data, 'Capital loss')

    plot_bar_charts_mult(
        data,
        title=f"Frequency of all variables for data pre-processing (n = {data.shape[0]})",
        ncols=4)

    data = drop_column(data, 'Native country')
    data = drop_column(data, 'Work class')
    data = convert_age_to_categorical(data)

    plot_bar_charts_mult(
        data,
        title=f"Frequency of categorical variables for data pre-processing after dropping"
        f"Native country and Work class (n = {data.shape[0]})",
        col_type=None,
        ncols=3)

    data = drop_row(data, 'Marital status', 'Married spouse in armed forces')
    data = drop_row(data, 'Occupation', 'Armed-Forces')
    data = drop_row(data, 'Occupation', 'Priv-house-serv')
    data = drop_row(data, 'Race', 'Amer-Indian-Eskimo')
    data = drop_row(data, 'Race', 'Other')

    explore_data(data)

    cat_vars = ['Occupation', 'Age', 'Marital status', 'Level of education',
                'Relationship', 'Race', 'Sex', 'Annual income']

    data_filtered = drop_rows(data, cat_vars, FREQUENCY_THRESHOLD)

    plot_polar_barplots(data_filtered, 'Work hours per week', cat_vars,
                        title=f'Mean work hours per week by category (n={data_filtered.shape[0]})')

    poor_filt = data['Annual income'] == '<=50K'
    rich_filt = data['Annual income'] == '>50K'
    data_poor = data[poor_filt]
    data_poor = drop_rows(data_poor, cat_vars, FREQUENCY_THRESHOLD)
    data_rich = data[rich_filt]
    data_rich = drop_rows(data_rich, cat_vars, FREQUENCY_THRESHOLD)

    cat_vars = [
        'Annual income',
        'Sex',
        'Race',
        'Age',
        'Occupation',
        'Level of education',
    ]

    plot_barplots_two(data_poor, data_rich, 'Work hours per week', cat_vars,
                      '<=50K', '>50K', split_title='annual income',
                      bar_color='brown', bar_color1='orange')
    male_filt = data['Sex'] == 'Male'
    female_filt = data['Sex'] == 'Female'
    white_filt = data['Race'] == 'White'
    black_filt = data['Race'] == 'Black'
    poor_filt = data['Annual income'] == '<=50K'
    rich_filt = data['Annual income'] == '>50K'

    data_male = data[male_filt]
    data_male = drop_rows(data_male, cat_vars, FREQUENCY_THRESHOLD)
    data_female = data[female_filt]
    data_female = drop_rows(data_female, cat_vars, FREQUENCY_THRESHOLD)
    cat_vars = [
        'Annual income',
        'Sex',
        'Race',
        'Age',
        'Occupation',
        'Level of education',
    ]

    plot_barplots_two(
        data_male,
        data_female,
        'Work hours per week',
        cat_vars,
        "Male",
        "Female",
        split_title='sex',
        bar_color='green',
        bar_color1='purple')

    data_black = data[black_filt]
    data_black = drop_rows(data_black, cat_vars, FREQUENCY_THRESHOLD)
    data_white = data[white_filt]
    data_white = drop_rows(data_white, cat_vars, FREQUENCY_THRESHOLD)

    cat_vars = [
        'Annual income',
        'Sex',
        'Race',
        'Age',
        'Occupation',
        'Level of education',
    ]
    plot_barplots_two(
        data_white,
        data_black,
        'Work hours per week',
        cat_vars,
        "White",
        "Black",
        split_title='race',
        bar_color='blue',
        bar_color1='red',
        cols=3)


if __name__ == "__main__":
    main()
