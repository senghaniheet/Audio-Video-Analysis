"""
Order Status Lookup Module
Provides function to check order status from Excel file
"""
import pandas as pd
import os
import re
from typing import Dict, Optional

def check_order_status(mobile_number: str = None, order_id: str = None) -> dict:
    """
    Check order status from Excel file
    
    Args:
        mobile_number: Customer mobile number (10 digits)
        order_id: Order ID (alphanumeric)
        
    Returns:
        dict with status_found, customer_name, order_status, delivery_date, last_update
        OR status_found=False with message if not found
    """
    excel_path = "data/orders.xlsx"
    
    # Check if Excel file exists
    if not os.path.exists(excel_path):
        return {
            "status_found": False,
            "message": "Order database not found. Please contact support."
        }
    
    try:
        # Load Excel file
        df = pd.read_excel(excel_path)
        
        # Validate required columns
        required_columns = ['MobileNumber', 'OrderID', 'CustomerName', 'OrderStatus', 'DeliveryDate', 'LastUpdate']
        if not all(col in df.columns for col in required_columns):
            return {
                "status_found": False,
                "message": "Order database format is invalid. Please contact support."
            }
        
        # Both mobile_number and order_id are required for lookup
        if not mobile_number or not order_id:
            return {
                "status_found": False,
                "message": "Both mobile number and order ID are required to check order status."
            }
        
        # Clean mobile number (remove spaces, dashes, etc.)
        mobile_clean = re.sub(r'[^\d]', '', str(mobile_number))
        if len(mobile_clean) != 10:
            return {
                "status_found": False,
                "message": "Invalid mobile number format. Please provide a 10-digit mobile number."
            }
        
        # Clean order ID (uppercase, remove spaces)
        order_id_clean = str(order_id).strip().upper()
        
        # Search for matching record where BOTH mobile_number AND order_id match
        df['MobileNumber_Clean'] = df['MobileNumber'].astype(str).str.replace(r'[^\d]', '', regex=True)
        df['OrderID_Clean'] = df['OrderID'].astype(str).str.upper().str.strip()
        
        match = df[
            (df['MobileNumber_Clean'] == mobile_clean) & 
            (df['OrderID_Clean'] == order_id_clean)
        ]
        
        if len(match) > 0:
            row = match.iloc[0]
            return {
                "status_found": True,
                "customer_name": str(row.get('CustomerName', '')),
                "order_status": {
                    "status": str(row.get('OrderStatus', 'Unknown')),
                    "delivery_date": str(row.get('DeliveryDate', '')),
                    "last_update": str(row.get('LastUpdate', ''))
                }
            }
        else:
            return {
                "status_found": False,
                "message": "Order not found for given mobile number or order ID."
            }
            
    except Exception as e:
        print(f"Error in check_order_status: {str(e)}")
        return {
            "status_found": False,
            "message": f"Error checking order status: {str(e)}"
        }

