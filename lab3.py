import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import altair_catplot as altcat

########## Setup ##########
st.title("Lab 3 - Ethics in Data Visualization")
# st.markdown("##### By: Taylor Keckley")

df = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")

st.markdown("#### Dataset used in this analysis:")
countries = df['Country\year']
years = df.columns.difference(['Country\year','Non-OECD Economies'])
df[years] = df[years].apply(pd.to_numeric, errors='coerce')
df
df.drop(columns=['Non-OECD Economies'], inplace=True)


########## Part 1 ##########
st.markdown("## Part 1: Honest")
with st.echo():
    # Making a dataframe so each country/year pair 
    # has its own row (more compatible with altair)
    df2 = pd.melt(df, id_vars=['Country\year'], var_name='Year', value_name="Emissions")
    df2.rename({'Country\year': 'Country'}, axis=1, inplace=True)

    # Add a multiselect list for countries
    options = st.multiselect("Select/Deselect Countries", countries, countries, key="heatmapHonest")
    data = df2.loc[df2['Country'].isin(options)]

    # Plot interactive heatmap of data
    chart = alt.Chart(data, title="Tons of CO\u2082 Emissions by Country and Year").mark_rect(stroke="white").encode(
        alt.X('Year:N'),
        alt.Y('Country:N', sort=alt.EncodingSortField(field='Emissions', order='descending')),
        alt.Color('Emissions:Q', title="Emissions (tons of CO2)"),
        tooltip=[
            alt.Tooltip('Country:N', title='Country'),
            alt.Tooltip('Year:N', title='Year'),
            alt.Tooltip("Emissions:Q", title='Emissions (tons of CO2)', format=",")
        ]
    ).properties(
        width=1000,
        height=700
    )
    chart

st.markdown("**Chart Caption:**")
'''This heatmap shows CO\u2082 emissions (in tons) by country and year, where blank spaces indicate missing data. 
It is sorted with the top CO\u2082 emission producing countries at the top. Above the chart is a multiselect list 
where you can select and deselect subsets of countries to view in the chart. The chart is also interactive 
so you can hover over an area to see the specific amount of CO\u2082 emissions produced by a specific country 
during a specific year. '''

st.markdown("**Commentary:**")
'''I would say this plot is the better of the two presented.
- Pros
    - It is not too difficult to tell relative differences in emissions between countries (lighter color = lower emissions, darker color=higher emissions).
    - The sorting of the y-axis is helpful when the data has outliers that make many countries look the same.
    - The subsetting allows you to remove outliers or just see trends in a small group of countries.
- Cons
    - It can be hard to see the scale of emissions because of the continuous colormap and the wide range of emissions in the data (the interactivity helps with this).
'''


########## Part 2 ##########
st.markdown("## Part 2: Dishonest") 
"Assuming code would not be visible, so viewers would not have any information except what can be seen on the graph."
with st.echo():
    # Transform emissions by taking the log base 2 
    df2['Emissions_log2'] = np.log(df2['Emissions'])

    # Plot heatmap of data
    chart = alt.Chart(df2).mark_rect().encode(
        alt.X('Year:N', sort="descending", title=""),
        alt.Y('Country:N', title=""),
        alt.Color('Emissions_log2:Q', title="Emissions", scale=alt.Scale(scheme='rainbow'))
    ).properties(
        width=900,
        height=700
    )

    # Fill in missing values
    nulls = chart.transform_filter(
        "!isValid(datum.Emissions)"
    ).mark_rect(opacity=0.5).encode(
        alt.Color('Emissions:N', scale=alt.Scale(scheme='rainbow'), legend=None)
    )
    chart + nulls

st.markdown("**Chart Caption:**")
"\*Blank\*"

st.markdown("**Commentary:**")
'''This chart is by far the worse of the two options, and can be very misleading.
- Potentially Misleading Factors:
    - No caption describing chart in any way.
    - Missing values are colored in but not mentioend in the caption or legend. 
    - The legend doesn't show scale of emissions (log tons of CO2). 
    - There are no lines separating the entries which makes it more difficult to find emissions from a particular country during a particular year. 
    - The color palette is confusing because it is not intuitive for ordered data like this. Lighter colors do not match up with lower emissions and darker colors don't only match up with higher emissions, in fact the color for the highest and lowest emissions is very similar if not the same. This is made worse by the fact that there is no interactivity to see exact values. 
    - The years are in reverse order on the x-axis.
    - There was a log transformation applied to emissions but it was never mentioned.
    - There is no option to subset the data in order to see some of the smaller values. 
Overall it is hard to see most trends and relative differences in the data because of these factors.
'''


########## Extra ##########
st.markdown("## Extra") 

"**Altair Boxplot**"
with st.echo():
    options = st.multiselect("Select/Deselect Countries", countries, ('OECD - Total', 'OECD America', 'OECD - Europe', 'European Union (28 countries)'), key="catplot")
    data = df2.loc[df2['Country'].isin(options)]

    cat = altcat.catplot(data,
                height=500,
                width=700,
                mark='point',
                box_mark=dict(strokeWidth=2, opacity=0.6),
                whisker_mark=dict(strokeWidth=2, opacity=0.9),
                encoding=dict(x=alt.X('Country:N', title="Country"),
                            y=alt.Y('Emissions:Q', title="Emissions (tons of CO\u2082)"),
                            color=alt.Color('Country:N', legend=None)),
                transform="jitterbox", jitter_width=0.5)
    cat


"**Seaborn Swarmplots**"
with st.echo():
    ### Seaborn Swarmplots
    df_data_sorted = df.sort_values(by=['2019'], ascending=False)
    df_data_sorted = df_data_sorted[df_data_sorted['Country\year'] != 'OECD - Total']
    top_5_countries = df_data_sorted.head(5)['Country\year']
    data = df2[df2['Country'].isin(top_5_countries)]

    fig, ax = plt.subplots(figsize=(9, 6), dpi = 50)
    ax.grid(alpha = 0.3)
    ax.set_axisbelow(True) 
    ax = sns.boxplot(x="Country", y="Emissions", data=data, boxprops=dict(alpha=.7))
    ax = sns.swarmplot(x="Country", y="Emissions", data=data, color=".2", size = 5)

    ax.set_xlabel('Country / Region')
    ax.set_ylabel('Emissions (tons of CO\u2082)')
    xaxis = plt.xticks(rotation=0, ha='center', fontsize=8)
    yaxis = plt.yticks(fontsize=8)
    ax.set_title("Top 5 CO\u2082 Emission Producing Countries & Regions")

    st.pyplot(fig)


df_data_sorted = df.sort_values(by=['2019'], ascending=True)
bottom_5_countries = df_data_sorted.head(5)['Country\year']
data = df2[df2['Country'].isin(bottom_5_countries)]

fig, ax = plt.subplots(figsize=(9, 6), dpi = 50)
ax.grid(alpha = 0.3)
ax.set_axisbelow(True) 
ax = sns.boxplot(x="Country", y="Emissions", data=data, boxprops=dict(alpha=.7))
ax = sns.swarmplot(x="Country", y="Emissions", data=data, color=".2", size = 5)

ax.set_xlabel('Country / Region')
ax.set_ylabel('Emissions (tons of CO\u2082)')
xaxis = plt.xticks(rotation=0, ha='center', fontsize=8)
yaxis = plt.yticks(fontsize=8)
ax.set_title("Bottom 5 CO\u2082 Emission Producing Countries & Regions")
st.pyplot(fig)


df_data_sorted = df.sort_values(by=['2019'], ascending=True)
bottom_2_countries = df_data_sorted.head(2)['Country\year']
data = df2[df2['Country'].isin(bottom_2_countries)]

fig, ax = plt.subplots(figsize=(9, 6), dpi = 50)
ax.grid(alpha = 0.3)
ax.set_axisbelow(True) 
ax = sns.boxplot(x="Country", y="Emissions", data=data, boxprops=dict(alpha=.7))
ax = sns.swarmplot(x="Country", y="Emissions", data=data, color=".2", size = 5)

ax.set_xlabel('Country / Region')
ax.set_ylabel('Emissions (tons of CO\u2082)')
ax.set(ylim=(0, 275))
xaxis = plt.xticks(rotation=0, ha='center', fontsize=8)
yaxis = plt.yticks(fontsize=8)
ax.set_title("Bottom 2 CO\u2082 Emission Producing Countries & Regions")
st.pyplot(fig)


'''These plots are helpful in showing emissions for some of the top and bottom countries and regions.
They give a closer view so you can see the range of emissions values for individual countries like Liechtenstein
and Monaco which appear to have almost 0 emissions when in plots with larger countries. The altair plot is also helpful
because it allows you to choose the countries you want to look at.'''