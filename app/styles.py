import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>

        /* ================================
           GLOBAL
        ================================= */

        .stApp {
            background: #E9EAF2;
            color: #414770;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stHeader"] :is(button, a, [role="button"]),
        [data-testid="stHeader"] :is(button, a, [role="button"]) *,
        [data-testid="stToolbar"] :is(button, a, [role="button"]),
        [data-testid="stToolbar"] :is(button, a, [role="button"]) * {
            color: inherit !important;
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* Remove some default Streamlit spacing */
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        h1 {
            font-weight: 750 !important;
        }

        h2 {
            margin-top: 2.5rem !important;
            font-weight: 700 !important;
        }

        h3 {
            font-weight: 650 !important;
        }

        /* Body Text */
        [data-testid="stMarkdownContainer"] p {
            font-size: 1rem;
            line-height: 1.65;
        }

        [data-testid="stAlert"] {
            background: rgba(128, 128, 128, 0.08);
            border-left: 4px solid #f59e0b;
            color: inherit !important;
        }

        [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
            color: inherit !important;
        }


        /* ================================
           SIDEBAR
        ================================= */

        [data-testid="stSidebar"] {
            background: #414770;
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] a:visited {
            color: #B7C3F3 !important;
            text-decoration: none !important;
        }

        [data-testid="stSidebar"] a:hover {
            color: #DD7596 !important;
            text-decoration: none !important;
        }

        [data-testid="stSidebar"] h3 {
            color: white !important;
        }


        /* ================================
           KPI CARDS
        ================================= */

        [data-testid="stMetric"] {
            background: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 14px;
            border-bottom: 3px solid #DD7596;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
            border-color: #DD7596;
        }

        [data-testid="stMetricLabel"] {
            color: inherit !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stMetricValue"] p {
            font-size: 2.25rem !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stMetricLabel"] p {
            font-size: 1rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
        }


        /* ================================
           CONTENT CARDS
        ================================= */

        .content-card {
            background: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            min-height: 220px;
            height: auto;
            box-sizing: border-box;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease;
        }

        .content-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(221, 117, 150, 0.18);
            border-color: #DD7596;
        }

        .insight-card {
            background: rgba(128, 128, 128, 0.08);
            border-left: 4px solid #DD7596;
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            margin: 1rem 0;
        }

        .insight-title {
            font-weight: 700;
            color: inherit;
            margin-bottom: 0.35rem;
        }

        .insight-text {
            color: inherit;
            line-height: 1.6;
        }


        /* ================================
           HERO
        ================================= */

        .hero {
            background: linear-gradient(
                135deg,
                #414770 0%,
                #343957 100%
            );
            border-radius: 20px;
            padding: 2.8rem 3rem;
            margin-bottom: 1.8rem;
            color: white;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.12);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }

        .hero:hover {
            transform: translateY(-3px);
            box-shadow: 0 14px 35px rgba(15, 23, 42, 0.18);
        }

        .hero-kicker {
            color: #B7C3F3;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .hero-kicker::before {
            content: "";
            display: inline-block;
            width: 28px;
            height: 3px;
            background: #DD7596;
            margin-right: 10px;
            vertical-align: middle;
            border-radius: 3px;
        }

        .hero-title {
            color: white;
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.8rem;
        }

        .hero-subtitle {
            color: #E9ECFF;
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 850px;
        }


        /* ================================
           SECTION LABELS
        ================================= */

        .section-label {
            color: #DD7596; 
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-top: 2.5rem;
            margin-bottom: 0.25rem;
        }


        /* ================================
           EDA / CHART CONTAINERS
        ================================= */

        .chart-card {
            background: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 16px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .chart-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(221, 117, 150, 0.16); 
            border-color: #DD7596;
        }


        /* ================================
           TABLES
        ================================= */

        [data-testid="stMarkdownContainer"] table {
            border-radius: 10px;
            overflow: hidden;
            transition: box-shadow 0.2s ease;
        }

        [data-testid="stMarkdownContainer"] table:hover {
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
        }


        /* ================================
           DIVIDERS
        ================================= */

        hr {
            border: none;
            border-top: 1px solid rgba(128, 128, 128, 0.25);
            margin: 2rem 0;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
