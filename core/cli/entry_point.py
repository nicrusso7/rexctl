import os
import subprocess

import click


@click.group()
def cli():
    pass


@cli.command()
def init():
    click.echo("-> Creating Rex context.")
    # this is a very poor hardcoded path
    # @ TODO
    ctl_dir_path = '/usr/local/lib/python3.6/dist-packages/webserver'
    # --------------------------------------------------------------
    subprocess.run(["sudo", "sh", os.path.join(ctl_dir_path, "scripts/setup.sh"), ctl_dir_path],
                   check=True, stdout=subprocess.PIPE, universal_newlines=True)
    click.echo("-> Done!")
    click.echo("-> Rex is loading its daemons. It will takes some minutes, please check the log.")


@cli.command()
def status():
    proc = subprocess.run(["curl", "-s", "http://rex/status"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


@cli.command()
@click.option('--command', '-c')
def exec(command):
    proc = subprocess.run(["curl", "-s", "-H", "Content-Type: application/json",
                           "-X", "POST", "-d", f"'{command}'", "http://rex/exec"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


@cli.command()
def stop_all():
    proc = subprocess.run(["curl", "-s", "http://rex/stop_all"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


@cli.command()
def log():
    proc = subprocess.run(["sudo", "cat", "/var/log/uwsgi/app/portal.log"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


@cli.command()
def debug_pose():
    proc = subprocess.run(["curl", "-s", "http://rex/debug_pose"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


@cli.command()
def calibration():
    proc = subprocess.run(["curl", "-s", "http://rex/get_calibration"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


@cli.command()
def store_calibration():
    proc = subprocess.run(["curl", "-s", "http://rex/store_calibration"],
                          check=True, stdout=subprocess.PIPE, universal_newlines=True)
    out = proc.stdout
    click.echo(out)


if __name__ == '__main__':
    init()
