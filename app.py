import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
import plotly.graph_objects as go
import plotly.express as px

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Skill Categorization Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'selected_skills' not in st.session_state:
    st.session_state.selected_skills = []

if 'show_validation_dialog' not in st.session_state:
    st.session_state.show_validation_dialog = False

if 'selected_skill' not in st.session_state:
    st.session_state.selected_skill = None

# Add custom CSS for modern dark theme
st.markdown("""
    <style>
    /* Global theme */
    .stApp {
        background: linear-gradient(135deg, #1a1f2c, #161923);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1f2c;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: rgba(30, 36, 51, 0.6);
        padding: 1rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #a0aec0 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #fff !important;
        background: linear-gradient(135deg, #a742ff, #8a2be2);
        border-radius: 8px;
    }
    
    /* Custom card styling */
    .category-card {
        background: linear-gradient(145deg, rgba(30, 36, 51, 0.95), rgba(26, 31, 44, 0.95));
        border-radius: 15px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .skill-description-card {
        background: linear-gradient(145deg, rgba(30, 36, 51, 0.95), rgba(26, 31, 44, 0.95));
        border-radius: 15px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #a742ff;
        backdrop-filter: blur(10px);
    }
    
    .alternative-card {
        background: linear-gradient(145deg, rgba(30, 36, 51, 0.8), rgba(26, 31, 44, 0.8));
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .alternative-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(167, 66, 255, 0.2);
        background: linear-gradient(145deg, rgba(30, 36, 51, 0.95), rgba(26, 31, 44, 0.95));
    }
    
    .description-text {
        color: #cbd5e0;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-top: 0.8rem;
    }
    
    .info-icon {
        color: #a742ff;
        font-size: 1.1rem;
        margin-right: 0.5rem;
        opacity: 0.9;
    }
    
    .category-description {
        color: #a0aec0;
        font-size: 0.92rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        line-height: 1.5;
    }
    
    .section-title {
        color: #fff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(167, 66, 255, 0.3);
        background: linear-gradient(90deg, #fff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .category-name {
        color: #fff;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: 0.01em;
    }
    
    .category-score {
        background: linear-gradient(90deg, #a742ff, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        font-size: 1rem;
        margin-top: 0.6rem;
        display: inline-block;
        padding: 0.3rem 0;
    }
    
    .related-skills {
        color: #8796a8;
        font-size: 0.9rem;
        margin-top: 0.8rem;
        line-height: 1.5;
    }
    
    .source-history {
        font-family: 'SF Mono', monospace;
        font-size: 0.9rem;
        color: #cbd5e0;
        line-height: 1.5;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #a742ff, #8a2be2);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #8a2be2, #a742ff);
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
        transform: translateY(-1px);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: rgba(30, 36, 51, 0.9);
        border: 1px solid rgba(167, 66, 255, 0.2);
        border-radius: 8px;
        color: #fff;
        padding: 0.5rem;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(167, 66, 255, 0.4);
    }
    
    /* Success message styling */
    .stSuccess {
        background: rgba(167, 66, 255, 0.1);
        border: 1px solid rgba(167, 66, 255, 0.2);
        color: #fff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(26, 31, 44, 0.7);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Search box styling */
    .search-container {
        background: rgba(30, 36, 51, 0.9);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(167, 66, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input {
        background: rgba(26, 31, 44, 0.9);
        border: 1px solid rgba(167, 66, 255, 0.2);
        color: #fff;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(167, 66, 255, 0.6);
        box-shadow: 0 0 0 1px rgba(167, 66, 255, 0.2);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #718096;
    }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for better styling with theme support
st.markdown("""
    <style>
    /* Base styles */
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
    
    /* Dark theme styles */
    .dark-theme {
        background-color: #0e1117;
        color: #ffffff;
    }
    .dark-theme .upload-section {
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid #2d2d2d;
    }
    
    /* Modal/Dialog styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.75);
        z-index: 1000;
        backdrop-filter: blur(4px);
        transition: all 0.3s ease-in-out;
    }
    
    .modal-content {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: var(--background-color);
        padding: 2.5rem;
        border-radius: 1rem;
        width: 90%;
        max-width: 900px;
        max-height: 85vh;
        overflow-y: auto;
        z-index: 1001;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        animation: modalSlideIn 0.3s ease-out;
    }

    @keyframes modalSlideIn {
        from {
            transform: translate(-50%, -45%);
            opacity: 0;
        }
        to {
            transform: translate(-50%, -50%);
            opacity: 1;
        }
    }

    .validation-card {
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .validation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .validation-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 1rem;
    }

    .close-button {
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        cursor: pointer;
        font-size: 1.5rem;
        color: var(--text-color);
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.2s ease;
        background: rgba(0, 0, 0, 0.05);
    }

    .close-button:hover {
        background: rgba(0, 0, 0, 0.1);
        transform: rotate(90deg);
    }

    .validation-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        margin-top: 2rem;
    }

    .stButton button {
        border-radius: 0.5rem;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Category box styles */
    .category-box {
        padding: 8px 12px;
        border-radius: 4px;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        margin: 4px 0;
    }
    
    .dark-theme .category-box {
        background-color: #2d2d2d;
        border-color: #444;
    }
    
    .dark-theme .tooltip .tooltip-text {
        background-color: #2d2d2d;
        color: #ffffff;
        border-color: #444;
    }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for better styling
st.markdown("""
    <style>
    /* Custom card styling */
    .category-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .alternative-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        transition: all 0.2s ease;
    }
    
    .alternative-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .history-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #6c757d;
    }
    
    .section-title {
        color: #1f77b4;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1f77b4;
    }
    
    .category-score {
        color: #2c3e50;
        font-weight: 500;
    }
    
    .related-skills {
        color: #6c757d;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .source-history {
        font-family: monospace;
        font-size: 0.9rem;
        color: #495057;
    }
    
    .skill-description-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #a742ff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .description-text {
        color: #a0aec0;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-top: 0.5rem;
    }
    
    .info-icon {
        color: #718096;
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    .category-description {
        color: #718096;
        font-size: 0.9rem;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

# Placeholder function to infer best skill categorizations
def infer_skill_categorization(skill_description):
    return "Recommended Category", "This category was recommended based on ..."

# Add this after the infer_skill_categorization function
def get_category_match_scores(skill_description):
    """Return match scores and related skills for each category for a given skill"""
    # In a real implementation, this would use an AI model or algorithm
    # Currently returning mock data
    return {
        "Software Development": {
            "score": 0.9238654,
            "related_skills": ["Java Programming", "Software Architecture"]
        },
        "Big Data": {
            "score": 0.9114384,
            "related_skills": ["Hadoop", "Spark"]
        },
        "Data and Analytics": {
            "score": 0.9057195,
            "related_skills": ["SQL", "Data Visualization"]
        },
        "Data Modeling": {
            "score": 0.8941223,
            "related_skills": ["Database Design", "ERD"]
        },
        "SAP Basis": {
            "score": 0.7046884,
            "related_skills": ["SAP Administration", "SAP Security"]
        }
    }

# Add category descriptions
CATEGORY_DESCRIPTIONS = {
    "Software Development": """
    Focus on designing, developing, and maintaining software applications and systems.
    Includes web development, mobile apps, system architecture, and programming practices.
    Key skills: Programming languages, software design patterns, version control, testing.
    """,
    
    "Big Data": """
    Focuses on processing and analyzing large volumes of structured and unstructured data.
    Involves big data technologies, distributed computing, and data pipelines.
    Key skills: Hadoop, Spark, NoSQL databases, data processing.
    """,
    
    "Data and Analytics": """
    Analyzes data to derive insights and support decision-making.
    Includes business intelligence, reporting, and data visualization.
    Key skills: SQL, BI tools, data analysis, reporting.
    """,
    
    "Data Modeling": """
    Designs and implements data structures and relationships.
    Focuses on database design, schema optimization, and data architecture.
    Key skills: ERD, database design, normalization, data warehousing.
    """,
    
    "SAP Basis": """
    Manages and maintains SAP systems and infrastructure.
    Includes system administration, security, and performance optimization.
    Key skills: SAP NetWeaver, system administration, security management.
    """
}

# Mock data for recent runs
recent_runs = [
    {
        "run_id": "Run 1 - Dec 18, 2024 - 2:30pm IST",
        "timestamp": "2024-12-18 14:30:00",
        "input_skill": "React.js Development",
        "skill_description": "5+ years of experience building scalable web applications using React.js, Redux, and modern JavaScript. Implemented complex UI components, state management, and RESTful API integration.",
        "recommended_category": "Software Development",
        "reasoning": "Strong alignment with front-end development and modern web technologies.",
        "categorization_source": "Algorithm (Initial) → Validated by John Smith",
        "history": [
            {"timestamp": "2024-12-18 14:30:00", "source": "Algorithm", "category": "Software Development"},
            {"timestamp": "2024-12-18 14:45:00", "source": "John Smith", "category": "Software Development", "action": "Validated"}
        ]
    },
    {
        "run_id": "Run 2 - Dec 18, 2024 - 2:35pm IST",
        "timestamp": "2024-12-18 14:35:00",
        "input_skill": "Tableau Dashboard Creation",
        "skill_description": "Created interactive business dashboards using Tableau. Experience with data visualization, KPI tracking, and executive reporting. Integrated multiple data sources and implemented drill-down capabilities.",
        "recommended_category": "Data and Analytics",
        "reasoning": "Direct match with data visualization and business intelligence tools.",
        "categorization_source": "Algorithm (Initial) → Changed by Sarah Lee → Validated by Mike Johnson",
        "history": [
            {"timestamp": "2024-12-18 14:35:00", "source": "Algorithm", "category": "Business Intelligence"},
            {"timestamp": "2024-12-18 14:40:00", "source": "Sarah Lee", "category": "Data and Analytics", "action": "Changed"},
            {"timestamp": "2024-12-18 15:00:00", "source": "Mike Johnson", "category": "Data and Analytics", "action": "Validated"}
        ]
    },
    {
        "run_id": "Run 3 - Dec 18, 2024 - 2:40pm IST",
        "timestamp": "2024-12-18 14:40:00",
        "input_skill": "Apache Spark Processing",
        "skill_description": "Developed and optimized big data processing pipelines using Apache Spark. Experience with data transformation, ETL processes, and distributed computing. Worked with both batch and streaming data.",
        "recommended_category": "Big Data",
        "reasoning": "Clear alignment with big data processing technologies and distributed computing.",
        "categorization_source": "Algorithm (Initial)",
        "history": [
            {"timestamp": "2024-12-18 14:40:00", "source": "Algorithm", "category": "Big Data"}
        ]
    },
    {
        "run_id": "Run 4 - Dec 18, 2024 - 2:45pm IST",
        "timestamp": "2024-12-18 14:45:00",
        "input_skill": "Database Schema Design",
        "skill_description": "Designed and optimized database schemas for large-scale applications. Experience with normalization, indexing strategies, and performance tuning. Worked with both SQL and NoSQL databases.",
        "recommended_category": "Data Modeling",
        "reasoning": "Direct match with database design and schema optimization.",
        "categorization_source": "Algorithm (Initial) → Changed by Sarah Lee",
        "history": [
            {"timestamp": "2024-12-18 14:45:00", "source": "Algorithm", "category": "Software Development"},
            {"timestamp": "2024-12-18 15:15:00", "source": "Sarah Lee", "category": "Data Modeling", "action": "Changed"}
        ]
    },
    {
        "run_id": "Run 5 - Dec 18, 2024 - 2:50pm IST",
        "timestamp": "2024-12-18 14:50:00",
        "input_skill": "SAP HANA Administration",
        "skill_description": "Managed and maintained SAP HANA databases, including backup, recovery, and performance optimization. Experience with SAP Basis administration and security configuration.",
        "recommended_category": "SAP Basis",
        "reasoning": "Perfect match with SAP system administration and database management.",
        "categorization_source": "Algorithm (Initial) → Validated by Mike Johnson",
        "history": [
            {"timestamp": "2024-12-18 14:50:00", "source": "Algorithm", "category": "SAP Basis"},
            {"timestamp": "2024-12-18 15:30:00", "source": "Mike Johnson", "category": "SAP Basis", "action": "Validated"}
        ]
    }
]

# Cache recent runs
@st.cache_data
def get_recent_runs():
    return recent_runs

temp_recent_runs = get_recent_runs()

# Main title with subtle description
st.title("🎯 Skill Categorization Dashboard")
st.markdown("*Automatically categorize and validate professional skills with AI assistance*")

# Calculate metrics from recent_runs
total_skills = len(recent_runs)
validated_skills = len([run for run in recent_runs if len(run['history']) > 1])
pending_validation = total_skills - validated_skills
changed_categories = len([run for run in recent_runs if any(h.get('action') == 'Changed' for h in run['history'])])
validation_rate = (validated_skills / total_skills * 100) if total_skills > 0 else 0
accuracy_rate = ((validated_skills - changed_categories) / validated_skills * 100) if validated_skills > 0 else 0

# Dashboard Metrics Section
st.markdown("""
    <style>
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        flex: 1;
        min-width: 300px;
        background: rgba(30, 36, 51, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(167, 66, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .metric-title {
        color: #a742ff;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #fff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-subtitle {
        color: #718096;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Metrics Row 1
st.markdown('<div class="metric-row">', unsafe_allow_html=True)

# Validation Rate with Gauge Chart
with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">VALIDATION RATE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-subtitle">{validated_skills} of {total_skills} skills validated</div>', unsafe_allow_html=True)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=validation_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#a742ff"},
            'bgcolor': "rgba(30, 36, 51, 0.9)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(167, 66, 255, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(167, 66, 255, 0.4)'},
                {'range': [80, 100], 'color': 'rgba(167, 66, 255, 0.6)'}
            ]
        },
        number={'suffix': "%", 'font': {'color': "white"}}
    ))
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AI Accuracy Over Time
accuracy_data = []
for run in recent_runs:
    changes = [h for h in run['history'] if h.get('action') == 'Changed']
    accuracy_data.append({
        'timestamp': datetime.strptime(run['timestamp'], "%Y-%m-%d %H:%M:%S"),
        'accurate': len(changes) == 0
    })

accuracy_df = pd.DataFrame(accuracy_data)
if not accuracy_df.empty:
    accuracy_df['cumulative_accuracy'] = (accuracy_df['accurate'].cumsum() / 
                                        (pd.Series(range(1, len(accuracy_df) + 1))) * 100)

    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-title">AI ACCURACY TREND</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-subtitle">Current accuracy: {accuracy_rate:.1f}%</div>', unsafe_allow_html=True)
        
        fig = px.line(accuracy_df, x='timestamp', y='cumulative_accuracy',
                     line_shape='spline')
        fig.update_traces(line_color='#a742ff')
        fig.update_layout(
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            xaxis={'showgrid': False, 'title': None},
            yaxis={'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 
                  'title': None, 'range': [0, 100]}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Pending Validations Pie Chart
with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">VALIDATION STATUS</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-subtitle">{pending_validation} skills awaiting review</div>', unsafe_allow_html=True)
    
    fig = go.Figure(data=[go.Pie(
        labels=['Validated', 'Pending'],
        values=[validated_skills, pending_validation],
        hole=.7,
        marker=dict(colors=['#a742ff', 'rgba(167, 66, 255, 0.2)']),
        textinfo='percent',
        textfont=dict(color='white')
    )])
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Metrics Row 2
st.markdown('<div class="metric-row">', unsafe_allow_html=True)

# Category Distribution Bar Chart
category_counts = {}
for run in recent_runs:
    current_category = run['recommended_category']
    category_counts[current_category] = category_counts.get(current_category, 0) + 1

with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">CATEGORY DISTRIBUTION</div>', unsafe_allow_html=True)
    
    fig = go.Figure(data=[go.Bar(
        x=list(category_counts.keys()),
        y=list(category_counts.values()),
        marker_color='#a742ff'
    )])
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        xaxis={'showgrid': False, 'title': None},
        yaxis={'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 'title': None}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Recent Activity Timeline
recent_changes = [h for run in recent_runs for h in run['history'] if h.get('action') in ['Changed', 'Validated']]
recent_changes.sort(key=lambda x: x['timestamp'], reverse=True)

with st.container():
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">ACTIVITY TIMELINE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-subtitle">{len(recent_changes)} recent changes</div>', unsafe_allow_html=True)
    
    activity_df = pd.DataFrame(recent_changes)
    if not activity_df.empty:
        activity_df['timestamp'] = pd.to_datetime(activity_df['timestamp'])
        activity_df['count'] = 1
        activity_df = activity_df.resample('H', on='timestamp')['count'].sum().reset_index()
        
        fig = px.bar(activity_df, x='timestamp', y='count',
                    color_discrete_sequence=['#a742ff'])
        fig.update_layout(
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            xaxis={'showgrid': False, 'title': None},
            yaxis={'showgrid': True, 'gridcolor': 'rgba(255,255,255,0.1)', 'title': None}
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Add tabs after the dashboard
tab1, tab2 = st.tabs(["Categorize Skills", "Recent History"])

# File Upload Tab
with tab1:
    st.markdown("### Upload Skills Data")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a CSV or Excel file",
                type=["csv", "xlsx"],
                help="Upload a file containing work experience descriptions or skills"
            )
            
        with col2:
            st.markdown("#### File Requirements")
            st.markdown("""
                - CSV or Excel format
                - One skill per row
                - Headers included
            """)
    
    if uploaded_file:
        st.success("File uploaded successfully!")
        
        # Preview section
        with st.expander("Preview Uploaded Data", expanded=True):
            st.markdown("#### File Preview")
            
            try:
                # Read the file based on its type
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:  # Excel file
                    df = pd.read_excel(uploaded_file)
                
                # Display file info
                st.markdown(f"**File Info:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"Rows: {df.shape[0]}")
                with col2:
                    st.markdown(f"Columns: {df.shape[1]}")
                with col3:
                    st.markdown(f"File type: {uploaded_file.type}")
                
                # Display column names
                st.markdown("**Columns:**")
                st.write(", ".join(df.columns.tolist()))
                
                # Show first few rows of data
                st.markdown("**Data Preview:**")
                st.dataframe(
                    df.head(5),
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                st.markdown("Please ensure your file is properly formatted with headers and data.")
        
        if st.button("Process Skills", type="primary"):
            with st.spinner("Processing skills..."):
                st.session_state.processing = True
                # Add processing logic here
                st.success("✅ Processing complete! View results in the Recent Runs tab.")

# Recent Runs Tab
with tab2:
    st.markdown("### Recent Categorization History")
    
    # Add search and filter functionality
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])
    
    with filter_col1:
        search_query = st.text_input("Search for a specific skill", 
                                   placeholder="Enter skill name...",
                                   key="skill_search")
    
    with filter_col2:
        run_id_filter = st.selectbox(
            "Filter by Run",
            options=["All"] + [run["run_id"] for run in recent_runs],
            index=0
        )
    
    with filter_col3:
        st.markdown("<div style='padding-top: 0.3rem;'>", unsafe_allow_html=True)
        search_button = st.button("🔍 Search", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_runs = recent_runs
    
    # Apply run ID filter
    if run_id_filter != "All":
        filtered_runs = [run for run in filtered_runs if run["run_id"] == run_id_filter]
    
    # Apply search filter if search button is clicked
    if search_query and search_button:
        filtered_runs = [run for run in filtered_runs 
                        if search_query.lower() in run['input_skill'].lower()]
    
    if not filtered_runs:
        st.info("No skills found matching your criteria.")
    
    # Display runs in a cleaner layout
    if filtered_runs:
        # Create header row
        header_cols = st.columns([2, 2, 2, 3, 1])
        
        with header_cols[0]:
            st.markdown("**Run ID**")
        with header_cols[1]:
            st.markdown("**Input Skill**")
        with header_cols[2]:
            st.markdown("**Recommended Category**")
        with header_cols[3]:
            st.markdown("**Reasoning**")
        with header_cols[4]:
            st.markdown("**Actions**")
        
        # Add a separator
        st.markdown("<hr style='margin: 0.5rem 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Display each run
        for run in filtered_runs:
            cols = st.columns([2, 2, 2, 3, 1])
            
            with cols[0]:
                st.markdown(f"_{run['run_id']}_")
            with cols[1]:
                st.markdown(f"**{run['input_skill']}**")
            with cols[2]:
                st.markdown(f"_{run['recommended_category']}_")
            with cols[3]:
                st.markdown(run['reasoning'])
            with cols[4]:
                if st.button("Review", key=f"review_{run['run_id']}", use_container_width=True):
                    st.session_state.selected_skills = [run['run_id']]
                    st.session_state.selected_skill = run
                    st.session_state.show_validation_dialog = True
                    st.experimental_rerun()
# Add this button inside the validation dialog
if st.session_state.show_validation_dialog:
    validation_container = st.container()
    
    with validation_container:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown("### Maintain Categories")
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Add the Clear/Exit button at the top
        if st.button("Exit", key="clear_button"):
            # Reset the session state variables related to validation
            st.session_state.show_validation_dialog = False
            st.session_state.selected_skills = []
            st.session_state.selected_skill = None
            st.experimental_rerun()  # Rerun the app to refresh the state
        
        skill_data = next((run for run in recent_runs if run['run_id'] in st.session_state.selected_skills), None)
        
        # Display skill description
        st.markdown('<div class="section-title">Skill Details</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="skill-description-card">'
            f'<div class="category-name">{skill_data["input_skill"]}</div>'
            f'<div class="description-text">{skill_data["skill_description"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Get category matches and related skills
        category_matches = get_category_match_scores(skill_data["skill_description"])
        
        # Current category with match score
        current_category = skill_data.get("recommended_category", "Uncategorized")
        current_score = category_matches.get(current_category, {}).get("score", 0)
        current_related_skills = category_matches.get(current_category, {}).get("related_skills", [])
        
        # Current Category Section
        st.markdown('<div class="section-title">Current Category</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="category-card">'
            f'<div class="category-name">{current_category}</div>'
            f'<div class="category-score">Match Score: {current_score:.7f}</div>'
            f'<div class="related-skills">Related Skills: {", ".join(current_related_skills)}</div>'
            f'<div class="category-description">'
            f'<span class="info-icon">ℹ️</span>{CATEGORY_DESCRIPTIONS.get(current_category, "No description available.")}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Alternative categories
        st.markdown('<div class="section-title">Possible Alternative Categories</div>', unsafe_allow_html=True)
        sorted_categories = sorted(
            [(cat, data["score"], data["related_skills"]) 
             for cat, data in category_matches.items() 
             if cat != current_category],
            key=lambda x: x[1],
            reverse=True
        )
        
        for cat, score, related_skills in sorted_categories[:4]:
            st.markdown(
                f'<div class="alternative-card">'
                f'<div class="category-name">{cat}</div>'
                f'<div class="category-score">Match Score: {score:.7f}</div>'
                f'<div class="related-skills">Related Skills: {", ".join(related_skills)}</div>'
                f'<div class="category-description">'
                f'<span class="info-icon">ℹ️</span>{CATEGORY_DESCRIPTIONS.get(cat, "No description available.")}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Categorization source tracking
        st.markdown('<div class="section-title">Categorization Source History</div>', unsafe_allow_html=True)
        source = skill_data.get("categorization_source", "Unknown")
        st.markdown(
            f'<div class="history-card">'
            f'<div class="source-history">{source}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        # Add buttons for accepting or changing the category
        if new_category := st.selectbox(
            "Change Category",
            options=[cat for cat, _, _ in sorted_categories],
            key="category_change"
        ):
            if st.button("Apply Category Change", use_container_width=True):
                new_source = f"Changed to {new_category} by {st.session_state.get('user_id', 'unknown')} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                st.success(f"Category changed to {new_category}. New source: {new_source}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with help
with st.sidebar:
    st.markdown("### 📖 Quick Guide")
    st.markdown("""
    1. **Upload Data**
       - Use the Upload tab
       - Support for CSV and Excel
    
    2. **Review Results**
       - Switch to Recent Runs
       - Filter by Run ID
       
    3. **Validate Categories**
       - Select skills to review
       - Update categorizations
       - Provide feedback
    """)
    
    st.markdown("### 🔍 Need Help?")
    if st.button("View Documentation"):
        st.markdown("Documentation link here")