import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib.pyplot import title
from wordcloud import WordCloud
from calendar import TextCalendar

import preprocessor,helper  # Ensure this is your preprocessor module

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    try:
        preprocessed_data = preprocessor.preprocess(data)
        # Display the DataFrame
        st.write("Preprocessed Data Preview:")
        st.dataframe(preprocessed_data)
    except Exception as e:
        st.error(f"Error processing data: {e}")


 #fetch unique users
    user_list = preprocessed_data['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

       num_messages, words, num_media_message, num_links = helper.fetch_stats(selected_user,preprocessed_data)
       st.title("Top Statistics")
       col1, col2, col3, col4 = st.columns(4)

       with col1:
            st.header("Total Messages")
            st.title(num_messages)
       with col2:
           st.header("Total Words")
           st.title(words)
       with col3:
           st.header("Media Shared")
           st.title(num_media_message)
       with col3:
           st.header("Links Shared")
           st.title(num_links)

           # monthly timeline
       st.title("Monthly Timeline")
       timeline = helper.monthly_timeline(selected_user, preprocessed_data)
       fig, ax = plt.subplots()
       ax.plot(timeline['time'], timeline['message'], color='green')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       # daily timeline
       st.title("Daily Timeline")
       daily_timeline = helper.daily_timeline(selected_user, preprocessed_data)
       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
       # activity map
       st.title('Activity Map')
       col1, col2 = st.columns(2)

       with col1:
           st.header("Most busy day")
           busy_day = helper.week_activity_map(selected_user, preprocessed_data)
           fig, ax = plt.subplots()
           ax.bar(busy_day.index, busy_day.values, color='purple')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       with col2:
           st.header("Most busy month")
           busy_month = helper.month_activity_map(selected_user, preprocessed_data)
           fig, ax = plt.subplots()
           ax.bar(busy_month.index, busy_month.values, color='orange')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       st.title("Weekly Activity Map")
       user_heatmap = helper.activity_heatmap(selected_user, preprocessed_data)
       fig, ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)
       #finding the busiest users
       if selected_user =='Overall':
           st.title('Most Busy Users')
           x, new_df = helper.most_busy_users(preprocessed_data)
           fig, ax = plt.subplots()

           col1, col2 = st.columns(2)

           with col1:
               ax.bar(x.index, x.values,color='red')
               plt.xticks(rotation = 'vertical')
               st.pyplot(fig)
               with col2:
                   st.dataframe(new_df)
        #WordCloud
       st.title("WordCloud")
       df_wc = helper.create_wordcloud( selected_user, preprocessed_data)
       fig,ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)

       #Most Common Words

       most_common_df = helper.most_common_words(selected_user, preprocessed_data)
       fig,ax = plt.subplots()
       ax.barh(most_common_df['Word'], most_common_df['Frequency'])
       plt.xticks(rotation = 'vertical')
       st.title('Most common words')
       st.pyplot(fig)

       # Emoji analysis
       emoji_df = helper.emoji_helper(selected_user,preprocessed_data)
       st.title("Emoji Analysis")
       col1,col2 = st.columns(2)

       with col1:
           st.dataframe(emoji_df)
       with col2:
           fig,ax = plt.subplots()
           ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct='%0.2f')
       st.pyplot(fig)