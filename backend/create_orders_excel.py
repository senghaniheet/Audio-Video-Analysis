"""
Script to create Excel file with 15 order records as per requirements
"""
import pandas as pd
import os
from datetime import datetime, timedelta

def create_orders_excel():
    """Create Excel file with 15 sample orders"""
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # 15 sample orders as per requirements
    orders = [
        {
            "MobileNumber": "9876543210",
            "OrderID": "AMZ12345",
            "CustomerName": "Rahul Sharma",
            "OrderStatus": "Shipped",
            "DeliveryDate": "2025-11-20",
            "LastUpdate": "2025-11-15"
        },
        {
            "MobileNumber": "9123456780",
            "OrderID": "AMZ98765",
            "CustomerName": "Priya Patel",
            "OrderStatus": "Out for Delivery",
            "DeliveryDate": "2025-11-16",
            "LastUpdate": "2025-11-15"
        },
        {
            "MobileNumber": "9988776655",
            "OrderID": "AMZ56789",
            "CustomerName": "Amit Verma",
            "OrderStatus": "Delivered",
            "DeliveryDate": "2025-11-10",
            "LastUpdate": "2025-11-10"
        },
        {
            "MobileNumber": "9876543211",
            "OrderID": "AMZ11111",
            "CustomerName": "Sneha Kumar",
            "OrderStatus": "Processing",
            "DeliveryDate": "2025-11-25",
            "LastUpdate": "2025-11-14"
        },
        {
            "MobileNumber": "9123456781",
            "OrderID": "AMZ22222",
            "CustomerName": "Vikram Singh",
            "OrderStatus": "Shipped",
            "DeliveryDate": "2025-11-18",
            "LastUpdate": "2025-11-15"
        },
        {
            "MobileNumber": "9988776656",
            "OrderID": "AMZ33333",
            "CustomerName": "Anjali Gupta",
            "OrderStatus": "Out for Delivery",
            "DeliveryDate": "2025-11-17",
            "LastUpdate": "2025-11-15"
        },
        {
            "MobileNumber": "9876543212",
            "OrderID": "AMZ44444",
            "CustomerName": "Rohit Reddy",
            "OrderStatus": "Delivered",
            "DeliveryDate": "2025-11-12",
            "LastUpdate": "2025-11-12"
        },
        {
            "MobileNumber": "9123456782",
            "OrderID": "AMZ55555",
            "CustomerName": "Kavya Mehta",
            "OrderStatus": "Shipped",
            "DeliveryDate": "2025-11-21",
            "LastUpdate": "2025-11-14"
        },
        {
            "MobileNumber": "9988776657",
            "OrderID": "AMZ66666",
            "CustomerName": "Arjun Joshi",
            "OrderStatus": "Processing",
            "DeliveryDate": "2025-11-26",
            "LastUpdate": "2025-11-13"
        },
        {
            "MobileNumber": "9876543213",
            "OrderID": "AMZ77777",
            "CustomerName": "Meera Shah",
            "OrderStatus": "Out for Delivery",
            "DeliveryDate": "2025-11-16",
            "LastUpdate": "2025-11-15"
        },
        {
            "MobileNumber": "9123456783",
            "OrderID": "AMZ88888",
            "CustomerName": "Rajesh Kumar",
            "OrderStatus": "Delivered",
            "DeliveryDate": "2025-11-11",
            "LastUpdate": "2025-11-11"
        },
        {
            "MobileNumber": "9988776658",
            "OrderID": "AMZ99999",
            "CustomerName": "Pooja Sharma",
            "OrderStatus": "Shipped",
            "DeliveryDate": "2025-11-19",
            "LastUpdate": "2025-11-14"
        },
        {
            "MobileNumber": "9876543214",
            "OrderID": "AMZ00001",
            "CustomerName": "Suresh Patel",
            "OrderStatus": "Processing",
            "DeliveryDate": "2025-11-24",
            "LastUpdate": "2025-11-13"
        },
        {
            "MobileNumber": "9123456784",
            "OrderID": "AMZ00002",
            "CustomerName": "Neha Verma",
            "OrderStatus": "Out for Delivery",
            "DeliveryDate": "2025-11-17",
            "LastUpdate": "2025-11-15"
        },
        {
            "MobileNumber": "9988776659",
            "OrderID": "AMZ00003",
            "CustomerName": "Manoj Singh",
            "OrderStatus": "Delivered",
            "DeliveryDate": "2025-11-09",
            "LastUpdate": "2025-11-09"
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(orders)
    
    # Save to Excel
    excel_path = "data/orders.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Created {excel_path} with {len(orders)} sample orders")
    print(f"\nSample records:")
    print(df.head(15).to_string())
    
    return excel_path

if __name__ == "__main__":
    create_orders_excel()

