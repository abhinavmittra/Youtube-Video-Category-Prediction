from youtube_videos import youtube_search
import pandas as pd
video_dict = {'youID':[], 'title':[], 'description':[],'category':[]}
#Enter your developer key on line 5 in youtube_videos.py
print("Enter number of instances (Multiple of 50)")
num=input()
print("Enter search query")
query=input()
def grab_videos(keyword, token=None):
    res = youtube_search(keyword)
    token = res[0]
    videos = res[1]
    category=keyword.replace(" ","")
    for vid in videos:
        video_dict['youID'].append(vid['id']['videoId'])
        video_dict['title'].append(vid['snippet']['title'])
        video_dict['description'].append(vid['snippet']['description'])
        video_dict['category'].append(category)
    return token
token = grab_videos(query)
while len(video_dict['youID'])<int(num)-49 and token!="last_page":
    token = grab_videos(query, token=token)
pdf = pd.DataFrame.from_dict(video_dict)
pdf.to_csv(query+'.csv')