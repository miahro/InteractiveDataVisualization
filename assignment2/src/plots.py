"""Module for plotting functions"""

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from data_cleaning import drop_column
from config import RES_X, RES_Y


def plot_bar_charts_mult(df, title=None, col_type=None, ncols=4):
    """Plots multiple bar charts for the given dataframe."""

    if 'Work hours per week' in df.columns:
        df = drop_column(df, 'Work hours per week')
    if col_type == 'categorical':
        cols = df.select_dtypes(include=['object']).columns
    elif col_type == 'numerical':
        cols = df.select_dtypes(include=['int64']).columns
    else:
        cols = df.columns
    subplot_titles = [f"{col}" for col in cols]

    num_plots = len(cols)
    num_cols = ncols
    num_rows = num_plots // num_cols if num_plots % num_cols == 0 else num_plots // num_cols + 1
    subplot_width = RES_X // num_cols
    subplot_height = RES_Y // num_rows

    fig = make_subplots(rows=num_rows, cols=num_cols,
                        subplot_titles=subplot_titles)

    for i, col in enumerate(cols, start=1):
        counts = df[col].value_counts().reset_index()
        counts.columns = [col, 'Count']
        fig.add_trace(go.Bar(x=counts[col], y=counts['Count'], name=col), row=(
            i-1)//num_cols+1, col=(i-1) % num_cols+1)

    fig.update_layout(
        height=subplot_height*num_rows,
        width=subplot_width*num_cols,
        title=dict(text=title, x=0.5, font=dict(size=24, color='black')),
        showlegend=False
    )

    fig.update_xaxes(tickangle=35)
    fig.show()


def plot_polar_barplots(df, num_var, cat_vars, title=None):
    """Plots polar bar plots for the given dataframe."""
    fig = go.Figure()

    for i, cat_var in enumerate(cat_vars):
        df[cat_var] = df[cat_var].replace('?', cat_var + ' Undefined')
        means = df.groupby(cat_var, observed=True)[num_var].mean()
        print(cat_var)
        if cat_var not in ('Level of education', 'Age'):
            means = means.sort_values(ascending=True)

        fig.add_trace(go.Barpolar(
            r=means.values,
            theta=means.index,
            name=cat_var,
            marker_color=px.colors.qualitative.Plotly[i % len(
                px.colors.qualitative.Plotly)]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, df[num_var].mean()+10]
            ),
            angularaxis=dict(tickangle=0),
            hole=0.2
        ),
        title=dict(text=title, x=0.5, font=dict(size=24, color='black')),
        showlegend=True,
        legend=dict(x=0.2, y=0)
    )

    fig.show()


def plot_barplots_all(df, num_var, cat_vars, cols=3):
    """Plots bar plots for the given dataframe."""

    total = len(cat_vars)
    rows = total // cols if total % cols == 0 else total // cols + 1
    subplot_width = RES_X // cols
    subplot_height = RES_Y // rows

    total = len(cat_vars)
    cols = 3
    rows = total // cols if total % cols == 0 else total // cols + 1

    subplot_titles = [f'Mean {num_var} by {cat_var}' for cat_var in cat_vars]

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles)

    for i, cat_var in enumerate(cat_vars):
        means = df.groupby(cat_var, observed=True)[num_var].mean()
        if cat_var not in ('Level of education', 'Age'):
            means = means.sort_values(ascending=True)
        row = i // cols + 1
        col = i % cols + 1

        if cat_var == 'Level of education':
            means.index = means.index.astype(str)

        fig.add_trace(
            go.Bar(x=means.index, y=means.values, name=cat_var),
            row=row,
            col=col
        )
        fig.update_layout(
            height=subplot_height*rows,
            width=subplot_width*cols,
            title=dict(text=f'Mean {num_var} by category',
                       x=0.5, font=dict(size=24, color='black')),
            showlegend=False
        )
    fig.show()


def plot_barplots_two(df1, df2, num_var, cat_vars, df1_name, df2_name, split_title,
                      bar_color='blue', bar_color1='red', cols=3):
    """Plots bar plots for two given dataframes."""
    total = len(cat_vars)
    rows = total // cols if total % cols == 0 else total // cols + 1
    subplot_width = RES_X // cols
    subplot_height = RES_Y // rows

    y_max = 60

    subplot_titles = [f'Mean {num_var} by {cat_var}' for cat_var in cat_vars]

    fig = make_subplots(rows=rows, cols=cols,
                        subplot_titles=subplot_titles)

    for i, cat_var in enumerate(cat_vars):
        means1 = df1.groupby(cat_var, observed=True)[num_var].mean()
        means2 = df2.groupby(cat_var, observed=True)[num_var].mean()

        if cat_var not in ('Level of education', 'Age'):
            means1 = means1.sort_values(ascending=True)
            means2 = means2.sort_values(ascending=True)

        row = i // cols + 1
        col = i % cols + 1

        if cat_var == 'Level of education':
            means1.index = means1.index.astype(str)
            means2.index = means2.index.astype(str)

        fig.add_trace(
            go.Bar(x=means1.index, y=means1.values,
                   name=df1_name, marker_color=bar_color, showlegend=i == 0),
            row=row,
            col=col
        )

        fig.add_trace(
            go.Bar(x=means2.index, y=means2.values,
                   name=df2_name, marker_color=bar_color1, showlegend=i == 0),
            row=row,
            col=col
        )
    y_range = [0, y_max]
    fig.update_yaxes(range=y_range)
    fig.update_layout(
        height=subplot_height*rows,
        width=subplot_width*cols,
        title=dict(
            text=(
                f'Mean {num_var} by category split by {split_title} : '
                f'{df1_name} (n={df1.shape[0]}) vs {df2_name} (n={df2.shape[0]})'
            ),
            x=0.5,
            font=dict(size=24, color='black')
        ),
        showlegend=True
    )
    fig.show()
