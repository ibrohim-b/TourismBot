#!/bin/bash

cd "$(dirname "$0")"
mkdir -p logs

# --- Helper Functions ---

setup_venv() {
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install  -r requirements.txt
}

is_running() {
    local pidfile="$1"
    if [ -f "$pidfile" ]; then
        local pid
        pid=$(cat "$pidfile")
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # running
        else
            rm -f "$pidfile"  # stale PID file
        fi
    fi
    return 1  # not running
}

start_service() {
    local name="$1"
    local cmd="$2"
    local logfile="logs/nohup_${name}.log"
    local pidfile="logs/${name}.pid"

    if is_running "$pidfile"; then
        echo "$name is already running (PID: $(cat "$pidfile"))"
        return 1
    fi

    nohup python3 "$cmd" > "$logfile" 2>&1 &
    echo $! > "$pidfile"
    echo "$name started (PID: $!)"
}

stop_service() {
    local name="$1"
    local pidfile="logs/${name}.pid"

    if is_running "$pidfile"; then
        kill "$(cat "$pidfile")" 2>/dev/null
        rm -f "$pidfile"
        echo "$name stopped"
    else
        echo "$name is not running"
    fi
}

# --- Main ---

case "$1" in
    bot)
        setup_venv
        start_service "bot" "bot/main.py"
        ;;
    admin)
        setup_venv
        start_service "admin" "web/run_admin.py"
        ;;
    both)
        setup_venv
        start_service "admin" "web/run_admin.py"
        start_service "bot" "bot/main.py"
        ;;
    stop)
        stop_service "bot"
        stop_service "admin"
        ;;
    status)
        for svc in bot admin; do
            if is_running "logs/${svc}.pid"; then
                echo "$svc is running (PID: $(cat "logs/${svc}.pid"))"
            else
                echo "$svc is not running"
            fi
        done
        ;;
    *)
        echo "Usage: ./start.sh [bot|admin|both|stop|status]"
        exit 1
        ;;
esac
