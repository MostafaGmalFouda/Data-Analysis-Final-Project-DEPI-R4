import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('clean_data.csv')
TOTAL_TRIPS = len(df)

def calc_kpis(filtered_df):
    avg_duration = filtered_df['duration_min'].mean() if not filtered_df.empty else 0
    active_users = len(filtered_df)
    most_popular_station = filtered_df['start_station_name'].value_counts().idxmax() if not filtered_df.empty else "N/A"
    return avg_duration, active_users, most_popular_station

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Interactive Dashboard"

# Sidebar
sidebar = html.Div([
    html.H2("DASHBOARD", className="sidebar-title"),
    html.Hr(style={"color": "#475569"}),
    html.P("FILTERS", className="filter-label"),

    html.Div([
        html.Label("User Type", className="dropdown-label"),
        dcc.Checklist(
            id='user_type_filter',
            options=[{'label': i, 'value': i} for i in df['user_type'].unique()],
            value=df['user_type'].unique().tolist(),
            className="custom-checklist"
        ),
    ], className="filter-group"),

    html.Div([
        html.Label("Gender", className="dropdown-label"),
        dcc.Checklist(
            id='gender_filter',
            options=[{'label': i, 'value': i} for i in df['member_gender'].unique()],
            value=df['member_gender'].unique().tolist(),
            className="custom-checklist"
        ),
    ], className="filter-group"),

    html.Div([
        html.Label("Age Group", className="dropdown-label"),
        dcc.Checklist(
            id='age_group_filter',
            options=[{'label': i, 'value': i} for i in df['age_group'].unique()],
            value=df['age_group'].unique().tolist(),
            className="custom-checklist"
        ),
    ], className="filter-group"),

], className="sidebar")

# Main content
content = html.Div([
    html.H1("Bike Sharing Overview", className="main-title"),
    html.Div(id="kpi-cards", className="kpi-container"),

    # First Row: Pie + Bar
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='user_type_pie'), className="graph-card"), width=5),
        dbc.Col(html.Div(dcc.Graph(id='gender_bar'), className="graph-card"), width=7),
    ], className="mb-4 g-3"),

    # Second Row: Wave Chart فقط
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='duration_wave'), className="graph-card"), width=12),
    ], className="mb-4 g-3"),

    # Third Row: Top Stations Bar
    dbc.Row([
        dbc.Col(html.Div(dcc.Graph(id='top_start'), className="graph-card"), width=6),
        dbc.Col(html.Div(dcc.Graph(id='top_end'), className="graph-card"), width=6),
    ], className="mb-4 g-3"),

], className="content-area")

app.layout = html.Div([sidebar, content])

# Callback
@app.callback(
    [Output('kpi-cards','children'),
     Output('user_type_pie','figure'),
     Output('gender_bar','figure'),
     Output('duration_wave','figure'),
     Output('top_start','figure'),
     Output('top_end','figure')],
    [Input('user_type_filter','value'),
     Input('gender_filter','value'),
     Input('age_group_filter','value')]
)
def update_dashboard(user_types, genders, age_groups):
    filtered_df = df[
        df['user_type'].isin(user_types) &
        df['member_gender'].isin(genders) &
        df['age_group'].isin(age_groups)
    ]

    avg_duration, active_users, most_popular_station = calc_kpis(filtered_df)

    gradient_colors = ["#24255d","#8b5cf6","#c648ec","#bc81f3","#471E33","#ec4899","#c45cba","#012b4e","#3189d0","#87d6f5"]

    # KPI Cards
    kpi_cards = [
        html.Div([html.P("Total Trips", className="kpi-label"), html.H3(f"{TOTAL_TRIPS:,}")], className="kpi-box"),
        html.Div([html.P("Avg Duration", className="kpi-label"), html.H3(f"{avg_duration:.1f}m")], className="kpi-box"),
        html.Div([html.P("Active Users", className="kpi-label"), html.H3(f"{active_users:,}")], className="kpi-box"),
        html.Div([html.P("Top Station", className="kpi-label"), html.H3(most_popular_station, style={"fontSize":"14px"})], className="kpi-box"),
    ]

    # Pie Chart
    user_type_pie = px.pie(filtered_df, names='user_type', hole=0.4, color_discrete_sequence=gradient_colors)
    
    # Gender Bar
    gender_counts = filtered_df['member_gender'].value_counts().reset_index()
    gender_bar = px.bar(gender_counts, x='member_gender', y='count', color='member_gender', color_discrete_sequence=gradient_colors)

  # Wave Chart (Duration)
    # Wave Chart (Duration)
    duration_wave = px.line(
        filtered_df.sort_values('duration_min').reset_index(),
        x=range(len(filtered_df)),
        y='duration_min'
    )

    duration_wave.update_traces(
        mode="lines+markers",
        line=dict(width=4, color="#6366f1"),
        marker=dict(
            size=8,                
            color="#a855f7",       
            line=dict(width=1, color="#24255d") 
        ),
        fill='tozeroy',
        fillcolor='rgba(99,102,241,0.15)'
    )
    duration_wave.update_layout(
    hovermode="x unified"
     )    
    # Top Stations
    start_counts = filtered_df['start_station_name'].value_counts().nlargest(10).reset_index()
    top_start = px.scatter(
    start_counts,
    x='count',
    y='start_station_name',
    size='count',
    color='count',
    color_continuous_scale=gradient_colors
     )
    top_start.update_traces(marker=dict(line=dict(width=1,color="white")))
    end_counts = filtered_df['end_station_name'].value_counts().nlargest(10).reset_index()
    top_end = px.funnel(
    end_counts,
    x='count',
    y='end_station_name',
    color='count',
    color_discrete_sequence=gradient_colors
     )
    # Apply dark theme
    for fig in [user_type_pie, gender_bar, duration_wave, top_start, top_end]:
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#f8fafc',
            margin=dict(l=20,r=20,t=30,b=20),
            height=300,
            showlegend=False if fig != user_type_pie else True
        )
        if hasattr(fig.layout, 'xaxis'):
            fig.update_xaxes(showgrid=False, zeroline=False)
            fig.update_yaxes(showgrid=False, zeroline=False)

    return kpi_cards, user_type_pie, gender_bar, duration_wave, top_start, top_end

if __name__ == "__main__":
    app.run(debug=True)