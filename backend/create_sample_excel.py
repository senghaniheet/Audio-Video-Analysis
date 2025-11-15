"""
Script to create sample Excel file with 50 order records
"""
import pandas as pd
import os
from datetime import datetime, timedelta
import random

def create_sample_orders():
    """Create sample orders Excel file"""
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Sample data
    statuses = ["Processing", "Shipped", "Out for Delivery", "Delivered", "Cancelled"]
    couriers = ["BlueDart", "Amazon Logistics", "Delhivery", "FedEx", "DTDC"]
    first_names = ["Raj", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohit", "Kavya", "Arjun", "Meera"]
    last_names = ["Kumar", "Sharma", "Patel", "Singh", "Gupta", "Reddy", "Mehta", "Joshi", "Verma", "Shah"]
    
    orders = []
    
    # Add specific test order for Audio File 1 (Rahul Sharma)
    orders.append({
        "MobileNumber": "9876543210",
        "OrderID": "AMZ12345",
        "CustomerName": "Rahul Sharma",
        "OrderStatus": "Shipped",
        "DeliveryDate": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "LastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    for i in range(1, 51):
        mobile = f"9{random.randint(100000000, 999999999)}"
        order_id = f"AMZ{random.randint(10000, 99999)}"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        customer_name = f"{first_name} {last_name}"
        status = random.choice(statuses)
        
        # Generate dates
        base_date = datetime.now()
        if status == "Delivered":
            delivery_date = base_date - timedelta(days=random.randint(1, 30))
            last_update = delivery_date
        elif status == "Out for Delivery":
            delivery_date = base_date + timedelta(days=random.randint(0, 2))
            last_update = base_date - timedelta(days=random.randint(1, 3))
        elif status == "Shipped":
            delivery_date = base_date + timedelta(days=random.randint(3, 7))
            last_update = base_date - timedelta(days=random.randint(1, 5))
        else:
            delivery_date = base_date + timedelta(days=random.randint(5, 10))
            last_update = base_date - timedelta(days=random.randint(1, 3))
        
        orders.append({
            "MobileNumber": mobile,
            "OrderID": order_id,
            "CustomerName": customer_name,
            "OrderStatus": status,
            "DeliveryDate": delivery_date.strftime("%Y-%m-%d"),
            "LastUpdate": last_update.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Create DataFrame
    df = pd.DataFrame(orders)
    
    # Save to Excel
    excel_path = "data/orders.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Created {excel_path} with {len(orders)} sample orders")
    print(f"\nSample records:")
    print(df.head(10).to_string())
    
    return excel_path

if __name__ == "__main__":
    create_sample_orders()

