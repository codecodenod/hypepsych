# 🚀 Hyperliquid Emotional Trading Journal

A comprehensive trading journal application that helps you track your trades and emotions to identify fear, greed, and FOMO patterns in your trading behavior. Built specifically for Hyperliquid traders using Streamlit.

![Trading Journal Screenshot](https://via.placeholder.com/800x400/1976D2/FFFFFF?text=Hyperliquid+Trading+Journal)

## ✨ Features

### 📊 **Trade Tracking**
- **API Integration**: Automatically fetch trades from Hyperliquid using your wallet address
- **Manual Entry**: Add trades manually with detailed information
- **Portfolio Overview**: Real-time account value and open positions
- **Trade Statistics**: Win rate, P/L analysis, and performance metrics

### 🧠 **Emotional Analysis**
- **Interactive Bubbles**: Click-to-select emotional states, triggers, and mistakes
- **Smart Tracking**: Frequently used emotions grow in prominence
- **Pattern Recognition**: Identify recurring psychological patterns
- **Corrective Actions**: Track your improvement strategies

### 💾 **Data Management**
- **Local Storage**: All data stored securely on your device
- **Export Options**: Download as Markdown or JSON
- **Backup System**: Automatic backup creation
- **Load/Save**: Persistent journal storage

### 🔒 **Security**
- **No Private Keys**: Only requires your public wallet address
- **Optional Verification**: Signature verification for additional security
- **Local Processing**: All data stays on your computer

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hyperliquid-trading-journal.git
cd hyperliquid-trading-journal
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

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
Navigate to `http://localhost:8501`

## 📦 Dependencies

- `streamlit>=1.28.0` - Web application framework
- `pandas>=1.5.0` - Data manipulation and analysis
- `hyperliquid-python-sdk>=0.1.0` - Hyperliquid API integration
- `python-dateutil>=2.8.0` - Date/time utilities
- `requests>=2.28.0` - HTTP library

## 🚀 Usage

### 1. Connect Your Wallet
- Enter your Ethereum wallet address (starts with 0x)
- No private keys required - only your public address
- Optional: Verify ownership with message signing

### 2. Fetch Trades
- Click "Fetch Latest Trades" to get your recent Hyperliquid trades
- View your portfolio summary and open positions
- Automatic trade formatting and organization

### 3. Add Emotional Analysis
- Use interactive buttons to select:
  - **Emotional States**: Fear, Greed, FOMO, Panic, etc.
  - **Triggers**: Market volatility, News, Social media, etc.
  - **Mistakes**: FOMO buying, Panic selling, Overtrading, etc.
  - **Actions**: Risk management, Research, Planning, etc.

### 4. Manual Trade Entry
- Add trades not captured by the API
- Include leverage, fees, and timing details
- Complete emotional analysis for each trade

### 5. Track Patterns
- Review your emotional patterns over time
- Identify recurring triggers and mistakes
- Monitor your psychological improvement

### 6. Export Data
- Download as Markdown for external analysis
- Save as JSON for data backup
- Export to CSV for spreadsheet analysis

## 📁 File Structure

```
hyperliquid-trading-journal/
├── app.py                      # Main Streamlit application
├── journal.py                  # Trading data fetching and storage
├── emotional_analysis.py       # Interactive emotional analysis component
├── wallet_helper.py           # Wallet connection utilities
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── data/                      # Generated data files
    ├── trade-log-YYYYMMDD.json
    ├── emotional_stats.json
    └── *.json.backup
```

## 🎯 Emotional Analysis Categories

### Emotional States
- Fear, Greed, FOMO (Fear of Missing Out)
- Panic, Overconfidence, Anxiety
- Euphoria, Doubt, Frustration, Hope

### Common Triggers
- Market volatility, Price surges/crashes
- Positive/Negative news, Social media buzz
- Seeing others' profits, Recent losses
- Winning streaks, Herd mentality

### Psychological Mistakes
- FOMO buying, Panic selling, Revenge trading
- Overconfidence bias, Overtrading
- Ignoring risk management, Chasing losses
- Poor research, Overleveraging

### Corrective Actions
- Develop clear trading plan
- Implement risk management strategies
- Conduct thorough research
- Keep trading journal, Stick to strategy
- Diversify portfolio, Set realistic goals

## 📊 Data Privacy & Security

- **Local Storage**: All data stored on your local machine
- **No Cloud Sync**: Data never leaves your computer
- **Public Address Only**: No private keys or sensitive data required
- **Optional Verification**: Signature verification available but not required
- **Backup System**: Automatic local backups created

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Reporting Issues

Please use the GitHub issue tracker to report bugs or request features.

## 📈 Roadmap

- [ ] **Multi-Exchange Support**: Add support for other DEXs and CEXs
- [ ] **Advanced Analytics**: More detailed performance metrics
- [ ] **Data Visualization**: Charts and graphs for emotional patterns
- [ ] **Export Formats**: PDF reports, Excel files
- [ ] **Mobile Responsive**: Better mobile interface
- [ ] **Themes**: Dark mode and custom themes
- [ ] **Notifications**: Alerts for emotional pattern detection

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It does not constitute financial advice. Always do your own research and consult with financial professionals before making trading decisions.

Trading cryptocurrencies involves substantial risk and may result in significant losses. Past performance does not guarantee future results.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hyperliquid](https://hyperliquid.xyz/) for providing the trading platform and API
- [Streamlit](https://streamlit.io/) for the excellent web framework
- The trading psychology research community for emotional analysis frameworks

## 📞 Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the code comments and docstrings
- **Community**: Join trading psychology discussions

---

**Made with ❤️ for traders who want to improve their psychological edge**

*"The most important thing in trading is not being right, but knowing when you're wrong and cutting your losses quickly."*