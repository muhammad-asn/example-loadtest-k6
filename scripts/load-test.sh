#!/bin/bash

show_help() {
    echo "Usage: ./load-test.sh [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help            Show this help message"
    echo "  -v, --vus             Number of virtual users (default: 10)"
    echo "  -d, --duration        Duration of the test (default: 30s)"
    echo "  -f, --file            Path to the k6 test script file (default: ./k6-load-test/load-test.js)"
    echo ""
    echo "Example:"
    echo "  ./load-test.sh --vus 20 --duration 60s --file ./k6-load-test/another-test.js"
}

# Default values
VUS=10
DURATION="30s"
FILE="./k6-load-test/load-test.js"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        -v|--vus) VUS="$2"; shift ;;
        -d|--duration) DURATION="$2"; shift ;;
        -f|--file) FILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; show_help; exit 1 ;;
    esac
    shift
done

# Run the K6 load test
docker run -p 5665:5665 --network=test-fastapi -e K6_WEB_DASHBOARD=true --rm -i grafana/k6 run --vus "$VUS" --duration "$DURATION" - < "$FILE"