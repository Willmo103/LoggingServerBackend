from .controllers import Web
from .controllers import Local
import secrets
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import create_log_model
from .models import APIKey
import json


# Set up the database session
engine = create_engine("sqlite:///instance/logging_api.db")
Session = sessionmaker(bind=engine)
session = Session()


@click.group()
def cli():
    pass


@click.command()
def init():
    click.echo("Initializing LiteLog configuration...")

    conf = {"instance_type": None, "database_path": None, "api_url": None}

    if click.confirm("Do you want to create a new logging instance?"):
        conf["instance_type"] = "local"
        conf["database_path"] = click.prompt(
            "Enter the path to the SQLite database",
            default="instance/logging_api.db"
        )
        confirm_choice = None
        while True:
            if confirm_choice is None:
                app_name = click.prompt(
                    "Enter the name of your application to register it"
                )
            else:
                app_name = click.prompt(
                    "Enter the name of your application to register it"
                )
            confirm_choice = click.confirm(
                f"Register app '{app_name}'?", abort=True)
            if confirm_choice:
                break

        # Register the app and get the API key to save in the config
        controller = Local()
        response, status_code = controller.register_app(app_name)
        if status_code == 201:
            conf["api_key"] = response["api_key"]
        else:
            click.echo(f"Error: {response['error']}", err=True)
            raise click.Abort()
        click.echo(f"App '{app_name}' registered successfully.")
        click.echo(f"API key: {conf['api_key']}")
        click.echo("Please save this API key")
    else:
        conf["instance_type"] = "remote"
        conf["api_url"] = click.prompt(
            "Enter the URL of the running Logging API instance"
        )
        conf["api_key"] = click.prompt("Enter your API key")
        # Check if the API key is valid
        controller = Web()
        response, status_code = controller.get_logs("test")
        if status_code != 200:
            click.echo(f"Error: {response['error']}", err=True)
            raise click.Abort()
        click.echo("API key is valid.")

    # Save the config
    with open("logging_api/config.json", "w") as f:
        json.dump(conf, f)
    click.echo("Configuration saved successfully.")
    click.echo("Initialization complete.")
    click.echo("You can now start using LiteLog.")
    click.echo("Run 'logging-api --help' to see available commands.")
    click.echo("Run 'logging-api start_api' to start the API server.")
    click.echo("Run 'logging-api add_log' to add a new log entry.")
    click.echo("Run 'logging-api get_logs' to get all log entries.")
    click.echo("Run 'logging-api register_app' to register a new app.")
    click.echo("Run 'logging-api init' to re-initialize the configuration.")
    click.echo("Run 'logging-api --version' to see the version.")
    click.echo("configuration can be found in logging_api/config.json")


# Add the init command to your CLI group
cli.add_command(init)


@cli.command()
@click.argument("app_name")
def register_app(app_name):
    """Registers a new app to send logs."""

    # Check if the app name is already registered
    api_key_entry = session.query(APIKey).filter_by(app_name=app_name).first()
    if api_key_entry:
        click.echo(
            "App name already registered. Please choose another name.",
            err=True
        )
        raise click.Abort()

    # Generate a new API key
    api_key = secrets.token_hex(32)
    new_api_key = APIKey(key=api_key, app_name=app_name)
    session.add(new_api_key)
    session.commit()

    # Create the log table for the app
    LogModel = create_log_model(app_name)
    LogModel.__table__.create(bind=engine, checkfirst=True)

    click.echo(f"App '{app_name}' registered successfully.")
    click.echo(f"API key: {api_key}")
    click.echo("Please save this API key in your app.")


@click.command()
@click.argument("app_name")
def get_logs_command(app_name):
    controller = Local()  # or Web() if you're using the Web version
    logs, status_code = controller.get_logs(app_name)
    if status_code == 200:
        for log in logs:
            click.echo(log)
    else:
        click.echo(f"Error: {logs['error']}")


@cli.command()
@click.argument("app_name")
@click.argument("message")
def add_log(app_name, message):
    """Adds a new log entry for a specific app."""
    # Your logic to add a new log entry to the database


@cli.command()
def start_api():
    """Starts the Flask API server."""
    # Your logic to start the Flask app


if __name__ == "__main__":
    cli()
