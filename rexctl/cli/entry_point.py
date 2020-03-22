import click

from control_unit.rex_daemon import RexDaemon


@click.group()
def cli():
    pass


@cli.command()
@click.pass_context
def init(ctx):
    click.echo("Create Rex context")
    ctx.obj = RexDaemon()


@cli.command()
@click.pass_context
def status(rex_daemon):
    click.echo(rex_daemon.DAEMONS_MAP)


@cli.command()
@click.option('--command', '-c')
@click.pass_context
def exec(rex_daemon, command):
    rex_daemon.exec(command)


if __name__ == '__main__':
    cli()
