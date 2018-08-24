import click
import sys
import pprint
import copy


@click.group()
@click.pass_context
def generate(ctx):
    click.secho('ATTENTION', blink=True, bold=True)
    pass


@generate.command()
@click.pass_obj
def app(config):
    click.secho('ATTENTION', blink=True, bold=True)