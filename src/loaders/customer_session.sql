SELECT 
    session_id,
    customer_id,
    session_start_time,
    session_end_time,
    pages_visited,
    conversion_flag
FROM 
    customer_sessions
WHERE 
    session_start_time BETWEEN '{start_time}' AND '{end_time}'
    AND customer_id = '{customer_id}'
ORDER BY
    session_start_time DESC;
