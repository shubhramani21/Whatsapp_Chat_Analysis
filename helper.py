from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_word = len(words)

    num_media_share = df[df['message'] == '<Media omitted>\n'].shape[0]

    link = []
    for msg in df['message']:
        link.extend(extractor.find_urls(msg))

    num_link = len(link)

    return num_messages, num_word, num_media_share, num_link


def most_busy_user(df):
    x = df['user'].value_counts().head(15)
    df = round(((df.user.value_counts() / df.shape[0]) * 100), 2).reset_index()

    df.rename(columns={'count': 'percent'}, inplace=True)

    return x, df


def create_wordCloud(selected_user, df):
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['user'] != 'group notification']

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []
    for message in df.message:
        words.extend(message.split())

    links = []
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))

    clean = []
    for word in words:
        if word not in links:
            clean.append(word)

    long_string = ' '.join(clean)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(long_string)
    return df_wc


def most_common_word(selected_user, df):
    f = open('stop_hinglish.txt', 'r')

    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['message', 'count'])

    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emoji_list = []
    for message in df['message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))), columns=['Emoji', 'counts'])

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline_df = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline_df


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    table_heat = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return table_heat
