import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from numpy.ma.extras import column_stack

app = dash.Dash(__name__)


# Load your data
wc = pd.read_excel("WC - Rona.xlsx", sheet_name = "Leaderboard")
pred = pd.read_excel("WC - Rona.xlsx", sheet_name = "Sheet2")


#stats
goals_scored = wc.loc[0,"Goals Scored"]
games_played = wc.loc[0,"Games Played"]
games_remaining = wc.loc[0,"Games Remaining"]
print(goals_scored)
print(games_played)
print(games_remaining)

#leaderboard

leaderboard_df = wc[["Rank","Name","Points"]]
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
predictions_df = pred[["Date", "Group", "Home", "Away", "Matthew O'Brien", "Aaron Twiss", "Arion Aliu", "Rayan Zaibag", "Jorge Lopez"]]
list_length = len(predictions_df)

@app.callback(
    Output("prediction-table", "data"),
    Output("prediction-table", "columns"),
    Input("prediction-table", "id")
)

def load_prediction(_):
    df = predictions_df.copy()
    data = predictions_df.to_dict("records")


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
            html.H3("Games Played:"),
            html.H2(id="games_played")
        ], className="kpi-card"),

        html.Div([
            html.H3("Games remaining"),
            html.H2(id="kpi-games-played")
        ], className="kpi-card"),

        html.Div([
            html.H3("Goals Scored"),
            html.H2(id="kpi-goals-scored")
        ], className="kpi-card"),

        html.Div([
            html.H3("Games Remaining"),
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
                data = predictions_df.to_dict("records")),

        ], className="right-panel"),

    ], className="content-container")

])

if __name__ == "__main__":
    app.run(debug=True)
