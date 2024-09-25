import csv
import collections
import argparse

class Log:
    def __init__(self, log_entry: str):
        attributes = log_entry.split()
        
        #Check for valid log format
        if len(attributes) < 14:
            self.valid = False  
            return
        
        self.valid = True

        self.version = attributes[0]
        self.account_id = attributes[1]
        self.interface_id = attributes[2]
        self.src_addr = attributes[3]
        self.dst_addr = attributes[4]
        self.src_port = attributes[5]
        self.dst_port = attributes[6]
        self.protocol = attributes[7] 
        self.packets = attributes[8]
        self.bytes = attributes[9]
        self.start = attributes[10]
        self.end = attributes[11]
        self.action = attributes[12]
        self.log_status = attributes[13]

    def get_protocol_name(self, protocol_map):
        return protocol_map.get(self.protocol)

    def is_valid(self):
        return self.valid


def create_lookup_mapping(file: str) -> dict:
    tag_mappings = dict()
        
    with open(file, "r") as f:
        for each_row in f:
            row_elements = each_row.strip().split(',')

            #Check for correct format - dstport, protocol, tag
            if len(row_elements) == 3:     
                key = (row_elements[0], row_elements[1].lower())  # case insensitive
                tag_mappings[key] = row_elements[2]
        
    return tag_mappings

def find_tags_to_logs(tag_mapping: dict, protocol_mapping: dict, flow_logs_file: str, output_file: str):
    tag_counts = collections.defaultdict(int)  
    port_protocol_counts = collections.defaultdict(int)

    with open(flow_logs_file, 'r') as input:
        for flow_log in input:
                log = Log(flow_log)

                if log.is_valid():
                    protocol_name = log.get_protocol_name(protocol_mapping)
                    lookup_key = (log.dst_port, protocol_name)
                    # Match lookup and determine tag
                    if lookup_key in tag_mapping:
                        tag = tag_mapping[lookup_key]
                    else:
                        tag = "Untagged"

                    #Update tag counts
                    tag = tag_mapping.get(lookup_key, "Untagged")
                    tag_counts[tag] += 1

                    #Update port/protocol counts
                    port_protocol_counts[(log.dst_port, log.get_protocol_name(protocol_mapping))] += 1

    with open(output_file, 'w') as outfile:
        # Write Tag Counts
        outfile.write("Tag Counts:\n")
        for tag, count in tag_counts.items():
            outfile.write(f"{tag},{count}\n")

        outfile.write("\nPort/Protocol Combination Counts:\n")
        for (port, protocol), count in port_protocol_counts.items():
            outfile.write(f"{port},{protocol},{count}\n")

def create_protocol_mapping(file_path: str) -> dict:
    protocol_mapping = {}

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            protocol_number = row['Decimal']
            protocol_name = row['Keyword'].lower()
            protocol_mapping[protocol_number] = protocol_name
    
    return protocol_mapping

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('protocol_mapping_file', type=str)
    parser.add_argument('tag_mapping_file', type=str)
    parser.add_argument('input_file', type=str)
    parser.add_argument('output_file', type=str)

    args = parser.parse_args()

    protocol_file = args.protocol_mapping_file
    mapping_file = args.tag_mapping_file
    input_file = args.input_file
    output_file = args.output_file

    #Create a dictionary that will map the protocol numbers to protocol names
    protocol_mapping = create_protocol_mapping(protocol_file)
    
    #Create a dictionary that will map the dstport,protocol combination to tags
    tag_mapping = create_lookup_mapping(mapping_file)
    
    #Call function to find counts and write to output file
    find_tags_to_logs(tag_mapping, protocol_mapping, input_file, output_file)
    