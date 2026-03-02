import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv(r"D:\Gemy Study\DEPI\Machine learning DEPI round_4\TEC\Amit-1\src\ML\data-analysis\Final_Project\clean_data.csv")

# ثابت: Total Trips
TOTAL_TRIPS = len(df)

# KPIs function
def calc_kpis(filtered_df):
    avg_duration = filtered_df['duration_min'].mean()
    active_users = len(filtered_df)  # عدد الصفوف بعد الفلترة
    if not filtered_df.empty:
        most_popular_station = filtered_df['start_station_name'].value_counts().idxmax()
    else:
        most_popular_station = "N/A"
    return avg_duration, active_users, most_popular_station

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar filters (كل فلتر في Card منفصل)
sidebar = html.Div([
    dbc.Card([
        dbc.CardHeader("User Type"),
        dbc.CardBody([
            dcc.Checklist(
                id='user_type_filter',
                options=[{'label': i, 'value': i} for i in df['user_type'].unique()],
                value=df['user_type'].unique().tolist(),
                inputStyle={"margin-right":"10px"},
                style={"marginBottom":"10px"}
            )
        ])
    ], className="mb-3"),

    dbc.Card([
        dbc.CardHeader("Gender"),
        dbc.CardBody([
            dcc.Checklist(
                id='gender_filter',
                options=[{'label': i, 'value': i} for i in df['member_gender'].unique()],
                value=df['member_gender'].unique().tolist(),
                inputStyle={"margin-right":"10px"},
                style={"marginBottom":"10px"}
            )
        ])
    ], className="mb-3"),

    dbc.Card([
        dbc.CardHeader("Age Group"),
        dbc.CardBody([
            dcc.Checklist(
                id='age_group_filter',
                options=[{'label': i, 'value': i} for i in df['age_group'].unique()],
                value=df['age_group'].unique().tolist(),
                inputStyle={"margin-right":"10px"},
                style={"marginBottom":"10px"}
            )
        ])
    ], className="mb-3"),
], style={"width":"20%", "float":"left", "padding":"20px", "height":"100vh", "backgroundColor":"#f8f9fa"})

# Main content
content = dbc.Container([
    html.H1("Bike Sharing Dashboard", style={'textAlign':'center'}),

    dbc.Row(id="kpi-cards", className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='user_type_pie'), width=6),
        dbc.Col(dcc.Graph(id='gender_bar'), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='duration_hist'), width=12),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='top_start'), width=6),
        dbc.Col(dcc.Graph(id='top_end'), width=6),
    ], className="mb-4"),
], style={"width":"75%", "float":"right"})

app.layout = html.Div([sidebar, content])

# Callbacks
@app.callback(
    [Output('kpi-cards','children'),
     Output('user_type_pie','figure'),
     Output('gender_bar','figure'),
     Output('duration_hist','figure'),
     Output('top_start','figure'),
     Output('top_end','figure')],
    [Input('user_type_filter','value'),
     Input('gender_filter','value'),
     Input('age_group_filter','value')]
)
def update_dashboard(user_types, genders, age_groups):
    # Filter data
    filtered_df = df[
        df['user_type'].isin(user_types) &
        df['member_gender'].isin(genders) &
        df['age_group'].isin(age_groups)
    ]

    # KPIs
    avg_duration, active_users, most_popular_station = calc_kpis(filtered_df)
    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card([html.H4("Total Trips"), html.H2(f"{TOTAL_TRIPS:,}")]), width=3),
        dbc.Col(dbc.Card([html.H4("Avg Duration (min)"), html.H2(f"{avg_duration:.1f}")]), width=3),
        dbc.Col(dbc.Card([html.H4("Active Users"), html.H2(f"{active_users:,}")]), width=3),
        dbc.Col(dbc.Card([html.H4("Most Popular Station"), html.H2(most_popular_station)]), width=3),
    ])

    # Charts
    user_type_pie = px.pie(filtered_df, names='user_type', title="Subscriber vs Customer Usage")

    gender_counts = filtered_df['member_gender'].value_counts().reset_index()
    gender_counts.columns = ['gender','count']
    gender_bar = px.bar(gender_counts, x='gender', y='count', title="Gender Distribution", color='gender')

    duration_hist = px.histogram(filtered_df, x='duration_min', color='member_gender', nbins=50, title="Trip Duration Distribution")

    start_counts = filtered_df['start_station_name'].value_counts().nlargest(10).reset_index()
    start_counts.columns = ['station','count']
    top_start = px.bar(start_counts, x='count', y='station', orientation='h', title="Top 10 Start Stations")

    end_counts = filtered_df['end_station_name'].value_counts().nlargest(10).reset_index()
    end_counts.columns = ['station','count']
    top_end = px.bar(end_counts, x='count', y='station', orientation='h', title="Top 10 End Stations")

    return kpi_cards, user_type_pie, gender_bar, duration_hist, top_start, top_end

if __name__ == "__main__":
    app.run(debug=True)

