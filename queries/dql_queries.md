## DQL-style Log Queries (Simulated)

### 1. Fetch logs from a specific source
```dql
fetch logs
| filter log.source == "dql-exercise"
```

### 2. Find Function Invocations
```
fetch logs
| filter contains(content, "FunctionInvocation")
```

### 3. Find error logs
```
fetch logs
| filter level == "ERROR"
```

### 4. Count errors by service
```
fetch logs
| filter level == "ERROR"
| summarize count(), by: {service}
```

### 5. Chaining and using some more DQL commands 
```
fetch logs
| filter log.source == "dql-exercise"
| filter level == "ERROR"
| parse content, "FunctionInvocation failed due to " LD reason
| summarize failures = count(), by: { service, reason }
| sort failures desc
```