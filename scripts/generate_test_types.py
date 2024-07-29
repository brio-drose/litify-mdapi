import re
import csv

def extract_classes_and_types(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex patterns to capture class names and types
    class_pattern = re.compile(r'\bpublic\s+class\s+(\w+)')
    variable_type_pattern = re.compile(r'\b(?:public|private|protected)?\s*(\w+)\s+\w+\s*[;,=)\[{]')
    
    classes = set(class_pattern.findall(content))
    # Comprehensive list of keywords to filter out
    keywords = {
        'public', 'private', 'protected', 'new', 'implements', 'extends', 'static', 'final', 'abstract', 
        'class', 'interface', 'enum', 'void', 'return', 'boolean', 'byte', 'char', 'short', 'int', 
        'long', 'float', 'double', 'String', 'Boolean', 'Integer', 'Double', 'List', 'Map', 'Set', 
        'ANY', 'STRICT', 'OR', 'BUSINESS', 'string', 'Object', 'Date', 'Datetime', 'Time', 'Blob'
    }

    types = set()
    for match in variable_type_pattern.findall(content):
        if match not in keywords:
            types.add(match)

    # Merge classes and types into a single set
    all_classes_types = classes.union(types)

    return list(all_classes_types)

def write_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Class/Type"])
        for item in data:
            writer.writerow([f"new MetadataService.{item}createMetadataResponse_element();"])

file_path = r'./force-app/main/default/classes/MetadataService.cls'
output_file = r'./scripts/temp/classes_and_types.csv'

classes_and_types = extract_classes_and_types(file_path)
write_to_csv(classes_and_types, output_file)

print(f"CSV file generated and saved to {output_file}")
