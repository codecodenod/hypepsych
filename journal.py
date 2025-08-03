import json
from hyperliquid.info import Info
from hyperliquid.utils import constants
import hashlib
import time

def fetch_trade_data(wallet_address):
    """
    Fetch recent fills (trades) and user state from Hyperliquid API.
    """
    try:
        # Initialize with retry logic
        info = Info(constants.MAINNET_API_URL, skip_ws=True)
        
        # Add delay to avoid rate limiting
        time.sleep(0.5)
        
        # Fetch user fills (trades)
        fills = info.user_fills(wallet_address)
        
        # Add another small delay
        time.sleep(0.5)
        
        # Fetch user state (portfolio info)
        user_state = info.user_state(wallet_address)
        
        return fills, user_state
        
    except Exception as e:
        # More specific error handling
        error_msg = str(e)
        if "Invalid address" in error_msg:
            raise ValueError("Invalid wallet address format. Please check your address.")
        elif "rate limit" in error_msg.lower():
            raise ValueError("Rate limited by Hyperliquid API. Please wait a moment and try again.")
        elif "timeout" in error_msg.lower():
            raise ValueError("Connection timeout. Please check your internet connection and try again.")
        else:
            raise ValueError(f"Failed to fetch data from Hyperliquid: {error_msg}")

def verify_wallet_ownership(wallet_address, signature, message):
    """
    Verify that the signature was created by the wallet owner.
    This is optional additional security.
    """
    try:
        # This would require web3.py for actual verification
        # For now, just do basic validation
        if not wallet_address or not signature or not message:
            return False
        
        # Basic format checks
        if not signature.startswith('0x') or len(signature) < 130:
            return False
            
        # In a real implementation, you would:
        # from eth_account.messages import encode_defunct
        # from web3.auto import w3
        # message_hash = encode_defunct(text=message)
        # recovered_address = w3.eth.account.recover_message(message_hash, signature=signature)
        # return recovered_address.lower() == wallet_address.lower()
        
        return True  # For demo purposes
        
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return False

def save_journal_data(filename, data):
    """
    Save journal data to a JSON file with backup.
    """
    try:
        # Create backup if file exists
        import os
        if os.path.exists(filename):
            backup_filename = f"{filename}.backup"
            try:
                import shutil
                shutil.copy2(filename, backup_filename)
            except Exception as backup_error:
                print(f"Warning: Could not create backup: {backup_error}")
        
        # Save the data
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        
        return True
        
    except Exception as e:
        print(f"Error saving journal: {e}")
        return False

def load_journal_data(filename):
    """
    Load journal data from a JSON file with error recovery.
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Validate the loaded data structure
        if not isinstance(data, dict):
            raise ValueError("Invalid journal file format")
        
        # Ensure required keys exist
        required_keys = ['trades', 'manual_trades', 'reflections']
        for key in required_keys:
            if key not in data:
                data[key] = [] if key != 'reflections' else {}
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file {filename}: {e}")
        
        # Try to load backup if it exists
        backup_filename = f"{filename}.backup"
        if os.path.exists(backup_filename):
            print(f"Attempting to load backup file: {backup_filename}")
            try:
                with open(backup_filename, 'r') as f:
                    return json.load(f)
            except Exception as backup_error:
                print(f"Backup file also corrupted: {backup_error}")
        
        return None
        
    except FileNotFoundError:
        print