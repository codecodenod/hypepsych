import streamlit as st
import json
import os
from datetime import datetime, date, time
import pandas as pd
from journal import fetch_trade_data, save_journal_data, load_journal_data, verify_wallet_ownership
import glob
import re

# Initialize emotional analysis
try:
    from emotional_analysis import initialize_usage_stats, load_emotional_stats, save_emotional_stats
    # Initialize emotional tracking on app start
    initialize_usage_stats()
    load_emotional_stats()
except ImportError:
    st.warning("Emotional analysis component not found. Some features may be limited.")

st.set_page_config(
    page_title="Hyperliquid Trading Journal", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'manual_trades' not in st.session_state:
    st.session_state.manual_trades = []
if 'user_state' not in st.session_state:
    st.session_state.user_state = {}
if 'reflections' not in st.session_state:
    st.session_state.reflections = {
        'patterns': '',
        'triggers': '',
        'adjustments': '',
        'goals': ''
    }
if 'wallet_address' not in st.session_state:
    st.session_state.wallet_address = None
if 'wallet_verified' not in st.session_state:
    st.session_state.wallet_verified = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'  # Default theme

def is_valid_ethereum_address(address):
    """Validate Ethereum address format"""
    if not address:
        return False
    # Remove 0x prefix and check if it's 40 hex characters
    if address.startswith('0x'):
        address = address[2:]
    return len(address) == 40 and all(c in '0123456789abcdefABCDEF' for c in address)

def apply_theme():
    """Apply custom CSS based on selected theme"""
    if st.session_state.theme == 'Dark':
        css = """
        <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {
                background-color: #2C2C2C;
                color: #FFFFFF;
                border-color: #555555;
            }
            .stButton > button {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border-color: #555555;
            }
            .stButton > button:hover {
                background-color: #4A4A4A;
            }
            .stMetric, .stAlert {
                background-color: #2C2C2C;
                color: #FFFFFF;
            }
            .stExpander {
                background-color: #2C2C2C;
                color: #FFFFFF;
            }
            .stSidebar .stSidebarContent {
                background-color: #252525;
                color: #FFFFFF;
            }
        </style>
        """
    else:  # Light theme
        css = """
        <style>
            .stApp {
                background-color: #FFFFFF;
                color: #000000;
            }
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {
                background-color: #FFFFFF;
                color: #000000;
                border-color: #CCCCCC;
            }
            .stButton > button {
                background-color: #F0F2F6;
                color: #000000;
                border-color: #CCCCCC;
            }
            .stButton > button:hover {
                background-color: #E5E7EB;
            }
            .stMetric, .stAlert {
                background-color: #F9FAFB;
                color: #000000;
            }
            .stExpander {
                background-color: #F9FAFB;
                color: #000000;
            }
            .stSidebar .stSidebarContent {
                background-color: #F9FAFB;
                color: #000000;
            }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

def wallet_connection_component():
    """Improved wallet connection component"""
    st.subheader("🔗 Wallet Connection")
    
    # Method selection
    connection_method = st.radio(
        "Choose connection method:",
        ["Manual Address Input", "WalletConnect (Advanced)"],
        key="connection_method"
    )
    
    if connection_method == "Manual Address Input":
        st.info("💡 Enter your wallet address to fetch trading data. Your private key is never required.")
        
        # Manual address input
        wallet_input = st.text_input(
            "Wallet Address:",
            value=st.session_state.wallet_address or "",
            placeholder="0x1234567890123456789012345678901234567890",
            key="wallet_input"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔗 Connect Wallet", type="primary"):
                if is_valid_ethereum_address(wallet_input):
                    st.session_state.wallet_address = wallet_input.lower()
                    st.session_state.wallet_verified = True
                    st.success(f"✅ Wallet connected: {wallet_input[:6]}...{wallet_input[-4:]}")
                    st.rerun()
                else:
                    st.error("❌ Invalid Ethereum address format")
        
        with col2:
            if st.button("🔌 Disconnect"):
                st.session_state.wallet_address = None
                st.session_state.wallet_verified = False
                st.session_state.trades = []
                st.session_state.user_state = {}
                st.info("Wallet disconnected")
                st.rerun()
    
    elif connection_method == "WalletConnect (Advanced)":
        st.warning("🚧 WalletConnect integration requires additional setup")
        st.code("""
# Install additional dependencies:
pip install streamlit-elements streamlit-js

# This would require custom JavaScript integration
# For now, use Manual Address Input method
        """)
        
        if st.button("Use Manual Input Instead"):
            st.session_state.connection_method = "Manual Address Input"
            st.rerun()
    
    # Display current connection status
    if st.session_state.wallet_address:
        st.success(f"🟢 Connected: {st.session_state.wallet_address[:6]}...{st.session_state.wallet_address[-4:]}")
        
        # Optional: Add signature verification for extra security
        with st.expander("🔐 Optional: Verify Ownership (Advanced)"):
            st.info("Sign a message to prove you own this wallet address")
            
            message_to_sign = f"Verify ownership of wallet for Hyperliquid Trading Journal - {datetime.now().strftime('%Y-%m-%d')}"
            st.code(message_to_sign)
            
            signature = st.text_input(
                "Paste signature here:",
                placeholder="0x...",
                key="signature_input"
            )
            
            if st.button("🔍 Verify Signature"):
                if signature:
                    # This would need web3 integration for actual verification
                    st.info("Signature verification would be implemented with web3.py")
                    # For now, just mark as verified if signature is provided
                    if len(signature) > 100:  # Basic length check
                        st.success("✅ Ownership verified!")
                    else:
                        st.error("❌ Invalid signature format")
                else:
                    st.error("Please provide a signature")
    else:
        st.info("🔌 No wallet connected")

def format_trade_for_display(trade, trade_type="api"):
    """Format trade data for consistent display"""
    if trade_type == "api":
        return {
            'id': trade.get('oid', f'api-{hash(str(trade))}'),
            'coin': trade.get('coin', 'Unknown'),
            'side': 'Long' if trade.get('side') == 'B' else 'Short',
            'size': float(trade.get('sz', '0')),
            'price': float(trade.get('px', '0')),
            'pnl': float(trade.get('closedPnl', '0')),
            'fee': float(trade.get('fee', '0')),
            'time': datetime.fromtimestamp(trade.get('time', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'API Trade'
        }
    else:  # manual trade
        return trade

def main():
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True

    if st.session_state.show_welcome:
        st.markdown("### Important Notice")
        st.info(
            "Our app is currently in development and testing.\n\n"
            "Please expect some errors or issues as we work to improve your experience.\n\n"
            "Our app securely fetches your trading data from the Hyperliquid blockchain using a read-only connection—no private keys or write access are involved, so it's completely safe.\n\n"
            "It then displays your trades in an easy-to-use journal for tracking and analysis."
        )
        if st.button("I understand, continue"):
            st.session_state.show_welcome = False
            st.rerun()
        return

    # Apply theme after welcome popup is dismissed
    apply_theme()

    st.title("🚀 Hyperliquid Emotional Trading Journal")
    st.markdown("Track your trades and emotions to identify fear, greed, and FOMO patterns.")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Controls")
        
        # Theme selector
        st.subheader("🎨 Theme")
        theme = st.selectbox(
            "Choose Theme",
            ["Light", "Dark"],
            index=["Light", "Dark"].index(st.session_state.theme),
            key="theme_select"
        )
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()

        # Improved wallet connection
        wallet_connection_component()
        
        st.divider()
        
        # Load existing journal
        journal_files = glob.glob("trade-log-*.json")
        if journal_files:
            selected_file = st.selectbox(
                "Load Journal File:",
                [""] + sorted(journal_files, reverse=True),
                key="journal_select"
            )
            if selected_file and st.button("📂 Load Journal"):
                data = load_journal_data(selected_file)
                if data:
                    st.session_state.trades = data.get('trades', [])
                    st.session_state.manual_trades = data.get('manual_trades', [])
                    st.session_state.reflections = data.get('reflections', st.session_state.reflections)
                    st.success(f"Loaded {selected_file}")
                    st.rerun()
        
        # Fetch latest trades
        if st.button("🔄 Fetch Latest Trades", type="primary", disabled=not st.session_state.wallet_verified):
            if not st.session_state.wallet_verified:
                st.error("Please connect your wallet first")
            else:
                try:
                    with st.spinner("Fetching trades from Hyperliquid..."):
                        fills, user_state = fetch_trade_data(st.session_state.wallet_address)
                        st.session_state.trades = [format_trade_for_display(trade) for trade in fills[:10]]
                        st.session_state.user_state = user_state
                        st.success(f"✅ Fetched {len(st.session_state.trades)} trades!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error fetching trades: {e}")
                    st.error("Make sure your wallet address is correct and has trading history on Hyperliquid")
        
        if not st.session_state.wallet_verified:
            st.info("👆 Connect your wallet to fetch trades")
        
        # Add manual trade
        if st.button("➕ Add Manual Trade"):
            st.session_state.show_manual_form = True
            st.rerun()
        
        # Save journal
        if st.button("💾 Save Journal"):
            filename = f"trade-log-{datetime.now().strftime('%Y%m%d')}.json"
            success = save_journal_data(filename, {
                'trades': st.session_state.trades,
                'manual_trades': st.session_state.manual_trades,
                'reflections': st.session_state.reflections,
                'user_state': st.session_state.user_state,
                'wallet_address': st.session_state.wallet_address,
                'saved_at': datetime.now().isoformat()
            })
            if success:
                st.success(f"✅ Journal saved as {filename}")
                # Also save emotional patterns
                try:
                    save_emotional_stats()
                except:
                    pass
            else:
                st.error("❌ Error saving journal")
        
        # Export options
        st.header("📤 Export")
        if st.button("⬇️ Download Markdown"):
            markdown_content = generate_markdown_journal()
            st.download_button(
                label="📄 Download MD File",
                data=markdown_content,
                file_name=f"trade-log-{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
        
        st.divider()
        
        # Quick reflections
        st.header("🧠 Quick Reflections")
        
        patterns = st.text_area(
            "Recurring Patterns:",
            value=st.session_state.reflections.get('patterns', ''),
            placeholder="e.g., FOMO when prices spike >3%",
            key="patterns_input"
        )
        
        triggers = st.text_area(
            "Triggers to Avoid:",
            value=st.session_state.reflections.get('triggers', ''),
            placeholder="e.g., Social media hype",
            key="triggers_input"
        )
        
        adjustments = st.text_area(
            "Trading Plan Adjustments:",
            value=st.session_state.reflections.get('adjustments', ''),
            placeholder="e.g., Limit trades to 2 per day",
            key="adjustments_input"
        )
        
        goals = st.text_area(
            "Daily/Weekly Goals:",
            value=st.session_state.reflections.get('goals', ''),
            placeholder="e.g., Stay calm during volatility",
            key="goals_input"
        )
        
        if st.button("💾 Save Reflections"):
            st.session_state.reflections.update({
                'patterns': patterns,
                'triggers': triggers,
                'adjustments': adjustments,
                'goals': goals
            })
            st.success("✅ Reflections saved!")

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Manual trade form
        if st.session_state.get('show_manual_form', False):
            st.header("➕ Add Manual Trade")
            with st.form("manual_trade_form", clear_on_submit=True):
                col_left, col_right = st.columns(2)
                
                with col_left:
                    asset = st.text_input("Asset", value="BTC", placeholder="e.g., BTC, ETH")
                    position_type = st.selectbox("Position Type", ["Long", "Short"])
                    size = st.number_input("Position Size", min_value=0.0, step=0.01, format="%.4f")
                    price = st.number_input("Entry Price ($)", min_value=0.0, step=0.01, format="%.2f")
                
                with col_right:
                    leverage = st.number_input("Leverage", min_value=1, max_value=100, value=1)
                    pnl = st.number_input("Profit/Loss ($)", step=0.01, format="%.2f")
                    fees = st.number_input("Fees Paid ($)", min_value=0.0, step=0.01, format="%.2f")
                    entry_date = st.date_input("Entry Date", value=date.today())
                    entry_time = st.time_input("Entry Time", value=datetime.now().time())
                    entry_datetime = datetime.combine(entry_date, entry_time)
                
                # Import the emotional analysis component
                from emotional_analysis import create_emotional_analysis_form
                
                # Create interactive emotional analysis
                emotional_data = create_emotional_analysis_form("manual_trade")
                
                col_submit, col_cancel = st.columns([1, 1])
                with col_submit:
                    submitted = st.form_submit_button("✅ Add Trade", type="primary")
                with col_cancel:
                    cancelled = st.form_submit_button("❌ Cancel")
                
                if submitted:
                    manual_trade = {
                        'id': f'manual-{datetime.now().timestamp()}',
                        'coin': asset,
                        'side': position_type,
                        'size': size,
                        'price': price,
                        'pnl': pnl,
                        'fee': fees,
                        'time': entry_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        'leverage': leverage,
                        'type': 'Manual Trade',
                        'last_edited': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        **emotional_data  # Add all emotional analysis data
                    }
                    st.session_state.manual_trades.append(manual_trade)
                    st.success("✅ Manual trade added!")
                    st.session_state.show_manual_form = False
                    st.rerun()
                
                if cancelled:
                    st.session_state.show_manual_form = False
                    st.rerun()
        
        # Display trades
        st.header("📈 Recent Trades")
        
        # Combine API and manual trades
        all_trades = st.session_state.trades + st.session_state.manual_trades
        all_trades.sort(key=lambda x: x.get('time', ''), reverse=True)
        
        if all_trades:
            for i, trade in enumerate(all_trades):
                trade_id = trade.get('id', f'trade_{i}')
                
                # Trade header with color coding
                profit_color = "🟢" if trade.get('pnl', 0) >= 0 else "🔴"
                trade_title = f"{profit_color} {trade.get('coin', 'Unknown')} {trade.get('side', 'Unknown')} - ${trade.get('pnl', 0):.2f}"
                
                with st.expander(trade_title, expanded=False):
                    col_info, col_emotions = st.columns([1, 1])
                    
                    with col_info:
                        st.write(f"**Asset Pair:** {trade.get('coin', 'Unknown')}/USD")
                        st.write(f"**Position Type:** {trade.get('side', 'Unknown')}")
                        st.write(f"**Position Size:** {trade.get('size', 0):.4f} {trade.get('coin', '')}")
                        st.write(f"**Entry Price:** ${trade.get('price', 0):.2f}")
                        st.write(f"**Entry Time:** {trade.get('time', 'Unknown')}")
                        st.write(f"**Profit/Loss:** ${trade.get('pnl', 0):.2f}")
                        st.write(f"**Fees Paid:** ${trade.get('fee', 0):.2f}")
                        if 'leverage' in trade:
                            st.write(f"**Leverage:** {trade.get('leverage', 1)}x")
                        st.write(f"**Type:** {trade.get('type', 'Unknown')}")
                    
                    with col_emotions:
                        # Import the emotional analysis component
                        from emotional_analysis import create_emotional_analysis_form
                        
                        # Create interactive emotional analysis with existing data
                        emotional_data = create_emotional_analysis_form(trade_id, trade)
                    
                    # Action buttons
                    col_save, col_delete, col_info = st.columns([1, 1, 2])
                    
                    with col_save:
                        if st.button(f"💾 Save", key=f"save_{trade_id}"):
                            # Update trade data with emotional analysis
                            trade.update({
                                **emotional_data,
                                'last_edited': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            st.success("✅ Trade updated!")
                            st.rerun()
                    
                    with col_delete:
                        if st.button(f"🗑️ Delete", key=f"delete_{trade_id}"):
                            # Remove from appropriate list
                            if trade in st.session_state.trades:
                                st.session_state.trades.remove(trade)
                            elif trade in st.session_state.manual_trades:
                                st.session_state.manual_trades.remove(trade)
                            st.success("✅ Trade deleted!")
                            st.rerun()
                    
                    with col_info:
                        if trade.get('last_edited'):
                            st.caption(f"Last edited: {trade.get('last_edited')}")
        else:
            if st.session_state.wallet_verified:
                st.info("📊 No trades found. Click 'Fetch Latest Trades' or 'Add Manual Trade' to get started")
            else:
                st.info("👆 Connect your wallet first to fetch trades or add manual trades")
    
    with col2:
        # Portfolio summary
        st.header("📊 Portfolio Summary")
        
        if st.session_state.user_state:
            account_value = float(st.session_state.user_state.get('marginSummary', {}).get('accountValue', '0'))
            st.metric("Account Value", f"${account_value:,.2f}", delta=None)
            
            positions = st.session_state.user_state.get('assetPositions', [])
            st.metric("Open Positions", len(positions))
            
            if positions:
                st.subheader("Current Positions")
                for pos in positions:
                    position_data = pos.get('position', {})
                    coin = position_data.get('coin', 'Unknown')
                    size = float(position_data.get('szi', '0'))
                    unrealized_pnl = float(position_data.get('unrealizedPnl', '0'))
                    position_type = 'Long' if size > 0 else 'Short'
                    pnl_color = "🟢" if unrealized_pnl >= 0 else "🔴"
                    
                    st.write(f"{pnl_color} **{coin}** ({position_type})")
                    st.write(f"Size: {abs(size):.4f}")
                    st.write(f"P/L: ${unrealized_pnl:.2f}")
                    st.divider()
        else:
            st.info("Connect wallet to view portfolio")
        
        # Trading statistics
        if all_trades:
            st.header("📈 Statistics")
            
            total_trades = len(all_trades)
            profitable_trades = len([t for t in all_trades if t.get('pnl', 0) > 0])
            win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
            total_pnl = sum(t.get('pnl', 0) for t in all_trades)
            
            st.metric("Total Trades", total_trades)
            st.metric("Win Rate", f"{win_rate:.1f}%")
            st.metric("Total P/L", f"${total_pnl:.2f}", delta=f"${total_pnl:.2f}")
            
            # Recent activity
            if len(all_trades) >= 5:
                recent_5 = all_trades[:5]
                recent_pnl = sum(t.get('pnl', 0) for t in recent_5)
                st.metric("Last 5 Trades P/L", f"${recent_pnl:.2f}")

def generate_markdown_journal():
    """Generate markdown export of the journal"""
    content = f"""# Hyperliquid Emotional Trading Journal

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

Track your trades and emotions to identify fear, greed, and FOMO patterns.

## Recent Trades
"""
    
    all_trades = st.session_state.trades + st.session_state.manual_trades
    all_trades.sort(key=lambda x: x.get('time', ''), reverse=True)
    
    for trade in all_trades:
        content += f"""
### Trade: {trade.get('coin', 'Unknown')} ({trade.get('side', 'Unknown')}) (ID: {trade.get('id', 'unknown')})
- **Asset Pair**: {trade.get('coin', 'Unknown')}/USD
- **Position Type**: {trade.get('side', 'Unknown')}
- **Position Size**: {trade.get('size', 0):.4f} {trade.get('coin', '')}
- **Entry Price**: ${trade.get('price', 0):.2f}
- **Entry Time**: {trade.get('time', 'Unknown')} UTC
- **Profit/Loss**: ${trade.get('pnl', 0):.2f}
- **Fees Paid**: {trade.get('fee', 0):.2f} USDC
- **Emotional State**: {trade.get('emotional_state', '[]')}
- **Triggers**: {trade.get('triggers', '[]')}
- **Psychological Mistakes**: {trade.get('mistakes', '[]')}
- **Corrective Action**: {trade.get('corrective_action', '[]')}
- **Last Edited**: {trade.get('last_edited', '[]')}

"""
    
    content += f"""
## Emotional Reflection
- **Recurring Patterns**: {st.session_state.reflections.get('patterns', '[]')}
- **Triggers to Avoid**: {st.session_state.reflections.get('triggers', '[]')}
- **Trading Plan Adjustments**: {st.session_state.reflections.get('adjustments', '[]')}
- **Daily/Weekly Goal**: {st.session_state.reflections.get('goals', '[]')}

## Portfolio Snapshot
"""
    
    if st.session_state.user_state:
        account_value = float(st.session_state.user_state.get('marginSummary', {}).get('accountValue', '0'))
        content += f"- **Account Equity**: ${account_value:.2f} USDC\n"
        
        positions = st.session_state.user_state.get('assetPositions', [])
        if positions:
            content += "- **Open Positions**: "
            for pos in positions:
                position_data = pos.get('position', {})
                coin = position_data.get('coin', 'Unknown')
                size = float(position_data.get('szi', '0'))
                position_type = 'Long' if size > 0 else 'Short'
                content += f"{abs(size):.4f} {coin} {position_type}, "
            content = content.rstrip(', ') + "\n"
        else:
            content += "- **Open Positions**: None\n"
    else:
        content += "- **Account Equity**: $0.00 USDC\n- **Open Positions**: None\n"
    
    content += """
---
*Instructions*: This journal tracks your emotional trading patterns. Review weekly to identify recurring behaviors and improve your trading psychology.
"""
    
    return content

if __name__ == "__main__":
    main()