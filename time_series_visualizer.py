import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import calendar

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df['date']=pd.to_datetime(df['date'])
# Clean data
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)

# Filter the dataset to exclude the extremes
df = df[(df['value'] > lower_bound) & (df['value'] < upper_bound)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10,6))

    ax.plot(df['date'], df['value'], label='Page Views')
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.legend()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year']=df_bar['date'].dt.year
    df_bar['month']=df_bar['date'].dt.month
    df_bar['days_in_month'] = df_bar['date'].dt.days_in_month
    df_bar = df_bar.groupby(['year','month','days_in_month'])['value'].sum().reset_index()
    df_bar['views_per_month'] = df_bar['value']/df_bar['days_in_month']
    table=df_bar.pivot(index='year',columns='month',values='views_per_month')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axes
    table.plot(kind='bar', ax=ax, width=0.6, cmap='tab10')  # Plot on the axes

    # Customizing the plot
    ax.set_xlabel('Years', fontsize=14)
    ax.set_ylabel('Average Page Views', fontsize=14)

    # Custom y-ticks
    plt.yticks(range(20000, 140000 + 1, 20000))

    # Custom legend
    ax.legend(
        title='Months',
        labels=[calendar.month_name[m] for m in table.columns],
        fontsize=12,
        title_fontsize=12,
    )

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['value'] = df_box['value'].astype(float)

    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # Year-wise Box Plot
    sns.boxplot(
        x='year',
        y='value',
        hue='year',
        data=df_box,
        ax=axes[0]
    )
    axes[0].set_title('Year-wise Box Plot (Trend)', fontsize=16)
    axes[0].set_xlabel('Year', fontsize=12)
    axes[0].set_ylabel('Page Views', fontsize=12)
    axes[0].set_yticks(range(0, 200000 + 1, 20000))  # Adjust y-ticks range
    axes[0].set_ylim(0, 200000)  # Adjust y-axis limits

    # Month-wise Box Plot
    sns.boxplot(
        x='month',
        y='value',
        hue='month',
        data=df_box,
        ax=axes[1],
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)', fontsize=16)
    axes[1].set_xlabel('Month', fontsize=12)
    axes[1].set_ylabel('Page Views', fontsize=12)
    axes[1].set_yticks(range(0, 200000 + 1, 20000))  # Adjust y-ticks range
    axes[1].set_ylim(0, 200000)  # Adjust y-axis limits


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig