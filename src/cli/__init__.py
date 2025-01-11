import click
from src.jobs.main import main as run_job

@click.command()
def cli():
    """Command Line Interface to run the job
    with command python -m src.cli
    """
    run_job()

if __name__ == '__main__':
    cli()
