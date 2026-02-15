# Local Setup Instructions

To run the Mortgage Price Analyzer on your local machine, follow these steps:

### Prerequisites
- Python 3.11 or higher
- `uv` (recommended) or `pip`

### Steps
1. **Clone the repository** (or download the source code).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # OR if using uv:
   uv pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   Create a `.env` file in the root directory with the following:
   ```env
   UWM_USERNAME=your_username
   UWM_PASSWORD=your_password
   UWM_CLIENT_ID=your_client_id
   UWM_CLIENT_SECRET=your_client_secret
   UWM_SCOPE=your_scope
   SESSION_SECRET=a_random_secret_string
   ```
4. **Run the application**:
   ```bash
   python main.py
   ```
   The app will be available at `http://localhost:5000`.

### Note
The application uses a local SQLite database (`project.db`) which is automatically created and seeded with sample data on the first run.
