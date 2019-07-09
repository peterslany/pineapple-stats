# pineapple-stats
Facebook messages stats for groups and individuals from JSON data. Built using the awesome tools: plotly and Dash.

**Please note that this version is working on Windows OS only.**

# Requirements
• emoji `pip install emoji`

• plotly `pip install plotly`

• dash and requirements for dash, [please visit this site for the installation instructions](https://dash.plot.ly/installation)

# Preview
You can see the preview of the statistics with sample data [here](https://pineapple-stats.herokuapp.com/).

# How to make your own statistics
Clone the repository.
Open `data_proccessing.py` and place your `message.json` file into the repository or specify the path to this file (*Line 19*).

Run the `data_proccessing.py` file. *It could take some time to execute due to the amount of the messages.*
This script structures the data for the statistics app. *You should get `structured_data.pickle`.*

When you get the message on the success of data proccessing, run the `app.py`. Now you are running your statistics app as localhost and you can find your statistics [here](http://127.0.0.1:8050/).

# Deployment
If you want to deploy this app with your own statistics you can use [heroku](https://devcenter.heroku.com/articles/getting-started-with-python). Or you can use [other methods of deployment](https://dash.plot.ly/deployment).

*Note: This code is just my first attempt with dash and I hope I will refactor the app.py file soon. Apologies for bad readability.*

