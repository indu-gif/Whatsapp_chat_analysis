import pandas as pd
from collections import Counter
from pygments.lexer import words
from pygments.styles.dracula import background
from streamlit import columns
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()

def fetch_stats(selected_user, preprocessed_data):
    if selected_user == 'Overall':
        num_messages = preprocessed_data.shape[0]

        words = []
        for message in preprocessed_data['message']:
            words.extend(message.split())

        # Count media messages in the entire dataset
        num_media_message = \
        preprocessed_data[preprocessed_data['message'].str.contains(r'<Media omitted>', na=False)].shape[0]

        links = []
        for message in preprocessed_data['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_message,len(links)
    else:
        # Filter by the selected user
        new_df = preprocessed_data[preprocessed_data['user'] == selected_user]
        num_messages = new_df.shape[0]

        words = []
        for message in new_df['message']:
            words.extend(message.split())

        # Count media messages only in the filtered dataframe (new_df)
        num_media_message = new_df['message'].str.contains(r'<Media omitted>', na=False).sum()

        links = []
        for message in new_df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_message,len(links)


def most_busy_users(preprocessed_data):
    x = preprocessed_data['user'].value_counts().head()
    preprocessed_data = round((preprocessed_data['user'].value_counts()/ preprocessed_data.shape[0])*100, 2).reset_index().rename(columns = {'index':'name ', 'user':'percent'})
    return x, preprocessed_data


def create_wordcloud(selected_user, preprocessed_data):

    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().splitlines())


    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[(preprocessed_data['user'] == selected_user) &
                                 (preprocessed_data['user'] != 'group_notification')]


    temp = temp[temp['message'] != '<media omitted>\n'] 


    combined_text = ' '.join(message for message in temp['message'] if message not in stop_words)


    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white', stopwords=stop_words)
    df_wc = wc.generate(combined_text)

    return df_wc

def most_common_words(selected_user,preprocessed_data):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    # Filter data based on user
    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[(preprocessed_data['user'] == selected_user) &
                                 (preprocessed_data['user'] != 'group_notification')]
    temp = temp[temp['message'] != '<media omitted>\n']
    words = []
    for message in temp['message']:
        cleaned_message = message.lower().replace(':', '').replace('<media omitted>', '')
        for word in cleaned_message.split():
            if word not in stop_words:
                words.append(word)

    if words:
        most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    else:
        most_common_df = pd.DataFrame(columns=['Word', 'Frequency'])


    return most_common_df


def emoji_helper(selected_user, preprocessed_data):
    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[preprocessed_data['user'] == selected_user]

    emojis = []
    for message in temp['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def monthly_timeline(selected_user,preprocessed_data):
    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[preprocessed_data['user'] == selected_user]

    timeline = preprocessed_data.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,preprocessed_data):
    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[preprocessed_data['user'] == selected_user]



    daily_timeline = preprocessed_data.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,preprocessed_data):

    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[preprocessed_data['user'] == selected_user]


    return preprocessed_data['day_name'].value_counts()

def month_activity_map(selected_user,preprocessed_data):
    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[preprocessed_data['user'] == selected_user]

    return preprocessed_data['month'].value_counts()

def activity_heatmap(selected_user, preprocessed_data):
    if selected_user == 'Overall':
        temp = preprocessed_data[preprocessed_data['user'] != 'group_notification']
    else:
        temp = preprocessed_data[preprocessed_data['user'] == selected_user]

    # Use 'temp' instead of 'preprocessed_data' here
    user_heatmap = temp.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
