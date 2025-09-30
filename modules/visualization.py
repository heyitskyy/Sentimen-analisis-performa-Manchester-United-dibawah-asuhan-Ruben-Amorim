import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_results(tweets_file="data/tweets_results.csv", keywords_file="data/keywords.csv"):
    try:
        df = pd.read_csv(tweets_file)
        kw = pd.read_csv(keywords_file)
    except FileNotFoundError:
        print("⚠️ File hasil tidak ditemukan, pastikan crawling sudah dijalankan.")
        return

    # --- Subplot dengan 3 chart ---
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Distribusi Sentimen (Bar)", "Persentase Sentimen (Pie)", "Top Keywords"),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"colspan": 2, "type": "bar"}, None]]
    )

    # === BAR CHART Sentimen ===
    sentiment_counts = df["sentiment"].value_counts()
    fig.add_trace(
        go.Bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            marker=dict(color=["red", "gray", "green"]),
            name="Sentiment Count"
        ),
        row=1, col=1
    )

    # === PIE CHART Sentimen ===
    fig.add_trace(
        go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=0.3,
            name="Sentiment Share"
        ),
        row=1, col=2
    )

    # === Keyword Frequency ===
    fig.add_trace(
        go.Bar(
            x=kw["keyword"].head(30),
            y=kw["frequency"].head(30),
            marker=dict(color="blue"),
            name="Keyword Frequency"
        ),
        row=2, col=1
    )

    # === Layout ===
    fig.update_layout(
        height=800,
        width=1000,
        title_text="📊 Dashboard Analisis Tweet (Sentimen & Keyword)",
        showlegend=True
    )

    fig.show()
