# Pineapple Stats
Facebook messages stats for groups and individuals, created from FB's JSON data. Built using the awesome tools: plotly and Dash.

**Please note that this version is working on Windows OS only.**

# Requirements
• `message.json` file with your mesages downloaded from the Facebook, [guide here](https://www.facebook.com/help/1701730696756992). **Don't forget to choose the JSON format.**

• emoji `pip install emoji`

• plotly `pip install plotly`

• dash and requirements for dash, [please visit this site for the installation instructions](https://dash.plot.ly/installation)

# Preview
You can see the preview of the statistics with sample data [here](https://pineapple-stats.herokuapp.com/).

# How to make your own statistics
Clone the repository.
Open `data_proccessing.py` and place your `message.json` file into the repository or specify the path to this file (*Line 19*).

Run the `data_proccessing.py` file. It could take some time to execute depending on the amount of the messages.
This script structures the data for the statistics app. *You should get `structured_data.pickle`.*

When you get the message on the success of data proccessing, run the `app.py`. Now you are running your statistics app as localhost and you should be able to find your statistics [here](http://127.0.0.1:8050/).

# Deployment
If you want to deploy this app with your own statistics you can use [heroku](https://devcenter.heroku.com/articles/getting-started-with-python). Or you can use [other methods of deployment](https://dash.plot.ly/deployment).

*Note: This project is just my first attempt with dash and I hope I will refactor the app.py code soon. Apologies for bad readability.*



Facebook message statistics FB messages stats statistics charts plotly dash python 
