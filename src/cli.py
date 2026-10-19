"""CLI interface for Lambda management"""

import click
import json
from .lambda_manager import LambdaManager


@click.group()
@click.option("--region", default="us-east-1", help="AWS region")
@click.pass_context
def cli(ctx, region):
    """Lambda Management Tool"""
    ctx.ensure_object(dict)
    ctx.obj["manager"] = LambdaManager(region=region)


@cli.command()
@click.argument("function_name")
@click.pass_context
def get_config(ctx, function_name):
    """Get Lambda function configuration"""
    try:
        manager = ctx.obj["manager"]
        config = manager.get_function_config(function_name)
        click.echo(json.dumps(config, indent=2, default=str))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("function_name")
@click.option("--timeout", type=int, help="Timeout in seconds")
@click.option("--memory", type=int, help="Memory in MB")
@click.option("--env", type=str, multiple=True, help="Environment variables (KEY=VALUE)")
@click.pass_context
def update_config(ctx, function_name, timeout, memory, env):
    """Update Lambda function configuration"""
    try:
        manager = ctx.obj["manager"]
        config_updates = {}

        if timeout:
            config_updates["Timeout"] = timeout
        if memory:
            config_updates["MemorySize"] = memory

        if env:
            environment_vars = {}
            for var in env:
                key, value = var.split("=")
                environment_vars[key] = value
            config_updates["Environment"] = {"Variables": environment_vars}

        result = manager.update_function_config(function_name, config_updates)
        click.echo("Function updated successfully!")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.pass_context
def list_functions(ctx):
    """List all Lambda functions"""
    try:
        manager = ctx.obj["manager"]
        functions = manager.list_functions()
        click.echo(f"Found {len(functions)} functions:")
        for func in functions:
            click.echo(f"  - {func['FunctionName']} ({func['Runtime']})")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("function_name")
@click.argument("config_file")
@click.pass_context
def update_from_file(ctx, function_name, config_file):
    """Update Lambda function from configuration file"""
    try:
        manager = ctx.obj["manager"]
        result = manager.update_from_config_file(function_name, config_file)
        click.echo("Function updated successfully!")
        click.echo(json.dumps(result, indent=2, default=str))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
