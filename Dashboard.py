import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output


data = pd.read_csv('final_data.csv')
data['start_time'] = pd.to_datetime(data['start_time'], errors='coerce')
user_type = data['user_type'].dropna().unique()
gender = data['member_gender'].dropna().unique()
age_classification = {
    '18-30': 'Young Adult',
    '30-40': 'Adult',
    '40-50': 'Middle-aged',
    '50-60': 'Older Adult',
    '60+'  : 'Senior'
}
data['age_class_for_display'] = data['age_group'].map(age_classification)
age_group = data['age_class_for_display'].dropna().unique()

app = Dash(__name__)
app.title = "Interactive Dashboard"
numeric_cols = data.select_dtypes(include='number').columns

app.layout = html.Div([
 html.Div([

    html.H2("Filters", style={
        'marginBottom': '25px',
        'fontSize': '26px',
        'fontWeight': 'bold'
    }),

    # Date Filter Box
    html.Div([
        html.H4("Date Range", className="filter-title"),
        dcc.DatePickerRange(
            id='date_filter',
            start_date=data['start_time'].min(),
            end_date=data['start_time'].max(),
            style={'position': 'relative', 'zIndex': 9999}
        )
    ], className="filter-box"),

    # User Type Box
    html.Div([
        html.H4("User Type", className="filter-title"),
        dcc.Checklist(
            id='user_type_filter',
            options=[{'label': i, 'value': i} for i in user_type],
            labelStyle={'display': 'block'},
            className='custom-checklist'
        )
    ], className="filter-box"),

    # Gender Box
    html.Div([
        html.H4("Gender", className="filter-title"),
        dcc.Checklist(
            id='gender_filter',
            options=[{'label': i, 'value': i} for i in gender],
            labelStyle={'display': 'block'},
            className='custom-checklist'
        )
    ], className="filter-box"),

    # Age Group Box
    html.Div([
        html.H4("Age Group", className="filter-title"),
        dcc.Checklist(
            id='age_filter',
            options=[{'label': i, 'value': i} for i in age_group],
            labelStyle={'display': 'block'},
            className='custom-checklist'
        )
    ], className="filter-box")

],
style={
        'flex': '1',               
        'minWidth': '250px',
        'maxWidth': '300px',
        'padding': '25px',
        'backgroundColor': '#f8f9fa',
        'overflowY': 'auto',
        'boxShadow': '2px 0px 5px rgba(0,0,0,0.1)',
        'height': '100vh'

}),html.Div([

        dcc.Graph(id='trips_per_day'),

        dcc.Graph(id='user_type_chart'),

    ], style={
       'flex': '3',      
        'padding': '20px',
        'overflowY': 'auto'
    })
], style={
    'display': 'flex',   
    'flexDirection': 'row',
    'height': '100vh'
})

@app.callback(
    Output('trips_per_day', 'figure'),
    Output('user_type_chart', 'figure'),
    Input('date_filter', 'start_date'),
    Input('date_filter', 'end_date'),
    Input('user_type_filter', 'value'),
    Input('gender_filter', 'value'),
    Input('age_filter', 'value')
)
def update_dashboard(start_date, end_date, user_type_val, gender_val, age_group_val):
    filtered_data =data.copy()

    filtered_data = filtered_data[
        (filtered_data['start_time']>=start_date)&
        (filtered_data['start_time']<=end_date)
    ]

    if user_type_val:
        filtered_data = filtered_data[filtered_data['user_type'].isin(user_type_val)]
    if gender_val:
        filtered_data = filtered_data[filtered_data['member_gender'].isin(gender_val)]
    if age_group_val:
        filtered_data = filtered_data[filtered_data['age_class_for_display'].isin(age_group_val)]
 
    fig1 = px.histogram(filtered_data, x='day_of_week')
    fig2 = px.pie(filtered_data, names='user_type')
    
    return fig1, fig2

if __name__ == '__main__' :
    app.run(debug=True)

