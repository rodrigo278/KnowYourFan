import re
import random
from datetime import datetime, timedelta

def extract_social_media_info(social_media_data):
    """
    Extract and analyze information from social media profiles.
    
    In a real implementation, this would use actual social media APIs to get real data.
    For this demonstration, we generate plausible simulated data.
    
    Args:
        social_media_data (dict): Dictionary containing social media profile information
        
    Returns:
        dict: Analyzed social media information
    """
    # This is a simulated analysis - in a real implementation,
    # you would use social media APIs to fetch and analyze real data
    
    # Check if there are any social media profiles to analyze
    if not any(social_media_data.values()):
        return {
            'esports_posts': 0,
            'team_mentions': 0,
            'engagement_score': 0,
            'activity': [],
            'top_mentioned_games': [],
            'top_mentioned_teams': []
        }
    
    # Common esports games
    games = ["League of Legends", "Counter-Strike", "Valorant", "Dota 2", "Overwatch", 
             "Fortnite", "Rainbow Six Siege", "Rocket League", "Apex Legends", "FIFA"]
    
    # Common esports teams
    teams = ["FURIA", "LOUD", "Team Liquid", "paiN Gaming", "Cloud9", "Fnatic", 
             "G2 Esports", "T1", "FaZe Clan", "NaVi", "Sentinels"]
    
    # Generate simulated data
    esports_posts = random.randint(15, 50)
    team_mentions = random.randint(5, 20)
    engagement_score = round(random.uniform(5.0, 9.8), 1)
    
    # Generate activity data for the past 6 months
    activity = []
    today = datetime.now()
    for i in range(180, 0, -7):  # Past 6 months, weekly data points
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        activity.append({
            'date': date,
            'posts': random.randint(0, 5),
            'interactions': random.randint(0, 10)
        })
    
    # Generate top mentioned games and teams
    num_games = min(random.randint(2, 5), len(games))
    num_teams = min(random.randint(2, 4), len(teams))
    
    top_games = random.sample(games, num_games)
    top_teams = random.sample(teams, num_teams)
    
    top_mentioned_games = [
        {'name': game, 'mentions': random.randint(5, 30)} for game in top_games
    ]
    
    top_mentioned_teams = [
        {'name': team, 'mentions': random.randint(3, 15)} for team in top_teams
    ]
    
    # Sort by mentions
    top_mentioned_games.sort(key=lambda x: x['mentions'], reverse=True)
    top_mentioned_teams.sort(key=lambda x: x['mentions'], reverse=True)
    
    return {
        'esports_posts': esports_posts,
        'team_mentions': team_mentions,
        'engagement_score': engagement_score,
        'activity': activity,
        'top_mentioned_games': top_mentioned_games,
        'top_mentioned_teams': top_mentioned_teams
    }

def analyze_social_relevance(esports_profiles, interests):
    """
    Analyze the relevance of esports profiles based on user interests.
    
    Args:
        esports_profiles (dict): Dictionary containing esports profile information
        interests (dict): Dictionary containing user interests
        
    Returns:
        dict: Analysis of the relevance of esports profiles
    """
    # This is a simulated analysis - in a real implementation,
    # you would use gaming platform APIs to fetch and analyze real data
    
    # Check if there are any profiles to analyze
    if not any(value for key, value in esports_profiles.items() if key in ['twitch_username', 'steam_profile']):
        return {
            'relevance_score': 0,
            'confidence': 'Low',
            'matching_interests': []
        }
    
    # Calculate a relevance score based on the number of profiles and user interests
    base_score = random.randint(5, 8)
    
    # Adjust score based on available profiles
    profile_count = sum(1 for key, value in esports_profiles.items() 
                       if key in ['twitch_username', 'steam_profile'] and value)
    
    score_adjustment = profile_count * 0.5
    
    # Adjust score based on user interests
    interest_adjustment = 0
    
    # Check for matching interests
    matching_interests = []
    
    if 'favorite_games' in interests and interests['favorite_games']:
        # Simulate finding matching games in the esports profiles
        for game in interests['favorite_games']:
            if game != 'Other' and random.random() > 0.3:  # 70% chance of matching
                matching_interests.append(game)
                interest_adjustment += 0.3
    
    if 'favorite_teams' in interests and interests['favorite_teams']:
        # Simulate finding matching teams in the esports profiles
        for team in interests['favorite_teams']:
            if team != 'Other' and random.random() > 0.5:  # 50% chance of matching
                matching_interests.append(team)
                interest_adjustment += 0.2
    
    # Calculate final score
    final_score = min(10, base_score + score_adjustment + interest_adjustment)
    final_score = round(final_score, 1)
    
    # Determine confidence level
    if final_score >= 8:
        confidence = 'High'
    elif final_score >= 5:
        confidence = 'Medium'
    else:
        confidence = 'Low'
    
    return {
        'relevance_score': final_score,
        'confidence': confidence,
        'matching_interests': matching_interests
    }

def validate_esports_profile(profile_url, interests):
    """
    Validate if an esports profile is relevant to the user's interests.
    
    Args:
        profile_url (str): URL of the esports profile
        interests (dict): Dictionary containing user interests
        
    Returns:
        dict: Validation result
    """
    # Extract platform from URL
    platform = None
    if 'twitch.tv' in profile_url:
        platform = 'Twitch'
    elif 'steamcommunity.com' in profile_url:
        platform = 'Steam'
    elif 'discord.gg' in profile_url:
        platform = 'Discord'
    else:
        platform = 'Unknown'
    
    # Generate a relevance score
    relevance_score = random.randint(1, 10)
    
    # Determine if the profile is valid based on the score
    is_valid = relevance_score >= 6
    
    return {
        'platform': platform,
        'is_valid': is_valid,
        'relevance_score': relevance_score,
        'message': f"Profile {'validated' if is_valid else 'not validated'} with a relevance score of {relevance_score}/10."
    }
