# Dynatrace DQL Log Analysis Simulation

## Overview

This project simulates **Dynatrace Query Language (DQL)** log analysis using **Python**, without requiring access to a Dynatrace tenant.  
It demonstrates how to parse logs, filter events, summarize failures, and sort results — mirroring real-world observability workflows.

The key focus is on **LD (Literal Delimiter) parsing**, which is widely used in Dynatrace to extract structured information from consistent log messages.

---

## Features

- **LD Parsing Simulation**: Extracts fields from logs using literal delimiter logic.
- **Filtering Logs**: Filters by log source and severity (`ERROR` logs).
- **Summarization**: Counts failures grouped by `service` and `reason`.
- **Sorting**: Outputs results in descending order of failures.
- **DQL ↔ Python Mapping**: Shows direct equivalence between Dynatrace DQL queries and Python code.
- **Extensible**: Easy to add regex parsing, time-based grouping, or additional metrics.

---

## Project Structure

```
dynatrace-dql-log-analysis/
├── analysis/
│ └── log_analysis.py # Python script simulating DQL logic
├── logs/
│ └── sample_logs.json # Sample log data
├── queries/
│ └── dql_queries.md # DQL-style example queries
└── README.md # Project overview & instructions
```


---

## How It Works

### Sample Log Format

```
{
    "timestamp": "2025-12-10T10:16:10Z",
    "log.source": "dql-exercise",
    "content": "FunctionInvocation failed due to timeout",
    "level": "ERROR",
    "service": "payment-service"
}
```

### Python ↔ DQL Mapping

| Dynatrace DQL                                                  | Python Implementation                                                  |
| -------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `filter log.source == "dql-exercise"`                          | `if log.get("log.source") == "dql-exercise":`                          |
| `filter level == "ERROR"`                                      | `if log.get("level") == "ERROR":`                                      |
| `parse content, "FunctionInvocation failed due to " LD reason` | `reason = parse_ld(log.get("content", ""), "FunctionInvocation failed due to ")` |
| `summarize failures = count(), by: { service, reason }`        | `summary[(log['service'], reason)] += 1  # using defaultdict(int)`     |
| `sort failures desc`                                           | `sorted_summary = sorted(summary.items(), key=lambda x: x[1], reverse=True)` |



### Usage
```
git clone https://github.com/subir-the-coder/dynatrace-dql-log-analysis.git
cd dynatrace-dql-log-analysis/analysis
python log_analysis.py
```
### Sample output

<img width="597" height="73" alt="simulating" src="https://github.com/user-attachments/assets/bef2d276-af9a-4182-a301-e1318754411f" />

### Learning Outcomes

- Practical understanding of Dynatrace DQL syntax
- Implementation of LD parsing logic in Python
- Experience with log filtering, summarization, and sorting
- Mapping between observability queries and real code
- Prepares for Dynatrace Associate Certification and real-world monitoring tasks

### Future Improvements

- Add regex fallback parsing for variable logs
- Implement time-based grouping and metrics visualization
- Add unit tests for parsing functions
- Extend to simulate real Dynatrace dashboards

### LICENSE
This project is open-source and available for learning and portfolio purposes

