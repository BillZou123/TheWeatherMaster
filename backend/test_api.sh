#!/bin/bash

BASE_URL="http://127.0.0.1:10000"

TOTAL=0
PASSED=0
FAILED=0

# Run a test command, pretty-print JSON, and count pass/fail by `"status": "success"`
run_test () {
  local NAME="$1"
  local CMD="$2"

  echo ""
  echo "=============================="
  echo "$NAME"
  echo "=============================="

  # Run command and capture output (should be JSON)
  local OUT
  OUT=$(eval "$CMD")

  # Pretty print JSON (even for error cases)
  echo "$OUT" | python3 -m json.tool 2>/dev/null || echo "$OUT"

  TOTAL=$((TOTAL+1))

  if echo "$OUT" | grep -q '"status"[[:space:]]*:[[:space:]]*"success"'; then
    echo "✔ PASSED: $NAME"
    PASSED=$((PASSED+1))
  else
    echo "✘ FAILED: $NAME"
    FAILED=$((FAILED+1))
  fi
}

echo "=============================="
echo "RUNNING API TESTS"
echo "=============================="

# -------------------------
# TEST CREATE
# -------------------------
run_test "TEST CREATE" \
"curl -s -X POST $BASE_URL/weather \
-H 'Content-Type: application/json' \
-d '{
  \"location\":\"Toronto\",
  \"start_date\":\"2026-03-01\",
  \"end_date\":\"2026-03-03\"
}'"

# -------------------------
# TEST READ ALL
# -------------------------
run_test "TEST READ ALL" \
"curl -s $BASE_URL/weather"

# -------------------------
# TEST UPDATE (change location)
# -------------------------
run_test "TEST UPDATE (change location)" \
"curl -s -X PUT $BASE_URL/weather/1 \
-H 'Content-Type: application/json' \
-d '{
  \"location\":\"Vancouver\"
}'"

# -------------------------
# TEST READ BY LOCATION
# -------------------------
run_test "TEST READ BY LOCATION" \
"curl -s '$BASE_URL/weather?location=Vancouver'"

# -------------------------
# TEST DELETE BY ID
# -------------------------
run_test "TEST DELETE BY ID" \
"curl -s -X DELETE $BASE_URL/weather/1"

# -------------------------
# CREATE MULTIPLE RECORDS (not counted as tests; just setup)
# -------------------------
echo ""
echo "=============================="
echo "CREATE MULTIPLE RECORDS (setup)"
echo "=============================="

curl -s -X POST $BASE_URL/weather \
-H "Content-Type: application/json" \
-d '{
  "location":"Toronto",
  "start_date":"2026-02-01",
  "end_date":"2026-02-03"
}' > /dev/null

curl -s -X POST $BASE_URL/weather \
-H "Content-Type: application/json" \
-d '{
  "location":"Toronto",
  "start_date":"2026-03-05",
  "end_date":"2026-03-09"
}' > /dev/null

echo "Created two records"

# -------------------------
# DELETE BY LOCATION
# -------------------------
run_test "DELETE BY LOCATION" \
"curl -s -X DELETE $BASE_URL/weather/location/Toronto"

# -------------------------
# CREATE AGAIN FOR DELETE ALL TEST (setup)
# -------------------------
echo ""
echo "=============================="
echo "CREATE AGAIN FOR DELETE ALL TEST (setup)"
echo "=============================="

curl -s -X POST $BASE_URL/weather \
-H "Content-Type: application/json" \
-d '{
  "location":"Montreal",
  "start_date":"2026-02-01",
  "end_date":"2026-02-05"
}' > /dev/null

echo "Created one record"

# -------------------------
# DELETE ALL (SAFETY CONFIRM)
# -------------------------
run_test "DELETE ALL (SAFETY CONFIRM)" \
"curl -s -X DELETE '$BASE_URL/weather/all?confirm=true'"

# -------------------------
# FINAL READ
# -------------------------
run_test "FINAL READ" \
"curl -s $BASE_URL/weather"

# -------------------------
# SUMMARY
# -------------------------
echo ""
echo "=============================="
echo "TEST SUMMARY"
echo "=============================="
echo "Total tests: $TOTAL"
echo "Passed:      $PASSED"
echo "Failed:      $FAILED"

if [ "$FAILED" -eq 0 ]; then
  echo "✔ All tests passed."
else
  echo "⚠ Some tests failed."
fi