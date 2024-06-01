# Youtube Data Harvesting And Warehousing


## A streamlit application that collects and store youtube channel's information

### we can see what this project does by looking at the name of the project (i.e) Data harvesting means collecting information and Warehousing means storing those information in a proper format.You can understand how to do this project by following:

#### * Firstly, create an API key using API reference credentials and build a connection with youtube using googleapiclient.discovery library.
#### * Install all the required packages like pandas,streamlit,mongodb, pymysql and other needed packages.
#### * Collect the details of channels,videos and comments from a particular youtube channel.
#### * Establish a connection with mongodb to store all the collected data and convert those data into a dataframe.
#### * Establish a connection with mysql and insert those dataframes into a particular database inside the mysql.
#### * Using streamlit display those data in a table format and in other data visualizations like bar chart,scatter chart and so on....
#### * Use your imagination to design the front end using streamlit.

## Softwares used 

#### * VS Code
#### * Python
#### * Mongodb
#### * Streamlit
#### * MySql

## Packages to install
#### To install the below packages, open new terminal in your source code editor(I used VS Code to run my codes) and type the following pip commands

### * pip install google-api-python-client
#### googleapiclient.discovery is a library which is used to 
### * pip install pandas
#### Pandas is used to convert json or dictionary to a Dataframe
### * pip install streamlit
#### * Streamlit is used to design and display data to users like a frondend or user end application
### * pip install pymongo
#### * Mongodb is used to store data in the cloud and we can retrieve those data anytime
### * pip install pymysql
#### * It's used to connect with MySQl and perform queries
### * pip install datetime
#### * It's a library that is used to convert string into time(Hours,Minutes,Seconds) and date(Days,Month,Year)

## Demo Images of my project

![Screenshot 2024-06-01 180516](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/bfb126b0-5826-4156-9833-5d6af4ee4ef8)

##### Enter a channel ID and click the "collect and store data" button to store all the data to mongodb

![Screenshot 2024-06-01 182307](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/bd2d9420-df25-4475-939a-14359f25a9b4)

##### All the data inserted into mongodb, so it shows a success message

![Screenshot 2024-06-01 182926](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/94236b98-02d7-4be0-b6fc-be9c7142bca7)

##### If you enter channel ID that already exists in mongodb, it shows a warning message

![Screenshot 2024-06-01 182337](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/b1d21a8f-3535-4bc9-a9ba-503490f8f9b8)

![Screenshot 2024-06-01 182358](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/ef32950f-0848-4b87-8237-40f3d4aa134c)

##### In this page, we can insert all the data collected in mongodb into MySQL 

![Screenshot 2024-06-01 182501](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/ca0febcb-68dd-4c27-bee9-b76222b9ac9e)

##### Likewise if you try to insert a channel details that already exists in MySql, it will show a warning message

![Screenshot 2024-06-01 182409](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/e05da88b-20da-4aa5-8c57-37282f389488)

![Screenshot 2024-06-01 182421](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/99482e48-1690-4d1a-8857-0ef00d0a1b8c)

![Screenshot 2024-06-01 182439](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/ec214715-3c16-408a-8817-aff9bd5f3347)

##### After inserted, you can see all the channels, videos and comments details in a table format 

![Screenshot 2024-06-01 182705](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/51891830-7462-4d9d-8edb-dfe243cc2991)

##### In Queries section, there are totally 10 queries 

![Screenshot 2024-06-01 182517](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/42918a4f-85e6-4dfa-957c-dc52fec0f424)

![Screenshot 2024-06-01 182534](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/3d23fdb7-b516-4856-8f5a-0c90f57bfcbd)

##### You can select any queries and the data will appear in table format according to that query with data analysis of the table in chart format.

![Screenshot 2024-06-01 182715](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/f39a703f-e22b-482c-b08b-00fa423c06d1)

![Screenshot 2024-06-01 182723](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/c9078410-7225-4e2d-9101-9c1be7ae127d)

![Screenshot 2024-06-01 182735](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/af36b8d1-13f1-4100-8114-d8911ac66d84)

![Screenshot 2024-06-01 182747](https://github.com/Harini3198/my-first-youtube-project/assets/169538709/815af0c1-908d-4533-a163-ab103d11775d)

##### I used different charts for each queries.

## Conclusion

#### This project is an example for how to use the above mentioned softwares in data analysis.


# Thank you, ALL !!!!!!









