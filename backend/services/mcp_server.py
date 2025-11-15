"""
MCP Server for Order Status Processing
Handles text analysis, Excel lookup, and response generation
"""
import os
import json
import re
from openai import OpenAI
from typing import Dict, Optional, Any
from datetime import datetime

# Import order.py function
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from order import check_order_status

class MCPServer:
    """MCP Server for order status extraction and lookup"""
    
    def __init__(self, excel_path: str = "data/orders.xlsx", openai_api_key: str = None):
        """
        Initialize MCP Server
        
        Args:
            excel_path: Path to Excel file with orders (for reference, actual lookup in order.py)
            openai_api_key: OpenAI API key (or uses environment variable)
        """
        self.excel_path = excel_path
        self.client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))
    
    def extract_from_text(self, transcript: str) -> Dict[str, Any]:
        """
        Extract information from transcript using AI with improved prompt
        
        Args:
            transcript: Text transcript from audio
            
        Returns:
            dict with mobile_number, order_id, customer_name, topic, intent
        """
        prompt = f"""You are an MCP server for Amazon order status lookup.

Your tasks:
1. Extract the following information from the transcript:
   - mobile_number: Extract the 10-digit mobile number (Indian format like 9876543210, 9123456780). 
     Look for patterns like: "my mobile number is 9876543210", "number is 9876543210", 
     "9876543210", "nine eight seven six five four three two one zero", etc.
     CRITICAL: If you see ANY 10-digit number in the transcript, extract it. Return as string of 10 digits.
   - order_id: Extract the order ID (alphanumeric like AMZ12345, MZ12345, AMZ98765, ORD123, etc.).
     Look for patterns like: "order ID is AMZ12345", "my order AMZ12345", "order MZ12345", 
     "AMZ12345", "MZ12345", etc.
     CRITICAL: Order IDs can be 2-4 letters followed by 4-6 digits. Examples: AMZ12345, MZ12345, ORD123.
     Extract ANY alphanumeric code that looks like an order ID.
   - customer_name: Extract the customer's name if mentioned (e.g., "Rahul Sharma", "Priya Patel")
   - topic: What the conversation is about (e.g., "Order Status Inquiry", "Delivery Inquiry")
   - intent: User's intention (e.g., "check_status", "delivery_inquiry", "complaint")

2. IMPORTANT: Be very thorough in finding mobile numbers and order IDs. They may be:
   - Mobile numbers: "9876543210", "my number is 9876543210", "mobile 9876543210"
   - Order IDs: "AMZ12345", "MZ12345", "order AMZ12345", "order ID is MZ12345", "A M Z 1 2 3 4 5"

3. EXAMPLES:
   - Transcript: "My mobile number is 9876543210" → mobile_number: "9876543210"
   - Transcript: "My order ID is MZ12345" → order_id: "MZ12345"
   - Transcript: "order AMZ12345" → order_id: "AMZ12345"

4. If mobile number or order ID is not found after careful analysis, return them as empty string "" (not null).

5. Return ONLY valid JSON, no markdown, no code blocks, no explanations.

Transcript:
{transcript}

Return only JSON:
{{
  "mobile_number": "",
  "order_id": "",
  "customer_name": "",
  "topic": "",
  "intent": ""
}}"""

        try:
            # Try with response_format first (for newer OpenAI API versions)
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,  # Lower temperature for more consistent extraction
                    response_format={"type": "json_object"}  # Force JSON response
                )
            except TypeError:
                # Fallback for older API versions that don't support response_format
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
            
            text = response.choices[0].message.content or "{}"
            text = text.strip()
            
            # Remove markdown code blocks if present (though response_format should prevent this)
            if text.startswith("```"):
                text = re.sub(r'^```json\s*', '', text)
                text = re.sub(r'^```\s*', '', text)
                text = re.sub(r'```\s*$', '', text)
            
            extracted = json.loads(text)
            print(f"AI Extraction result: {extracted}")
            
            # Clean and validate mobile number
            mobile = extracted.get("mobile_number", "") or ""
            # Handle both empty string and None - convert None to empty string
            if mobile and str(mobile).strip() and str(mobile).strip().lower() != "null":
                # Remove all non-digits
                mobile_clean = re.sub(r'[^\d]', '', str(mobile))
                # If it's a valid 10-digit number, use it; otherwise set to None
                if len(mobile_clean) == 10:
                    extracted["mobile_number"] = mobile_clean
                else:
                    extracted["mobile_number"] = None
            else:
                extracted["mobile_number"] = None
            
            # Fallback: Try to extract mobile number from transcript using regex if AI missed it
            if not extracted["mobile_number"]:
                # More robust patterns - look for 10-digit numbers anywhere
                # First, try to find numbers that look like mobile numbers
                mobile_patterns = [
                    r'(?:mobile|number|phone|contact)[\s:]*(\d{10})',  # "mobile number is 9876543210"
                    r'(\d{10})',  # Any 10 consecutive digits
                    r'(\d{3}[\s-]?\d{3}[\s-]?\d{4})',  # Formatted: 987-654-3210 or 987 654 3210
                ]
                for pattern in mobile_patterns:
                    matches = re.findall(pattern, transcript, re.IGNORECASE)
                    if matches:
                        # Get the first match and clean it
                        mobile_raw = matches[0] if isinstance(matches[0], str) else matches[0]
                        mobile_clean = re.sub(r'[^\d]', '', str(mobile_raw))
                        if len(mobile_clean) == 10 and mobile_clean.startswith('9'):  # Indian mobile starts with 9
                            extracted["mobile_number"] = mobile_clean
                            print(f"Fallback: Extracted mobile number {mobile_clean} from transcript using pattern: {pattern}")
                            break
                        elif len(mobile_clean) == 10:
                            extracted["mobile_number"] = mobile_clean
                            print(f"Fallback: Extracted mobile number {mobile_clean} from transcript using pattern: {pattern}")
                            break
            
            # Clean order ID
            order_id = extracted.get("order_id", "") or ""
            # Handle both empty string and None - convert None to empty string
            if order_id and str(order_id).strip() and str(order_id).strip().lower() != "null":
                # Remove spaces, convert to uppercase
                order_id_clean = str(order_id).strip().upper().replace(" ", "")
                extracted["order_id"] = order_id_clean if order_id_clean else None
            else:
                extracted["order_id"] = None
            
            # Fallback: Try to extract order ID from transcript using regex if AI missed it
            if not extracted["order_id"]:
                # More robust patterns - look for order IDs in various formats
                order_patterns = [
                    r'(?:order\s*(?:id|number|ID|Number)[\s:]*)?([A-Z]{2,4}[\s-]?\d{4,6})',  # "order ID is AMZ12345" or "order AMZ12345"
                    r'\b([A-Z]{2,4}\d{4,6})\b',  # AMZ12345, MZ12345, ORD12345
                    r'\b([A-Z]{2,4}[\s-]?\d{4,6})\b',  # AMZ 12345 or AMZ-12345
                    r'(?:order|Order)[\s:]+([A-Z]{1,4}[\s-]?\d{3,6})',  # "order MZ12345"
                ]
                for pattern in order_patterns:
                    matches = re.findall(pattern, transcript, re.IGNORECASE)
                    if matches:
                        # Get the first match and clean it
                        order_raw = matches[0] if isinstance(matches[0], str) else matches[0]
                        order_id_clean = str(order_raw).strip().upper().replace(" ", "").replace("-", "")
                        if order_id_clean and len(order_id_clean) >= 5:  # At least 5 chars (e.g., MZ123)
                            extracted["order_id"] = order_id_clean
                            print(f"Fallback: Extracted order ID {order_id_clean} from transcript using pattern: {pattern}")
                            break
            
            return extracted
        except Exception as e:
            print(f"Error in extraction: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "mobile_number": None,
                "order_id": None,
                "customer_name": None,
                "topic": "Order Inquiry",
                "intent": "check_status"
            }
    
    def generate_response(self, extracted: Dict, order_result: Dict, status_found: bool) -> Dict[str, str]:
        """
        Generate response text based on extracted data and order status
        
        Args:
            extracted: Extracted data from transcript
            order_result: Result from check_order_status() function
            status_found: Whether order was found
            
        Returns:
            dict with response_text and response_voice_text
        """
        mobile = extracted.get("mobile_number") or "Not provided"
        order_id = extracted.get("order_id") or "Not provided"
        customer_name = extracted.get("customer_name") or ""
        
        if status_found and order_result:
            order_status = order_result.get("order_status", {})
            customer_name = order_result.get("customer_name", customer_name) or customer_name
            status = order_status.get("status", "Unknown")
            delivery_date = order_status.get("delivery_date", "")
            
            # Format delivery date for voice
            delivery_voice = ""
            if delivery_date:
                try:
                    # Try to parse and format date
                    if isinstance(delivery_date, str):
                        # Handle different date formats
                        date_obj = None
                        for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]:
                            try:
                                date_obj = datetime.strptime(str(delivery_date).split()[0], fmt)
                                break
                            except:
                                continue
                        if date_obj:
                            delivery_voice = date_obj.strftime("%d %b").replace("0", "").lstrip()
                        else:
                            delivery_voice = str(delivery_date)
                    else:
                        delivery_voice = str(delivery_date)
                except:
                    delivery_voice = str(delivery_date)
            
            # Build response
            if customer_name:
                response_text = f"Your order {order_id} for {customer_name} is {status}."
            else:
                response_text = f"Your order {order_id} is {status}."
            
            if delivery_date:
                response_text += f" Expected delivery date: {delivery_date}."
            
            # Voice-friendly response
            if customer_name:
                response_voice_text = f"Your order {order_id} for {customer_name} is {status}."
            else:
                response_voice_text = f"Your order {order_id} is {status}."
            
            if delivery_voice:
                response_voice_text += f" It will be delivered on {delivery_voice}."
        else:
            # Order not found
            message = order_result.get("message", "Order not found for given mobile number or order ID.")
            response_text = message
            response_voice_text = "I could not find any order linked with that mobile number or order ID."
        
        return {
            "response_text": response_text,
            "response_voice_text": response_voice_text
        }
    
    def process(self, transcript: str) -> Dict[str, Any]:
        """
        Main processing function: Extract -> Lookup -> Generate Response
        
        Args:
            transcript: Text transcript from audio
            
        Returns:
            Complete JSON response with all extracted data and order status
        """
        # Step 1: Extract information from transcript
        extracted = self.extract_from_text(transcript)
        
        mobile_number = extracted.get("mobile_number")
        order_id = extracted.get("order_id")
        customer_name = extracted.get("customer_name")
        topic = extracted.get("topic", "Order Inquiry")
        intent = extracted.get("intent", "check_status")
        
        # Step 2: Call check_order_status() from order.py
        # This requires BOTH mobile_number AND order_id
        order_result = None
        status_found = False
        order_status_dict = None
        
        if mobile_number and order_id:
            order_result = check_order_status(
                mobile_number=mobile_number,
                order_id=order_id
            )
            status_found = order_result.get("status_found", False)
            
            if status_found:
                order_status_dict = order_result.get("order_status", {})
                # Update customer_name from order result if available
                if order_result.get("customer_name"):
                    customer_name = order_result.get("customer_name")
        else:
            # Missing required fields
            order_result = {
                "status_found": False,
                "message": "Both mobile number and order ID are required to check order status."
            }
        
        # Step 3: Generate response
        response = self.generate_response(extracted, order_result, status_found)
        
        # Step 4: Build final response according to requirements
        result = {
            "transcript": transcript,
            "mobile_number": mobile_number,
            "order_id": order_id,
            "customer_name": customer_name,
            "topic": topic,
            "intent": intent,
            "status_found": status_found,
            "order_status": order_status_dict if status_found else {
                "status": "",
                "delivery_date": "",
                "last_update": ""
            },
            "response_text": response["response_text"],
            "response_voice_text": response["response_voice_text"]
        }
        
        return result
