import click
import sys
from .converters import convert_csv_to_json, convert_json_to_excel
from .merger import merge_csv_files
from .validator import validate_csv_data
from .utils.logger import setup_logger

logger = setup_logger("dataops-cli")

@click.group()
def main():
    """DataOps Toolkit: A modular automation framework."""
    pass

@main.command()
@click.argument("input_path")
@click.argument("output_path")
def csv_to_json(input_path, output_path):
    """Convert CSV file to JSON."""
    try:
        convert_csv_to_json(input_path, output_path)
        click.echo(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument("input_path")
@click.argument("output_path")
@click.option("--json-fields", help="Comma-separated list of JSON fields to keep (e.g. 'key,doc_count')")
@click.option("--output-headers", help="Comma-separated list of Excel headers (e.g. 'id,count')")
def json_to_excel(input_path, output_path, json_fields, output_headers):
    """Convert JSON file to Excel. Optionally filter and rename fields."""
    try:
        field_map = None
        
        if json_fields and output_headers:
            j_fields = [f.strip() for f in json_fields.split(",")]
            o_headers = [h.strip() for h in output_headers.split(",")]
            
            if len(j_fields) != len(o_headers):
                raise ValueError("Number of json-fields and output-headers must match.")
            
            field_map = dict(zip(j_fields, o_headers))
            logger.info(f"Field mapping configured: {field_map}")
        
        elif json_fields or output_headers:
            raise ValueError("Both --json-fields and --output-headers must be provided together.")
                
        convert_json_to_excel(input_path, output_path, fields=field_map)
        click.echo(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument("input_files", nargs=-1)
@click.argument("output_path")
@click.option("--on", help="Columns to join on. Format: 'col' or 'col1,col2' for left/right.")
@click.option("--how", default="inner", help="Join type: inner, left, right, outer.")
def merge(input_files, output_path, on, how):
    """Merge multiple CSV files. Use --on for joins."""
    try:
        join_on = None
        if on:
            join_on = [x.strip() for x in on.split(",")]
            
        merge_csv_files(list(input_files), output_path, join_on=join_on, how=how)
        click.echo(f"Successfully merged files into {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument("input_path")
def validate(input_path):
    """Validate CSV data."""
    try:
        report = validate_csv_data(input_path)
        click.echo("Validation Report:")
        for key, value in report.items():
            click.echo(f"  {key}: {value}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
