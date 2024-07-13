import re
import pandas as pd


def preprocessor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    chats = {
        'user_message': message,
        'message_data': dates
    }
    df = pd.DataFrame(chats)

    df['message_data'] = pd.to_datetime(df['message_data'], format='%m/%d/%y, %H:%M - ')

    users = []
    messages = []

    count = 0

    for msg in df['user_message']:
        if count == 5: break
        entry = re.split('([\w\W]+?):\s', msg)

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['message_data'].dt.year
    df['month_num'] = df['message_data'].dt.month
    df['month'] = df['message_data'].dt.month_name()
    df['day'] = df['message_data'].dt.day
    df['hour'] = df['message_data'].dt.hour
    df['minute'] = df['message_data'].dt.minute
    df['only_date'] = df['message_data'].dt.date
    df['day_name'] = df['message_data'].dt.day_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df
