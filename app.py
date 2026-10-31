import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart City Traffic Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. FUTURISTIC UI DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --cyan: #00e5ff;
    --blue: #3988ff;
    --purple: #a855f7;
    --pink: #ec4899;
    --green: #39e6b0;
    --text: #eaf4ff;
    --muted: #a8bfd8;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #172b50 0%, transparent 40%),
        radial-gradient(ellipse at 90% 10%, #251747 0%, transparent 35%),
        linear-gradient(145deg, #050d1b, #0b1730 55%, #10152b);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #081326, #11132c);
    border-right: 1px solid #29456e;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--text);
}

/* BRAND LOGO */

.brand-mark {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 16px 12px;
    margin-bottom: 18px;
    background: linear-gradient(120deg, #102d50, #251847);
    border: 1px solid #35639a;
    border-radius: 15px;
    box-shadow: 0 0 22px #087bff25;
}

.brand-icon {
    font-size: 34px;
}

.brand-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 19px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #ffffff;
    text-shadow: 0 0 12px #00d9ff;
}

.brand-subtitle {
    font-size: 9px;
    letter-spacing: 2px;
    color: var(--cyan);
    font-weight: 700;
    margin-top: 4px;
}

/* TOP LABEL */

.tag {
    display: inline-block;
    color: var(--cyan);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    padding: 7px 13px;
    border: 1px solid #00cfff65;
    border-radius: 7px;
    background: #00cfff12;
    margin-bottom: 12px;
}

/* MAIN PAGE TITLE */

.page-heading {
    padding: 12px 0 20px 0;
    margin-bottom: 12px;
}

.page-heading h1 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: clamp(27px, 4vw, 43px) !important;
    font-weight: 800 !important;
    letter-spacing: 1px;
    line-height: 1.3;
    background: linear-gradient(90deg, #ffffff, #00e5ff, #9b7bff, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px #00cfff30;
    margin: 0 !important;
}

.heading-accent {
    width: 145px;
    height: 4px;
    margin-top: 15px;
    border-radius: 10px;
    background: linear-gradient(90deg, #00e5ff, #8b5cf6, transparent);
    box-shadow: 0 0 15px #00d9ff;
}

.page-description {
    color: #a8bfd8;
    font-size: 14px;
    margin-top: 12px;
}

/* SECTION HEADING BARS */

.stMarkdown h3 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    color: #ffffff !important;
    background: linear-gradient(90deg, #12385a, #172343 75%, #171b35);
    border-left: 5px solid var(--cyan);
    border-bottom: 1px solid #3979a8;
    border-radius: 7px;
    padding: 13px 16px;
    margin-top: 25px;
    margin-bottom: 17px;
    text-shadow: 0 0 12px #00d9ff65;
    box-shadow: 0 4px 18px #00000025;
}

/* SUBHEADINGS */

.stMarkdown h4 {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    color: #9edcff !important;
    padding: 8px 12px;
    border-left: 3px solid #a855f7;
    border-radius: 4px;
    background: linear-gradient(90deg, #a855f71c, transparent);
    margin-top: 18px;
    margin-bottom: 12px;
}

/* HERO PANEL */

.hero {
    background:
        radial-gradient(circle at 90% 10%, #8b5cf630, transparent 35%),
        linear-gradient(120deg, #10365c, #111e3c 65%, #211b42);
    padding: 30px;
    border: 1px solid #3c75a8;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0 0 28px #087bff20;
}

.hero h2 {
    font-family: 'Orbitron', sans-serif;
    color: #ffffff;
    font-size: 24px;
    text-shadow: 0 0 15px #00d9ff50;
}

.hero p {
    color: #c6ddf5;
    margin-bottom: 0;
}

/* METRIC CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #142e50, #151d3a);
    border: 1px solid #35618e;
    border-radius: 15px;
    padding: 18px 20px;
    box-shadow: 0 5px 20px #00000030;
}

[data-testid="stMetricLabel"] {
    color: #a9c8e8 !important;
    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {
    color: #00e5ff !important;
    font-family: 'Orbitron', sans-serif;
    text-shadow: 0 0 12px #00d9ff55;
}

[data-testid="stMetricDelta"] {
    color: #39e6b0 !important;
}

/* TEXT */

p, label, li {
    color: #c7d8ec;
}

.small-note {
    color: #9bb6d2;
    font-size: 13px;
}

hr {
    border-color: #29466b;
}

/* INPUTS AND BUTTONS */

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    border: 1px solid #3988ff;
    background: linear-gradient(100deg, #1553a0, #5935a5);
    color: white;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    border: 1px solid #00e5ff;
    box-shadow: 0 0 15px #00d9ff60;
    color: white;
}

div[data-baseweb="select"] > div {
    background-color: #11243d;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #315276 !important;
    border-radius: 14px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #315276;
    border-radius: 10px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. LOAD AND CLEAN DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("practice_traffic_data.csv")

    required = [
        "date_time", "traffic_volume", "temp",
        "rain_1h", "clouds_all"
    ]

    missing_columns = [
        c for c in required if c not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required columns missing: " + ", ".join(missing_columns)
        )

    original_rows = len(df)
    df = df.drop_duplicates().copy()

    df["date_time"] = pd.to_datetime(
        df["date_time"], errors="coerce"
    )

    for column in [
        "traffic_volume", "temp", "rain_1h", "clouds_all"
    ]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df = df.dropna(
        subset=["date_time", "traffic_volume", "temp"]
    ).copy()

    for column in ["rain_1h", "clouds_all"]:
        median = df[column].median()
        df[column] = df[column].fillna(
            0 if pd.isna(median) else median
        )

    if "holiday" in df.columns:
        df["holiday"] = df["holiday"].fillna(
            "Unknown"
        ).astype(str)
    else:
        df["holiday"] = "Unknown"

    for column in ["weather_main", "weather_description"]:
        if column not in df.columns:
            df[column] = "Unknown"

    df = df.sort_values("date_time").reset_index(drop=True)

    df["hour"] = df["date_time"].dt.hour
    df["day_of_week"] = df["date_time"].dt.dayofweek
    df["day_name"] = df["date_time"].dt.day_name()
    df["date"] = df["date_time"].dt.date
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["day_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

    return df, original_rows


try:
    data, original_rows = load_data()
except Exception as exc:
    st.error(f"Could not load dataset: {exc}")
    st.info("Keep practice_traffic_data.csv in the same folder as app.py.")
    st.stop()

if len(data) < 20:
    st.error("The dataset needs at least 20 valid rows.")
    st.stop()


# =========================================================
# 4. TRAIN REGULARISED LINEAR REGRESSION
# =========================================================

FEATURES = [
    "hour_sin", "hour_cos",
    "day_sin", "day_cos",
    "is_weekend", "temp",
    "rain_1h", "clouds_all"
]


def make_model_matrix(X, means=None, scales=None):
    if means is None:
        means = X.mean(axis=0)

    if scales is None:
        scales = X.std(axis=0)

    scales = np.where(scales == 0, 1, scales)
    X_scaled = (X - means) / scales

    X_model = np.column_stack([
        np.ones(len(X_scaled)), X_scaled
    ])

    return X_model, means, scales


@st.cache_resource
def train_model(df):
    X = df[FEATURES].to_numpy(dtype=float)
    y = df["traffic_volume"].to_numpy(dtype=float)

    split_index = int(len(df) * 0.8)
    split_index = min(max(split_index, 1), len(df) - 1)

    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    X_train_model, means, scales = make_model_matrix(X_train)
    X_test_model, _, _ = make_model_matrix(
        X_test, means, scales
    )

    alpha = 10.0
    identity = np.eye(X_train_model.shape[1])
    identity[0, 0] = 0

    coefficients = np.linalg.solve(
        X_train_model.T @ X_train_model + alpha * identity,
        X_train_model.T @ y_train
    )

    predictions = X_test_model @ coefficients

    mae = float(np.mean(np.abs(y_test - predictions)))
    rmse = float(np.sqrt(np.mean((y_test - predictions) ** 2)))

    ss_total = float(np.sum((y_test - np.mean(y_test)) ** 2))
    ss_residual = float(np.sum((y_test - predictions) ** 2))

    r2 = (
        float(1 - ss_residual / ss_total)
        if ss_total > 0 else float("nan")
    )

    comparison = pd.DataFrame({
        "Date and time": df["date_time"].iloc[split_index:].values,
        "Actual traffic": y_test,
        "Predicted traffic": predictions,
        "Absolute error": np.abs(y_test - predictions)
    })

    return (
        coefficients, means, scales,
        mae, rmse, r2, comparison, split_index
    )


(
    coefficients, feature_means, feature_scales,
    mae, rmse, r2, comparison, split_index
) = train_model(data)


def predict_traffic(hour, day_of_week, temp, rain, clouds):
    is_weekend = int(day_of_week >= 5)

    raw = np.array([[
        np.sin(2 * np.pi * hour / 24),
        np.cos(2 * np.pi * hour / 24),
        np.sin(2 * np.pi * day_of_week / 7),
        np.cos(2 * np.pi * day_of_week / 7),
        is_weekend, temp, rain, clouds
    ]], dtype=float)

    scaled = (raw - feature_means) / np.where(
        feature_scales == 0, 1, feature_scales
    )

    model_input = np.column_stack([
        np.ones(len(scaled)), scaled
    ])

    prediction = float((model_input @ coefficients)[0])
    return max(0, prediction)


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================

pages = [
    "🏠 Overview",
    "📈 Traffic Analytics",
    "🌦️ Weather Analysis",
    "🤖 Traffic Prediction",
    "🎯 Model Performance",
    "💡 Smart City Insights",
    "🗂️ Dataset Explorer",
    "🏆 Project Presentation"
]

with st.sidebar:
    st.markdown("""
    <div class="brand-mark">
        <div class="brand-icon">🚦</div>
        <div>
            <div class="brand-name">SMART CITY</div>
            <div class="brand-subtitle">TRAFFIC INTELLIGENCE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("CONTROL CENTRE / DASHBOARD")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        pages,
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.success("Dataset loaded")
    st.success("Prediction model ready")
    st.caption("Educational prototype • Simulated dataset")


# =========================================================
# 6. COMMON PAGE HEADER
# =========================================================

st.markdown("""
<div class="tag">DATA-DRIVEN URBAN MOBILITY</div>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="page-heading">
        <h1>{page}</h1>
        <div class="heading-accent"></div>
        <div class="page-description">
            Explore traffic patterns, understand contributing factors
            and estimate traffic volume.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# 7. OVERVIEW
# =========================================================

if page == "🏠 Overview":

    avg_traffic = data["traffic_volume"].mean()
    max_traffic = data["traffic_volume"].max()
    peak_hour = int(
        data.groupby("hour")["traffic_volume"].mean().idxmax()
    )

    st.markdown("""
    <div class="hero">
        <div class="tag">SMART MOBILITY • DATA • MACHINE LEARNING</div>
        <h2>Understand traffic. Discover patterns. Plan smarter.</h2>
        <p>A data analytics dashboard that explores traffic trends
        and demonstrates how machine learning can estimate traffic volume.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valid records", f"{len(data):,}")
    c2.metric("Average traffic", f"{avg_traffic:,.0f}")
    c3.metric("Highest recorded", f"{max_traffic:,.0f}")
    c4.metric("Busiest hour", f"{peak_hour:02d}:00")

    st.markdown("### 📊 TRAFFIC AT A GLANCE")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Hourly traffic profile")
        hourly = data.groupby("hour")[
            "traffic_volume"
        ].mean().reindex(range(24))
        st.bar_chart(hourly, x_label="Hour", y_label="Average traffic")

    with right:
        st.markdown("#### Traffic over time")
        daily = data.groupby("date")["traffic_volume"].mean()
        st.line_chart(daily, x_label="Date", y_label="Average traffic")

    st.markdown("### 🤖 MODEL SNAPSHOT")
    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{mae:,.2f}")
    m2.metric("RMSE", f"{rmse:,.2f}")
    m3.metric("R² score", f"{r2:.3f}" if np.isfinite(r2) else "N/A")

    st.info(
        "The supplied practice dataset is simulated. These results are "
        "a demonstration, not a validated forecast of live city traffic."
    )


# =========================================================
# 8. TRAFFIC ANALYTICS
# =========================================================

elif page == "📈 Traffic Analytics":

    st.markdown("### 📈 TRAFFIC PATTERN ANALYSIS")

    min_date = data["date_time"].min().date()
    max_date = data["date_time"].max().date()

    if min_date != max_date:
        start_date, end_date = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    else:
        start_date, end_date = min_date, max_date

    filtered = data[
        (data["date_time"].dt.date >= start_date)
        & (data["date_time"].dt.date <= end_date)
    ].copy()

    if filtered.empty:
        st.warning("No records available for this date range.")
        st.stop()

    a, b, c = st.columns(3)
    a.metric("Records in range", f"{len(filtered):,}")
    b.metric("Average traffic", f"{filtered['traffic_volume'].mean():,.0f}")
    c.metric("Maximum traffic", f"{filtered['traffic_volume'].max():,.0f}")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Hourly traffic profile")
        hourly = filtered.groupby("hour")[
            "traffic_volume"
        ].mean().reindex(range(24))
        st.bar_chart(hourly, x_label="Hour", y_label="Average traffic")

    with right:
        st.markdown("#### Daily traffic trend")
        daily = filtered.groupby("date")["traffic_volume"].mean()
        st.line_chart(daily, x_label="Date", y_label="Average traffic")

    st.markdown("### 📅 WEEKLY TRAFFIC PATTERN")

    day_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]

    by_day = filtered.groupby("day_name")[
        "traffic_volume"
    ].mean().reindex(day_order)

    st.bar_chart(by_day, x_label="Day", y_label="Average traffic")

    st.markdown("### 🌊 TRAFFIC DISTRIBUTION")

    st.area_chart(
        filtered[["traffic_volume"]].reset_index(drop=True),
        x_label="Record",
        y_label="Traffic volume"
    )


# =========================================================
# 9. WEATHER ANALYSIS
# =========================================================

elif page == "🌦️ Weather Analysis":

    st.markdown("### 🌦️ WEATHER AND TRAFFIC ANALYSIS")

    w1, w2 = st.columns(2)

    with w1:
        st.markdown("#### Traffic by weather condition")
        weather_avg = data.groupby("weather_main")[
            "traffic_volume"
        ].mean().sort_values(ascending=False)
        st.bar_chart(weather_avg, x_label="Weather", y_label="Average traffic")

    with w2:
        st.markdown("#### Cloud cover and traffic")
        cloud_bins = pd.cut(
            data["clouds_all"],
            bins=[-1, 20, 40, 60, 80, 100],
            labels=["0–20", "21–40", "41–60", "61–80", "81–100"]
        )
        cloud_summary = data.assign(
            cloud_group=cloud_bins
        ).groupby("cloud_group", observed=False)[
            "traffic_volume"
        ].mean()
        st.bar_chart(
            cloud_summary,
            x_label="Cloud cover group",
            y_label="Average traffic"
        )

    st.markdown("### 🌧️ RAINFALL ANALYSIS")

    rain_summary = data.copy()
    rain_summary["rain_group"] = pd.cut(
        rain_summary["rain_1h"],
        bins=[-0.001, 0, 1, 5, 10, np.inf],
        labels=["No rain", "0–1", "1–5", "5–10", "Above 10"]
    )

    rain_avg = rain_summary.groupby(
        "rain_group", observed=False
    )["traffic_volume"].mean()

    st.bar_chart(rain_avg, x_label="Rainfall group", y_label="Average traffic")

    st.caption(
        "These charts show associations in the supplied dataset. "
        "They do not prove that weather caused a traffic change."
    )


# =========================================================
# 10. TRAFFIC PREDICTION
# =========================================================

elif page == "🤖 Traffic Prediction":

    st.markdown("### 🤖 SMART TRAFFIC ESTIMATOR")
    st.write(
        "Choose a time and weather conditions to generate an estimate "
        "from the trained regression model."
    )

    with st.form("prediction_form"):

        c1, c2 = st.columns(2)

        with c1:
            selected_date = st.date_input("Date", value=date.today())
            selected_time = st.time_input("Time", value=time(8, 0))

            temp_min = float(data["temp"].min())
            temp_max = float(data["temp"].max())

            if temp_min == temp_max:
                temp_max = temp_min + 1

            temperature = st.number_input(
                "Temperature (dataset units)",
                min_value=temp_min,
                max_value=temp_max,
                value=float(data["temp"].median())
            )

        with c2:
            rain_min = max(0.0, float(data["rain_1h"].min()))
            rain_max = max(rain_min + 1.0, float(data["rain_1h"].max()))

            rainfall = st.number_input(
                "Rainfall in the last hour",
                min_value=rain_min,
                max_value=rain_max,
                value=float(np.clip(
                    data["rain_1h"].median(), rain_min, rain_max
                )),
                step=0.1
            )

            cloud_cover = st.slider(
                "Cloud cover",
                min_value=0,
                max_value=100,
                value=int(np.clip(data["clouds_all"].median(), 0, 100))
            )

        submitted = st.form_submit_button(
            "🚦 ESTIMATE TRAFFIC",
            use_container_width=True
        )

    if submitted:
        prediction = predict_traffic(
            selected_time.hour,
            selected_date.weekday(),
            temperature,
            rainfall,
            cloud_cover
        )

        st.divider()
        st.markdown("### 🎯 PREDICTION RESULT")

        r1, r2 = st.columns(2)
        r1.metric("Estimated traffic volume", f"{prediction:,.0f}")
        r2.metric("Selected time", selected_time.strftime("%H:%M"))

        st.caption(
            f"Date: {selected_date.strftime('%d %B %Y')} • "
            f"{selected_date.strftime('%A')}"
        )

        if prediction >= 2500:
            st.warning("Demo category: Higher traffic estimate.")
            category = "Higher"
        elif prediction >= 1500:
            st.info("Demo category: Moderate traffic estimate.")
            category = "Moderate"
        else:
            st.success("Demo category: Lower traffic estimate.")
            category = "Lower"

        st.caption(
            "These category thresholds are illustrative demo settings, "
            "not official congestion standards. This is not a live forecast."
        )

        result = pd.DataFrame([{
            "Date": str(selected_date),
            "Time": selected_time.strftime("%H:%M"),
            "Day": selected_date.strftime("%A"),
            "Temperature": temperature,
            "Rainfall": rainfall,
            "Cloud cover": cloud_cover,
            "Estimated traffic volume": round(prediction, 2),
            "Demo category": category
        }])

        st.download_button(
            "⬇️ Download prediction",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name="traffic_prediction.csv",
            mime="text/csv"
        )


# =========================================================
# 11. MODEL PERFORMANCE
# =========================================================

elif page == "🎯 Model Performance":

    st.markdown("### 🎯 MODEL PERFORMANCE CENTRE")

    c1, c2, c3 = st.columns(3)
    c1.metric("MAE", f"{mae:,.2f}")
    c2.metric("RMSE", f"{rmse:,.2f}")
    c3.metric("R² score", f"{r2:.3f}" if np.isfinite(r2) else "N/A")

    st.markdown("### 📘 UNDERSTANDING THE METRICS")

    with st.expander("What does MAE mean?"):
        st.write(
            "Mean Absolute Error is the average absolute difference "
            "between actual and predicted traffic values. Lower is better."
        )

    with st.expander("What does RMSE mean?"):
        st.write(
            "Root Mean Squared Error penalises larger errors more heavily. "
            "Lower is generally better."
        )

    with st.expander("What does R² mean?"):
        st.write(
            "An R² score of 0.479 means the model explains about 47.9% "
            "of the test-set variation relative to a mean-based baseline. "
            "It does not mean 47.9% of predictions are correct."
        )

    st.markdown("### 📊 ACTUAL VS PREDICTED TRAFFIC")

    st.line_chart(
        comparison.set_index("Date and time")[
            ["Actual traffic", "Predicted traffic"]
        ],
        x_label="Date and time",
        y_label="Traffic volume"
    )

    st.markdown("### ERROR DISTRIBUTION")

    st.bar_chart(
        comparison[["Absolute error"]].reset_index(drop=True),
        x_label="Test observation",
        y_label="Absolute error"
    )

    st.markdown("### TEST-SET COMPARISON")

    st.dataframe(comparison.round(2), use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download model evaluation",
        data=comparison.to_csv(index=False).encode("utf-8"),
        file_name="model_evaluation.csv",
        mime="text/csv"
    )

    st.info(
        f"Training records: {split_index:,} | "
        f"Testing records: {len(comparison):,}. "
        "The dataset is simulated, so these metrics are not evidence "
        "of real-world traffic accuracy."
    )


# =========================================================
# 12. SMART CITY INSIGHTS
# =========================================================

elif page == "💡 Smart City Insights":

    st.markdown("### 💡 SMART CITY INTELLIGENCE")

    hourly = data.groupby("hour")[
        "traffic_volume"
    ].mean().reindex(range(24))

    peak_hour = int(hourly.idxmax())
    quiet_hour = int(hourly.idxmin())

    weekday_avg = data.loc[
        data["is_weekend"] == 0, "traffic_volume"
    ].mean()

    weekend_avg = data.loc[
        data["is_weekend"] == 1, "traffic_volume"
    ].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Busiest average hour", f"{peak_hour:02d}:00")
    c2.metric("Quietest average hour", f"{quiet_hour:02d}:00")
    c3.metric(
        "Weekday average",
        f"{weekday_avg:,.0f}" if pd.notna(weekday_avg) else "N/A"
    )

    st.markdown("### 🔍 KEY OBSERVATIONS")

    st.markdown(
        f"- **Peak period:** Highest average traffic occurs at "
        f"approximately **{peak_hour:02d}:00**."
    )

    st.markdown(
        f"- **Quieter period:** Lowest average traffic occurs at "
        f"approximately **{quiet_hour:02d}:00**."
    )

    if pd.notna(weekday_avg) and pd.notna(weekend_avg):
        if weekday_avg > weekend_avg:
            st.markdown(
                "- **Weekday/weekend pattern:** Weekday average traffic "
                "is higher in this dataset."
            )
        elif weekend_avg > weekday_avg:
            st.markdown(
                "- **Weekday/weekend pattern:** Weekend average traffic "
                "is higher in this dataset."
            )
        else:
            st.markdown("- **Weekday/weekend pattern:** The averages are equal.")

    st.markdown("### 📅 WEEKDAY VS WEEKEND")

    comparison_day = pd.DataFrame({
        "Day type": ["Weekday", "Weekend"],
        "Average traffic": [weekday_avg, weekend_avg]
    }).set_index("Day type")

    st.bar_chart(comparison_day, y_label="Average traffic")

    st.markdown("### 🏙️ POTENTIAL SMART CITY IDEAS")

    st.markdown("""
    - Review high-traffic time windows when planning signal timings.
    - Compare traffic patterns across weekdays and weekends.
    - Combine traffic observations with roadworks, incidents and public
      transport data before making operational decisions.
    - Validate findings with real sensor or traffic authority data.
    """)

    st.caption(
        "These are exploratory observations from the practice dataset, "
        "not verified recommendations for a real city."
    )


# =========================================================
# 13. DATASET EXPLORER
# =========================================================

elif page == "🗂️ Dataset Explorer":

    st.markdown("### 🗂️ DATASET CONTROL ROOM")

    c1, c2, c3 = st.columns(3)
    c1.metric("Original rows", f"{original_rows:,}")
    c2.metric("Cleaned rows", f"{len(data):,}")
    c3.metric(
        "Removed duplicate rows",
        f"{original_rows - len(data):,}"
    )

    st.markdown("### 🔎 FILTER THE RECORDS")

    available_weather = sorted(
        data["weather_main"].dropna().astype(str).unique().tolist()
    )

    selected_weather = st.multiselect(
        "Weather conditions",
        available_weather,
        default=available_weather
    )

    min_volume = float(data["traffic_volume"].min())
    max_volume = float(data["traffic_volume"].max())

    traffic_range = st.slider(
        "Traffic volume range",
        min_value=min_volume,
        max_value=max_volume,
        value=(min_volume, max_volume)
    )

    filtered = data[
        data["weather_main"].astype(str).isin(selected_weather)
        & data["traffic_volume"].between(
            traffic_range[0], traffic_range[1]
        )
    ].copy()

    st.write(f"Showing **{len(filtered):,}** matching records.")

    visible_columns = [
        c for c in [
            "date_time", "traffic_volume", "hour", "day_name",
            "temp", "rain_1h", "clouds_all",
            "weather_main", "weather_description", "holiday"
        ] if c in filtered.columns
    ]

    st.dataframe(
        filtered[visible_columns],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 📊 SUMMARY STATISTICS")

    st.dataframe(
        filtered[
            ["traffic_volume", "temp", "rain_1h", "clouds_all"]
        ].describe().round(2),
        use_container_width=True
    )

    st.download_button(
        "⬇️ Download filtered dataset",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_traffic_data.csv",
        mime="text/csv"
    )

    st.download_button(
        "⬇️ Download cleaned dataset",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_traffic_data.csv",
        mime="text/csv"
    )


# =========================================================
# 14. PROJECT PRESENTATION
# =========================================================

elif page == "🏆 Project Presentation":

    st.markdown("""
    <div class="hero">
        <div class="tag">PROJECT SHOWCASE</div>
        <h2>Smart City Traffic Intelligence</h2>
        <p>Using data analytics and machine learning concepts to
        understand traffic patterns and estimate traffic volume.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 THE PROBLEM")

    st.write(
        "Traffic congestion makes urban travel less predictable. "
        "Data analysis can help reveal busy periods and recurring patterns."
    )

    st.markdown("### 💡 OUR SOLUTION")

    st.write(
        "We clean and analyse traffic records, visualise time and weather "
        "patterns, and use a regularised regression model to demonstrate "
        "traffic-volume estimation."
    )

    st.markdown("### 🛠️ TECHNOLOGY STACK")

    t1, t2, t3 = st.columns(3)
    t1.metric("Language", "Python")
    t2.metric("Data processing", "Pandas + NumPy")
    t3.metric("Dashboard", "Streamlit")

    st.markdown("### 🧠 MACHINE LEARNING APPROACH")

    st.write(
        "We implemented Ridge-style regularised linear regression using "
        "NumPy. Cyclical features represent repeating hours and days, "
        "while standardisation helps features operate on comparable scales."
    )

    st.markdown("### 📈 MODEL EVALUATION")

    p1, p2, p3 = st.columns(3)
    p1.metric("MAE", f"{mae:,.2f}")
    p2.metric("RMSE", f"{rmse:,.2f}")
    p3.metric("R²", f"{r2:.3f}" if np.isfinite(r2) else "N/A")

    st.markdown("### ⚠️ CURRENT LIMITATIONS")

    st.write(
        "The current dataset is simulated practice data. The dashboard "
        "does not use live GPS, road sensors or real-time Mumbai traffic "
        "feeds. Its model must be tested on representative real-world data "
        "before practical deployment."
    )

    st.markdown("### 🚀 FUTURE SCOPE")

    st.markdown("""
    - Integrate verified live traffic and road-sensor feeds.
    - Add incident, road-closure and public transport information.
    - Evaluate advanced forecasting approaches on real data.
    - Validate predictions across different roads and time periods.
    - Develop evidence-based traffic management recommendations.
    """)

    st.success(
        "Our goal is not just to display traffic data. It is to show how "
        "data analysis and machine learning can support smarter urban planning."
    )


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption(
    "SMART CITY TRAFFIC INTELLIGENCE | Educational prototype | "
    "Simulated dataset | Predictions are estimates, not live traffic data."
)
