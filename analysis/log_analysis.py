import json
from collections import defaultdict
from pathlib import Path


# -------------------------------
# Configuration
# -------------------------------
LOG_FILE = Path(__file__).parent.parent / "logs" / "sample_logs.json"
LD_DELIMITER = "FunctionInvocation failed due to "


# -------------------------------
# LD Parsing Function
# -------------------------------
def parse_ld(content: str, delimiter: str):
    """
    Simulates Dynatrace LD (Literal Delimiter) parsing.

    Logic:
    - If content starts with the literal delimiter,
      return everything after it.
    - Otherwise, return None.

    This mirrors:
    parse content, "<literal>" LD field
    """
    if not content:
        return None

    if content.startswith(delimiter):
        return content[len(delimiter):].strip()

    return None


# -------------------------------
# Load Logs
# -------------------------------
def load_logs(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------
# Main Analysis Logic
# -------------------------------
def analyze_logs(logs):
    """
    Implements the equivalent of this DQL:

    fetch logs
    | filter log.source == "dql-exercise"
    | filter level == "ERROR"
    | parse content, "FunctionInvocation failed due to " LD reason
    | summarize failures = count(), by: { service, reason }
    | sort failures desc
    """
    parsed_entries = []

    # Filtering + LD parsing
    for log in logs:
        if (
            log.get("log.source") == "dql-exercise"
            and log.get("level") == "ERROR"
        ):
            reason = parse_ld(log.get("content", ""), LD_DELIMITER)

            if reason:
                parsed_entries.append({
                    "service": log.get("service"),
                    "reason": reason
                })

    # Summarize (count by service + reason)
    summary = defaultdict(int)
    for entry in parsed_entries:
        key = (entry["service"], entry["reason"])
        summary[key] += 1

    # Sort descending by failure count
    sorted_summary = sorted(
        summary.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_summary


# -------------------------------
# Output
# -------------------------------
def print_results(results):
    print("\nFailures by service and reason\n" + "-" * 40)

    if not results:
        print("No matching failures found.")
        return

    for (service, reason), count in results:
        print(
            f"Service: {service:<20} | "
            f"Reason: {reason:<15} | "
            f"Failures: {count}"
        )


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    logs = load_logs(LOG_FILE)
    results = analyze_logs(logs)
    print_results(results)
