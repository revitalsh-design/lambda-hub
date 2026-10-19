"""Core Lambda management functionality"""

import boto3
from typing import Dict, Any, List, Optional
import json


class LambdaManager:
    """Manage AWS Lambda function configurations"""

    def __init__(self, region: str = "us-east-1"):
        """
        Initialize Lambda manager

        Args:
            region: AWS region
        """
        self.client = boto3.client("lambda", region_name=region)
        self.region = region

    def get_function_config(self, function_name: str) -> Dict[str, Any]:
        """
        Get Lambda function configuration

        Args:
            function_name: Name or ARN of the Lambda function

        Returns:
            Function configuration dict
        """
        try:
            response = self.client.get_function_configuration(
                FunctionName=function_name
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to get function config: {str(e)}")

    def update_function_config(
        self, function_name: str, config_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update Lambda function configuration

        Args:
            function_name: Name or ARN of the Lambda function
            config_updates: Dictionary of configuration updates

        Returns:
            Updated function configuration
        """
        try:
            response = self.client.update_function_configuration(
                FunctionName=function_name, **config_updates
            )
            return response
        except Exception as e:
            raise Exception(f"Failed to update function config: {str(e)}")

    def list_functions(self) -> List[Dict[str, Any]]:
        """
        List all Lambda functions in the region

        Returns:
            List of function configurations
        """
        try:
            functions = []
            paginator = self.client.get_paginator("list_functions")
            for page in paginator.paginate():
                functions.extend(page.get("Functions", []))
            return functions
        except Exception as e:
            raise Exception(f"Failed to list functions: {str(e)}")

    def update_from_config_file(
        self, function_name: str, config_file: str
    ) -> Dict[str, Any]:
        """
        Update Lambda function from a configuration file (JSON/YAML)

        Args:
            function_name: Name or ARN of the Lambda function
            config_file: Path to configuration file

        Returns:
            Updated function configuration
        """
        import yaml

        try:
            with open(config_file, "r") as f:
                if config_file.endswith(".json"):
                    config = json.load(f)
                else:  # YAML
                    config = yaml.safe_load(f)

            return self.update_function_config(function_name, config)
        except Exception as e:
            raise Exception(f"Failed to update from config file: {str(e)}")
