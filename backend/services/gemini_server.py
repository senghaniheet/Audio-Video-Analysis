import json
import google.generativeai as genai
import re
import os
import csv
from typing import Dict, Optional, List

# ----------------------------------------
# CONFIGURE GEMINI
# ----------------------------------------
genai.configure(api_key="AIzaSyCv4FJBNT5Ob5oiy-V8AzTr5IS0tNI9b8k"
)

model = genai.GenerativeModel("models/gemini-2.5-flash")   

# ----------------------------------------
# REGEX HELPERS (fallback if AI misses)
# ----------------------------------------
def extract_mobile(text: str):
    match = re.search(r"\b[6-9]\d{9}\b", text)
    return match.group(0) if match else ""

def extract_order_id(text: str):
    match = re.search(r"\b(?:OR|OD|ORD)?\d{4,10}\b", text, re.IGNORECASE)
    return match.group(0) if match else ""

def extract_name(text: str):
    # Very simple fallback if Gemini does not find
    words = text.split()
    if len(words) > 0:
        return words[0].capitalize()
    return ""


# ----------------------------------------
# CSV LOADER FUNCTIONS
# ----------------------------------------
def load_csv_data(csv_file: str = "order_data.csv") -> List[Dict[str, str]]:
    """Load data from CSV file"""
    orders = []
    csv_path = os.path.join(os.path.dirname(__file__), '..', csv_file)
    
    # If CSV doesn't exist in backend, try current directory
    if not os.path.exists(csv_path):
        csv_path = csv_file
        if not os.path.exists(csv_path):
            print(f"[WARNING] CSV file not found: {csv_file}")
            return orders
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Normalize column names (handle different case variations)
                order = {}
                for key, value in row.items():
                    key_lower = key.lower().strip()
                    if 'mobile' in key_lower or 'phone' in key_lower:
                        order['mobile_number'] = str(value).strip()
                    elif 'order' in key_lower and 'id' in key_lower:
                        order['order_id'] = str(value).strip().upper()
                    elif 'customer' in key_lower and 'name' in key_lower:
                        order['customer_name'] = str(value).strip()
                    elif 'status' in key_lower:
                        order['order_status'] = str(value).strip()
                    elif 'delivery' in key_lower and 'date' in key_lower:
                        order['delivery_date'] = str(value).strip()
                    elif 'last' in key_lower and 'update' in key_lower:
                        order['last_update'] = str(value).strip()
                
                # Ensure required fields exist
                if 'mobile_number' not in order:
                    order['mobile_number'] = ""
                if 'order_id' not in order:
                    order['order_id'] = ""
                if 'customer_name' not in order:
                    order['customer_name'] = ""
                if 'order_status' not in order:
                    order['order_status'] = "Unknown"
                if 'delivery_date' not in order:
                    order['delivery_date'] = ""
                if 'last_update' not in order:
                    order['last_update'] = ""
                
                orders.append(order)
        
        print(f"[OK] Loaded {len(orders)} orders from {csv_path}")
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {str(e)}")
    
    return orders


def find_order_by_id(order_id: str, csv_file: str = "order_data.csv") -> Optional[Dict[str, str]]:
    """Find order by order ID from CSV"""
    if not order_id:
        return None
    
    orders = load_csv_data(csv_file)
    order_id_clean = str(order_id).strip().upper().replace(" ", "")
    
    for order in orders:
        order_id_db = str(order.get("order_id", "")).strip().upper().replace(" ", "")
        if order_id_db == order_id_clean:
            return order
    
    return None


# ----------------------------------------
# GEMINI EXTRACTION FUNCTION
# ----------------------------------------
def extract_details(text: str):
    prompt = f"""
Extract the following from the user text:

- Mobile Number (Indian 10-digit)
- Order ID (like OR12345, OD6754, ORD8890 etc.)
- Customer Name (only if clearly mentioned)
- If getting details out of the context then return OutOfTheContext as True

Return only JSON:
{{
  "order_id": "",
  "OutOfTheContext": True/False
}}

Text: {text}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # --- CLEAN & EXTRACT JSON ---
        match = re.search(r"\{[\s\S]*\}", raw)   # extract first {...} block
        if not match:
            raise ValueError("No valid JSON found in response")

        clean_json_str = match.group(0)

        # Remove trailing commas or broken braces if any
        clean_json_str = clean_json_str.replace("```json", "").replace("```", "").strip()

        # --- PARSE ---
        data = json.loads(clean_json_str)

        print("Clean JSON:", clean_json_str)
        print("Parsed:", data)

    except Exception as e:
        print("❌ Exception occurred")
        print("Error Type:", type(e).__name__)
        print("Error Message:", str(e))

        # AI failed → use fallback regex
        data = {
            "OutOfTheContext" : True
        }
        print("data", data)


    

    # Load CSV data and find order using order_id
    order_id = data.get("order_id", "")
    OutOfTheContext = data.get("OutOfTheContext", True)
    print("Outofthecontext",OutOfTheContext)
    if not OutOfTheContext:
        if order_id:
            print(f"[INFO] Searching for order in CSV: Order ID={order_id}")
            order_data = find_order_by_id(order_id)
            
            if order_data:
                print(f"[OK] Order found: Status={order_data.get('order_status', 'Unknown')}")
                # Update data with order information from CSV
                if order_data.get("customer_name") and not data.get("name"):
                    data["name"] = order_data.get("customer_name")
                if order_data.get("mobile_number") and not data.get("mobile_number"):
                    data["mobile_number"] = order_data.get("mobile_number")
                
                # Add order status information to data
                data["order_status"] = order_data.get("order_status", "")
                data["delivery_date"] = order_data.get("delivery_date", "")
                data["last_update"] = order_data.get("last_update", "")
                data["status_found"] = True
            else:
                print(f"[WARNING] Order not found in CSV: {order_id}")
                data["status_found"] = False
        else:
            data["status_found"] = False

    return data


# ----------------------------------------
# HUMAN READABLE RESPONSE
# ----------------------------------------
def format_service_boy_response(data, original_text):
    prompt = f"""
You are a customer support service person. I will give you extracted order details in JSON format.
Speak like a polite service boy talking to a customer. Use simple, clear, friendly English.
Do NOT add emojis. Do NOT add markdown. Just plain English sentences.

Before giving any response, check this:
- If OutOfTheContext is True, then you must return this exact message:
  "Sir, we are extremely sorry but we provide only the order related details."

If OutOfTheContext is not true, continue normally using the rules below.

Here is the extracted data:
{data}

Rules:
- If name is available, address the customer by name (example: "Hello Ravi sir").
- Explain the details in friendly speech.
- Include these details if available: order ID, mobile number, order status, delivery date, last update.
- If any value is missing, mention that politely.
- If order_id is present but order_status is missing, say:
  "Sir, the order ID is correct but I cannot find the status in the system right now."
- If status_found is false, say:
  "Sir, we are extremely sorry, but we couldn't find any order associated with this ID."
-"Here is the original message we received dont add in the response:"
{original_text}

Tone guideline:
- Friendly
- Helpful
- Natural speech like a real service boy talking
- No JSON, no lists, no formatting. Only natural English sentences.
"""

    response = model.generate_content(prompt)
    return response.text.strip()

# ----------------------------------------
# MAIN METHOD (runnable function)
# ----------------------------------------
def process_text(text: str):
    extracted = extract_details(text)
    return format_service_boy_response(extracted, text)


# ----------------------------------------
# TESTING (optional)
# ----------------------------------------
if __name__ == "__main__":
    sample = "Hi my name is Rahul. My order id is OR4599 and my mobile number is 9876543210."
    print(process_text(sample))
