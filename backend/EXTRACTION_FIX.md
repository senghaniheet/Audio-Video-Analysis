# Extraction Fix - Mobile Number and Order ID

## Issue Identified

The extraction was failing to extract mobile numbers and order IDs from transcripts even when they were clearly present in the text.

## Root Causes

1. **Regex patterns were too strict** - Required word boundaries that might not match with punctuation
2. **AI prompt could be more explicit** - Needed better examples and clearer instructions
3. **Order ID format mismatch** - Transcript had "MZ12345" but Excel has "AMZ12345" (this is a data issue, not extraction)

## Fixes Applied

### 1. Improved Regex Patterns

**Mobile Number Extraction:**
- Added pattern: `(?:mobile|number|phone|contact)[\s:]*(\d{10})` - Matches "mobile number is 9876543210"
- Added pattern: `(\d{10})` - Matches any 10 consecutive digits
- Added pattern: `(\d{3}[\s-]?\d{3}[\s-]?\d{4})` - Matches formatted numbers like "987-654-3210"

**Order ID Extraction:**
- Added pattern: `(?:order\s*(?:id|number|ID|Number)[\s:]*)?([A-Z]{2,4}[\s-]?\d{4,6})` - Matches "order ID is AMZ12345"
- Added pattern: `\b([A-Z]{2,4}\d{4,6})\b` - Matches "MZ12345", "AMZ12345", etc.
- Added pattern: `(?:order|Order)[\s:]+([A-Z]{1,4}[\s-]?\d{3,6})` - Matches "order MZ12345"

### 2. Improved AI Prompt

- Added explicit examples showing how to extract mobile numbers and order IDs
- Added CRITICAL markers for important extraction rules
- Clarified that order IDs can be 2-4 letters followed by 4-6 digits (e.g., MZ12345, AMZ12345)

### 3. Added Debug Logging

- Added print statements to show AI extraction results
- Added print statements when fallback regex extraction succeeds

## Testing

Test with this transcript:
```
"Hello, my name is Rahul Sharma. My mobile number is 9876543210. My order ID is MZ12345. I want to know the status of my Amazon order."
```

**Expected Results:**
- mobile_number: "9876543210" ✓
- order_id: "MZ12345" ✓

## Important Note: Order ID Mismatch

⚠️ **Data Mismatch Issue:**
- Transcript contains: "MZ12345"
- Excel file contains: "AMZ12345"

Even if extraction works correctly, the order won't be found because:
- The lookup requires **BOTH** mobile_number AND order_id to match exactly
- "MZ12345" ≠ "AMZ12345"

**Solutions:**
1. **Update Excel file** - Change "AMZ12345" to "MZ12345" in the Excel file
2. **Update audio/transcript** - Ensure the audio says "AMZ12345" instead of "MZ12345"
3. **Add both variants** - Add a row in Excel with "MZ12345" for the same mobile number

## How to Verify Fix

1. Restart the backend server
2. Test with the same audio/transcript
3. Check the console output for:
   - "AI Extraction result: {...}"
   - "Fallback: Extracted mobile number ..."
   - "Fallback: Extracted order ID ..."

## Next Steps

1. Test the extraction with various formats
2. If order ID still doesn't match, check the Excel file and ensure order IDs match exactly
3. Consider adding fuzzy matching for order IDs if partial matches are acceptable

