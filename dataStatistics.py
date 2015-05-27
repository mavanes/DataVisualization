import math, datetime, time
from pymongo import MongoClient

client = MongoClient()
db = client['big_data']
exclusions = ['the', 'a' , 'and', 'of', 'on', 'in', 'to', 'one', 'with', 
              'some', 'is', 'his', 'her', 'for', 'by', 'us', 'more', 'at', 
              'as', 'she', 'he', 'you', 'from', 'few', 'this', 'was', 'an',
              'that', '', '&', 'my', '|', 'here', 'all']

for x in range(0, 100):
    exclusions.append(str(x))
    
replaced = ["\n", ",", ".", "'", '"', "!", "(", ")", ":", ";", "*", "@", 
            "/", "\\", '[', ']', "-", "#"]

def convert_to_datetime(timestamp):
    print timestamp
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def convert_to_timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())

def word_count_yt(text):
    words = {}
    youtube = db.youtube
    for video in youtube.find():
        words_list = video["snippet"][text]
        for r in replaced:
            words_list = words_list.replace(r, "")
        words_list = words_list.replace("_", " ")
        words_list = words_list.lower().split(" ")
        for w in words_list:
            if w not in exclusions:
                if w in words:
                    words[w] = words[w] + 1
                else:
                    words[w] = 1
    count = 0
    for w in sorted(words, key=words.get, reverse=True):
        print "\t", w, words[w]
        count += 1
        if count == 20:
            break

def word_count_dailymotion():            
    words = {}
    dailymotion = db.dailymotion
    for video in dailymotion.find():
        words_list = video["title"]
        for r in replaced:
            words_list = words_list.replace(r, "")
        words_list = words_list.replace("_", " ")
        words_list = words_list.lower().split(" ")
        for w in words_list:
            if w not in exclusions:
                if w in words:
                    words[w] = words[w] + 1
                else:
                    words[w] = 1
    count = 0
    for w in sorted(words, key=words.get, reverse=True):
        print "\t",w, words[w]
        count += 1
        if count == 20:
            break

def acquire_youtube():
    views = list()
    dates = list()
    youtube = db.youtube
    for videos in youtube.find():
        views.append(int(videos["statistics"]["viewCount"]))
        dates.append(convert_to_timestamp((videos["snippet"]["publishedAt"]).split("T")[0]))
    return (views, dates)

def acquire_dailymotion():
    views = list()
    dates = list()
    dailymotion = db.dailymotion
    for videos in dailymotion.find():
        views.append(int(videos["views_total"]))
        dates.append(int(videos["created_time"]))
    return (views, dates)
    
def mean(data):
    return sum(data)/len(data)

def median(data):
    data.sort()
    half_size = len(data) // 2
    if (len(data) % 2) == 0:
        return (data[half_size - 1] + data[half_size]) / 2
    else:
        return data[half_size]

def variance(data):
    # Use the Computational Formula for Variance.
    n = len(data)
    ss = sum(x**2 for x in data) - (sum(data)**2)/n
    return ss/(n-1)

def standard_deviation(data):
    return math.sqrt(variance(data))

def main():
    dailymotion = acquire_dailymotion()
    print "Dailymotion"
    print "total videos: " + str(len(dailymotion[0]))
    print "mean views: " + str(mean(dailymotion[0]))
    print "median views: " + str(median(dailymotion[0]))
    print "STD views: " + str(standard_deviation(dailymotion[0]))
    #print "Average Date: " + str(convert_to_datetime(mean(dailymotion[1])))
    #print "Median Date: " + str(convert_to_datetime(median(dailymotion[1])))
    print "Top 10 most used word in title: "
    word_count_dailymotion()
    youtube = acquire_youtube()
    print "YouTube"
    print "total videos: " + str(len(youtube[0]))
    print "mean views: " + str(mean(youtube[0]))
    print "median views: " + str(median(youtube[0]))
    print "STD views: " + str(standard_deviation(youtube[0]))
    print "Average Date: " + str(convert_to_datetime(mean(youtube[1])))
    print "Median Date: " + str(convert_to_datetime(median(youtube[1])))
    print "Top 10 most used word in title: "
    word_count_yt("title")
    print "Top 10 most used words in description: "
    word_count_yt("description")
    client.close()

if __name__ == '__main__':
    main()
