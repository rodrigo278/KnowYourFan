import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta


def create_interest_chart(interests_data):
    """
    Create a visualization of the user's esports interests.
    
    Args:
        interests_data (dict): User's interests data
        
    Returns:
        plotly.graph_objects.Figure: Visualization figure
    """
    # Extract favorite games and teams
    favorite_games = interests_data.get('favorite_games', [])
    favorite_teams = interests_data.get('favorite_teams', [])

    # Remove 'Other' if present
    if 'Other' in favorite_games:
        favorite_games.remove('Other')
    if 'Other' in favorite_teams:
        favorite_teams.remove('Other')

    # Generate interest scores (1-10) for games and teams
    game_scores = [random.randint(7, 10) for _ in range(len(favorite_games))]
    team_scores = [random.randint(7, 10) for _ in range(len(favorite_teams))]

    # Create data for the chart
    categories = []
    scores = []
    types = []

    for game, score in zip(favorite_games, game_scores):
        categories.append(game)
        scores.append(score)
        types.append('Game')

    for team, score in zip(favorite_teams, team_scores):
        categories.append(team)
        scores.append(score)
        types.append('Team')

    # Create a DataFrame
    if categories:
        df = pd.DataFrame({
            'Category': categories,
            'Interest Score': scores,
            'Type': types
        })

        # Create a bar chart
        fig = px.bar(
            df,
            x='Category',
            y='Interest Score',
            color='Type',
            color_discrete_map={
                'Game': '#FF5722',
                'Team': '#2196F3'
            },
            labels={
                'Interest Score': 'Nível de Interesse (1-10)',
                'Category': ''
            },
            title='Seus Interesses em Esports',
        )

        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',
                          font_color='white',
                          title_font_size=20,
                          legend_title_font_color='white',
                          legend_title_font_size=14)

        return fig
    else:
        # Create an empty figure with a message
        fig = go.Figure()
        fig.add_annotation(text="No interest data available",
                           xref="paper",
                           yref="paper",
                           x=0.5,
                           y=0.5,
                           showarrow=False,
                           font=dict(size=16, color="white"))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',
                          font_color='white',
                          height=300)
        return fig


def create_activity_timeline(social_media_analysis):
    """
    Create a timeline visualization of the user's social media activity.
    
    Args:
        social_media_analysis (dict): Analyzed social media data
        
    Returns:
        plotly.graph_objects.Figure: Visualization figure
    """
    # Extract activity data
    activity = social_media_analysis.get('activity', [])

    if activity:
        # Create a DataFrame
        df = pd.DataFrame(activity)

        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Create a line chart
        fig = go.Figure()

        # Add posts line
        fig.add_trace(
            go.Scatter(x=df['date'],
                       y=df['posts'],
                       mode='lines+markers',
                       name='Posts',
                       line=dict(color='#FF5722', width=2),
                       marker=dict(size=6)))

        # Add interactions line
        fig.add_trace(
            go.Scatter(x=df['date'],
                       y=df['interactions'],
                       mode='lines+markers',
                       name='Interactions',
                       line=dict(color='#2196F3', width=2),
                       marker=dict(size=6)))

        # Update layout
        fig.update_layout(
            title='Atividade de eSports nas mídias sociais (Last 6 Months)',
            xaxis_title='Date',
            yaxis_title='Count',
            legend_title='Activity Type',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=16,
            legend_title_font_color='white',
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))

        return fig
    else:
        # Create an empty figure with a message
        fig = go.Figure()
        fig.add_annotation(
            text="Sem dados de atividades de mídia social disponíveis",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="white"))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',
                          font_color='white',
                          height=300)
        return fig


def create_engagement_radar(social_media_analysis, interests_data):
    """
    Create a radar chart visualization of the user's engagement across different aspects.
    
    Args:
        social_media_analysis (dict): Analyzed social media data
        interests_data (dict): User's interests data
        
    Returns:
        plotly.graph_objects.Figure: Visualization figure
    """
    # Define categories for the radar chart
    categories = [
        'Presença nas mídias sociais', 'Conhecimento em jogos',
        'Suporte de Equipe', 'Participação no evento', 'Criação de conteúdo',
        'Envolvimento na comunidade'
    ]

    # Calculate scores for each category (1-10)
    scores = []

    # Social Media Presence
    social_score = min(10, social_media_analysis.get('engagement_score', 0))
    scores.append(social_score)

    # Game Knowledge (based on favorite games)
    game_knowledge = min(10, len(interests_data.get('favorite_games', [])) * 2)
    scores.append(game_knowledge)

    # Team Support (based on favorite teams)
    team_support = min(10, len(interests_data.get('favorite_teams', [])) * 2.5)
    scores.append(team_support)

    # Event Attendance
    events = interests_data.get('attended_events', '')
    event_count = len([e for e in events.split('\n')
                       if e.strip()]) if events else 0
    event_attendance = min(10, event_count * 2)
    scores.append(event_attendance)

    # Content Creation (simulated)
    content_creation = random.randint(3, 8)
    scores.append(content_creation)

    # Community Involvement (simulated)
    community_involvement = random.randint(4, 9)
    scores.append(community_involvement)

    # Create the radar chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(r=scores,
                        theta=categories,
                        fill='toself',
                        fillcolor='rgba(255, 87, 34, 0.3)',
                        line=dict(color='#FF5722', width=2),
                        name='Engagement Score'))

    fig.update_layout(polar=dict(
        radialaxis=dict(visible=True,
                        range=[0, 10],
                        gridcolor='rgba(255,255,255,0.1)'),
        angularaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        bgcolor='rgba(0,0,0,0)'),
                      title='Fan Engagement Profile',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      font_color='white',
                      title_font_size=16)

    return fig
