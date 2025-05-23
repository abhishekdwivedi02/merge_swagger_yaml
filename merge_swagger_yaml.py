from openapi_spec_validator import validate_spec
import os
import yaml
import argparse

def merge_swagger_yaml(dir_path, swagger_filename):
    combined_yaml = {}
    openapi_version = None

    for file_name in os.listdir(dir_path):
        if file_name.endswith(".yaml"):
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as yaml_file:
                yaml_content = yaml.safe_load(yaml_file)
                # Check OpenAPI version
                if "openapi" in yaml_content and openapi_version is None:
                    openapi_version = yaml_content["openapi"]

                for key, value in yaml_content.items():
                    if key in combined_yaml:
                        # Merge arrays if the key exists
                        if isinstance(combined_yaml[key], list) and isinstance(value, list):
                            combined_yaml[key].extend(value)
                        # Merge dictionaries if the key exists
                        elif isinstance(combined_yaml[key], dict) and isinstance(value, dict):
                            combined_yaml[key].update(value)
                        else:
                            print(f"Conflict for key '{key}' in file '{file_name}'. Key will be ignored.")
                    else:
                        combined_yaml[key] = value

    if openapi_version is not None:
        combined_yaml["openapi"] = openapi_version
    else:
        combined_yaml["openapi"] = "3.0.1"

    # Save combined YAML
    with open(swagger_filename, 'w') as sfile:
        yaml.dump(combined_yaml, sfile)

    print(f"Master Swagger YAML created: {swagger_filename}")

    # Validate combined YAML
    try:
        validate_spec(combined_yaml)
        print("Master YAML validated successfully.")
    except Exception as e:
        print(f"Schema validation error: {e}")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Merge Swagger YAML files into one master YAML.")
    parser.add_argument("dir_path", type=str, help="Path to the folder containing Swagger YAML files")
    parser.add_argument(
        "--swagger_filename", type=str, default="master_swagger.yaml",
        help="Name of the master project file (default: master_swagger.yaml)"
    )
    args = parser.parse_args()

    merge_swagger_yaml(args.dir_path, args.swagger_filename)
