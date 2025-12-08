import argparse
import sys
import json
from .src.dataops.converters import csv_to_json
from .src.dataops.converters import json_to_excel
from .src.dataops.merger import merge_files
from .src.dataops.validator import validate_data
from .src.dataops.utils.logger import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="DataOps Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Convert Command
    convert_parser = subparsers.add_parser("convert", help="Convert data formats")
    convert_parser.add_argument("input", help="Input file path")
    convert_parser.add_argument("output", help="Output file path")
    convert_parser.add_argument("--format", choices=['json', 'excel'], required=True, help="Target format")

    # Merge Command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple files")
    merge_parser.add_argument("inputs", nargs="+", help="Input file paths")
    merge_parser.add_argument("output", help="Output file path")

    # Validate Command
    validate_parser = subparsers.add_parser("validate", help="Validate data quality")
    validate_parser.add_argument("input", help="Input file path")

    args = parser.parse_args()

    if args.command == "convert":
        if args.format == "json":
            csv_to_json(args.input, args.output)
        elif args.format == "excel":
            json_to_excel(args.input, args.output)
            
    elif args.command == "merge":
        merge_files(args.inputs, args.output)
        
    elif args.command == "validate":
        report = validate_data(args.input)
        print(json.dumps(report, indent=4))
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
