# GitHub Actions Dashboard 🚀

A Streamlit-based dashboard to track and visualize GitHub Actions workflow status in real-time.

## Features

✅ **Real-time Workflow Monitoring**
- View all workflow runs with their current status
- Track pass/fail metrics at a glance
- Monitor in-progress workflows

📊 **Analytics & Metrics**
- Total runs counter
- Pass/Fail statistics with percentages
- In-progress workflow count
- Group workflows by status and conclusion

🔍 **Advanced Filtering**
- Filter by workflow status (completed, in-progress)
- Filter by result (success, failure, neutral, cancelled)
- View detailed breakdown of each workflow

📥 **Export Capabilities**
- Download workflow data as CSV
- Generate reports with timestamps

🔗 **Quick Links**
- Direct links to GitHub Actions runs
- View commit details
- Author information

## Setup

### Prerequisites
- Python 3.8+
- GitHub Personal Access Token (PAT) with `actions:read` scope
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/NaveenKondapuram/gitactionboard.git
   cd gitactionboard
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

#### Get GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" (Classic)
3. Select scope: `repo` and `actions:read`
4. Copy the token

#### Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

#### Using Environment Variables (Recommended)
```bash
export GITHUB_TOKEN="your_token_here"
streamlit run app.py
```

## Usage

1. **Configure in Sidebar**
   - Paste your GitHub token
   - Enter repository owner (e.g., `NaveenKondapuram`)
   - Enter repository name (e.g., `gitactionboard`)

2. **View Dashboard**
   - See metrics: Total runs, passed, failed, in-progress
   - Browse workflow runs in the table
   - Filter by status and conclusion

3. **Export Data**
   - Click "Download as CSV" to export workflow data
   - Import into your analytics tools

## Workflow Run Status Meanings

- **✅ Success**: Workflow completed without errors
- **❌ Failure**: Workflow completed with errors
- **⏳ In Progress**: Workflow is currently running
- **⚠️ Neutral**: Workflow completed but was cancelled or skipped
- **⚠️ Cancelled**: Workflow was manually cancelled

## API Rate Limits

- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour

The dashboard caches data for 5 minutes to minimize API calls.

## Troubleshooting

### "Error fetching workflow data"
- Check your GitHub token is valid
- Verify the repository owner and name are correct
- Ensure token has `actions:read` permission

### "No workflow runs found"
- Repository has no workflows yet
- Workflows haven't run in the monitored period

### Rate limit exceeded
- Wait for the cache to clear (5 minutes)
- Use an authenticated token for higher limits

## Project Structure

```
gitactionboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .github/workflows/    # CI/CD workflows
```

## Future Enhancements

- 📈 Historical trend analysis
- 🔔 Slack/Email notifications for failures
- 📅 Scheduled report generation
- 🎯 Workflow performance analytics
- 🏷️ Custom filtering by workflow name and tags
- 📱 Mobile-friendly responsive design

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ by [NaveenKondapuram](https://github.com/NaveenKondapuram)
