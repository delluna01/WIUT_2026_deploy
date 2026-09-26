import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>

        /* ================================
           GLOBAL
        ================================= */

        .stApp {
            background: var(--background-color, #f5f7fa);
            color: var(--text-color, #111827);
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
            font-size: 1 rem;
            line-height: 1.65
        }


        /* ================================
           SIDEBAR
        ================================= */

        [data-testid="stSidebar"] {
            background: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        [data-testid="stSidebar"] h3 {
            color: white !important;
        }


        /* ================================
           KPI CARDS
        ================================= */

        [data-testid="stMetric"] {
            background: var(--secondary-background-color, #ffffff);
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.10);
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-color, #64748b) !important;
            font-size: 0.82rem !important;
            opacity: 0.75;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-color, #111827) !important;
            font-weight: 700 !important;
        }


        /* ================================
           CONTENT CARDS
        ================================= */

        .content-card {
            background: var(--secondary-background-color, #ffffff);
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
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
            border-color: var(--text-color, #cbd5e1);
        }

        .insight-card {
            background: var(--secondary-background-color, #ffffff);
            border-left: 4px solid var(--text-color, #64748b);
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            margin: 1rem 0;
        }

        .insight-title {
            font-weight: 700;
            color: var(--text-color, #111827);
            margin-bottom: 0.35rem;
        }

        .insight-text {
            color: var(--text-color, #475569);
            line-height: 1.6;
            opacity: 0.8;
        }


        /* ================================
           HERO
        ================================= */

        .hero {
            background: linear-gradient(
                135deg,
                #111827 0%,
                #1e293b 100%
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
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .hero-title {
            color: white;
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.8rem;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 850px;
        }


        /* ================================
           SECTION LABELS
        ================================= */

        .section-label {
            color: var(--text-color, #64748b);
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
            background: var(--secondary-background-color, #ffffff);
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 16px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .chart-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
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
