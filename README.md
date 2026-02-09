# 💰 Gold Portfolio Tracker

A mobile-friendly web application to track your gold purchases and monitor portfolio value in real-time. Fetches live gold prices from Galeri24 and calculates profit/loss automatically.

![Gold Portfolio Tracker](https://img.shields.io/badge/status-ready-success)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)

## ✨ Features

- 📱 **Mobile-First Design** - Optimized for phones, tablets, and desktop
- 💰 **Real-Time Pricing** - Live gold prices from Galeri24
- 📊 **Portfolio Tracking** - Track all your gold purchases
- 📈 **Profit/Loss Calculator** - Automatic calculation based on current prices
- 🗄️ **Cloud Database** - Turso database for reliable data storage
- 🚀 **Railway Ready** - One-click deployment to Railway

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Turso account (free tier available)
- Railway account (for deployment)

### Local Development

1. **Clone and navigate to the project**
   ```bash
   cd /Users/nawidodo/Development/Python/gol-d-roger
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   TURSO_DATABASE_URL=libsql://your-database.turso.io
   TURSO_AUTH_TOKEN=your-auth-token
   FLASK_SECRET_KEY=your-random-secret-key
   FLASK_ENV=development
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🗄️ Database Setup (Turso)

1. **Install Turso CLI**
   ```bash
   brew install tursodatabase/tap/turso
   ```

2. **Login to Turso**
   ```bash
   turso auth login
   ```

3. **Create database**
   ```bash
   turso db create gold-tracker
   ```

4. **Get database URL**
   ```bash
   turso db show gold-tracker --url
   ```

5. **Create auth token**
   ```bash
   turso db tokens create gold-tracker
   ```

6. **Add credentials to `.env`**

The database tables will be created automatically when you first run the app.

## 🚂 Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Add environment variables**
   ```bash
   railway variables set TURSO_DATABASE_URL="your-database-url"
   railway variables set TURSO_AUTH_TOKEN="your-auth-token"
   railway variables set FLASK_SECRET_KEY="your-secret-key"
   railway variables set FLASK_ENV="production"
   ```

5. **Deploy**
   ```bash
   railway up
   ```

6. **Get deployment URL**
   ```bash
   railway domain
   ```

## 📁 Project Structure

```
gol-d-roger/
├── app.py                 # Flask application & API endpoints
├── database.py            # Database configuration
├── models.py              # SQLAlchemy models
├── galeri24.py           # Gold price scraper
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── runtime.txt           # Python version
├── .env.example          # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css     # Styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── templates/
    └── index.html        # Main HTML template
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/prices` | Get current gold prices from Galeri24 |
| GET | `/api/purchases` | List all purchases |
| POST | `/api/purchases` | Create new purchase |
| PUT | `/api/purchases/<id>` | Update purchase |
| DELETE | `/api/purchases/<id>` | Delete purchase |
| GET | `/api/portfolio` | Get portfolio summary |

## 🎨 Design Features

- **Dark Theme** - Gold and black color scheme
- **Glassmorphism** - Modern frosted glass effects
- **Smooth Animations** - Micro-interactions for premium feel
- **Responsive Grid** - Adapts to any screen size
- **Touch-Friendly** - Optimized for mobile interactions

## 🧪 Testing

Test the price scraper:
```bash
python galeri24.py
```

Test the Flask app:
```bash
python app.py
```

## 📝 Usage

1. **View Current Prices** - See live gold prices in the header ticker
2. **Add Purchase** - Fill in the form with weight, price, and date
3. **Track Portfolio** - View total gold, invested amount, and current value
4. **Monitor Profit/Loss** - See real-time profit/loss calculations
5. **Manage Purchases** - Edit or delete purchases as needed

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use strong secret keys in production
- Keep Turso auth tokens secure
- Enable HTTPS in production (Railway does this automatically)

## 🐛 Troubleshooting

**Database connection error:**
- Verify Turso credentials in `.env`
- Check database URL format: `libsql://your-db.turso.io`

**Price fetching fails:**
- Check internet connection
- Galeri24 website might be down or changed structure

**Railway deployment fails:**
- Verify all environment variables are set
- Check Railway logs: `railway logs`

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 🤝 Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using Flask, Turso, and Railway
