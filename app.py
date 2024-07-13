import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

import helper
import preprocessor

st.sidebar.title('Whatsapp chat analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = preprocessor.preprocessor(data)

    user_list = df['user'].unique().tolist()

    user_list.remove('group notification')

    user_list.sort()

    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Analysis of', user_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')

        num_messages, num_words, num_media_share, num_link = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Media Share')
            st.title(num_media_share)
        with col4:
            st.header('Link Shared')
            st.title(num_link)

        # Monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index, busy_month.values)
            st.pyplot(fig)

        # Activity HeatMap
        st.title('Weekly activity Map')
        table_heat = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots()
        ax = sns.heatmap(table_heat)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud

        st.title('WordCloud')
        df_wc = helper.create_wordCloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # Most common word
        st.title('Most Common Word')
        most_common_df = helper.most_common_word(selected_user, df)

        fig, ax = plt.subplots(figsize=(5, 5))

        ax.barh(most_common_df['message'], most_common_df['count'])
        plt.xticks(rotation='vertical')

        col1, _, col2 = st.columns([1, 0.2, 0.45])

        with col1:
            st.pyplot(fig)
        with col2:
            st.dataframe(most_common_df)

        # most used Emoji

        emoji_df = helper.emoji_helper(selected_user, df)

        # _, col_center, _ = st.columns([2, 2.5, 0.5])
        #
        # with col_center:
        st.title('Most Used Emoji')
        st.dataframe(emoji_df.head(10))
