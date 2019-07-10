import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pickle
import os
from participant import Participant


# Run this file to start localhost. This file is just the first working version so 
# please excuse it's readability. Enjoy the stats!

os.chdir(os.path.dirname(os.path.realpath(__file__))) 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




# Data import from exported pickle file
with open('structured_data.pickle', 'rb') as data_in:
    loaded_data = pickle.load(data_in)

names = {'messages' : 'All messages', 'words' : 'Words', 'emojis' : 'Emojis',
        'swearing' : 'Swearing', 'reactions' : 'Reactions', 'photos' : 'Photos',
       'videos' : 'Videos', 'audio_files' : 'Audio files', 'gifs' : 'Gifs', 
       'sticker' : 'Stickers', 'share' : 'Shares'}

def get_xy(person, content, period, dependent=False):
    if type(person) == Participant:
        trace = loaded_data[person.name].content[content].period[period]
        mes = loaded_data[person.name].content['messages'].period[period]
    else:
        trace = loaded_data['participants'][person].content[content].period[period]
        mes = loaded_data['participants'][person].content['messages'].period[period]
    x = [z for z in loaded_data['sorted_time'].period[period]]
    if dependent:
        y = [trace[z]/mes[z] if z in trace else 0 for z in x]
    else:   
        y = [trace[z] if z in trace else 0 for z in x]
    return x, y

def get_max_date(person, content, dependent=False):
    if person not in loaded_data['participants']:
        date_dict = loaded_data[person].content[content].period['date']
        date_mes_dict = loaded_data[person].content['messages'].period['date']
    else:
        date_dict = loaded_data['participants'][person].content[content].period['date']
        date_mes_dict = loaded_data['participants'][person].content['messages'].period['date']
    if not dependent:
        max_date = max(date_dict, key =date_dict.get)
    else:
        max_date = max(date_dict, key = lambda x: (date_dict[x])/(date_mes_dict[x]))
    return date_dict[max_date], max_date

def get_graph(person, content, period, dependent=False, title_change='',reaction=False):
    if title_change:
        title_change = ' per message'
    if reaction:
        transmission = 'recevied'
    else:
        transmission = 'sent'
    if period == 'year-week_number':
        return(html.Div(
            [dcc.Graph(
                figure = go.Figure(
                data = [go.Scatter(x=get_xy(loaded_data['average'],content, 'year-week_number', dependent)[0], 
                                   y=get_xy(loaded_data['average'],content, 'year-week_number', dependent)[1],
                                   name='Average', line = dict(color = ('rgb(122, 196, 158)'),
                                   width = 4)),
                        go.Scatter(x=get_xy(person,content, 'year-week_number', dependent)[0], 
                                   y=get_xy(person,content, 'year-week_number', dependent)[1],
                                   name=person, line = dict(color = ('rgb(55, 83, 109)'),
                                   width = 4))
                        ],
                layout= go.Layout(title="{} - count of {}{} {} weekly.".format(person, content, title_change, transmission), 
                                  showlegend=True, legend=go.layout.Legend(x=0, y=1.0)
                                  )
                ))]))
    else:
        return (html.Div(
                dcc.Graph(
            figure = go.Figure(
            data = [go.Bar(x=get_xy(person, content, period, dependent)[0], 
                               y=get_xy(person,content, period, dependent)[1],
                               name=person, marker=go.bar.Marker(color='rgb(55, 83, 109)')),
                    go.Bar(x=get_xy(loaded_data['average'],content, period, dependent)[0], 
                               y=get_xy(loaded_data['average'],content, period,dependent)[1],
                               name='Average', marker=go.bar.Marker(color='rgb(122, 196, 158)'))],
            layout= go.Layout(title="{} - count of {}{} {} in each {}.".format(person, content, title_change, transmission,
                                                                              period), 
                              showlegend=True, legend=go.layout.Legend(x=0, y=1.0)
                              ))
            ))
                   )



def message_content(participant, content, period, align='left', reaction=False):
    person = participant.name
    if align == 'left':
        align = ['left', 'right']
    else:
        align = ['right' , 'none']
    return html.Div([html.Div([html.Div([html.P('`'),html.P('`')], style={'color': colors['bg']}),
                               html.P('Total {}: {}'.format(content, participant.content[content].total)),
                               html.P('Average {} per message: {}'.format(content, round((participant.content[content].total/
                                                                          participant.content['messages'].total),2))),
                               html.Hr(),
                               html.P('Most {} per day: {}'.format(content, get_max_date(person, content)[0])),
                               html.P('Most {} on date: {}'. format(content, get_max_date(person, content)[1])),
                               html.Hr(),
                               html.P('Most {} per message per day: {}'.format(content, get_max_date(person, content, True)[0])),
                               html.P('Most {} per message on date: {}'. format(content, get_max_date(person, content, True)[1]))],
                                style={'width': '32%', 'float':align[0], 'display': 'inline-block'}),
                      html.Div(get_graph(person, content, period, True, True, reaction), 
                               style={'width': '68%',  'display': 'inline-block'}),html.Hr()])

def get_slider_dict(period):
    return {i: list(loaded_data['sorted_time'].period[period].keys())[i] for i
           in range(len(loaded_data['sorted_time'].period[period]))}

def get_top_people(content, dependent=False, number=5):
    extra_text=''
    if dependent:
        values_dict = {p: round(loaded_data['participants'][p].content[content].total/
                       loaded_data['participants'][p].content['messages'].total, 2)
                            for p in loaded_data['participants']}
        extra_text = ' per message'
    else:
        values_dict = {p: loaded_data['participants'][p].content[content].total
                                for p in loaded_data['participants']}
    sorted_people = sorted(values_dict, key= values_dict.get)
    children = []
    rank=1
    while sorted_people and rank<=number:
        person = sorted_people.pop()
        children.append( html.P('{}.{} : {}'.format(rank, person, values_dict[person])))
        rank +=1
    return html.Div([html.H6('Top {} {}{} counts'.format(rank-1, content, extra_text)),
                     html.Div(children)])

def get_all_data_scatter():
    data = []
    color = 137
    x = [z for z in loaded_data['sorted_time'].period['year-week_number']]
    for content in loaded_data['all'].content:
        trace = loaded_data['all'].content[content].period['year-week_number']
        data.append(go.Scatter(x=x, y=[trace[z] if z in trace else 0 for z in x],
                                       name=content, line = dict(
                                           color = ('rgb'+ str(((122+color)%255,
                                                               (3*color)%255, 158))),
                                       width = 3)))
        color = color * len(content)**1.2
    return data

def avg_day_content(content):
    count = round(loaded_data['all'].content[content].total/
                  len(loaded_data['sorted_time'].period['date']),2)
    return html.Div(html.P('{1} : {0}'.format(count, names[content])))

def group_message_content(content, align_graph='left'):
    color='rgb(55, 83, 109)'
    style_graph = {'width': '71%', 'display': 'inline-block', 'float':'left'}
    style_text = {'width': '25%', 'display': 'inline-block', 'float':'right'}
    if align_graph == 'right':
        style_graph['float'], style_text['float'] = style_text['float'], style_graph['float']
        color='rgb(122, 196, 158)'
    graph = go.Bar(name = '{} per message'.format(content), 
                   x = [p for p in loaded_data['participants']],
                   y = [p.content[content].total/p.content['messages'].total for 
                   p in loaded_data['participants'].values()],
                   marker=go.bar.Marker(color=color))
    return html.Div([html.Div(dcc.Graph(figure=go.Figure(data=[graph], layout=go.Layout(
                                                    title='{} per message'.format(names[content])))),
                              style = style_graph),
                    html.Div([html.P('Average {} per message: {}'.format(content,
                                                                         round(loaded_data['average'].content[content].total/
                                                                         loaded_data['average'].content['messages'].total, 2))),
                              html.Hr(),
                              html.P('Most {} per message per day: {}'.format(content,get_max_date('average', content, True)[0])),
                              html.P('On date {}'.format(get_max_date('average', content, True)[1])),
                              html.Hr(),
                              get_top_people(content, True)],
                             style=style_text)],
                    style={'width': '100%', 'display': 'inline-block'})

    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {'bg' : '#FFFFFF', 'fg' : '#11111'}
app.layout = html.Div(style={'backgroundColor': colors['bg'], 'textAlign': 'center',
                             'color' : colors['fg']},
                      children=[
    html.H1(children=html.H1('{} statistics'.format(loaded_data['title']))),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Group', children=[
            html.Div([html.Hr(),
            html.Div('Choose content: ', style={'width': '10%', 'display': 'inline-block', 'textAlign':'right'}),
                
          html.Div(dcc.RadioItems(
                id='content-group',
                options=[{'label': names[i]+' ', 'value': i} for i in names],
                value='messages',
                labelStyle={'display': 'inline-block'} #rozhoduje ze sa zobrazuju v riadku
            ),style={'width': '87%', 'float': 'right', 'display': 'inline-block', 'textAlign' : 'left'} ),
            html.Div('Choose time period: ', style={'width': '10%', 'display': 'inline-block', 'textAlign':'right'}),
            html.Div(dcc.RadioItems(
                id='period-group',
                options=[{'label': 'Year', 'value': 'year'}, {'label': 'Month', 'value': 'month'}, 
                         {'label': 'Weekday', 'value': 'week_day'}, {'label': 'Hour', 'value': 'hour'},
                         {'label': 'Total', 'value': 'total'}],
                value='total',
                labelStyle={'display': 'inline-block'} #rozhoduje ze sa zobrazuju v riadku
            ), style={'width': '87%', 'float': 'right', 'display': 'inline-block', 'textAlign' : 'left'}),
                html.Div([dcc.Graph(id='group-graph',),
                         html.Div(id='slider-choose', style={'width': '16%','float' : 'left','textAlign':'right'}),
                         html.Div(dcc.Slider(id='slidertest', step=1, min=0, value=0),  
                                  style={'width': '80%','float' : 'right',  'textAlign':'left'})],
                         style={'width': '60%','float' : 'left', 'display': 'inline-block', 'textAlign':'right'}),
                        html.Div(id='group-info')])
        ]),
        dcc.Tab(label='Individuals', children=[
            html.Div('Choose person: ', style={'width': '10%', 'display': 'inline-block', 
                                               'textAlign':'right', 'font-size':'125%'}),
            html.Div(dcc.Dropdown(
        id='person',
        options=[{'label': i, 'value' : i} for i in loaded_data['participants']],
        value=list(loaded_data['participants'].keys())[0]
        ),style={'width': '87%', 'float': 'right', 'display': 'inline-block', 'textAlign' : 'left'}),
            html.Hr(),
            html.Div('Choose content: ', style={'width': '10%', 'display': 'inline-block', 'textAlign':'right'}),
                
          html.Div(dcc.RadioItems(
                id='content',
                options=[{'label': names[i]+' ', 'value': i} for i in names],
                value='messages',
                labelStyle={'display': 'inline-block'} #rozhoduje ze sa zobrazuju v riadku
            ),style={'width': '87%', 'float': 'right', 'display': 'inline-block', 'textAlign' : 'left'} ),
            html.Div('Choose time period: ', style={'width': '10%', 'display': 'inline-block', 'textAlign':'right'}),
            html.Div(dcc.RadioItems(
                id='period',
                options=[{'label': 'Year', 'value': 'year'}, {'label': 'Month', 'value': 'month'}, 
                         {'label': 'Weekday', 'value': 'week_day'}, {'label': 'Hour', 'value': 'hour'},
                         {'label': 'Whole existence weekly', 'value': 'year-week_number'}],
                value='year-week_number',
                labelStyle={'display': 'inline-block'} #rozhoduje ze sa zobrazuju v riadku
            ), style={'width': '87%', 'float': 'right', 'display': 'inline-block', 'textAlign' : 'left'}),
                html.Div(id='graphs')
       ], 
    )
 ]
),  html.Hr(),
    html.Div('Created in 2019 by Peter Slany, thanks to plotly and Dash.', style={'font-family':'Impact'})]
)
server = app.server
# Ked je zmena vo value v dropdown, spusti sa update_output funkcia
@app.callback(
    Output('graphs', 'children'),
    [Input('person', 'value'), Input('content', 'value'),
     Input('period', 'value')])
def update_figure(person, content, period):
    ##TODO UPRAVIT message graf komplexny, farby, a messages
    participant = loaded_data['participants'][person]
    if content == 'messages':
        labels = ['Text messages','Photos','Videos','Gifs', 'Audio files', 'Shares', 'Stickers']
        l_values ={'Photos': participant.content['photos'].total,'Videos': participant.content['videos'].total,
                   'Gifs': participant.content['gifs'].total, 'Audio files': participant.content['audio_files'].total,
                   'Shares': participant.content['share'].total, 'Stickers': participant.content['sticker'].total}
        values = [l_values[x] for x in l_values]
        values.insert(0, participant.content['messages'].total - sum(values))
        #colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']
        extra = html.Div([message_content(participant, 'words', period, align='right'),
                          message_content(participant, 'emojis', period),
                          message_content(participant, 'swearing', period, align='right'),
                          message_content(participant, 'reactions', period, reaction=True),
                      html.H6('Type of messages'),
                      dcc.Graph(
                      figure = go.Figure(
                                    data = [go.Pie(labels=labels, values=values)],
                                     layout= go.Layout( legend=go.layout.Legend(x=0.62, y=1.0))
                                  ))], style={'width':'100%', 'display':'inline-block'})
        return html.Div([html.Div([html.Div([html.P('`'),html.P('`')], style={'color': colors['bg']}),
                                   html.H5('{}'.format(participant.name)),
                                   html.Hr(),
                                   html.P('Total messages: {}'.format(participant.content['messages'].total)),
                                   html.P('{}% of all group messages'.format(round((participant.content['messages'].total/
                                                                             loaded_data['all'].content['messages'].total*100),2))),
                                   html.Hr(),
                                   html.P('Most messages per day: {}'.format(get_max_date(person, content)[0])),
                                   html.P('Most messages on date: {}'.format(get_max_date(person, content)[1]))],
                                  style={'width': '22%', 'display': 'inline-block'}),
                         html.Div(get_graph(person, content, period), 
                                  style={'width': '77%', 'float': 'right', 'display': 'inline-block'}),
                         html.Div(html.Hr(),style={'width':'100%', 'display':'inline-block'}),
                        extra])
    else:
        return html.Div(get_graph(person, content, period))

@app.callback(Output('group-graph', 'figure'),
    [Input('content-group', 'value'), Input('period-group', 'value'), 
     Input('slidertest', 'value')])
def update_graph(content, period, slider):
    labels = [i for i in loaded_data['participants']]
    if period == 'total':
        values =[loaded_data['participants'][i].content[content].total for i in labels]
    else:
        values = [loaded_data['participants'][i].content[content].
                  period[period][get_slider_dict(period)[slider]]
                 if get_slider_dict(period)[slider] in 
                 loaded_data['participants'][i].content[content].period[period] 
                 else 0 for i in labels]
    return go.Figure(data=[go.Pie(labels=labels, values=values ,hole=0.2, sort=False)],
                     layout = go.Layout(autosize=True, height=600, 
                                        margin=go.layout.Margin(autoexpand=True)))

@app.callback(Output('group-info', 'children'),
    [Input('content-group', 'value'), Input('period-group', 'value')])
def group_info(content, period):
    basic_info=html.Div([html.H3(loaded_data['title']),
                         html.Hr(),
                         html.P('{} members'.format(len(loaded_data['participants']))),
                         html.P('First message on {}'.format(list(loaded_data['sorted_time'].
                                                             period['date'].keys())[0])),
                         html.Hr(),
                         html.P('Total {}: {}'.format(content,loaded_data['all'].
                                                      content[content].total)),
                         html.Hr(),
                         html.P('Most {} per day: {}'.format(content, get_max_date('all',content)[0])),
                         html.P('On date: {}'.format(get_max_date('all',content)[1])),
                         html.Hr(),
                         html.P(get_top_people(content))],
                        style={'width': '36%', 'float': 'right'})
    messages=html.Div([html.Hr(),
                       html.Div([html.H5('Average day of {}'.format(loaded_data['title'])),
                                 html.Hr(),html.Div([avg_day_content(i) for i in names])
                                ], style={'width':'30%', 'display':'inline-block'}),
                       html.Div(dcc.Graph(
                                figure = go.Figure(
                                        data =get_all_data_scatter(),
                                        layout = go.Layout(title='Content created weekly'),)),
                                style={'width':'67%', 'display':'inline-block', 'float':'right'}),
                       html.Hr(), group_message_content('words'),
                       html.Hr(), group_message_content('emojis','right'),
                       html.Hr(), group_message_content('swearing'),
                       html.Hr(), group_message_content('reactions','right')], 
                      style={'width':'100%', 'display':'inline-block'})
    if content=='messages':
        return html.Div([basic_info, messages])
    return basic_info

@app.callback(Output('slidertest', 'marks'),
    [Input('period-group', 'value')])
def update_slider(period):
    if period == 'total':
        return {}
    return get_slider_dict(period)

@app.callback(Output('slidertest', 'min'),
    [Input('slidertest', 'marks')])
def update_slider_2(marks):
    return 0

@app.callback(Output('slidertest', 'max'),
    [Input('slidertest', 'marks')])
def update_slider_3(marks):
    return len(list(marks.keys()))-1

@app.callback(Output('slidertest', 'value'),
    [Input('slidertest', 'min')])
def update_slider_4(min):
    return min

@app.callback(Output('slider-choose', 'children'),
    [Input('period-group', 'options'), Input('period-group', 'value')])
def update_slider_text(options, period):
    for item in options:
        if item['value']==period:
            out=item['label']
    if period != 'total':
        return html.Div(['Choose {}:'.format(out.lower())])

if __name__ == '__main__':
    app.run_server(debug=False)
