import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
st.header("ChatBot 🤖")

df = pd.read_csv("/Users/testvagrant/Desktop/chatbot/resources/data_frame.csv")


level_df = df['Levels']
scale_df = df['Scale']

options_points = {
    "Regularly": 5,
    "Sometimes": 3,
    "Not Started": 0,
    "Not Applicable": -1,
}

# Function to get questions for a given level and scale
def get_filtered_questions(level, scale):
    return df[(level_df == f"level {level}") & (scale_df == scale)]

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = {}
    st.session_state.question_index = 0
    st.session_state.current_level = 3

# Display questions in sets of 7 at a time
questions_per_page = 7

# Fetch questions for the initial level and scale
filtered_df = get_filtered_questions(st.session_state.current_level, "Agile Practices")

if st.session_state.question_index < len(filtered_df):
    question_batch = filtered_df.iloc[st.session_state.question_index: st.session_state.question_index + questions_per_page]

    with st.form(key='question_form'):
        for index, row in question_batch.iterrows():
            question_id = f"{row['Scale'][0]}{st.session_state.current_level}_{index}"
            st.info(f"Question {question_id}\n : {row['Questions']}")
            user_response = st.selectbox("Select an option:", options_points.keys(), key=f"question_{question_id}")

            # Save user response and points
            st.session_state.responses[question_id] = {
                "Question": row['Questions'],
                "Response": user_response,
                "Points": options_points[user_response]
            }

        # Add a button for the user to proceed to the next set of questions
        next_button_clicked = st.form_submit_button("Next")

    if next_button_clicked:
        st.session_state.question_index += questions_per_page
else:
    st.success("All questions answered. Thank you!")

    # Calculate and display accuracy based on stored responses
    total_points_earned = sum(response["Points"] for response in st.session_state.responses.values())
    total_possible_points = len(filtered_df) * 5
    accuracy = (total_points_earned / total_possible_points) * 100

    # Display accuracy
    st.write(f"Accuracy: {accuracy:.2f}%")

    # Update current_level based on accuracy
    if accuracy > 70:
        st.session_state.current_level += 1
        # ------------------------------------------------graph code
        if st.session_state.current_level == 5:
            df = pd.read_csv('/Users/testvagrant/Desktop/chatbot/src/data_frame.csv')
            df['Points'] = df['Points'].str.wrap(30) 
            df['Points'] = df['Points'].str.replace('\n', '<br>') 
            df['Scale'] = df['Scale'].str.wrap(10) 
            df['Scale'] = df['Scale'].str.replace('\n', '<br>') 
            df['Value'] = df['Value'] + 0.01

            custom_colors = [      
                'rgb(255, 0, 0)',   # Red
                'rgb(255, 80, 0)',  # Orange-Red
                'rgb(255, 120, 0)', # Orange
                'rgb(255, 180, 0)', # Orange-Yellow
                'rgb(255, 220, 0)', # Yellow
                'rgb(200, 220, 0)', # Yellow-Green
                'rgb(150, 220, 0)', # Lime Green
                'rgb(0, 128, 0)', 'rgb(0, 128, 0)'
            ]

            fig = px.sunburst(
                data_frame=df,
                path=['Scale', 'Levels', 'Points'],
                values='Value',
                maxdepth=-2,
                width=800,
                height=800,
                color='Value', 
                custom_data=['Points', 'Questions'],
                color_continuous_scale=custom_colors, # Show label, value, and parent on hover
            )

            fig.update_traces(
                textfont_size=12,
                insidetextorientation='radial', 
                textinfo='label+text+percent entry',  
            )

            fig.update_layout(
                margin=dict(l=10, r=10, b=10, t=10),  # Adjust the values to control spacing
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # graph code end here----------------------------------------
        st.write(f"Congratulations! You've reached Level {st.session_state.current_level}")
    else:
        st.session_state.current_level = 1
        st.write(f"You need to review Level {st.session_state.current_level}")

    # Fetch questions for the updated level
    filtered_df = get_filtered_questions(st.session_state.current_level, "Agile Practices")
    st.session_state.question_index = 0

    # Display questions for the updated level
    st.write("Proceed to the next level:")
    for index, row in filtered_df.iterrows():
        question_id = f"{row['Scale'][0]}{st.session_state.current_level}_{index}"
        st.info(f"Question {question_id}\n : {row['Questions']}")
        user_response = st.selectbox("Select an option:", options_points.keys(), key=f"question_{question_id}")

        # Save user response and points
        st.session_state.responses[question_id] = {
            "Question": row['Questions'],
            "Response": user_response,
            "Points": options_points[user_response]
        }

    # Add a button for the user to proceed to the next set of questions
    next_button_clicked = st.button("Next")

    if next_button_clicked:
        st.session_state.question_index += questions_per_page

    # Reset session state for the next set of questions
    st.session_state.responses = {}
    st.session_state.question_index = 0
