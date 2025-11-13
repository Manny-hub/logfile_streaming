# Log Parsing Logic
import json
import re 
import os


def processor():
    """
    Processes the log content and extracts relevant information.
    
    Args:
        log_content (str): The content of the log file.
        
    """
    log_entries = []
    error_entries = []

    # Regular expression to match log entries
    log_pattern = re.compile(
        r'^(?P<ipaddress>\d{1,3}(?:\.\d{1,3}){3}) \- - \[(?P<timestamp>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>[^"]+) (?P<protocol>[^"]+)" (?P<status_code>\d{3}) (?P<bytes_sent>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"$',
        re.MULTILINE
    )
    
    for line in log_content.splitlines():
        match = log_pattern.match(line)
        if match:
            entry = {
                'ipaddress': match.group('ipaddress'),
                'timestamp': match.group('timestamp'),
                'method': match.group('method'),
                'path': match.group('path'),
                'protocol': match.group('protocol'),
                'status_code': match.group('status_code'),
                'bytes_sent': match.group('bytes_sent'),
                'referrer': match.group('referrer'),
                'user_agent': match.group('user_agent')
            }
            log_entries.append(entry)
        else:
            error_entries.append(line)

    return log_entries, error_entries