import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Interactive Dashboards with Streamlit and Python")
st.sidebar.title("Interactive Dashboards")

st.markdown("It is an interactive dashboard developed with streamlit and python!\n\nHere we have used Indian general election results-2019 (Winning-Candidates) Data-Set for the visualization.")

st.title("Project Team")
st.markdown("Made By:\n\n UTKARSH SRIVASTAVA  -- 18BEE0016\n\nSHIVANI MISHAL --------- 18BEE0075\n\nSEJAL ANISH MANIYAR -- 18BEE0011")

st.title("Course: IOT Fundamentals (ECE3501)")
st.markdown("Faculty: Geetha Mani\n\n SELECT School\n\nVIT Vellore")



st.sidebar.title("Visualization")

DATA_URL=("2019_Results_Winning_Candidate.csv")

#can use github url

#@st.cache(persist=True)   """caching for fast loading"""
def load_data():
    data=pd.read_csv(DATA_URL)
    return data

data = load_data()
#st.write(data)

st.sidebar.subheader("Political Parties")
random_Party = st.sidebar.radio('A few from the data set', ('Bharatiya Janata Party', 'Indian National Congress', 'Samajwadi Party', 'Aam Aadmi Party'))
st.sidebar.markdown("Output")
st.sidebar.markdown(data.query("Party == @random_Party")[["Constituency", "Candidate", "Votes"]].sample(n=1))


#Total number of votes
st.sidebar.markdown("### Number of Constituency seats")
st.sidebar.markdown("Party wise")
select =st.sidebar.selectbox("Visualization Type", ['Histogram', 'Pie chart'], key='1')
constituency_count=data['Party'].value_counts()
constituency_count=pd.DataFrame({'Party':constituency_count.index,'constituencys':constituency_count.values})

##Raw data
if st.sidebar.checkbox("Raw ", False, key='0'):
    st.markdown("### Number of Constituency seats per Party")
    st.write(constituency_count)    #produces Raw data



#plotly config  Histogram and pie charts
if not st.sidebar.checkbox("Hide", True, key='1'):
    st.markdown("### Number of Seats per Party")
    if select == 'Histogram':
        fig1=px.bar(constituency_count,x='Party', y='constituencys',color='constituencys', height=500)
        st.plotly_chart(fig1)
    else:
        fig1=px.pie(constituency_count, values='constituencys', names='Party')
        st.plotly_chart(fig1)



##Indian MAP
#st.map(data)

st.sidebar.subheader("Map visualization")
map_number=st.sidebar.slider("map",0,1)
if not st.sidebar.checkbox("close", True, key='2'):
    if map_number==1:
        st.markdown("### Interactive Map")
        st.map(data)
    if st.sidebar.checkbox("Data-Table", False, key='3'):
        st.markdown("### Data Table")
        st.write(data)


st.sidebar.markdown("### Seat Compare")
st.sidebar.subheader("State wise")
#choice=st.sidebar.multiselect("pick Parties",('Indian National Congress','Yuvajana Sramika Rythu Congress Party','Telugu Desam','Bharatiya Janata Party','All India United Democratic Front','Janata Dal (United)','Lok Jan Shakti Party','Independent','Jammu & Kashmir National Conference','AJSU Party','Communist Party of India (Marxist)','Shivsena','Biju Janata Dal','Aam Aadmi Party'), key='2')
choice=st.sidebar.multiselect("pick States",('Andhra Pradesh','Andaman & Nicobar Islands','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Lakshadweep','Madhya Pradesh','Maharashtra','Odisha','Punjab','Rajasthan','Tamil Nadu','Telangana','Uttar Pradesh'), key='2')


if len(choice)>0:
    choice_data=data[data.State.isin(choice)]
    fig_choice=px.histogram(choice_data, x='State', y='Party', histfunc='count', color="Party", facet_col="Party", labels={'State':'Party'}, height=600, width=800)
    st.markdown("### State-wise compare histogram")
    st.plotly_chart(fig_choice)



st.sidebar.header('Word Cloud')
word_cloud=st.sidebar.radio('Display word cloud for:', ('Bharatiya Janata Party', 'Indian National Congress'))

if not st.sidebar.checkbox("close", True, key='4'):
    st.header('Word Cloud for %s' %(word_cloud))
    dfparty=data[data['Party']==word_cloud]
    words=' '.join(dfparty['State'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white').generate(processed_words)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
