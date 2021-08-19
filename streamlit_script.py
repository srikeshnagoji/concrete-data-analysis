import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import streamlit as st

st.title("Analysis of the Concrete dataset by utilizing Numpy, Pandas and Visualization techniques")
'''
## What is Concrete?

### Concrete is a composite material composed of fine and coarse aggregate bonded together with a fluid cement that hardens over time.

Components:

#### Water - Water is needed to chemically react with the cement (hydration) and too provide workability with the concrete.
#### Aggregates- Sand is the fine aggregate. Gravel or crushed stone is the coarse aggregate in most mixes.
#### Cement - The cement and water form a paste that coats the aggregate and sand in the mix. The paste hardens and binds the aggregates and sand together.
'''

'''
## Insights drawn on following aspects:

1. To which age range most of the observations in the data fall into? ​
2. Which features in our data set are more correlated? ​ ​
3. Which materials have greater effect on strength of the concrete?  
4. What effect does the usage of slag, have on the strength of the concrete as it ages? ​ ​
5. Which ratio of materials is consistent throughout the compositions observed? ​ ​
6. How can the usage of superplastic and water be correlated?​ 
7. Will the strength of concrete increases with the proportion of Ash used along with cement?​ ​ 

'''
concrete = pd.read_csv('./concrete.csv')

if st.checkbox('Show dataframe'):
    concrete

'''
## Dimentionality of the dataframe.
'''
rows,cols = concrete.shape
st.write(f'Rows: {rows}, Columns: {cols}')


# 

## Concise summary of dataframe.
concrete.info()


# # Data cleaning

# The above information indicates that the data does not have null values. 

# 
# Check if there are duplicates in the data set
total_num_of_duplicates = concrete.duplicated().agg(np.sum)
st.write(f"Number of duplicate observations in Data set to be removed: {total_num_of_duplicates}" )


# 
# Remove duplicate observations in the data set.
q = concrete.drop_duplicates(inplace=True)


# 
'''
### The number of NAN values in each column
'''
st.write(concrete.isna().sum())


# 
'''
## Statistical description of concrete dataframe.
'''
st.write(concrete.describe())

'''
# 1. To which age range most of the observations in the data fall into? ​
'''
# 
pfig = px.histogram(concrete, x='age', title='Histogram of Concrete age')
pfig.update_layout(bargap=0.2)
st.plotly_chart(pfig)

'''
# 
## The above graph indicates that, most of our data set is concentrated in the age range of 30.
'''
# 
pie = px.pie(concrete, names='age', width=500, height=500, 
labels=['Ages'], title="To what age group does the major part of the data set belong to?")
st.plotly_chart(pie)
'''
# 2. Which features in our data set are more correlated? 
'''
# 
# plot the coorelation matrix
corr_matrix = concrete.corr()

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
cax = ax.matshow(corr_matrix, vmin=-1, vmax=1)
fig.colorbar(cax)

ticks = np.arange(0, len(concrete.columns), 1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(concrete.columns)
ax.set_yticklabels(concrete.columns)

ax.set_title("Correlation matrix heat map")
st.pyplot(fig)


'''
## From the above correlation matrix, we can see that the correlation between the following features are higher:
## 1. cement and strength
## 2. strength and age
## 3. strength and superplastic

## superplastic and water have negative correlation.
'''
'''
# 3. Which materials have greater effect on strength of the concrete?
'''
# TODO: uncomment
# for col in concrete.columns:
#     if(col!='strength'):
#         scat = px.scatter(concrete, x=col, y='strength', width=600 , height=600).show()
#         st.plotly_chart(scat)


# 
# histogram of strengths
pxfig = px.histogram(concrete, x = 'strength', title = 'Histogram of Concrete Strengths')
pxfig.update_layout(bargap=0.2)
st.plotly_chart(pxfig)


# 
# plot a scatter plot - cement against strength
scat = px.scatter(concrete, x='cement', y='strength', color='strength', width=600 , height=600, title = 'Scatter plot - Cement against Strength')
st.plotly_chart(scat)

# 
# Calculate ratio between water and cement
concrete['water_cement_ratio'] = concrete.water / concrete.cement
# Calculate ratio between slag and cement
concrete['slag_cement_ratio'] = concrete.slag / concrete.cement

# plot water_cement_ratio vs strength
scat2 = px.scatter(concrete, x='water_cement_ratio', y='strength', color='slag_cement_ratio',
           title='Water/Cement Ratio vs Strength', width=700, height=600)
st.plotly_chart(scat2)
'''
## From the above plot, it is evident that,​

## 1. Lower the water to cement ratio, the stronger is the concrete. ​
## 2. The proportion of cement is a major contributor to the strength.​
'''

'''
# 4. What effect does the usage of slag, have on the strength of the concrete as it ages?
'''
# 
# Calculate water to cement ratio
concrete['water_cement_ratio'] = concrete.water / concrete.cement
'''
## Filter the data and extract those in which slag is used (non zero)
## Further filter the data to remove those samples with less composition of water. Then, plot a 3D graph of Slag vs Age vs Strength.
'''
max_water_units = st.slider('Max water units', 120, 180, 175)

scat3d = px.scatter_3d(concrete[(concrete.slag != 0) & (concrete.water < max_water_units)], x='slag', y='age', z='strength',
              color_continuous_scale=px.colors.sequential.Viridis, color='water',
              title="Slag vs Age vs Strength", width=800, height=800)
st.plotly_chart(scat3d)
'''
## The plot shows that, the usage of slag, increases strength for long term.​
## Also, the strength increases slightly as the concrete ages in the presence of water/moisture. (around 160 units)​
'''
'''
# 5. Which ratio of materials is consistent throughout the compositions observed? 
'''
# 
# Calculate the ratio of Superplastic to water
concrete['water_plastic_ratio'] = concrete.water / concrete.superplastic


# 
# 3D plot of water_plastic_ratio, water_cement_ratio and strength
scat3d2 = px.scatter_3d(concrete, x='water_plastic_ratio', y='water_cement_ratio', z='strength',
              color_continuous_scale=px.colors.sequential.Viridis, color='strength',
              title='Water to plastic ratio VS water to cement ratio VS Strength', width=800, height=800)
st.plotly_chart(scat3d2)
'''
## This plot tells us that, Water to superplastic ratio is relatively constant in our data. ​
## But, lesser the water to cement ratio, greater would be the strength of the concrete. ​
'''
'''
# 6. How can the usage of superplastic and water be correlated?​
# scatter plot of water vs superplastic
'''
scat_w_vs_sp = px.scatter(concrete[concrete.strength > 60], x='water', y='superplastic',
           color='strength', trendline='ols', title='Water vs Superplastic')
st.plotly_chart(scat_w_vs_sp)
'''
## The usage of superplastic and water are inverse in proportion. ​
## However, the strength is dependent on other compositions as well.​
'''
# ​
'''
# 7. Will the strength of concrete increases with the proportion of Ash used along with cement?​
'''
# 
concrete_1 = concrete.copy()
# calculate the ratios
# Ash to cement ratio
concrete_1['ashCementRatio'] = concrete_1.ash/concrete_1.cement
# Super plastic to cement ratio
concrete_1['superCementRatio'] = concrete_1.superplastic/concrete_1.cement

'''
## Let us extract observations from data where the ash and superplastic is used, and remove outliers
'''
maskCondition = (concrete_1.ash > 0) & (concrete_1.superplastic > 0) & (
    concrete_1.ashCementRatio < 1.1) & (concrete_1.superCementRatio < .1)

ratio_scat = px.scatter(concrete_1[maskCondition], x='ashCementRatio', y='superCementRatio', labels={"ashCementRatio": 'Ash - Cement ratio', 'superCementRatio': 'Superplastic - Cement ratio'}, color='strength', trendline='ols', title='Ash - Cement Ratio VS Super plastic - Cement Ratio',
           width=800, height=550)
st.plotly_chart(ratio_scat)
'''
## As the proportion of Ash increases in the composition, the strength declines comparatively from 60 to 30 units.​

# What proportion of the dataset has superplastic as a part of the composition?​
'''
# 
conc_copy = concrete.copy()

conc_copy['is_superPlastic_used'] = conc_copy.superplastic.apply(lambda x: "Super plastic used" if x>0 else "Super plastic not used")

pie_sp_usage = px.pie(conc_copy, names = 'is_superPlastic_used', width =400, height = 400, title="Observations showing the usage of superplastic")
st.plotly_chart(pie_sp_usage)

'''
# What is the amount of Ash used in the concrete of greater strength?

Considering strength > 60 as we want to focus on the data pertaining to higher strength.
'''
# 
df1 = concrete[concrete.strength > 60].sort_values('strength', ascending=False)


# 
pxfig = px.histogram(df1, x = 'age', title = 'Histogram of Concrete age (strength > 60 units)', width=800, height=500)
pxfig.update_layout(bargap=0.2)
st.plotly_chart(pxfig)


# 
ash_hist = px.histogram(df1.ash, title = 'Histogram of Ash in (concrete strength > 60 and age < 60)', width=700, height=700, nbins=20)
st.plotly_chart(ash_hist)

'''
## The above hostogram indicates that ash is not used extensively in the concrete of greater strength (above 60 units).

'''
