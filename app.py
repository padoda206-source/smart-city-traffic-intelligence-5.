
import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart City Traffic Intelligence",
    page_icon="🚦",
    layout="wide"
)

# ==========================================
# 2. PROFESSIONAL DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #071426;
    color: white;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: white !important;
}

p, label {
    color: #c3d4e8;
}

.kpi-card {
    background: linear-gradient(135deg, #142b47, #0d2038);
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #245477;
    min-height: 135px;
}

.kpi-label {
    color: #a9c5df;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: white;
    font-size: 32px;
    font-weight: bold;
    margin-top: 12px;
}

.kpi-note {
    color: #7eb8df;
    font-size: 12px;
    margin-top: 8px;
}

.stButton button {
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD AND CLEAN DATA
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv("practice_traffic_data.csv")

    df = df.drop_duplicates()

    df["date_time"] = pd.to_datetime(df["date_time"])

    df["hour"] = df["date_time"].dt.hour
    df["day_of_week"] = df["date_time"].dt.day_of_week

    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    # Cyclical time features
    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )

    df["day_sin"] = np.sin(
        2 * np.pi * df["day_of_week"] / 7
    )

    df["day_cos"] = np.cos(
        2 * np.pi * df["day_of_week"] / 7
    )

    df["rain_1h"] = df["rain_1h"].fillna(
        df["rain_1h"].median()
    )

    df["clouds_all"] = df["clouds_all"].fillna(
        df["clouds_all"].median()
    )

    return df.sort_values(
        "date_time"
    ).reset_index(drop=True)


data = load_data()

# ==========================================
# 4. TRAIN REGULARISED REGRESSION MODEL
# ==========================================

FEATURES = [
    "hour_sin",
    "hour_cos",
    "day_sin",
    "day_cos",
    "is_weekend",
    "temp",
    "rain_1h",
    "clouds_all"
]


def make_model_matrix(X, means=None, scales=None):

    if means is None:
        means = X.mean(axis=0)

    if scales is None:
        scales = X.std(axis=0)

    scales = np.where(scales == 0, 1, scales)

    X_scaled = (X - means) / scales

    return (
        np.column_stack([
            np.ones(len(X_scaled)),
            X_scaled
        ]),
        means,
        scales
    )


@st.cache_resource
def train_model(df):

    X = df[FEATURES].to_numpy(dtype=float)
    y = df["traffic_volume"].to_numpy(dtype=float)

    split_index = int(len(df) * 0.8)

    X_train = X[:split_index]
    X_test = X[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]

    X_train_model, means, scales = make_model_matrix(
        X_train
    )

    X_test_model, _, _ = make_model_matrix(
        X_test,
        means,
        scales
    )

    # Ridge regularisation
    alpha = 10.0

    identity = np.eye(X_train_model.shape[1])
    identity[0, 0] = 0

    coefficients = np.linalg.solve(
        X_train_model.T @ X_train_model + alpha * identity,
        X_train_model.T @ y_train
    )

    predictions = X_test_model @ coefficients

    mae = np.mean(
        np.abs(y_test - predictions)
    )

    rmse = np.sqrt(
        np.mean((y_test - predictions) ** 2)
    )

    ss_total = np.sum(
        (y_test - np.mean(y_test)) ** 2
    )

    ss_residual = np.sum(
        (y_test - predictions) ** 2
    )

    r2 = 1 - ss_residual / ss_total

    comparison = pd.DataFrame({
        "Observation": np.arange(1, len(y_test) + 1),
        "Actual Traffic": y_test,
        "Predicted Traffic": predictions
    })

    return (
        coefficients,
        means,
        scales,
        mae,
        rmse,
        r2,
        comparison
    )


(
    coefficients,
    feature_means,
    feature_scales,
    mae,
    rmse,
    r2,
    comparison
) = train_model(data)

# ==========================================
# 5. TRAFFIC INSIGHTS
# ==========================================

hourly_traffic = (
    data.groupby("hour")["traffic_volume"]
    .mean()
    .reset_index()
)

busiest_hour = hourly_traffic.loc[
    hourly_traffic["traffic_volume"].idxmax()
]

least_busy_hour = hourly_traffic.loc[
    hourly_traffic["traffic_volume"].idxmin()
]

weekday_traffic = data.loc[
    data["is_weekend"] == 0,
    "traffic_volume"
].mean()

weekend_traffic = data.loc[
    data["is_weekend"] == 1,
    "traffic_volume"
].mean()

# ==========================================
# 6. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🚦 SMART CITY")

st.sidebar.caption(
    "TRAFFIC INTELLIGENCE SYSTEM"
)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Traffic Analytics",
        "Weather Analysis",
        "Traffic Prediction",
        "Model Performance",
        "Smart City Insights",
        "Dataset",
        "Project Presentation"
    ]
)

st.sidebar.divider()

st.sidebar.metric(
    "DATA RECORDS",
    f"{len(data):,}"
)

st.sidebar.caption(
    "Educational traffic intelligence prototype"
)

# ==========================================
# 7. MAIN HEADER
# ==========================================

st.title("🚦 SMART CITY TRAFFIC INTELLIGENCE")

st.caption(
    "SMARTER ROADS  |  SAFER CITIES  |  BETTER TOMORROW"
)

st.divider()

# ==========================================
# 8. DASHBOARD
# ==========================================

if page == "Dashboard":

    st.subheader("📊 TRAFFIC AT A GLANCE")

    avg_traffic = data["traffic_volume"].mean()
    peak_traffic = data["traffic_volume"].max()
    low_traffic = data["traffic_volume"].min()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">AVERAGE TRAFFIC</div>
            <div class="kpi-value">{avg_traffic:,.0f}</div>
            <div class="kpi-note">Mean recorded traffic volume</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">PEAK TRAFFIC</div>
            <div class="kpi-value">{peak_traffic:,}</div>
            <div class="kpi-note">Highest recorded traffic volume</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">LOWEST TRAFFIC</div>
            <div class="kpi-value">{low_traffic:,}</div>
            <div class="kpi-note">Lowest recorded traffic volume</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📈 TRAFFIC VOLUME MONITORING")

    st.line_chart(
        data,
        x="date_time",
        y="traffic_volume",
        color="#00C8FF",
        height=350
    )

    st.subheader("🕒 HOURLY TRAFFIC PATTERN")

    st.bar_chart(
        hourly_traffic,
        x="hour",
        y="traffic_volume",
        color="#00C8FF"
    )

    st.info(
        f"The busiest average hour in this dataset is "
        f"{int(busiest_hour['hour']):02d}:00."
    )

# ==========================================
# 9. TRAFFIC ANALYTICS
# ==========================================

elif page == "Traffic Analytics":

    st.subheader("📈 TRAFFIC ANALYTICS")

    st.write(
        "Explore traffic patterns across different hours."
    )

    st.bar_chart(
        hourly_traffic,
        x="hour",
        y="traffic_volume",
        color="#00C8FF"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Busiest Hour",
        f"{int(busiest_hour['hour']):02d}:00"
    )

    col2.metric(
        "Least Busy Hour",
        f"{int(least_busy_hour['hour']):02d}:00"
    )

    st.subheader("Traffic Distribution")

    st.area_chart(
        data,
        x="date_time",
        y="traffic_volume",
        color="#00C8FF"
    )

# ==========================================
# 10. WEATHER ANALYSIS
# ==========================================

elif page == "Weather Analysis":

    st.subheader("🌦️ WEATHER-WISE TRAFFIC ANALYSIS")

    weather_traffic = (
        data.groupby("weather_main")["traffic_volume"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.bar_chart(
        weather_traffic,
        x="weather_main",
        y="traffic_volume",
        color="#00C8FF"
    )

    st.subheader("Weather Statistics")

    st.dataframe(
        weather_traffic,
        width="stretch",
        hide_index=True
    )

# ==========================================
# 11. TRAFFIC PREDICTION
# ==========================================

elif page == "Traffic Prediction":

    st.subheader("🤖 AI-POWERED TRAFFIC PREDICTION")

    st.write(
        "Enter the conditions to estimate traffic volume."
    )

    col1, col2 = st.columns(2)

    with col1:

        hour = st.slider(
            "Hour of the day",
            0, 23, 8
        )

        day_name = st.selectbox(
            "Day of the week",
            [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ]
        )

        temperature = st.number_input(
            "Temperature (Kelvin)",
            min_value=200.0,
            max_value=330.0,
            value=290.0,
            step=1.0
        )

    with col2:

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.5
        )

        cloud_coverage = st.slider(
            "Cloud coverage (%)",
            0, 100, 40
        )

    day_number = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ].index(day_name)

    is_weekend = 1 if day_number >= 5 else 0

    st.divider()

    if st.button(
        "🔮 PREDICT TRAFFIC VOLUME",
        width="stretch"
    ):

        hour_sin = np.sin(
            2 * np.pi * hour / 24
        )

        hour_cos = np.cos(
            2 * np.pi * hour / 24
        )

        day_sin = np.sin(
            2 * np.pi * day_number / 7
        )

        day_cos = np.cos(
            2 * np.pi * day_number / 7
        )

        input_values = np.array([[
            hour_sin,
            hour_cos,
            day_sin,
            day_cos,
            is_weekend,
            temperature,
            rainfall,
            cloud_coverage
        ]], dtype=float)

        scaled_input = (
            input_values - feature_means
        ) / feature_scales

        input_model = np.column_stack([
            np.ones(1),
            scaled_input
        ])

        prediction = float(
            (input_model @ coefficients).item()
        )

        prediction = max(0, prediction)

        st.success("Traffic prediction generated!")

        st.metric(
            "Estimated Traffic Volume",
            f"{prediction:,.0f}"
        )

        if prediction >= 2500:

            st.warning(
                "High estimated traffic. Congestion may be possible."
            )

        elif prediction >= 1500:

            st.info(
                "Moderate estimated traffic."
            )

        else:

            st.success(
                "Low estimated traffic."
            )

        st.divider()

        st.subheader("🔍 PREDICTION EXPLANATION")

        st.write(
            "The model used the following conditions:"
        )

        result_data = pd.DataFrame({
            "Input": [
                "Hour",
                "Day",
                "Temperature",
                "Rainfall",
                "Cloud Coverage",
                "Weekend"
            ],
            "Selected Value": [
                f"{hour}:00",
                day_name,
                f"{temperature} K",
                f"{rainfall} mm",
                f"{cloud_coverage}%",
                "Yes" if is_weekend else "No"
            ]
        })

        st.dataframe(
            result_data,
            width="stretch",
            hide_index=True
        )

        st.info(
            "The estimate is calculated from the combined input "
            "features using a trained regression model. It is not "
            "a live traffic measurement."
        )

        prediction_download = pd.DataFrame({
            "Hour": [hour],
            "Day": [day_name],
            "Temperature_K": [temperature],
            "Rainfall_mm": [rainfall],
            "Cloud_Coverage": [cloud_coverage],
            "Predicted_Traffic": [round(prediction)]
        })

        st.download_button(
            "⬇️ Download Prediction",
            data=prediction_download.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="traffic_prediction.csv",
            mime="text/csv"
        )

# ==========================================
# 12. MODEL PERFORMANCE
# ==========================================

elif page == "Model Performance":

    st.subheader("📊 MODEL PERFORMANCE ANALYSIS")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", f"{mae:.2f}")
    col2.metric("RMSE", f"{rmse:.2f}")
    col3.metric("R² SCORE", f"{r2:.3f}")

    st.divider()

    st.subheader("Actual vs Predicted Traffic")

    chart_data = comparison.set_index(
        "Observation"
    )

    st.line_chart(
        chart_data[
            ["Actual Traffic", "Predicted Traffic"]
        ],
        height=400
    )

    st.subheader("Prediction Comparison")

    st.dataframe(
        comparison.head(20).round(0),
        width="stretch",
        hide_index=True
    )

    st.download_button(
        "⬇️ Download All Model Predictions",
        data=comparison.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="model_predictions.csv",
        mime="text/csv"
    )

    st.caption(
        "MAE and RMSE measure prediction errors. "
        "R² measures how much variation the model explains. "
        "Results are from a held-out portion of the simulated dataset."
    )

# ==========================================
# 13. SMART CITY INSIGHTS
# ==========================================

elif page == "Smart City Insights":

    st.subheader("🏙️ SMART CITY TRAFFIC INSIGHTS")

    col1, col2 = st.columns(2)

    col1.metric(
        "Busiest Hour",
        f"{int(busiest_hour['hour']):02d}:00",
        f"{busiest_hour['traffic_volume']:,.0f} average"
    )

    col2.metric(
        "Least Busy Hour",
        f"{int(least_busy_hour['hour']):02d}:00",
        f"{least_busy_hour['traffic_volume']:,.0f} average"
    )

    st.divider()

    st.subheader("Weekday vs Weekend Traffic")

    day_comparison = pd.DataFrame({
        "Day Type": ["Weekdays", "Weekends"],
        "Average Traffic": [
            weekday_traffic,
            weekend_traffic
        ]
    })

    st.bar_chart(
        day_comparison,
        x="Day Type",
        y="Average Traffic",
        color="#00C8FF"
    )

    difference = weekday_traffic - weekend_traffic

    if difference > 0:

        st.info(
            f"Weekday average traffic is {difference:,.0f} "
            "higher than weekend average traffic."
        )

    elif difference < 0:

        st.info(
            f"Weekend average traffic is {abs(difference):,.0f} "
            "higher than weekday average traffic."
        )

    else:

        st.info(
            "Weekday and weekend averages are equal."
        )

    st.divider()

    st.subheader("Automated Insights")

    st.write(
        f"• Busiest hour: {int(busiest_hour['hour']):02d}:00"
    )

    st.write(
        f"• Least busy hour: {int(least_busy_hour['hour']):02d}:00"
    )

    st.write(
        f"• Weekday average: {weekday_traffic:,.0f}"
    )

    st.write(
        f"• Weekend average: {weekend_traffic:,.0f}"
    )

# ==========================================
# 14. DATASET
# ==========================================

elif page == "Dataset":

    st.subheader("📁 TRAFFIC DATASET")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Records",
        f"{len(data):,}"
    )

    col2.metric(
        "Total Columns",
        len(data.columns)
    )

    st.dataframe(
        data,
        width="stretch",
        height=450
    )

    st.download_button(
        "⬇️ Download Cleaned Dataset",
        data=data.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="cleaned_traffic_data.csv",
        mime="text/csv"
    )

# ==========================================
# 15. PROJECT PRESENTATION
# ==========================================

elif page == "Project Presentation":

    st.subheader("🎤 PROJECT PRESENTATION")

    st.markdown("""
    ## Smart City Traffic Intelligence

    **Our objective**

    To analyse traffic patterns and estimate traffic volume
    using data analysis and a machine learning model.

    ---

    ### Problem Statement

    Increasing traffic creates challenges for urban mobility,
    travel planning and efficient road management.

    ### Our Solution

    We developed an interactive dashboard that:

    1. Analyses traffic patterns.
    2. Studies weather-related traffic trends.
    3. Identifies busy and less busy hours.
    4. Estimates traffic volume using regression.
    5. Presents findings through interactive visualisations.

    ### Technology Stack

    - Python — programming language
    - Pandas — data cleaning and analysis
    - NumPy — numerical calculations
    - Streamlit — interactive dashboard
    - Jupyter Notebook — data exploration

    ### Machine Learning

    We implemented regularised linear regression.

    The model learns relationships between traffic volume
    and input features such as time, day and weather.

    ### Evaluation

    - MAE — Mean Absolute Error
    - RMSE — Root Mean Squared Error
    - R² — Explained variation in the test data

    ### Future Scope

    - Integration with live traffic data.
    - Real-time traffic monitoring.
    - Accident and road-closure information.
    - More advanced prediction models.
    - Traffic management recommendations.

    ---

    ### Important Limitation

    This prototype uses a simulated practice dataset.
    It demonstrates the workflow but has not been validated
    on live city traffic data.
    """)

    st.divider()

    st.subheader("Current Model Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", f"{mae:.2f}")
    col2.metric("RMSE", f"{rmse:.2f}")
    col3.metric("R²", f"{r2:.3f}")

    st.caption(
        "Use these actual results when explaining the model to judges."
    )

# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.caption(
    "SMART CITY TRAFFIC INTELLIGENCE | EDUCATIONAL PROTOTYPE"
)

st.caption(
    "Simulated practice dataset — not live traffic information."
)
