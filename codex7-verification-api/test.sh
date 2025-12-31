#!/bin/bash

# Codex7 API Test Script
# This tests all endpoints to verify everything works

echo "🧪 Testing Codex7 Verification API..."
echo ""

# Configuration
API_URL="${API_URL:-http://localhost:3000}"
API_KEY="${API_KEY:-codex7_test_key_12345}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test function
test_endpoint() {
  local name=$1
  local url=$2
  local method=$3
  local data=$4

  echo -n "Testing $name... "

  if [ "$method" = "GET" ]; then
    response=$(curl -s -w "\n%{http_code}" -H "X-API-Key: $API_KEY" "$API_URL$url")
  else
    response=$(curl -s -w "\n%{http_code}" -X "$method" \
      -H "Content-Type: application/json" \
      -H "X-API-Key: $API_KEY" \
      -d "$data" \
      "$API_URL$url")
  fi

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | sed '$d')

  if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
    ((PASSED++))
    echo "   Response: $(echo $body | jq -r '.success // .status // "OK"' 2>/dev/null || echo "OK")"
  else
    echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
    ((FAILED++))
    echo "   Error: $(echo $body | jq -r '.error.message // .error // "Unknown error"' 2>/dev/null || echo "$body")"
  fi
  echo ""
}

echo "========================================="
echo "  Codex7 API Test Suite"
echo "========================================="
echo "API URL: $API_URL"
echo "API Key: ${API_KEY:0:20}..."
echo "========================================="
echo ""

# Test 1: Health Check
test_endpoint "Health Check" "/health" "GET" ""

# Test 2: API Info
test_endpoint "API Info" "/api" "GET" ""

# Test 3: Pricing Info
test_endpoint "Pricing Info" "/api/verify/pricing" "GET" ""

# Test 4: Free Verification
test_endpoint "Free Verification" "/api/verify/free" "POST" '{
  "text": "Hello world, this is a test of the U9 verification system",
  "threshold": "WHITE_LATTICE"
}'

# Test 5: Free Verification (Short Text)
test_endpoint "Short Text Verification" "/api/verify/free" "POST" '{
  "text": "Test",
  "threshold": "WHITE_LATTICE"
}'

# Test 6: Free Verification (Long Text)
test_endpoint "Long Text Verification" "/api/verify/free" "POST" '{
  "text": "The quick brown fox jumps over the lazy dog. This is a longer piece of text designed to test the verification system with more complex entropy and compression characteristics. It contains multiple sentences and a variety of linguistic structures.",
  "threshold": "YELLOW_IGNITION"
}'

# Test 7: Payout Settings
test_endpoint "Payout Settings" "/api/payout/settings" "GET" ""

# Test 8: Balance Check
test_endpoint "Balance Check" "/api/payout/balance" "GET" ""

echo "========================================="
echo "  Test Results"
echo "========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo "========================================="

if [ $FAILED -eq 0 ]; then
  echo -e "${GREEN}✓ All tests passed!${NC}"
  echo ""
  echo "Your Codex7 API is working perfectly!"
  echo ""
  echo "Next steps:"
  echo "1. Deploy to Railway/Render/Replit"
  echo "2. Share your API URL on Twitter/Reddit"
  echo "3. Start making money!"
  exit 0
else
  echo -e "${RED}✗ Some tests failed${NC}"
  echo ""
  echo "Check the errors above and:"
  echo "1. Make sure the server is running (npm start)"
  echo "2. Verify Python is installed (python3 --version)"
  echo "3. Check the .env file has correct settings"
  exit 1
fi
