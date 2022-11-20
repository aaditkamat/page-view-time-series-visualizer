import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
percentile_condition = (df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))
df = df[percentile_condition]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    ax.plot(df.index, df['value'])
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def plot_bars(df, ax):
  years = list(set(map(lambda x: x[0], df.index)))
  months = [pd.to_datetime(d, format='%Y-%m-%d').strftime("%B") for d in [f'2021-{month}-01' for month in range(1, 13)]]
  x = np.arange(len(years))
  original_width = 0.05
  differences = [- 5 * original_width + i * original_width for i in range(len(months))]
  
  heights = {}

  for month in months:
    for year in years:
      if month in heights:
          heights[month][year] = 0 if (year, month) not in df.index else df.loc[(year, month)]['value']
      else:
          heights[month] = {year: 0 if (year, month) not in df.index else df.loc[(year, month)]['value']}

  for i in range(len(differences)):
      ax.bar(x + differences[i], [heights[months[i]][year] for year in years], original_width, label=months[i])

  ax.set_xticks(x)
  ax.set_xticklabels(years)

  return ax
    
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = [d.year for d in df_bar['date']]
    df_bar['month'] = [d.strftime('%B') for d in df_bar['date']]
    df_bar = df_bar.groupby(by=[df_bar['year'], df_bar['month']]).mean()
    
    # Draw bar plot
    fig, ax = plt.subplots()
    ax = plot_bars(df_bar, ax)
    ax.legend(title='Months')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # Save image and return fig (don't change this part)
    plt.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months = [pd.to_datetime(d, format='%Y-%m-%d').strftime("%b") for d in [f'2021-{month}-01' for month in range(1, 13)]]
    
    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 9))
    sns.boxplot(data=df_box, x='year', y='value', ax=ax1)
    sns.boxplot(data=df_box, x='month', y='value', ax=ax2, order=months)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
