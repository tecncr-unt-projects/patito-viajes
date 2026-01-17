# 🦆 Patito Viajes

A powerful travel planning automation tool that combines n8n workflow automation with a Streamlit frontend to help you discover and plan your perfect trip.

[Español](README_ES.md) | English

## 📋 Overview

Patito Viajes is an intelligent travel planning assistant that leverages AI and multiple data sources to provide comprehensive travel information. The system extracts real-time data from:

- ✈️ **Google Flights** - Flight options and pricing
- 🏨 **Google Hotels** - Accommodation options and rates
- 🎯 **Activities & Attractions** - Things to do at your destination using AI recommendations

All data extraction is powered by **SerpAPI's official n8n node**, ensuring reliable and structured data from Google's search results.

## 🏗️ Architecture

The system consists of two main components:

### 1. n8n Workflow Backend
- **Purpose**: Data extraction and processing engine
- **Technology**: n8n (workflow automation platform)
- **Integration**: SerpAPI official n8n node
- **Functions**:
  - Receives travel search requests
  - Queries Google Flights via SerpAPI
  - Queries Google Hotels via SerpAPI
  - Queries activities and attractions using AI Mode
  - Aggregates and processes results
  - Returns structured data to the frontend

### 2. Streamlit Frontend
- **Purpose**: User interface for travel planning
- **Technology**: Streamlit (Python web framework)
- **Functions**:
  - Collects user travel preferences (destination, dates, budget)
  - Sends requests to n8n workflow
  - Displays search results in an intuitive interface
  - Allows comparison of flights and hotels
  - Shows recommended activities

### Data Flow

```
User Input (Streamlit)
    ↓
Travel Search Request
    ↓
n8n Workflow Orchestration
    ↓
├── SerpAPI: Google Flights
├── SerpAPI: Google Hotels
└── SerpAPI: Activities (AI Mode)
    ↓
Data Aggregation & Processing
    ↓
Results Display (Streamlit)
```

## 🎨 Design Notes

### n8n Workflow Design

The n8n workflow is designed with modularity and reliability in mind:

1. **Input Validation Node**: Validates incoming travel parameters (destination, dates, passenger count)
2. **Parallel Processing**: Flight, hotel, and activity searches run in parallel for performance
3. **Error Handling**: Each API call includes retry logic and fallback mechanisms
4. **Data Transformation**: Raw SerpAPI responses are transformed into a unified format
5. **Response Aggregation**: Results are combined into a single structured response

### SerpAPI Integration

- Uses the official SerpAPI n8n node for reliability
- Configured with appropriate search parameters for each service:
  - **Flights**: Departure/arrival airports, dates, passenger count, class
  - **Hotels**: Location, check-in/out dates, guests, filters (price, rating)
  - **Activities**: Location-based queries with AI Mode for contextual recommendations

### Streamlit Frontend Design

- **Clean Interface**: Minimalist design focusing on user experience
- **Progressive Disclosure**: Advanced options hidden until needed
- **Real-time Updates**: Loading indicators during API calls
- **Responsive Layout**: Works on desktop and tablet devices
- **Result Visualization**: Cards, tables, and charts for easy comparison

## 📦 Prerequisites

Before deploying Patito Viajes, ensure you have:

- **Python 3.8+** (for Streamlit frontend)
- **n8n instance** (self-hosted or cloud)
- **SerpAPI Account** with API key ([Get one here](https://serpapi.com/))
- **Docker** (optional, for containerized deployment)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tecncr/patito-viajes.git
cd patito-viajes
```

### 2. Set Up the n8n Workflow

#### Option A: n8n Cloud
1. Log in to your n8n cloud account
2. Import the workflow JSON file: `workflow/patito-viajes-workflow.json`
3. Configure SerpAPI credentials in n8n
4. Activate the workflow
5. Note the webhook URL for the Streamlit app

#### Option B: Self-hosted n8n
1. Install n8n:
   ```bash
   npm install -g n8n
   ```

2. Start n8n:
   ```bash
   n8n start
   ```

3. Access n8n at `http://localhost:5678`
4. Import the workflow: `workflow/patito-viajes-workflow.json`
5. Configure SerpAPI credentials
6. Activate the workflow

### 3. Set Up the Streamlit Frontend

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   ```
   N8N_WEBHOOK_URL=your_n8n_webhook_url
   SERPAPI_KEY=your_serpapi_key
   ```

## ⚙️ Configuration

### SerpAPI Configuration

1. Sign up at [SerpAPI](https://serpapi.com/)
2. Get your API key from the dashboard
3. Add the API key to n8n credentials:
   - Go to **Credentials** → **New**
   - Select **SerpAPI**
   - Enter your API key
   - Save as "SerpAPI Patito Viajes"

### n8n Workflow Configuration

Open the workflow in n8n and configure:

1. **SerpAPI Nodes**: Link to your SerpAPI credentials
2. **Webhook Node**: Set authentication if needed
3. **Response Node**: Ensure proper data formatting
4. **Error Handling**: Configure notification preferences

### Streamlit Configuration

The `.env` file controls the Streamlit app configuration:

```env
# n8n Configuration
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/patito-viajes

# SerpAPI Configuration (if calling directly)
SERPAPI_KEY=your_serpapi_api_key

# App Configuration
APP_TITLE=Patito Viajes
DEFAULT_CURRENCY=USD
RESULTS_PER_PAGE=10
```

## 🌐 Deployment

### Local Deployment

1. Start n8n (if self-hosted):
   ```bash
   n8n start
   ```

2. Start Streamlit:
   ```bash
   streamlit run app.py
   ```

3. Access the app at `http://localhost:8501`

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t patito-viajes .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 --env-file .env patito-viajes
   ```

### Cloud Deployment

#### Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy your fork
4. Add environment variables in Streamlit Cloud settings

#### Heroku

1. Install Heroku CLI
2. Create a new Heroku app:
   ```bash
   heroku create patito-viajes
   ```

3. Set environment variables:
   ```bash
   heroku config:set N8N_WEBHOOK_URL=your_webhook_url
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

#### Railway

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically on push

## 📖 Usage

1. **Open the Streamlit App**: Navigate to your deployed URL or `localhost:8501`

2. **Enter Travel Details**:
   - Destination city or airport code
   - Departure city or airport code
   - Travel dates (departure and return)
   - Number of passengers
   - Budget preferences (optional)

3. **Search**: Click "Find My Trip" to start the search

4. **View Results**:
   - **Flights Tab**: Compare flight options, prices, and durations
   - **Hotels Tab**: Browse accommodation options with ratings and prices
   - **Activities Tab**: Discover things to do at your destination

5. **Export Results**: Download results as PDF or share link

## 📁 Project Structure

```
patito-viajes/
├── workflow/
│   └── patito-viajes-workflow.json    # n8n workflow definition
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── Dockerfile                          # Docker configuration
├── README.md                           # English documentation
├── README_ES.md                        # Spanish documentation
└── assets/
    ├── logo.png                        # App logo
    └── screenshots/                    # App screenshots
```

## 🔧 Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black app.py
flake8 app.py
```

### Adding Features

The architecture is designed to be extensible:

1. **New Data Sources**: Add new SerpAPI nodes in the n8n workflow
2. **Custom Filters**: Extend the Streamlit sidebar with additional filters
3. **Export Formats**: Add new export options in the results display
4. **UI Themes**: Customize the Streamlit theme in `.streamlit/config.toml`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **n8n** - Workflow automation platform
- **SerpAPI** - Google Search API provider
- **Streamlit** - Python web framework
- **Google** - Flight, hotel, and activity data sources

## 📧 Support

For support, please open an issue on GitHub or contact [code@tecncr.com](mailto:code@tecncr.com).

## 🔗 Links

- [n8n Documentation](https://docs.n8n.io/)
- [SerpAPI Documentation](https://serpapi.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

Made with ❤️ by [tecncr](https://github.com/tecncr)
