
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Palo Alto Networks | Career Progression Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #dddddd;
        padding: 12px;
        border-radius: 10px;
        background-color: #fafafa;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = "Palo_Alto_Networks_Final_Analysis.csv"


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE)

    # Convert categorical columns where appropriate
    categorical_columns = [
        "Department",
        "JobRole",
        "CareerClusterName",
        "PromotionGapCategory",
        "TrainingNeedIndicator",
        "RetentionOpportunityCategory",
        "SuggestedAction"
    ]

    for column in categorical_columns:
        if column in data.columns:
            data[column] = data[column].fillna("Unknown")

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "The file 'Palo_Alto_Networks_Final_Analysis.csv' "
        "was not found in the dashboard folder."
    )
    st.stop()


# ============================================================
# BASIC VALIDATION
# ============================================================

required_columns = [
    "Department",
    "JobRole",
    "CareerCluster",
    "PromotionGapScore",
    "PromotionGapCategory",
    "TrainingNeedScore",
    "TrainingNeedIndicator",
    "RetentionOpportunityIndex",
    "RetentionOpportunityCategory",
    "SuggestedAction",
    "Attrition"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The following required columns are missing from the dataset:"
    )
    st.write(missing_columns)
    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    'Palo Alto Networks — Career Progression & Retention Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Career Path Clustering | Promotion Gap Monitoring | '
    'Training Needs | Retention Opportunities'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore employee career progression."
)


# Department
department_options = sorted(
    df["Department"].dropna().astype(str).unique()
)

selected_departments = st.sidebar.multiselect(
    "Department",
    options=department_options,
    default=department_options
)


# Job Role
job_role_options = sorted(
    df["JobRole"].dropna().astype(str).unique()
)

selected_job_roles = st.sidebar.multiselect(
    "Job Role",
    options=job_role_options,
    default=job_role_options
)


# Career Cluster
cluster_options = sorted(
    df["CareerCluster"].dropna().unique()
)

selected_clusters = st.sidebar.multiselect(
    "Career Cluster",
    options=cluster_options,
    default=cluster_options
)


# Promotion Gap
promotion_options = [
    "Low",
    "Medium",
    "High"
]

selected_promotion = st.sidebar.multiselect(
    "Promotion Gap",
    options=promotion_options,
    default=promotion_options
)


# Training Need
training_options = [
    "Low",
    "Medium",
    "High"
]

selected_training = st.sidebar.multiselect(
    "Training Need",
    options=training_options,
    default=training_options
)


# Retention Opportunity
retention_options = [
    "Low",
    "Medium",
    "High"
]

selected_retention = st.sidebar.multiselect(
    "Retention Opportunity",
    options=retention_options,
    default=retention_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["Department"].astype(str).isin(selected_departments)
    &
    df["JobRole"].astype(str).isin(selected_job_roles)
    &
    df["CareerCluster"].isin(selected_clusters)
    &
    df["PromotionGapCategory"].astype(str).isin(selected_promotion)
    &
    df["TrainingNeedIndicator"].astype(str).isin(selected_training)
    &
    df["RetentionOpportunityCategory"].astype(str).isin(
        selected_retention
    )
].copy()


# ============================================================
# DASHBOARD NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Dashboard Module",
    [
        "Executive Overview",
        "Career Path Clustering",
        "Promotion Gap Monitor",
        "Training Need Analysis",
        "Retention Opportunity",
        "Managerial Insights",
        "Employee Action Panel"
    ]
)


# ============================================================
# HELPER
# ============================================================

def percentage(value, total):
    if total == 0:
        return 0
    return value / total * 100


# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    total_employees = len(filtered_df)

    attrition_count = int(
        filtered_df["Attrition"].sum()
    )

    attrition_rate = percentage(
        attrition_count,
        total_employees
    )

    high_promotion_gap = int(
        (
            filtered_df["PromotionGapCategory"] == "High"
        ).sum()
    )

    high_training_need = int(
        (
            filtered_df["TrainingNeedIndicator"] == "High"
        ).sum()
    )

    high_retention = int(
        (
            filtered_df["RetentionOpportunityCategory"] == "High"
        ).sum()
    )

    retention_population = int(
        (
            (filtered_df["Attrition"] == 0)
            &
            (
                filtered_df[
                    "RetentionOpportunityCategory"
                ].isin(["Medium", "High"])
            )
        ).sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Employees",
        f"{total_employees:,}"
    )

    c2.metric(
        "Attrition Rate",
        f"{attrition_rate:.2f}%"
    )

    c3.metric(
        "High Promotion Gap",
        f"{high_promotion_gap:,}"
    )

    c4.metric(
        "High Training Need",
        f"{high_training_need:,}"
    )

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "High Retention Opportunity",
        f"{high_retention:,}"
    )

    c6.metric(
        "Retention Opportunity Population",
        f"{retention_population:,}"
    )

    c7.metric(
        "Career Clusters",
        filtered_df["CareerCluster"].nunique()
    )

    st.divider()

    # Promotion Gap
    col1, col2 = st.columns(2)

    with col1:

        promotion_counts = (
            filtered_df["PromotionGapCategory"]
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"],
                fill_value=0
            )
            .reset_index()
        )

        promotion_counts.columns = [
            "Category",
            "Employees"
        ]

        fig = px.bar(
            promotion_counts,
            x="Category",
            y="Employees",
            title="Promotion Gap Distribution",
            text="Employees"
        )

        fig.update_layout(
            xaxis_title="Promotion Gap",
            yaxis_title="Employees"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        retention_counts = (
            filtered_df[
                "RetentionOpportunityCategory"
            ]
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"],
                fill_value=0
            )
            .reset_index()
        )

        retention_counts.columns = [
            "Category",
            "Employees"
        ]

        fig = px.bar(
            retention_counts,
            x="Category",
            y="Employees",
            title="Retention Opportunity Distribution",
            text="Employees"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 2 — CAREER PATH CLUSTERING
# ============================================================

elif page == "Career Path Clustering":

    st.markdown(
        '<div class="section-title">'
        'Career Path Clustering'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore employee career segments identified through "
        "K-Means clustering."
    )

    cluster_profile = (
        filtered_df
        .groupby("CareerCluster")
        .agg(
            Employees=("CareerCluster", "size"),
            AvgPromotionGap=(
                "PromotionGapScore",
                "mean"
            ),
            AvgTrainingNeed=(
                "TrainingNeedScore",
                "mean"
            ),
            AvgRetentionOpportunity=(
                "RetentionOpportunityIndex",
                "mean"
            ),
            AttritionRate=(
                "Attrition",
                "mean"
            )
        )
        .reset_index()
    )

    cluster_profile["AttritionRate"] *= 100

    st.dataframe(
        cluster_profile.round(3),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            cluster_profile,
            x="CareerCluster",
            y="Employees",
            text="Employees",
            title="Employees by Career Cluster"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            cluster_profile,
            x="CareerCluster",
            y="AvgRetentionOpportunity",
            title="Retention Opportunity by Career Cluster"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Career Cluster vs Attrition")

    attrition_cluster = (
        filtered_df
        .groupby("CareerCluster")["Attrition"]
        .mean()
        .reset_index()
    )

    attrition_cluster["AttritionRate"] = (
        attrition_cluster["Attrition"] * 100
    )

    fig = px.bar(
        attrition_cluster,
        x="CareerCluster",
        y="AttritionRate",
        text="AttritionRate",
        title="Attrition Rate by Career Cluster"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 3 — PROMOTION GAP MONITOR
# ============================================================

elif page == "Promotion Gap Monitor":

    st.markdown(
        '<div class="section-title">'
        'Promotion Gap Monitor'
        '</div>',
        unsafe_allow_html=True
    )

    average_gap = (
        filtered_df["PromotionGapScore"].mean()
    )

    high_gap_count = int(
        (
            filtered_df["PromotionGapCategory"]
            == "High"
        ).sum()
    )

    high_gap_rate = percentage(
        high_gap_count,
        len(filtered_df)
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Average Promotion Gap Score",
        f"{average_gap:.3f}"
    )

    c2.metric(
        "High Promotion Gap %",
        f"{high_gap_rate:.2f}%"
    )

    st.divider()

    # Department analysis
    department_gap = (
        filtered_df
        .groupby("Department")
        .agg(
            Employees=("Department", "size"),
            AvgPromotionGap=(
                "PromotionGapScore",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "AvgPromotionGap",
            ascending=False
        )
    )

    fig = px.bar(
        department_gap,
        x="Department",
        y="AvgPromotionGap",
        text="AvgPromotionGap",
        title="Average Promotion Gap by Department"
    )

    fig.update_traces(
        texttemplate="%{text:.3f}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Role analysis
    role_gap = (
        filtered_df
        .groupby("JobRole")
        .agg(
            Employees=("JobRole", "size"),
            AvgPromotionGap=(
                "PromotionGapScore",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "AvgPromotionGap",
            ascending=False
        )
    )

    fig = px.bar(
        role_gap.head(15),
        x="AvgPromotionGap",
        y="JobRole",
        orientation="h",
        title="Top Job Roles by Promotion Gap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Promotion Gap Category Distribution"
    )

    category_data = (
        filtered_df[
            "PromotionGapCategory"
        ]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0
        )
        .reset_index()
    )

    category_data.columns = [
        "Category",
        "Employees"
    ]

    fig = px.pie(
        category_data,
        names="Category",
        values="Employees",
        hole=0.4,
        title="Promotion Gap Categories"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 4 — TRAINING NEED ANALYSIS
# ============================================================

elif page == "Training Need Analysis":

    st.markdown(
        '<div class="section-title">'
        'Training Need Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    high_training = int(
        (
            filtered_df["TrainingNeedIndicator"]
            == "High"
        ).sum()
    )

    training_rate = percentage(
        high_training,
        len(filtered_df)
    )

    avg_training_need = (
        filtered_df["TrainingNeedScore"].mean()
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "High Training Need",
        f"{high_training:,}"
    )

    c2.metric(
        "Average Training Need Score",
        f"{avg_training_need:.3f}"
    )

    st.write(
        f"High Training Need population: "
        f"{training_rate:.2f}%"
    )

    training_counts = (
        filtered_df[
            "TrainingNeedIndicator"
        ]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0
        )
        .reset_index()
    )

    training_counts.columns = [
        "Category",
        "Employees"
    ]

    fig = px.bar(
        training_counts,
        x="Category",
        y="Employees",
        text="Employees",
        title="Training Need Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if "PromotionGapScore" in filtered_df.columns:

        fig = px.scatter(
            filtered_df,
            x="PromotionGapScore",
            y="TrainingNeedScore",
            color="TrainingNeedIndicator",
            hover_data=[
                "Department",
                "JobRole"
            ],
            title="Training Need vs Promotion Gap"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 5 — RETENTION OPPORTUNITY
# ============================================================

elif page == "Retention Opportunity":

    st.markdown(
        '<div class="section-title">'
        'Retention Opportunity Panel'
        '</div>',
        unsafe_allow_html=True
    )

    # Required project population
    opportunity_df = filtered_df[
        (filtered_df["Attrition"] == 0)
        &
        (
            filtered_df[
                "RetentionOpportunityCategory"
            ].isin(["Medium", "High"])
        )
    ].copy()

    high_opportunity = int(
        (
            opportunity_df[
                "RetentionOpportunityCategory"
            ] == "High"
        ).sum()
    )

    total_opportunity = len(opportunity_df)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Retention Opportunity Population",
        f"{total_opportunity:,}"
    )

    c2.metric(
        "High Retention Opportunity",
        f"{high_opportunity:,}"
    )

    c3.metric(
        "Average Opportunity Score",
        f"{opportunity_df['RetentionOpportunityIndex'].mean():.3f}"
        if len(opportunity_df) > 0
        else "0.000"
    )

    st.divider()

    if len(opportunity_df) > 0:

        department_opportunity = (
            opportunity_df
            .groupby("Department")
            .agg(
                Employees=("Department", "size"),
                AvgOpportunity=(
                    "RetentionOpportunityIndex",
                    "mean"
                )
            )
            .reset_index()
            .sort_values(
                "Employees",
                ascending=False
            )
        )

        fig = px.bar(
            department_opportunity,
            x="Department",
            y="Employees",
            text="Employees",
            title="Retention Opportunity Population by Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            "Suggested Management Actions"
        )

        action_summary = (
            opportunity_df[
                "SuggestedAction"
            ]
            .value_counts()
            .reset_index()
        )

        action_summary.columns = [
            "Suggested Action",
            "Employees"
        ]

        fig = px.bar(
            action_summary,
            x="Employees",
            y="Suggested Action",
            orientation="h",
            title="Suggested Actions for Retention Opportunities"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader(
            "Priority Employee Population"
        )

        display_columns = [
            column
            for column in [
                "EmployeeNumber",
                "Department",
                "JobRole",
                "JobLevel",
                "YearsAtCompany",
                "YearsInCurrentRole",
                "YearsSinceLastPromotion",
                "PromotionGapScore",
                "PromotionGapCategory",
                "TrainingNeedScore",
                "TrainingNeedIndicator",
                "RetentionOpportunityIndex",
                "RetentionOpportunityCategory",
                "SuggestedAction"
            ]
            if column in opportunity_df.columns
        ]

        priority_table = (
            opportunity_df[
                display_columns
            ]
            .sort_values(
                "RetentionOpportunityIndex",
                ascending=False
            )
        )

        st.dataframe(
            priority_table,
            use_container_width=True,
            hide_index=True
        )

        csv_data = priority_table.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Retention Opportunity List",
            data=csv_data,
            file_name="Retention_Opportunity_Employees.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No Medium/High Retention Opportunity "
            "employees match the selected filters."
        )


# ============================================================
# PAGE 6 — MANAGERIAL INSIGHTS
# ============================================================

elif page == "Managerial Insights":

    st.markdown(
        '<div class="section-title">'
        'Managerial Insight Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Use this section to identify organizational areas "
        "requiring career-development attention."
    )

    department_insights = (
        filtered_df
        .groupby("Department")
        .agg(
            Employees=("Department", "size"),
            AvgPromotionGap=(
                "PromotionGapScore",
                "mean"
            ),
            AvgTrainingNeed=(
                "TrainingNeedScore",
                "mean"
            ),
            AvgRetentionOpportunity=(
                "RetentionOpportunityIndex",
                "mean"
            ),
            AttritionRate=(
                "Attrition",
                "mean"
            )
        )
        .reset_index()
    )

    department_insights["AttritionRate"] *= 100

    st.subheader(
        "Department Management Indicators"
    )

    st.dataframe(
        department_insights.sort_values(
            "AvgRetentionOpportunity",
            ascending=False
        ).round(3),
        use_container_width=True,
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            department_insights.sort_values(
                "AvgPromotionGap",
                ascending=False
            ),
            x="Department",
            y="AvgPromotionGap",
            title="Promotion Gap by Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            department_insights.sort_values(
                "AttritionRate",
                ascending=False
            ),
            x="Department",
            y="AttritionRate",
            title="Attrition Rate by Department"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Management Action Distribution"
    )

    action_data = (
        filtered_df["SuggestedAction"]
        .value_counts()
        .reset_index()
    )

    action_data.columns = [
        "SuggestedAction",
        "Employees"
    ]

    fig = px.bar(
        action_data,
        x="Employees",
        y="SuggestedAction",
        orientation="h",
        title="Suggested Management Actions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 7 — EMPLOYEE ACTION PANEL
# ============================================================

elif page == "Employee Action Panel":

    st.markdown(
        '<div class="section-title">'
        'Employee Action Panel'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Prioritized non-attrited employees showing "
        "Medium or High retention opportunity."
    )

    action_df = filtered_df[
        (filtered_df["Attrition"] == 0)
        &
        (
            filtered_df[
                "RetentionOpportunityCategory"
            ].isin(["Medium", "High"])
        )
    ].copy()

    action_df = action_df.sort_values(
        [
            "RetentionOpportunityIndex",
            "PromotionGapScore",
            "TrainingNeedScore"
        ],
        ascending=False
    )

    st.metric(
        "Employees Requiring Potential Intervention",
        f"{len(action_df):,}"
    )

    display_columns = [
        column
        for column in [
            "EmployeeNumber",
            "Department",
            "JobRole",
            "JobLevel",
            "CareerCluster",
            "CareerClusterName",
            "YearsAtCompany",
            "YearsInCurrentRole",
            "YearsSinceLastPromotion",
            "YearsWithCurrManager",
            "PromotionGapScore",
            "PromotionGapCategory",
            "TrainingNeedScore",
            "TrainingNeedIndicator",
            "ManagerStabilityRatio",
            "RetentionOpportunityIndex",
            "RetentionOpportunityCategory",
            "SuggestedAction"
        ]
        if column in action_df.columns
    ]

    display_df = action_df[
        display_columns
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Employee Action List",
        data=csv_data,
        file_name="Employee_Action_Panel.csv",
        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Palo Alto Networks — Career Progression and Promotion Gap "
    "Analysis for Retention Optimization"
)

st.caption(
    f"Dashboard records displayed: {len(filtered_df):,} "
    f"of {len(df):,}"
)
