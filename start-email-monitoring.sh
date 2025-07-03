#!/bin/bash

# Start Email Monitoring Script
# This script runs the monitoring in the background and updates every 30 minutes

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/monitoring.log"
PID_FILE="$SCRIPT_DIR/monitoring.pid"

# Check if monitoring is already running
if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Monitoring is already running (PID: $OLD_PID)"
        echo "To stop monitoring, run: kill $OLD_PID"
        exit 1
    else
        echo "Removing stale PID file"
        rm "$PID_FILE"
    fi
fi

echo "Starting email forwarding monitoring for vancouverpetservices.com"
echo "This will run in the background and check every 30 minutes"
echo ""

# Start the monitoring in background
nohup bash -c '
    while true; do
        echo "[$(date)] Running DNS check..." >> "'$LOG_FILE'"
        
        # Run the quick test
        cd "'$SCRIPT_DIR'"
        ./quick-email-test.sh >> "'$LOG_FILE'" 2>&1
        
        # Check if DNS is ready
        if grep -q "DNS is properly configured!" test-results.log 2>/dev/null; then
            echo "[$(date)] DNS configured! Running email tests..." >> "'$LOG_FILE'"
            python3 email-test-script.py --once >> "'$LOG_FILE'" 2>&1
        fi
        
        # Update dashboard
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M PST")
        if grep -q "DNS is properly configured!" test-results.log 2>/dev/null; then
            STATUS="🟢 DNS CONFIGURED - Testing Email"
        else
            STATUS="🔴 DNS NOT CONFIGURED"
        fi
        
        # Update the dashboard file
        sed -i.bak "s/\*\*Last Updated\*\*:.*/\*\*Last Updated\*\*: $TIMESTAMP/" email-test-dashboard.md
        sed -i.bak "s/## .* Current Status:.*/## $STATUS/" email-test-dashboard.md
        
        # Sleep for 30 minutes
        sleep 1800
    done
' > /dev/null 2>&1 &

# Save PID
echo $! > "$PID_FILE"
MONITOR_PID=$!

echo "✅ Monitoring started successfully!"
echo "Process ID: $MONITOR_PID"
echo ""
echo "📊 View status: cat email-test-dashboard.md"
echo "📝 View logs: tail -f monitoring.log"
echo "🛑 Stop monitoring: kill $MONITOR_PID"
echo ""
echo "The system will check DNS every 30 minutes and automatically"
echo "start email tests once DNS is configured."