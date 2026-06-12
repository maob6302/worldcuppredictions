import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from numpy.ma.extras import column_stack
from datetime import datetime

app = dash.Dash(__name__)


# Load your data
lead = pd.read_excel("WC - Rona.xlsx", sheet_name = "Leaderboard")
pred = pd.read_excel("WC - Rona.xlsx", sheet_name = "Sheet2")


#Time Formatting
time_formatted = []
for col in pred["Time"]:
    time_formatted.append(col.strftime("%H:%M"))

print(time_formatted)

#Date Formatting
date_formatted = []
for col in pred["Date"]:
    date_formatted.append(col.strftime("%d/%m/%Y"))




#stats
goals_scored = int(lead.loc[0,"Goals Scored"])
games_played = int(lead.loc[0,"Games Played"])
games_remaining = int(lead.loc[0,"Games Remaining"])
print(goals_scored)
print(games_played)
print(games_remaining)

#leaderboard

leaderboard_df = lead[["Rank","Name","Points"]]
leaderboard_df["Rank"] = leaderboard_df["Points"].rank(
    method="min", ascending=False
).astype(int)


print(leaderboard_df)


from dash.dependencies import Input, Output

@app.callback(
    Output("leaderboard-table", "data"),
    Output("leaderboard-table", "columns"),
    Input("leaderboard-table", "id")
)
def load_leaderboard(_):
    df = leaderboard_df.copy()   # ✔ use the filtered DataFrame

    data = leaderboard_df.to_dict("records")  # ✔ correct orientation
    columns = [
        {"name": "Rank", "id": "Rank"},
        {"name": "Name", "id": "Name"},
        {"name": "Points", "id": "Points"}
    ]

    return data, columns



#predictions
pred["Time"] = time_formatted
pred["Date"] = date_formatted
predictions_df = pred[["Date", "Time", "Group", "Home", "Away", "Result","Matthew O'Brien", "Aaron Twiss", "Arion Aliu", "Rayan Zaibag", "Jorge Lopez"]]
list_length = len(predictions_df)






@app.callback(
    Output("prediction-table", "data"),
    Output("prediction-table", "columns"),
    Input("prediction-table", "id")
)

def load_prediction(_):
    df = predictions_df.copy()
    data = predictions_df.to_dict("records")
    columns = [time_formatted]


#date
day = datetime.now()

next_matches = []
for idx, row in pred.iterrows():
    if int(row["Date"][0:2]) == int(day.day):
        next_matches.append(f"{row["Date"]} at {row["Time"]} | Group {row["Group"]} | {row["Home"]} vs {row["Away"]}")

print(next_matches)


# Layout
import dash
from dash import html, dcc, dash_table
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([

    # HEADER
    html.Div([
        html.H1("World Cup Leaderboard", className="header-title"),
        html.P("Live standings, stats, and performance insights", className="header-subtitle")
    ], className="header"),

    # KPI CARDS
    html.Div([
        html.Div([
            html.H3("Today's Fixtures:"),
            dcc.Markdown("<br>".join(next_matches), dangerously_allow_html=True),
            html.H2(id="next_match")
        ], className="kpi-card"),



        html.Div([
            html.H3(f"Games Played: {games_played}"),
            html.H2(id="kpi-games-played")
        ], className="kpi-card"),

        html.Div([
            html.H3(f"Games Remaining: {games_remaining}"),
            html.H2(id="games_remaining")
        ], className="kpi-card"),

        html.Div([
            html.H3(f"Goals Scored: {goals_scored}"),
            html.H2(id="kpi-games-remaining")
        ], className="kpi-card"),
    ], className="kpi-container"),

    # MAIN CONTENT
    html.Div([

        # LEFT: Leaderboard Table
        html.Div([
            html.H2("Leaderboard"),
            dash_table.DataTable(
                id="leaderboard-table",
                sort_action="native",
                page_size=5,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center"},
                style_header={
                    "backgroundColor": "#1f2c56",
                    "color": "white",
                    "fontWeight": "bold",
                    "border": "1px solid black"},
                data = leaderboard_df.to_dict("records"),


            )
        ], className="left-panel"),

        # RIGHT: Chart
        html.Div([
            html.H2("Predictions"),
            dash_table.DataTable(
                id="prediction-table",
                sort_action="native",
                page_size=list_length,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center"},
                style_header={
                    "backgroundColor": "#1f2c56",
                    "color": "white",
                    "fontWeight": "bold",
                    "border": "1px solid black"},
                data = predictions_df.to_dict("records"),
                style_data_conditional=[{
            "if": {
                "column_id": "Matthew O'Brien",
                "filter_query": "{Matthew O'Brien} = {Result}"
            },
            "backgroundColor": "#d4edda",
            "color": "black",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "Aaron Twiss",
                "filter_query": "{Aaron Twiss} = {Result}"
            },
            "backgroundColor": "#d4edda",
            "color": "black",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "Arion Aliu",
                "filter_query": "{Arion Aliu} = {Result}"
            },
            "backgroundColor": "#d4edda",
            "color": "black",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "Rayan Zaibag",
                "filter_query": "{Rayan Zaibag} = {Result}"
            },
            "backgroundColor": "#d4edda",
            "color": "black",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "Jorge Lopez",
                "filter_query": "{Jorge Lopez} = {Result}"
            },
            "backgroundColor": "#d4edda",
            "color": "black",
            "fontWeight": "bold"
        }])


        ], className="right-panel"),

    ], className="content-container")

])

if __name__ == "__main__":
    app.run(debug=True)
