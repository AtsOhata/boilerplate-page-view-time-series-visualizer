import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Clean data
df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))
    ]


def draw_line_plot():
    # Draw line plot
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['value'], marker='o', linestyle='-', color='b', label='value')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date') 
    plt.ylabel('Page Views')
    plt.tight_layout()
    fig = plt.gcf()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = [d.year for d in df_bar.date]
    df_bar['month'] = [d.strftime('%b') for d in df_bar.date]
    df_avg = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    df_avg.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=[calendar.month_name[i] for i in range(1, 13)])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box_year = df_box.copy()
    df_box_year.reset_index(inplace=True)
    df_box_year['year'] = df_box_year['date'].dt.year
    df_box_year['month'] = df_box_year['date'].dt.month_name()
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
    sns.boxplot(x='year', y='value', data=df_box_year, ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')

    df_box_month = df_box.copy()
    df_box_month.reset_index(inplace=True)
    month_order = calendar.month_abbr[1:]
    sns.boxplot(x='month', y='value', data=df_box_month, order=month_order, ax=ax[1])
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
