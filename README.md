# Flow Logs Parser

### Objective
The **output file** contains two sections:
   - **Tag Counts**: The number of times each tag appears in the flow logs.
   - **Port/Protocol Combination Counts**: The count of each unique `dstport, protocol` combination.

### Assumptions
1. Only the **default log format** (version 2) is supported.
2. The **flow log file size** can be up to 10 MB.
4. **Case insensitivity** is applied to the protocol names during the matching process.
5. If no tag is found for a specific `dstport, protocol` combination, the flow log entry is marked as **"Untagged"**.


---

### How to Run

#### Prerequisites:
- Python 3.x (tested on Python 3.11.4)
- Only Python's standard libraries are used (`argparse`, `csv`, `collections`).

#### Instructions:
1. **Clone the repository** or download the files to your local machine:
   ```bash
   git clone https://github.com/anahita20/flow-log-parser.git
   cd flow-log-parser
   ```
2. Make sure you have the necessary input files - 
 - `PROTOCOL_FILE`: For the purpose of mapping the protocol numbers to their corresponding names, I used the reference found on [IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)
 - `MAPPING_FILE`: This contains the tag mappings. For eg, _25,tcp,sv_P1_
 - `INPUT_FILE`: This contains the flow logs input data
 - `OUTPUT_FILE`: (Optional) The output will be written to this file path
3. Runing the program takes 4 arguments as shown below in the command:
    ```
    python flow_log_parser.py <PROTOCOL_FILE> <MAPPING_FILE> <INPUT_FILE> <OUTPUT_FILE> 
    ```
### Tests

1. Basic functionality: Verified that log entries are correctly mapped to tags.
2. Edge cases:
-- Unmatched entries are properly marked as "Untagged".
-- Case insensitivity is correctly applied during tag mapping.
3. Performance: The program was tested with log files of different sizes, up to 10MB.
4. Invalid entries: The program skips malformed or incomplete log entries. 


