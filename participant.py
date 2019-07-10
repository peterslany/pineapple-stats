import emoji
import datetime


class Content():
    def __init__(self, content):
        self.type = content
        self.total = 0
        self.period ={ 'year' : {}, 'month' : {}, 'week_number' : {},
                      'month_day' : {}, 'week_day' : {}, 'hour' : {}, 
                      'date' : {}, 'year-week_number' : {}}

    def add_entry(self, timestamp, multiple_entries=0, datetime_object=False):
        """Adds time entries to given type of content.
        """

        # Converts timestamp to format without miliseconds
        
        if multiple_entries:
            count = multiple_entries
        else:
            count = 1
        self.total += count
        if not datetime_object:
            timestamp = int(str(timestamp)[:-3])
            time = datetime.datetime.fromtimestamp(timestamp)
        else:
            time = timestamp
        time = time.strftime("%Y %B %W %d %A %H %d/%m/%y %Y:%W").split(' ')
        for interval in self.period:
            x = time.pop(0)
            self.period[interval][x] = self.period[interval].get(x, 0) + count

        



class Participant():
    def __init__(self, name):
        self.name = name
        self.content = {'photos' : Content('photos'), 'videos' : Content('videos'),
                      'audio_files' : Content('audio_files'), 
                      'gifs' : Content('gifs'), 'sticker' : Content('sticker'),
                      'share' : Content('share'),'reactions' : Content('reactions'),
                      'messages' : Content('reactions'), 'words' : Content('words'), 
                      'emojis' : Content('emojis'), 'swearing' : Content('swearing')}
        self.most_common_words = {}

    def add_message(self, message):
        """Analyses given message.
        """
        timestamp = message['timestamp_ms']
        for item in['photos', 'videos', 'gifs', 'share', 'audio_files', 'sticker']:
            if item in message:
                self.content[item].add_entry(timestamp)
                self.content['words'].total -= 4
        if 'reactions' in message:
            self.content['reactions'].add_entry(timestamp,len(message['reactions']))

        # If you want to get statistics of swearings, put the words as strings
        # into the list swearings
        swearings = []
        if 'content' in message:
            self.content['messages'].add_entry(timestamp)
            text = message['content']
            self.content['words'].add_entry(timestamp, len(text.split(' ')))
            if emoji.emoji_count(text):
                self.content['emojis'].add_entry(timestamp, emoji.emoji_count(text))
            for vulgarism in swearings:
                if vulgarism in text.lower():
                    self.content['swearing'].add_entry(timestamp)

    