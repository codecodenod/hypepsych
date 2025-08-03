"""
Interactive Emotional Analysis Component with clickable bubbles
"""

import streamlit as st
import json
from collections import defaultdict
from typing import Dict, List, Set

# Predefined emotional analysis options
EMOTIONAL_STATES = [
    "Fear", "Greed", "FOMO (Fear of Missing Out)", "Panic", "Overconfidence", 
    "Anxiety", "Euphoria", "Doubt", "Frustration", "Hope"
]

TRIGGERS = [
    "Market volatility", "Price surges", "Price crashes", "Positive news/hype", 
    "Negative news/FUD", "Social media buzz", "Seeing others' profits", 
    "Recent losses", "Winning streaks", "Herd mentality"
]

PSYCHOLOGICAL_MISTAKES = [
    "FOMO buying", "Panic selling", "Revenge trading", "Overconfidence bias", 
    "Herd mentality", "Overtrading", "Ignoring risk management", "Chasing losses", 
    "Not doing proper research", "Overleveraging"
]

CORRECTIVE_ACTIONS = [
    "Develop a clear trading plan", "Implement risk management strategies", 
    "Conduct thorough research", "Keep a trading journal", "Stick to your strategy", 
    "Diversify your portfolio", "Set realistic goals", "Use position sizing", 
    "Take regular breaks", "Continuously educate yourself"
]

def initialize_usage_stats():
    """Initialize usage statistics for bubble sizing"""
    if 'emotional_usage_stats' not in st.session_state:
        st.session_state.emotional_usage_stats = {
            'emotional_states': defaultdict(int),
            'triggers': defaultdict(int),
            'mistakes': defaultdict(int),
            'actions': defaultdict(int)
        }

def update_usage_stats(category: str, selected_items: List[str]):
    """Update usage statistics for selected items"""
    if category in st.session_state.emotional_usage_stats:
        for item in selected_items:
            st.session_state.emotional_usage_stats[category][item] += 1

def get_bubble_size(category: str, item: str) -> str:
    """Get CSS class for bubble size based on usage frequency"""
    usage_count = st.session_state.emotional_usage_stats.get(category, {}).get(item, 0)
    
    if usage_count == 0:
        return "bubble-small"
    elif usage_count <= 2:
        return "bubble-medium"
    elif usage_count <= 5:
        return "bubble-large"
    else:
        return "bubble-xlarge"

def create_bubble_css():
    """Create CSS for button styling to look like bubbles"""
    return """
    <style>
    .section-header {
        font-weight: 600;
        color: #333;
        margin: 15px 0 10px 0;
        font-size: 16px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 5px;
    }
    
    .stButton > button {
        border-radius: 20px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 8px 16px !important;
        margin: 4px 2px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        min-height: 40px !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Primary buttons (selected) */
    .stButton > button[kind="primary"] {
        background-color: #1976D2 !important;
        border-color: #1565C0 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Secondary buttons (unselected) */
    .stButton > button[kind="secondary"] {
        background-color: white !important;
        border-color: #d0d0d0 !important;
        color: #333 !important;
    }
    
    /* Usage-based styling */
    .usage-low {
        font-size: 12px !important;
        padding: 6px 12px !important;
    }
    
    .usage-medium {
        border-color: #4CAF50 !important;
        background-color: #f1f8e9 !important;
    }
    
    .usage-high {
        border-color: #FF9800 !important;
        background-color: #fff3e0 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .selection-summary {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1976D2;
    }
    </style>
    """

def create_interactive_bubble_selector(
    title: str, 
    options: List[str], 
    category: str, 
    key_prefix: str,
    current_selections: List[str] = None
) -> List[str]:
    """Create an interactive bubble selector component using Streamlit buttons"""
    
    if current_selections is None:
        current_selections = []
    
    # Initialize session state for this selector
    session_key = f"{key_prefix}_selected"
    if session_key not in st.session_state:
        st.session_state[session_key] = set(current_selections)
    
    selected_set = st.session_state[session_key]
    
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    
    # Create buttons in a grid layout
    cols_per_row = 3
    rows = [options[i:i + cols_per_row] for i in range(0, len(options), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for i, option in enumerate(row):
            with cols[i]:
                bubble_size = get_bubble_size(category, option)
                usage_count = st.session_state.emotional_usage_stats.get(category, {}).get(option, 0)
                
                # Determine button style based on selection and usage
                if option in selected_set:
                    button_type = "primary"
                    button_label = f"✓ {option}"
                else:
                    button_type = "secondary" 
                    button_label = option
                
                # Add usage indicator
                if usage_count > 0:
                    button_label += f" ({usage_count})"
                
                # Create button with unique key
                if st.button(
                    button_label,
                    key=f"{key_prefix}_{option}",
                    type=button_type,
                    help=f"Usage: {usage_count} times" if usage_count > 0 else "Click to select"
                ):
                    # Toggle selection
                    if option in selected_set:
                        selected_set.remove(option)
                    else:
                        selected_set.add(option)
                    st.rerun()
    
    # Display current selections
    col1, col2 = st.columns([3, 1])
    with col1:
        if selected_set:
            st.markdown(f"**Selected:** {', '.join(sorted(selected_set))}")
        else:
            st.markdown("*Click buttons above to select*")
    
    with col2:
        if st.button(f"Clear All", key=f"clear_{key_prefix}"):
            selected_set.clear()
            st.rerun()
    
    # Manual text input as fallback
    with st.expander(f"➕ Add custom {title.lower()}", expanded=False):
        custom_input = st.text_input(
            f"Custom {title}:",
            key=f"custom_{key_prefix}",
            placeholder=f"Enter custom {title.lower()}..."
        )
        if custom_input:
            col_add, col_clear_input = st.columns([1, 1])
            with col_add:
                if st.button(f"Add", key=f"add_custom_{key_prefix}"):
                    selected_set.add(custom_input)
                    # Clear the input
                    st.session_state[f"custom_{key_prefix}"] = ""
                    st.rerun()
    
    return list(selected_set)

def create_emotional_analysis_form(trade_id: str = None, existing_data: Dict = None):
    """Create the complete emotional analysis form with interactive bubbles"""
    
    initialize_usage_stats()
    
    # Apply CSS
    st.markdown(create_bubble_css(), unsafe_allow_html=True)
    
    st.subheader("🧠 Emotional Analysis")
    st.markdown("*Click on the bubbles below to select your emotional state and analysis. Frequently used options will grow larger.*")
    
    # Get existing selections if available
    existing_emotions = existing_data.get('emotional_state', '').split(', ') if existing_data and existing_data.get('emotional_state') else []
    existing_triggers = existing_data.get('triggers', '').split(', ') if existing_data and existing_data.get('triggers') else []
    existing_mistakes = existing_data.get('mistakes', '').split(', ') if existing_data and existing_data.get('mistakes') else []
    existing_actions = existing_data.get('corrective_action', '').split(', ') if existing_data and existing_data.get('corrective_action') else []
    
    # Clean empty strings
    existing_emotions = [x.strip() for x in existing_emotions if x.strip()]
    existing_triggers = [x.strip() for x in existing_triggers if x.strip()]
    existing_mistakes = [x.strip() for x in existing_mistakes if x.strip()]
    existing_actions = [x.strip() for x in existing_actions if x.strip()]
    
    # Create interactive selectors
    selected_emotions = create_interactive_bubble_selector(
        "Emotional States", 
        EMOTIONAL_STATES, 
        "emotional_states", 
        f"emotions_{trade_id}" if trade_id else "emotions",
        existing_emotions
    )
    
    selected_triggers = create_interactive_bubble_selector(
        "Triggers", 
        TRIGGERS, 
        "triggers", 
        f"triggers_{trade_id}" if trade_id else "triggers",
        existing_triggers
    )
    
    selected_mistakes = create_interactive_bubble_selector(
        "Psychological Mistakes", 
        PSYCHOLOGICAL_MISTAKES, 
        "mistakes", 
        f"mistakes_{trade_id}" if trade_id else "mistakes",
        existing_mistakes
    )
    
    selected_actions = create_interactive_bubble_selector(
        "Corrective Actions", 
        CORRECTIVE_ACTIONS, 
        "actions", 
        f"actions_{trade_id}" if trade_id else "actions",
        existing_actions
    )
    
    # Update usage statistics when selections are made
    if selected_emotions:
        update_usage_stats("emotional_states", selected_emotions)
    if selected_triggers:
        update_usage_stats("triggers", selected_triggers)
    if selected_mistakes:
        update_usage_stats("mistakes", selected_mistakes)
    if selected_actions:
        update_usage_stats("actions", selected_actions)
    
    # Show usage statistics
    with st.expander("📊 Your Emotional Patterns", expanded=False):
        st.markdown("**Most Common Patterns:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("*Emotional States:*")
            emotion_stats = st.session_state.emotional_usage_stats["emotional_states"]
            if emotion_stats:
                sorted_emotions = sorted(emotion_stats.items(), key=lambda x: x[1], reverse=True)[:5]
                for emotion, count in sorted_emotions:
                    st.write(f"• {emotion}: {count} times")
            else:
                st.write("No data yet")
            
            st.markdown("*Triggers:*")
            trigger_stats = st.session_state.emotional_usage_stats["triggers"]
            if trigger_stats:
                sorted_triggers = sorted(trigger_stats.items(), key=lambda x: x[1], reverse=True)[:5]
                for trigger, count in sorted_triggers:
                    st.write(f"• {trigger}: {count} times")
            else:
                st.write("No data yet")
        
        with col2:
            st.markdown("*Common Mistakes:*")
            mistake_stats = st.session_state.emotional_usage_stats["mistakes"]
            if mistake_stats:
                sorted_mistakes = sorted(mistake_stats.items(), key=lambda x: x[1], reverse=True)[:5]
                for mistake, count in sorted_mistakes:
                    st.write(f"• {mistake}: {count} times")
            else:
                st.write("No data yet")
            
            st.markdown("*Corrective Actions:*")
            action_stats = st.session_state.emotional_usage_stats["actions"]
            if action_stats:
                sorted_actions = sorted(action_stats.items(), key=lambda x: x[1], reverse=True)[:5]
                for action, count in sorted_actions:
                    st.write(f"• {action}: {count} times")
            else:
                st.write("No data yet")
    
    return {
        'emotional_state': ', '.join(selected_emotions),
        'triggers': ', '.join(selected_triggers),
        'mistakes': ', '.join(selected_mistakes),
        'corrective_action': ', '.join(selected_actions)
    }

def save_emotional_stats():
    """Save emotional usage statistics to file"""
    try:
        import json
        with open('emotional_stats.json', 'w') as f:
            # Convert defaultdict to regular dict for JSON serialization
            stats_to_save = {}
            for category, stats in st.session_state.emotional_usage_stats.items():
                stats_to_save[category] = dict(stats)
            json.dump(stats_to_save, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving emotional stats: {e}")
        return False

def load_emotional_stats():
    """Load emotional usage statistics from file"""
    try:
        import json
        import os
        if os.path.exists('emotional_stats.json'):
            with open('emotional_stats.json', 'r') as f:
                stats = json.load(f)
                # Convert back to defaultdict
                for category, category_stats in stats.items():
                    st.session_state.emotional_usage_stats[category] = defaultdict(int, category_stats)
        return True
    except Exception as e:
        st.error(f"Error loading emotional stats: {e}")
        return False

# Demo function
def demo_emotional_analysis():
    """Demo the emotional analysis component"""
    st.title("🧠 Interactive Emotional Analysis Demo")
    
    # Initialize and load stats
    initialize_usage_stats()
    load_emotional_stats()
    
    # Create the form
    results = create_emotional_analysis_form("demo_trade")
    
    # Show results
    st.subheader("Results:")
    for key, value in results.items():
        if value:
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Save stats button
    if st.button("💾 Save Emotional Patterns"):
        if save_emotional_stats():
            st.success("Emotional patterns saved!")

if __name__ == "__main__":
    demo_emotional_analysis()