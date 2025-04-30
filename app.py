import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from utils.document_validator import validate_document, process_image_ocr
from utils.social_media import extract_social_media_info, analyze_social_relevance
from utils.data_visualization import create_interest_chart, create_activity_timeline

# Page configuration
st.set_page_config(
    page_title="Know Your Fan - Esports",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'personal': {},
        'interests': {},
        'documents': {},
        'social_media': {},
        'esports_profiles': {}
    }
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Functions to navigate through steps
def next_step():
    if st.session_state.step < 5:
        st.session_state.step += 1
        st.session_state.progress = (st.session_state.step - 1) * 25

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.session_state.progress = (st.session_state.step - 1) * 25

def save_form_data(form_data, category):
    st.session_state.user_data[category].update(form_data)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.svg", width=80)
with col2:
    st.title("Know Your Fan - Esports")
    st.subheader("Build your fan profile to unlock exclusive experiences")

# Progress bar
st.progress(st.session_state.progress)

# Step indicators
steps_col1, steps_col2, steps_col3, steps_col4, steps_col5 = st.columns(5)
with steps_col1:
    st.markdown(f"**{'1. Personal Info' if st.session_state.step != 1 else '→ 1. Personal Info'}**")
with steps_col2:
    st.markdown(f"**{'2. Interests' if st.session_state.step != 2 else '→ 2. Interests'}**")
with steps_col3:
    st.markdown(f"**{'3. Verification' if st.session_state.step != 3 else '→ 3. Verification'}**")
with steps_col4:
    st.markdown(f"**{'4. Social Media' if st.session_state.step != 4 else '→ 4. Social Media'}**")
with steps_col5:
    st.markdown(f"**{'5. Dashboard' if st.session_state.step != 5 else '→ 5. Dashboard'}**")

# Step 1: Personal Information
if st.session_state.step == 1:
    st.header("Personal Information")
    
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.user_data['personal'].get('name', ''))
            email = st.text_input("Email", value=st.session_state.user_data['personal'].get('email', ''))
            cpf = st.text_input("CPF", value=st.session_state.user_data['personal'].get('cpf', ''))
            phone = st.text_input("Phone Number", value=st.session_state.user_data['personal'].get('phone', ''))
        
        with col2:
            address = st.text_input("Address", value=st.session_state.user_data['personal'].get('address', ''))
            city = st.text_input("City", value=st.session_state.user_data['personal'].get('city', ''))
            state = st.text_input("State", value=st.session_state.user_data['personal'].get('state', ''))
            birth_date = st.date_input("Birth Date", value=datetime.strptime(st.session_state.user_data['personal'].get('birth_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d') if 'birth_date' in st.session_state.user_data['personal'] else None)
        
        submitted = st.form_submit_button("Save & Continue")
        
        if submitted:
            form_data = {
                'name': name,
                'email': email,
                'cpf': cpf,
                'phone': phone,
                'address': address,
                'city': city,
                'state': state,
                'birth_date': birth_date.strftime('%Y-%m-%d') if birth_date else None
            }
            
            # Validate required fields
            required_fields = ['name', 'email', 'cpf']
            empty_fields = [field for field in required_fields if not form_data.get(field)]
            
            if empty_fields:
                st.error(f"Please fill in the following required fields: {', '.join(empty_fields)}")
            else:
                save_form_data(form_data, 'personal')
                next_step()

# Step 2: Interests & Activities
elif st.session_state.step == 2:
    st.header("Esports Interests & Activities")
    
    with st.form("interests_form"):
        # Favorite games
        st.subheader("Favorite Games")
        games_options = ["League of Legends", "Counter-Strike", "Valorant", "Dota 2", "Overwatch", "Fortnite", "Rainbow Six Siege", "Rocket League", "Other"]
        favorite_games = st.multiselect("Select your favorite games", games_options, default=st.session_state.user_data['interests'].get('favorite_games', []))
        
        if "Other" in favorite_games:
            other_games = st.text_input("Please specify other games", value=st.session_state.user_data['interests'].get('other_games', ''))
        
        # Favorite teams
        st.subheader("Favorite Teams")
        teams_options = ["FURIA", "LOUD", "Team Liquid", "paiN Gaming", "Cloud9", "Fnatic", "G2 Esports", "T1", "FaZe Clan", "Other"]
        favorite_teams = st.multiselect("Select your favorite teams", teams_options, default=st.session_state.user_data['interests'].get('favorite_teams', []))
        
        if "Other" in favorite_teams:
            other_teams = st.text_input("Please specify other teams", value=st.session_state.user_data['interests'].get('other_teams', ''))
        
        # Events attended
        st.subheader("Events Attended in the Last Year")
        attended_events = st.text_area("List events you attended (one per line)", value=st.session_state.user_data['interests'].get('attended_events', ''))
        
        # Gaming habits
        st.subheader("Gaming Habits")
        hours_gaming = st.slider("Hours spent gaming per week", 0, 50, st.session_state.user_data['interests'].get('hours_gaming', 10))
        hours_watching = st.slider("Hours spent watching esports per week", 0, 30, st.session_state.user_data['interests'].get('hours_watching', 5))
        
        # Merchandise purchases
        st.subheader("Merchandise Purchases")
        merch_options = ["Team Jerseys", "Team Accessories", "Gaming Equipment", "Collectibles", "None"]
        merchandise = st.multiselect("Merchandise purchased in the last year", merch_options, default=st.session_state.user_data['interests'].get('merchandise', []))
        
        submitted = st.form_submit_button("Save & Continue")
        
        if submitted:
            form_data = {
                'favorite_games': favorite_games,
                'favorite_teams': favorite_teams,
                'attended_events': attended_events,
                'hours_gaming': hours_gaming,
                'hours_watching': hours_watching,
                'merchandise': merchandise
            }
            
            if "Other" in favorite_games:
                form_data['other_games'] = other_games
            if "Other" in favorite_teams:
                form_data['other_teams'] = other_teams
            
            save_form_data(form_data, 'interests')
            next_step()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            prev_step()

# Step 3: Document Verification
elif st.session_state.step == 3:
    st.header("Document Verification")
    
    # Use columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Please upload your identification documents for verification.")
        
        # ID Document Upload
        st.subheader("Identity Document")
        id_doc = st.file_uploader("Upload your ID card (front)", type=["jpg", "jpeg", "png"])
        
        if id_doc:
            # Display the uploaded document
            st.image(id_doc, caption="Uploaded ID Document", width=300)
            
            # Process and validate document using OCR
            if st.button("Validate ID Document"):
                with st.spinner("Processing document..."):
                    # Process the document using OCR
                    extracted_text = process_image_ocr(id_doc)
                    
                    # Validate the extracted information
                    is_valid, validation_message = validate_document(extracted_text, st.session_state.user_data['personal'])
                    
                    if is_valid:
                        st.success(validation_message)
                        st.session_state.user_data['documents']['id_validated'] = True
                        st.session_state.user_data['documents']['id_validation_message'] = validation_message
                    else:
                        st.error(validation_message)
                        st.session_state.user_data['documents']['id_validated'] = False
                        st.session_state.user_data['documents']['id_validation_message'] = validation_message
        
        # Secondary document (optional)
        st.subheader("Secondary Document (Optional)")
        secondary_doc = st.file_uploader("Upload another document for additional verification", type=["jpg", "jpeg", "png"])
        
        if secondary_doc:
            st.image(secondary_doc, caption="Uploaded Secondary Document", width=300)

    with col2:
        st.subheader("Verification Status")
        
        # Display verification status
        if st.session_state.user_data['documents'].get('id_validated'):
            st.success("ID Document Verified ✓")
        else:
            st.warning("ID Document Not Verified Yet")
        
        # Information about the verification process
        st.info("""
        ## Document Verification Process
        
        1. Upload a clear image of your ID document
        2. Our AI will process the document
        3. The information will be cross-checked with your profile
        4. You'll receive a verification status
        
        Valid documents include:
        - National ID Card
        - Driver's License
        - Passport
        """)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            prev_step()
    
    with col2:
        # Only allow proceeding if the document is validated or user wants to skip
        if st.session_state.user_data['documents'].get('id_validated') or st.button("Skip Verification"):
            next_step()

# Step 4: Social Media Integration
elif st.session_state.step == 4:
    st.header("Social Media & Esports Profiles")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.form("social_media_form"):
            st.subheader("Connect Your Social Media")
            
            # Twitter/X
            twitter_username = st.text_input("Twitter/X Username", value=st.session_state.user_data['social_media'].get('twitter_username', ''))
            
            # Instagram
            instagram_username = st.text_input("Instagram Username", value=st.session_state.user_data['social_media'].get('instagram_username', ''))
            
            # Facebook
            facebook_profile = st.text_input("Facebook Profile URL", value=st.session_state.user_data['social_media'].get('facebook_profile', ''))
            
            # Discord
            discord_username = st.text_input("Discord Username", value=st.session_state.user_data['social_media'].get('discord_username', ''))
            
            st.subheader("Esports Platform Profiles")
            
            # Twitch
            twitch_username = st.text_input("Twitch Username", value=st.session_state.user_data['esports_profiles'].get('twitch_username', ''))
            
            # Steam
            steam_profile = st.text_input("Steam Profile URL", value=st.session_state.user_data['esports_profiles'].get('steam_profile', ''))
            
            # Other gaming platforms
            other_platforms = st.text_area("Other Gaming Platforms (Platform: Username)", value=st.session_state.user_data['esports_profiles'].get('other_platforms', ''))
            
            submitted = st.form_submit_button("Connect & Analyze")
            
            if submitted:
                social_media_data = {
                    'twitter_username': twitter_username,
                    'instagram_username': instagram_username,
                    'facebook_profile': facebook_profile,
                    'discord_username': discord_username
                }
                
                esports_profiles_data = {
                    'twitch_username': twitch_username,
                    'steam_profile': steam_profile,
                    'other_platforms': other_platforms
                }
                
                # Check if at least one social media profile is provided
                if any(social_media_data.values()):
                    save_form_data(social_media_data, 'social_media')
                    
                    # Simulate social media analysis
                    with st.spinner("Analyzing social media profiles..."):
                        social_media_info = extract_social_media_info(social_media_data)
                        st.session_state.user_data['social_media']['analysis'] = social_media_info
                        st.success("Social media profiles analyzed successfully!")
                else:
                    st.warning("Please provide at least one social media profile.")
                
                # Check if at least one esports profile is provided
                if any(esports_profiles_data.values()):
                    save_form_data(esports_profiles_data, 'esports_profiles')
                    
                    # Simulate esports profile analysis
                    with st.spinner("Analyzing esports profiles..."):
                        esports_relevance = analyze_social_relevance(esports_profiles_data, st.session_state.user_data['interests'])
                        st.session_state.user_data['esports_profiles']['relevance'] = esports_relevance
                        st.success("Esports profiles analyzed successfully!")
                else:
                    st.warning("Please provide at least one esports profile.")
    
    with col2:
        st.subheader("Why Connect Social Media?")
        st.info("""
        ## Benefits of Connecting
        
        1. **Personalized Experiences**: Get customized content based on your esports interests.
        
        2. **Community Access**: Join exclusive fan communities for your favorite teams.
        
        3. **Special Offers**: Receive targeted offers for events and merchandise.
        
        4. **Profile Validation**: Verify your status as a genuine esports enthusiast.
        
        Your data is protected and only used to enhance your fan experience.
        """)
        
        # Display a sample esports fan image
        st.image("https://images.unsplash.com/photo-1513151233558-d860c5398176", caption="Esports fans celebrating at an event", use_column_width=True)
    
    # Social media analysis results (if available)
    if 'analysis' in st.session_state.user_data['social_media']:
        st.subheader("Social Media Analysis Results")
        
        analysis = st.session_state.user_data['social_media']['analysis']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Esports Related Posts", analysis.get('esports_posts', 'N/A'))
        with col2:
            st.metric("Team Mentions", analysis.get('team_mentions', 'N/A'))
        with col3:
            st.metric("Engagement Score", analysis.get('engagement_score', 'N/A'))
    
    # Esports profile relevance (if available)
    if 'relevance' in st.session_state.user_data['esports_profiles']:
        st.subheader("Esports Profile Relevance")
        
        relevance = st.session_state.user_data['esports_profiles']['relevance']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Relevance Score", f"{relevance.get('relevance_score', 0)}/10")
        with col2:
            st.metric("Confidence Level", relevance.get('confidence', 'Medium'))
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            prev_step()
    
    with col2:
        if st.button("View Dashboard"):
            next_step()

# Step 5: Dashboard
elif st.session_state.step == 5:
    st.header("Your Fan Profile Dashboard")
    
    # Check if we have user data to display
    if st.session_state.user_data['personal'].get('name'):
        st.subheader(f"Welcome, {st.session_state.user_data['personal']['name']}!")
        
        # Profile summary
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Display a gaming setup image as profile picture
            st.image("https://images.unsplash.com/photo-1598550457678-aa60413d7c80", use_column_width=True)
            
            # Display verification status
            if st.session_state.user_data['documents'].get('id_validated'):
                st.success("✓ Verified Fan")
            else:
                st.warning("⚠ Unverified Fan")
            
            # Basic information
            st.markdown("### Basic Info")
            if 'personal' in st.session_state.user_data:
                personal = st.session_state.user_data['personal']
                st.markdown(f"**Email:** {personal.get('email', 'Not provided')}")
                st.markdown(f"**Location:** {personal.get('city', '')} {', ' + personal.get('state', '') if personal.get('state') else ''}")
        
        with col2:
            # Fan interests visualization
            st.markdown("### Your Esports Interests")
            
            if 'interests' in st.session_state.user_data and st.session_state.user_data['interests']:
                # Create interest chart
                fig = create_interest_chart(st.session_state.user_data['interests'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No interest data available. Complete step 2 to see your interests visualization.")
        
        # Social media insights
        st.markdown("### Social Media Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'analysis' in st.session_state.user_data['social_media']:
                # Create activity timeline
                fig = create_activity_timeline(st.session_state.user_data['social_media']['analysis'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No social media data available. Connect your accounts to see insights.")
        
        with col2:
            # Connected accounts
            st.markdown("### Connected Accounts")
            
            social_media = st.session_state.user_data['social_media']
            esports_profiles = st.session_state.user_data['esports_profiles']
            
            if any(social_media.get(platform) for platform in ['twitter_username', 'instagram_username', 'facebook_profile', 'discord_username']):
                for platform, username in social_media.items():
                    if platform in ['twitter_username', 'instagram_username', 'facebook_profile', 'discord_username'] and username:
                        st.markdown(f"- **{platform.replace('_username', '').replace('_profile', '').title()}**: {username}")
            else:
                st.info("No social media accounts connected.")
            
            st.markdown("### Esports Platforms")
            
            if any(esports_profiles.get(platform) for platform in ['twitch_username', 'steam_profile']):
                for platform, username in esports_profiles.items():
                    if platform in ['twitch_username', 'steam_profile'] and username:
                        st.markdown(f"- **{platform.replace('_username', '').replace('_profile', '').title()}**: {username}")
            else:
                st.info("No esports platform accounts connected.")
        
        # Recommendations based on profile
        st.markdown("### Personalized Recommendations")
        
        recommendations_col1, recommendations_col2, recommendations_col3 = st.columns(3)
        
        with recommendations_col1:
            st.markdown("#### Upcoming Events")
            st.markdown("- FURIA vs. Liquid - June 15")
            st.markdown("- ESL Pro League Season 18 - July 2023")
            st.markdown("- GamesCon Brazil - September 2023")
        
        with recommendations_col2:
            st.markdown("#### Merchandise")
            st.markdown("- Limited Edition Team Jersey")
            st.markdown("- Gaming Peripherals Bundle")
            st.markdown("- Collectible Championship Memorabilia")
        
        with recommendations_col3:
            st.markdown("#### Community")
            st.markdown("- Join the Official Discord")
            st.markdown("- Follow Team Social Media")
            st.markdown("- Participate in Fan Contests")
        
        # Fan images gallery
        st.markdown("### Esports Fan Community")
        
        gallery_col1, gallery_col2, gallery_col3, gallery_col4 = st.columns(4)
        
        with gallery_col1:
            st.image("https://images.unsplash.com/photo-1527529482837-4698179dc6ce", use_column_width=True)
        
        with gallery_col2:
            st.image("https://images.unsplash.com/photo-1593305841991-05c297ba4575", use_column_width=True)
        
        with gallery_col3:
            st.image("https://images.unsplash.com/photo-1516880711640-ef7db81be3e1", use_column_width=True)
        
        with gallery_col4:
            st.image("https://images.unsplash.com/photo-1467810563316-b5476525c0f9", use_column_width=True)
        
        # Export data option
        st.markdown("### Data Management")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("Export Profile Data"):
                # Convert the data to JSON
                profile_json = json.dumps(st.session_state.user_data, indent=4)
                
                # Create a download button
                st.download_button(
                    label="Download JSON",
                    data=profile_json,
                    file_name="esports_fan_profile.json",
                    mime="application/json"
                )
        
        with export_col2:
            if st.button("Start Over"):
                # Reset session state
                st.session_state.user_data = {
                    'personal': {},
                    'interests': {},
                    'documents': {},
                    'social_media': {},
                    'esports_profiles': {}
                }
                st.session_state.step = 1
                st.session_state.progress = 0
                st.rerun()
    else:
        st.warning("No profile data available. Please complete the previous steps.")
        
        if st.button("Start Profile Creation"):
            st.session_state.step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>Know Your Fan Platform &copy; 2023 - Connecting Esports Fans Worldwide</p>
    <p>Privacy Policy | Terms of Service | Data Protection</p>
</div>
""", unsafe_allow_html=True)
