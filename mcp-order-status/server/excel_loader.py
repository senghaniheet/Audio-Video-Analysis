"""
Excel Loader Module
Handles Excel file creation and data loading
"""
import openpyxl
from openpyxl import Workbook
import os
from typing import Dict, Optional, List

EXCEL_FILE = "order_data.xlsx"

def create_sample_excel():
    """Create Excel file with 15 sample orders"""
    
    # Sample data - 15 orders
    sample_orders = [
        {"mobile_number": "9876543210", "order_id": "AMZ12345", "order_status": "Delivered"},
        {"mobile_number": "9988776655", "order_id": "AMZ22222", "order_status": "Shipped"},
        {"mobile_number": "9123456780", "order_id": "AMZ33333", "order_status": "Out for Delivery"},
        {"mobile_number": "9876543211", "order_id": "AMZ44444", "order_status": "Processing"},
        {"mobile_number": "9988776656", "order_id": "AMZ55555", "order_status": "Delivered"},
        {"mobile_number": "9123456781", "order_id": "AMZ66666", "order_status": "Shipped"},
        {"mobile_number": "9876543212", "order_id": "AMZ77777", "order_status": "Out for Delivery"},
        {"mobile_number": "9988776657", "order_id": "AMZ88888", "order_status": "Processing"},
        {"mobile_number": "9123456782", "order_id": "AMZ99999", "order_status": "Delivered"},
        {"mobile_number": "9876543213", "order_id": "AMZ00001", "order_status": "Shipped"},
        {"mobile_number": "9988776658", "order_id": "AMZ00002", "order_status": "Out for Delivery"},
        {"mobile_number": "9123456783", "order_id": "AMZ00003", "order_status": "Processing"},
        {"mobile_number": "9876543214", "order_id": "AMZ00004", "order_status": "Delivered"},
        {"mobile_number": "9988776659", "order_id": "AMZ00005", "order_status": "Shipped"},
        {"mobile_number": "9123456784", "order_id": "AMZ00006", "order_status": "Out for Delivery"},
    ]
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"
    
    # Add headers
    ws.append(["mobile_number", "order_id", "order_status"])
    
    # Add data rows
    for order in sample_orders:
        ws.append([
            order["mobile_number"],
            order["order_id"],
            order["order_status"]
        ])
    
    # Save file
    wb.save(EXCEL_FILE)
    print(f"Created {EXCEL_FILE} with {len(sample_orders)} sample orders")
    
    return EXCEL_FILE

def load_excel_data() -> List[Dict[str, str]]:
    """Load data from Excel file"""
    
    if not os.path.exists(EXCEL_FILE):
        print(f"{EXCEL_FILE} not found. Creating sample file...")
        create_sample_excel()
    
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    
    orders = []
    
    # Skip header row (row 1)
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] and row[1]:  # Check if mobile_number and order_id exist
            orders.append({
                "mobile_number": str(row[0]).strip(),
                "order_id": str(row[1]).strip().upper(),
                "order_status": str(row[2]).strip() if row[2] else "Unknown"
            })
    
    return orders

def find_order(mobile_number: str, order_id: str) -> Optional[Dict[str, str]]:
    """Find order by mobile number and order ID"""
    
    orders = load_excel_data()
    
    # Clean inputs
    mobile_clean = str(mobile_number).strip().replace(" ", "").replace("-", "")
    order_id_clean = str(order_id).strip().upper().replace(" ", "")
    
    for order in orders:
        order_mobile = str(order["mobile_number"]).strip().replace(" ", "").replace("-", "")
        order_id_db = str(order["order_id"]).strip().upper().replace(" ", "")
        
        if order_mobile == mobile_clean and order_id_db == order_id_clean:
            return order
    
    return None

