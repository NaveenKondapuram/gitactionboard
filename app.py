import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="GitHub Actions Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .success {
        color: #28a745;
        font-weight: bold;
    }
    .failure {
        color: #dc3545;
        font-weight: bold;
    }
    .in-progress {
        color: #ffc107;
        font-weight: bold;
    }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 GitHub Actions Dashboard")
st.markdown("Track your workflow status at a glance")

# Sidebar configuration
st.sidebar.header("Configuration")
github_token = st.sidebar.text_input("GitHub Token", type="password", 
                                      value=os.getenv("GITHUB_TOKEN", ""),
                                      help="Personal Access Token for GitHub API")
repo_owner = st.sidebar.text_input("Repository Owner", value="NaveenKondapuram")
repo_name = st.sidebar.text_input("Repository Name", value="gitactionboard")

# Cache decorator for API calls
@st.cache_data(ttl=300)
def get_workflow_runs(owner, repo, token):
    """Fetch workflow runs from GitHub API"""
    headers = {
        "Authorization": f"token {token}" if token else "",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching workflow data: {e}")
        return None

@st.cache_data(ttl=300)
def get_workflow_details(owner, repo, run_id, token):
    """Fetch details for a specific workflow run"""
    headers = {
        "Authorization": f"token {token}" if token else "",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching run details: {e}")
        return None

# Main content
if repo_owner and repo_name:
    # Fetch workflow runs
    data = get_workflow_runs(repo_owner, repo_name, github_token)
    
    if data and "workflow_runs" in data:
        runs = data["workflow_runs"]
        
        if runs:
            # Calculate statistics
            total_runs = len(runs)
            passed = len([r for r in runs if r["conclusion"] == "success"])
            failed = len([r for r in runs if r["conclusion"] == "failure"])
            in_progress = len([r for r in runs if r["status"] == "in_progress"])
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Runs", total_runs)
            
            with col2:
                st.metric("✅ Passed", passed, delta=f"{(passed/total_runs*100):.1f}%")
            
            with col3:
                st.metric("❌ Failed", failed, delta=f"{(failed/total_runs*100):.1f}%")
            
            with col4:
                st.metric("⏳ In Progress", in_progress)
            
            st.divider()
            
            # Filter options
            st.subheader("Filters")
            col1, col2 = st.columns(2)
            
            with col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    ["completed", "in_progress"],
                    default=["completed"]
                )
            
            with col2:
                conclusion_filter = st.multiselect(
                    "Filter by Result",
                    ["success", "failure", "neutral", "cancelled"],
                    default=["success", "failure"]
                )
            
            st.divider()
            
            # Prepare dataframe
            df_data = []
            for run in runs:
                if run["status"] in status_filter:
                    if run["status"] == "in_progress" or run["conclusion"] in conclusion_filter:
                        df_data.append({
                            "Workflow Name": run["name"],
                            "Status": run["status"],
                            "Conclusion": run["conclusion"] if run["conclusion"] else "N/A",
                            "Branch": run["head_branch"],
                            "Commit": run["head_sha"][:7],
                            "Author": run["actor"]["login"],
                            "Created": pd.to_datetime(run["created_at"]).strftime("%Y-%m-%d %H:%M:%S"),
                            "Link": f"[View Run](https://github.com/{repo_owner}/{repo_name}/actions/runs/{run['id']})"
                        })
            
            df = pd.DataFrame(df_data)
            
            if not df.empty:
                # Display table with formatting
                st.subheader("Workflow Runs")
                
                # Use dataframe display
                display_df = df.copy()
                display_df["Conclusion"] = display_df["Conclusion"].apply(
                    lambda x: f"✅ {x}" if x == "success" else 
                              f"❌ {x}" if x == "failure" else 
                              f"⏳ {x}" if x in ["in_progress", "neutral"] else 
                              f"⚠️ {x}"
                )
                
                st.dataframe(
                    display_df.drop("Link", axis=1),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"workflow_runs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Detailed view
                st.subheader("Detailed View")
                
                if st.checkbox("Show detailed breakdown"):
                    # Group by conclusion
                    for conclusion in ["success", "failure"]:
                        runs_filtered = [r for r in runs if r["conclusion"] == conclusion]
                        if runs_filtered:
                            icon = "✅" if conclusion == "success" else "❌"
                            with st.expander(f"{icon} {conclusion.upper()} Runs ({len(runs_filtered)})"):
                                for run in runs_filtered[:5]:  # Show latest 5
                                    col1, col2, col3 = st.columns([2, 1, 1])
                                    with col1:
                                        st.write(f"**{run['name']}**")
                                        st.caption(f"Branch: {run['head_branch']}")
                                    with col2:
                                        st.write(pd.to_datetime(run["created_at"]).strftime("%Y-%m-%d %H:%M"))
                                    with col3:
                                        if st.button("View", key=run["id"]):
                                            st.link_button(
                                                "Open in GitHub",
                                                f"https://github.com/{repo_owner}/{repo_name}/actions/runs/{run['id']}"
                                            )
            else:
                st.info("No workflow runs match the selected filters.")
        else:
            st.warning("No workflow runs found in this repository.")
    else:
        st.error("Unable to fetch workflow data. Please check your token and repository details.")
else:
    st.info("👈 Please configure your repository details in the sidebar.")

# Footer
st.divider()
st.caption("🔄 Dashboard updates every 5 minutes | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
