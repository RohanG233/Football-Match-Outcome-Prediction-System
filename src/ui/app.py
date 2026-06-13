import requests
import streamlit as st
import os

API_URL = os.getenv(
    "API_URL",
    "https://football-match-outcome-prediction-system.onrender.com"
)

st.set_page_config(
    page_title="Football Match Outcome Prediction System",
    page_icon="⚽",
    layout="centered"
)

st.title("⚽ Football Match Outcome Prediction System")
st.markdown(
    "Predict the outcome probabilities of an international football match."
)

# ---------------------------
# Load teams from API
# ---------------------------
try:

    response = requests.get(
        f"{API_URL}/teams",
        timeout=5
    )

    teams = response.json()["teams"]

except Exception:

    st.error(
        "Could not connect to API. "
        "Make sure FastAPI server is running."
    )

    st.stop()

# ---------------------------
# Input Section
# ---------------------------
home_team = st.selectbox(
    "Home Team",
    teams
)

away_team = st.selectbox(
    "Away Team",
    teams
)

stage = st.selectbox(
    "Tournament Stage",
    [
        "Group Stage",
        "Round of 16",
        "Quarter-finals",
        "Semi-finals",
        "Final"
    ]
)

# ---------------------------
# Validation
# ---------------------------
if home_team == away_team:
    st.warning(
        "Home team and Away team cannot be the same."
    )

# ---------------------------
# Predict Button
# ---------------------------
predict_clicked = st.button(
    "Predict Match"
)

if predict_clicked:

    if home_team == away_team:

        st.error(
            "Please choose two different teams."
        )

    else:

        payload = {

            "home_team": home_team,
            "away_team": away_team,
            "stage": stage
        }

        with st.spinner(
            "Running prediction model..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/predict",
                    json=payload,
                    timeout=30
                )

                if response.status_code != 200:

                    st.error(
                        response.json().get(
                            "detail",
                            "Prediction failed."
                        )
                    )

                else:

                    result = response.json()

                    st.success(
                        "Prediction completed successfully!"
                    )

                    st.subheader(
                        f"{home_team} vs {away_team}"
                    )

                    st.caption(
                        f"Tournament Stage: {stage}"
                    )

                    home_prob = result[
                        "home_win_probability"
                    ]

                    draw_prob = result[
                        "draw_probability"
                    ]

                    away_prob = result[
                        "away_win_probability"
                    ]

                    # -------------------
                    # Winner Highlight
                    # -------------------
                    winner = max(
                        [
                            ("Home Win", home_prob),
                            ("Draw", draw_prob),
                            ("Away Win", away_prob)
                        ],
                        key=lambda x: x[1]
                    )

                    st.info(
                        f"Most likely outcome: "
                        f"**{winner[0]}** "
                        f"({winner[1]:.2f}%)"
                    )

                    # -------------------
                    # Probability Metrics
                    # -------------------
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            label=f"{home_team} Win",
                            value=f"{home_prob:.2f}%"
                        )

                    with col2:
                        st.metric(
                            label="Draw",
                            value=f"{draw_prob:.2f}%"
                        )

                    with col3:
                        st.metric(
                            label=f"{away_team} Win",
                            value=f"{away_prob:.2f}%"
                        )

                    # -------------------
                    # Progress Bars
                    # -------------------
                    st.markdown("### Probability Breakdown")

                    st.write(
                        f"{home_team} Win"
                    )
                    st.progress(
                        min(
                            int(home_prob),
                            100
                        )
                    )

                    st.write("Draw")
                    st.progress(
                        min(
                            int(draw_prob),
                            100
                        )
                    )

                    st.write(
                        f"{away_team} Win"
                    )
                    st.progress(
                        min(
                            int(away_prob),
                            100
                        )
                    )

                    # -------------------
                    # Raw Response
                    # -------------------
                    with st.expander(
                        "View Raw API Response"
                    ):
                        st.json(result)

            except Exception as e:

                st.error(
                    f"Error communicating with API: {str(e)}"
                )