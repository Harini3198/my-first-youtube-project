# IMPORTING NEEDED LIBRARIES

import googleapiclient.discovery
import pandas as pd
import seaborn as sns
from pymysql import connect
import pandas as pd
import pymongo
import streamlit as st
from datetime import datetime
import numpy as np
import plotly.express as px
from PIL import Image


#API KEY CONNECTION
def Api_connect():
    api_key="AIzaSyBlHmcZ2_xGDqCsZuWEpAmscofqY-MgBfI"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = api_key)
    return youtube
youtube=Api_connect()


#GATHERING CHANNELS INFORMATION
def channel_data(channel_Id):
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_Id)
    response = request.execute()
    
    for item in response["items"]:
        data = dict(
            channel_id=item['id'],
            channel_name=item['snippet']['title'],
            channel_des=item['snippet']['description'],
            channel_pid=item['contentDetails']['relatedPlaylists']['uploads'],
            channel_viewCount=item['statistics']['viewCount'],
            channel_sub=item['statistics']['subscriberCount'],
            channel_vc=item['statistics']['videoCount']
        )
        return data


#GATHERING VIDEO IDS
def get_video_ids(channel_id):
    request=youtube.channels().list(id=channel_id,
                                 part="contentDetails")
    response=request.execute()
    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    video_ids=[]
    next_page_token=None
    while True:
        request = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
        response1 = request.execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids


#FORMATTING DURATION TO DATETIME FORMAT AND THEN INTO STRING FORMAT
def convertTime(video_time):
    a=['H','M','S']
    b=['M','S']
    c=['S']
    d=['M']
    s=video_time.replace('PT','')
    if all(x in s for x in a):
        converted_time=datetime.strptime(s, '%HH%MM%SS').time()
        time_str = converted_time.strftime('%H:%M:%S')
        return time_str
    elif all(x in s for x in b):
        converted_time=datetime.strptime(s, '%MM%SS').time()
        time_str = converted_time.strftime('%H:%M:%S')
        return time_str
    elif all(x in s for x in c):
        converted_time=datetime.strptime(s,'%SS').time()
        time_str = converted_time.strftime('%H:%M:%S')
        return time_str
    elif all(x in s for x in d):
        converted_time=datetime.strptime(s,'%MM').time()
        time_str = converted_time.strftime('%H:%M:%S')
        return time_str


#GATHERING VIDEOS INFORMATION
def get_video_data(video_ids):
    video_data=[]
    for video_id in video_ids:
        request=youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response2=request.execute()
        

        for item in response2['items']:
            data=dict(video_id=item['id'],
                      channel_id=item['snippet']['channelId'],
                      channel_name=item['snippet']['channelTitle'],
                    video_name=item['snippet']['title'],
                    video_description=item['snippet'].get('description'),
                    tags=str(item['snippet'].get('tags')),
                    published_date=datetime.strptime((item['snippet']['publishedAt']),"%Y-%m-%dT%H:%M:%SZ"),
                    view_count=item['statistics'].get('viewCount'),
                    like_count=item['statistics']['likeCount'],
                    favorite_count=item['statistics']['favoriteCount'],
                    comment_count=(item['statistics'].get('commentCount')),
                    video_duration=convertTime(item['contentDetails']['duration']),
                    thumbnail=item['snippet']['thumbnails']['default']['url'],
                    caption_status=item['contentDetails'].get('caption')
                    ) 
            video_data.append(data)
    return video_data


#GATHERING COMMENTS INFORMATION
def get_comment_data(video_ids):
    comment_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response3=request.execute()
            
            for item in response3["items"]:
                data=dict(
                    comment_id=item['id'],
                    video_id=item['snippet']['videoId'],
                    comment_text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    comment_author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    comment_published_date=datetime.strptime(item['snippet']['topLevelComment']['snippet']['publishedAt'],"%Y-%m-%dT%H:%M:%SZ")
                )
                comment_data.append(data)
                
    except:
        pass
    return comment_data


#CONNECTING MONGODB WITH VS CODE
client=pymongo.MongoClient("mongodb+srv://harini31987:HariniS@cluster0.w6yps5g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client["youtube_data"]


#INSERTING ALL GATHERED INFORMATION INTO MONGODB
def channel_details(channel_id):
    ch_details=channel_data(channel_id)
    vi_id=get_video_ids(channel_id)
    vi_details=get_video_data(vi_id)
    com_details=get_comment_data(vi_id)
    

    coll1=db["channel_details"]
    coll1.insert_one({"channel_iformation":ch_details, "video_information":vi_details, "comment_information":com_details})
    return "upload completed successfully"


#CREATING TABLE FOR CHANNELS
def channel_table(channel):
    data_base=connect(host='localhost',
                    user='root',
                    password='1234',
                    database='youtube',
                    port=3306)
    cur=data_base.cursor()


    create_table_query='''create table if not exists channels_information(Channel_Id varchar(100) primary key,
    Channel_name varchar(80),
    Description text,
    Playlist_Id varchar(80),
    ViewCount bigint,
    Subcribers bigint,
    Videos int)'''
    cur.execute(create_table_query)
    data_base.commit()

    single_channel=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({"channel_iformation.channel_name":channel}, {"_id":0}):
        single_channel.append(ch_data["channel_iformation"])

    channel_info=pd.DataFrame(single_channel)


    for index, row in channel_info.iterrows():
        insert_query='''insert into channels_information(Channel_Id,
                                                Channel_Name,
                                                Description,
                                                Playlist_Id,
                                                ViewCount,
                                                Subcribers,
                                                Videos)
                                                
                                                values(%s,%s,%s,%s,%s,%s,%s)'''
        values=(row['channel_id'],
                row['channel_name'],
                row['channel_des'],
                row['channel_pid'],
                row['channel_viewCount'],
                row['channel_sub'],
                row['channel_vc'])
        
        try:
            cur.execute(insert_query,values)
            data_base.commit()

        except:
            err_msg="The channel {} that you entered is already exists".format(channel)
            return err_msg



#CREATING TABLE FOR VIDEOS
def viedos_table(channel):

    data_base=connect(host='localhost',
                    user='root',
                    password='1234',
                    database='youtube')
    cur=data_base.cursor()

    create_table_query='''create table if not exists videos_information(Video_Id varchar(30) primary key,
                                                                        Channel_id varchar(100),
                                                                        Channel_Name varchar(200),
                                                                        Title varchar(150),
                                                                        Description text,
                                                                        Tags varchar(1000),
                                                                        Published_Date timestamp,
                                                                        Views bigint,
                                                                        Likes bigint,
                                                                        Favorites int,
                                                                        Comments bigint,
                                                                        Duration varchar(50),
                                                                        Thumbnail varchar(200),
                                                                        Caption_Status varchar(10))'''
    cur.execute(create_table_query)
    data_base.commit()


    single_video=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({"channel_iformation.channel_name":channel}, {"_id":0}):
        single_video.append(ch_data["video_information"])

    video_info=pd.DataFrame(single_video[0])
    

    for index, row in video_info.iterrows():
        
        insert_video_query='''insert into videos_information(Video_id,
                                                        Channel_id,
                                                        Channel_Name,
                                                        Title,
                                                        Description,
                                                        Tags,
                                                        Published_Date,
                                                        Views,
                                                        Likes,
                                                        Favorites,
                                                        Comments,
                                                        Duration,
                                                        Thumbnail,
                                                        Caption_Status
                                                    )
                                                
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        
        values=(row['video_id'],
                row['channel_id'],
                row['channel_name'],
                row['video_name'],
                row['video_description'],
                row['tags'],
                row['published_date'],
                row['view_count'],
                row['like_count'],
                row['favorite_count'],
                row['comment_count'],
                row['video_duration'],
                row['thumbnail'],
                row['caption_status']
                )
        
        
        
        cur.execute(insert_video_query, values)
        data_base.commit()
       

            



#CREATING TABLE FOR COMMENTS
def commnets_table(channel_s):

    data_base=connect(host='localhost',
                    user='root',
                    password='1234',
                    database='youtube',
                    port=3306)
    cur=data_base.cursor()

    create_table_query='''create table if not exists comments(Comment_Id varchar(255) primary key,
    Video_Id varchar(255),
    Comment_Text text,
    Comment_Author varchar(255),
    Published_Date timestamp)'''
    cur.execute(create_table_query)
    data_base.commit()

    single_comment=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({"channel_iformation.channel_name":channel_s}, {"_id":0}):
        single_comment.append(ch_data["comment_information"])

    comment_info=pd.DataFrame(single_comment[0])


    for index, row in comment_info.iterrows():
        
        insert_comment_query='''insert into comments(Comment_Id,
                                                        Video_Id,
                                                        Comment_Text,
                                                        Comment_Author,
                                                        Published_Date
                                                    )
                                                
                                                values(%s,%s,%s,%s,%s)'''
        values=(row['comment_id'],
                row['video_id'],
                row['comment_text'],
                row['comment_author'],
                row['comment_published_date']
                )
        
        cur.execute(insert_comment_query, values)
        data_base.commit()
        
       



#FUNCTION FOR INSERTING VALUES ALL AT ONCE
def tables(channel):
    msg=channel_table(channel)
    if msg:
        return msg
    else:
        viedos_table(channel)
        commnets_table(channel)

    return "Tables created successfully"


#VIEWING THE CHANNEL TABLE
def show_channels_table():
    ch_list=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({}, {"_id":0, "channel_iformation":1}):
        ch_list.append(ch_data["channel_iformation"])
    channel_info=st.dataframe(ch_list)
    
    return channel_info


#VIWEING THE VIDEO TABLE
def show_videos_table():    
    vi_list=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for vi_data in coll1.find({},{"_id":0,"video_information":1}):
        for i in range(len(vi_data["video_information"])):
            vi_list.append(vi_data["video_information"][i])
    video_info=st.dataframe(vi_list)
    
    return video_info


#VIEWING THE COMMENTS TABLE
def show_comments_table()  :  
    com_list=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for com_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(com_data["comment_information"])):
            com_list.append(com_data["comment_information"][i])
    comment_info=st.dataframe(com_list)
    
    return comment_info


#STREAMLIT PART
#CREATING SIDE BAR
with st.sidebar:
    st.title(":blue[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    # st.header("Skills Take Away")
    # st.caption("Python Scripting")
    # st.caption("Data Collection")
    # st.caption("API Integretion")
    type=st.radio("Select any box",("Channel Information","Dataframe To SQL","Queries"))

if type == "Channel Information":
    # st.title(":blue[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    # tab1,tab2,tab3=st.tabs(["Channel Information","Dataframe To SQL","Querires",])
    # with tab1:
    #CREATING INPUT BOX FOR USERS
    channel_id=st.text_input("Enter the Channel ID")

    #BUTTON TO COLLECT AND STORE DATA OF CHANNEL ID
    if st.button("Collect and Store Data"):
        ch_ids=[]
        db=client["youtube_data"]
        coll1=db["channel_details"]
        for ch_data in coll1.find({}, {"_id":0, "channel_iformation":1}):
            ch_ids.append(ch_data["channel_iformation"]["channel_id"])
        
        if channel_id in ch_ids:
            st.warning("Channels details of the given channel id already exists")
        else:
            insert=channel_details(channel_id)
            st.success(insert)

elif type == "Dataframe To SQL":

    #BUTTON TO VIEW TABLES
    channels=[]
    db=client["youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({}, {"_id":0, "channel_iformation":1}):
        channels.append(ch_data["channel_iformation"]["channel_name"])

    unique_channel = st.selectbox("Select the channel",channels)
    if st.button("Migrate to SQL"):
        Table=tables(unique_channel)
        st.success(Table)

    show_table=st.radio("SELECT THE TABLE FOR VIEW",("CHANNELS","VIDEOS","COMMENTS"))
    if show_table == "CHANNELS":
        show_channels_table()
    elif show_table == "VIDEOS":
        show_videos_table()
    elif show_table == "COMMENTS":
        show_comments_table()

elif type == "Queries":

    #QUERY BOX TO ANALYSE DATA
    # sql connection

    data_base=connect(host='localhost',
                    user='root',
                    password='1234',
                    database='youtube',
                    port=3306)
    cur=data_base.cursor()

    question=st.selectbox("SELECT YOUR QUESTION",("1. All videos and channel name",
                                                "2. Channels with most number of videos",
                                                "3. 10 most viewed videos",
                                                "4. Comments in each video",
                                                "5. Video that has highest number of likes",
                                                "6. Total number of likes of each videos",
                                                "7. Total number of views of each channel",
                                                "8. Channels which are published videos in 2022",
                                                "9. Average duration of all videos in a channel",
                                                "10.Videos which have highest number of comments"))

    if question == "1. All videos and channel name":
        query1='''select Title as Videos,Channel_Name as ChannelName from videos_information'''
        cur.execute(query1)
        data_base.commit()
        t1=cur.fetchall()
        df=pd.DataFrame(t1,columns=["Video Title","Channel Name"])
        st.write(df)
        st.title(":green[Data visualization of records]")
        n=st.number_input("Enter the number of records to be analysed",value=None, placeholder="Type a number...")
        if n != None:
            int_n=int(n)
            analyse_df=df.head(int_n)
            st.line_chart(analyse_df,use_container_width=True,x="Video Title",y="Channel Name",color="#B233FF")

    elif question == "2. Channels with most number of videos":
        query2='''select Channel_name as ChannelName,Videos as No_of_Videos from channels_information order by Videos desc'''
        cur.execute(query2)
        data_base.commit()
        t2=cur.fetchall()
        df2=pd.DataFrame(t2,columns=["Video Title","Channel Name"])
        st.write(df2)
        st.title(":green[Data visualization of records]")
        analyse_df2=df2.head(10)
        st.bar_chart(analyse_df2,use_container_width=True,x="Video Title",y="Channel Name",color="#FF0000")

    elif question == "3. 10 most viewed videos":
        query3='''select Channel_Name as ChannelName,Title as Videos, Views from videos_information where Views is not null order by Views desc LIMIT 10'''
        cur.execute(query3)
        data_base.commit()
        t3=cur.fetchall()
        df3=pd.DataFrame(t3,columns=["Channel Name","Videos","Views"])
        st.write(df3)
        st.title(":green[Data visualization of records]")
        st.bar_chart(df3,use_container_width=True,x="Videos",y="Views",color="#A833FF")


    elif question == "4. Comments in each video":
        query4='''select Title as videos, Comments as no_of_comments from videos_information where Comments is not null'''
        cur.execute(query4)
        data_base.commit()
        t4=cur.fetchall()
        df4=pd.DataFrame(t4,columns=["Video Name","No of Comments"])
        st.write(df4)
        st.title(":green[Data visualization of records]")
        n=st.number_input("Enter the number of records to be analysed",value=None, placeholder="Type a number...")
        if n != None:
            int_n=int(n)
            analyse_df4=df4.head(int_n)
            st.area_chart(analyse_df4,use_container_width=True,x="Video Name",y="No of Comments",color="#FFB233")

    elif question == "5. Video that has highest number of likes":
        query5='''select Title as videos, Likes as no_of_likes,Channel_Name as channelname from videos_information where Likes is not null order by Likes desc'''
        cur.execute(query5)
        data_base.commit()
        t5=cur.fetchall()
        df5=pd.DataFrame(t5,columns=["Video Name","No of Likes","Channel Name"])
        st.write(df5)
        st.title(":green[Data visualization of records]")
        n=st.number_input("Enter the number of records to be analysed",value=None, placeholder="Type a number...")
        if n != None:
            int_n=int(n)
            analyse_df5=df5.head(int_n)
            st.line_chart(analyse_df5,use_container_width=True,x="Video Name",y="No of Likes",color="#FF3377")

    elif question == "6. Total number of likes of each videos":
        query6='''select Title as videos, Likes as no_of_likes from videos_information where Likes is not null'''
        cur.execute(query6)
        data_base.commit()
        t6=cur.fetchall()
        df6=pd.DataFrame(t6,columns=["Video Name","No of Likes"])
        st.write(df6)
        st.title(":green[Data visualization of records]")
        n=st.number_input("Enter the number of records to be analysed",value=None, placeholder="Type a number...")
        if n != None:
            int_n=int(n)
            analyse_df6=df6.head(int_n)
            st.line_chart(analyse_df6,use_container_width=True,x="Video Name",y="No of Likes",color="#600624")

    elif question == "7. Total number of views of each channel":
        query7='''select Channel_name as channelname, ViewCount as viewcount from channels_information where ViewCount is not null'''
        cur.execute(query7)
        data_base.commit()
        t7=cur.fetchall()
        df7=pd.DataFrame(t7,columns=["Channel Name","No of Views"])
        st.write(df7)
        st.title(":green[Data visualization of records]")
        st.bar_chart(df7,use_container_width=True,x="Channel Name",y="No of Views",color="#ABF442")

    elif question == "8. Channels which are published videos in 2022":
        query8='''select Channel_Name as channelname, Title as videoname,Published_Date as pubDate from videos_information where extract(year from Published_Date)=2022'''
        cur.execute(query8)
        data_base.commit()
        t8=cur.fetchall()
        df8=pd.DataFrame(t8,columns=["Channel Name","Video Name","Published Date"])
        st.write(df8)
        st.title(":green[Data visualization of records]")
        st.bar_chart(df8,use_container_width=True,x="Published Date",y="Channel Name",color="#ABF442")

    elif question == "9. Average duration of all videos in a channel":
        query9='''select Channel_Name as channelname, AVG(CAST(Duration AS time)) as averageduration from videos_information group by Channel_Name'''
        cur.execute(query9)
        data_base.commit()
        t9=cur.fetchall()
        df9=pd.DataFrame(t9,columns=["Channel Name","Average Duration"])
        st.write(df9)
        st.title(":green[Data visualization of records]")
        st.scatter_chart(df9,use_container_width=True,color=["#250444","#ABF442"])
        

    elif question == "10.Videos which have highest number of comments":
        query10='''select Channel_Name as channelname,Title as videoname,Comments as commentcount from videos_information 
                    where Comments is not null order by Comments desc'''
        cur.execute(query10)
        data_base.commit()
        t10=cur.fetchall()
        df10=pd.DataFrame(t10,columns=["Channel Name","Video Title","No of Comments"])
        st.write(df10)
        st.title(":green[Data visualization of records]")
        n=st.number_input("Enter the number of records to be analysed",value=None, placeholder="Type a number...")
        if n != None:
            int_n=int(n)
            analyse_df10=df10.head(int_n)
            st.bar_chart(analyse_df10,use_container_width=True,x="Video Title",y="No of Comments",color="#600624")










        
