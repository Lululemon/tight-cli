import click, os, sys, shutil, subprocess, yaml, glob, time
from os.path import basename, isfile
from inflector import Inflector, English
from colorama import init
from termcolor import colored
from jinja2 import Template
from dynamo3 import DynamoDBConnection
from collections import namedtuple
from flywheel import Engine

init()

INFLECTOR = Inflector(English)
HERE = os.path.dirname(os.path.realpath(__file__))
LAMBDA_APP_TEMPLATES = '{}/blueprints/providers/aws/lambda_app/templates'.format(HERE)
CWD = os.getcwd()
CONFIG = {}
VENDOR_DIR = None
ENV_DIST = '{}/env.dist.yml'.format(CWD)

def get_config(target):
    try:
        with open('{}/tight.yml'.format(target)) as tight_config:
            config = yaml.load(tight_config)
    except Exception as e:
        pass

    return config

if CONFIG and 'vendor_dir' in CONFIG:
    VENDOR_DIR = CONFIG['vendor_dir']

VENDOR_REQUIREMENTS_FILE = '{}/requirements-vendor.txt'.format(CWD)
TESTS_DIR = '{}/tests'.format(CWD)

def get_template(template_root, template):
    with open('{}/{}'.format(template_root, template), 'r') as handler_template:
        template = Template(handler_template.read())
    return template


def color(message):
    return colored(message, 'yellow', 'on_grey')


@click.group()
def main():
    pass


@click.group()
def generate():
    pass


def generate_app_provider_option(context, param, value):
    if value != 'aws':
        raise click.BadParameter('aws is the only provider currently supported')
    return value


def generate_app_type_option(context, param, value):
    if 'provider' not in context.params:
        raise click.BadParameter('--provider must be specified first')
    if context.params['provider'] == 'aws':
        if value != 'lambda':
            raise click.BadParameter('lambda is the only type currently supported')
    return value


@click.command()
@click.option('--provider', default='aws', help='Platform providers', callback=generate_app_provider_option,
              expose_value=True, is_eager=True)
@click.option('--type', default='lambda', help='Provider app type', callback=generate_app_type_option,
              expose_value=True, is_eager=True)
@click.option('--target', default=CWD, help='Location where app will be created.')
@click.argument('name')
def app(provider, type, target, name):
    generator = getattr(sys.modules[__name__], 'generate_app_{}_{}'.format(provider, type))
    generator(name, target)


@click.command()
@click.option('--provider', default='aws', help='Platform providers', type=click.Choice(['aws']))
@click.option('--type', default='lambda_proxy', help='Function type', type=click.Choice(['lambda_proxy']))
@click.option('--target', default=CWD, help='Location where app will be created.')
@click.argument('name')
def function(provider, type, target, name):
    function_dir = '{}/app/functions/{}'.format(target, name)
    try:
        os.mkdir(function_dir)
    except Exception as e:
        if e.strerror == 'File exists':
            raise click.BadParameter('Function already exists!', param_hint='NAME')
        else:
            raise Exception('Cannot create function dir')

    try:
        with open('{}/__init__.py'.format(function_dir), 'w') as file:
            file.write('')
    except Exception as e:
        raise Exception('Could not wite function __init__.py file')

    template = get_template(LAMBDA_APP_TEMPLATES, 'lambda_proxy_controller.jinja2')

    with open('{}/handler.py'.format(function_dir), 'w') as file:
        file.write(template.render())

    integration_test_dir = '{}/tests/functions/integration/{}'.format(target, name)
    integration_test_expectations_dir = '{}/tests/functions/integration/{}/expectations'.format(target, name)
    integration_test_placebos_dir = '{}/tests/functions/integration/{}/placebos'.format(target, name)
    unit_test_dir = '{}/tests/functions/unit/{}'.format(target, name)

    os.mkdir(integration_test_dir)
    os.mkdir(integration_test_expectations_dir)
    os.mkdir(integration_test_placebos_dir)
    os.mkdir(unit_test_dir)

    with open('{}/test_integration_{}.py'.format(integration_test_dir, name), 'w') as file:
        template = get_template(LAMBDA_APP_TEMPLATES, 'lambda_proxy_controller_integration_test.jinja2')
        file.write(template.render(name=name))

    with open('{}/test_unit_{}.py'.format(unit_test_dir, name), 'w') as file:
        template = get_template(LAMBDA_APP_TEMPLATES, 'lambda_proxy_controller_unit_test.jinja2')
        file.write(template.render(name=name))

    with open('{}/test_get_method.yml'.format(integration_test_expectations_dir, name), 'w') as file:
        template = get_template(LAMBDA_APP_TEMPLATES, 'lambda_proxy_controller_get_expectation.jinja2')
        file.write(template.render(name=name))

    command = ['py.test', '{}/tests'.format(target)]
    subprocess.call(command)
    click.echo(color(message='Successfully generated function and tests!'))


def generate_app_aws_lambda(name, target):
    HERE = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree('{}/blueprints/providers/aws/lambda_app/starter'.format(HERE), '{}/{}'.format(target, name))
    app_name = INFLECTOR.underscore(name).replace('_', '-')
    with open('{}/{}/tight.yml'.format(target, name), 'w') as tight_yml:
        template = get_template(LAMBDA_APP_TEMPLATES, 'tight.yml.jinja2')
        tight_yml.write(template.render(name=app_name))

    with open('{}/{}/conftest.py'.format(target, name), 'w') as conftest_template:
        template = get_template(LAMBDA_APP_TEMPLATES, 'conftest.jinja2')
        conftest_template.write(template.render(name=app_name))

    """ Create the app vendor directory """
    vendordir = '{}/{}/app/vendored'.format(target, name)
    os.mkdir(vendordir)

    with open('{}/__init__.py'.format(vendordir), 'w') as init_file:
        init_file.write('')


@click.group()
def pip():
    pass


@click.command()
@click.argument('package_name', nargs=-1)
@click.option('--requirements/--no-requirements', default=False)
@click.option('--requirements-file', default=VENDOR_REQUIREMENTS_FILE, help='Requirements file location', type=click.Choice([VENDOR_REQUIREMENTS_FILE]))
@click.option('--target', default=CWD, help='Target directory.')
def install(*args, **kwargs):
    target = kwargs.pop('target')
    vendor_dir = get_config(target)['vendor_dir']
    package_name = kwargs.pop('package_name')[0] if ('package_name' in kwargs) and len(kwargs['package_name']) > 0 else None
    requirements_file = kwargs.pop('requirements_file')
    vendor_dir_path = '{}/{}'.format(target, vendor_dir)
    if package_name:
        click.echo(color(message='Installing pacakage {}'.format(vendor_dir_path)))
        command = ['pip', 'install', package_name, '-t', vendor_dir_path, '--upgrade']
        subprocess.call(command)
        click.echo(color(message='Installed {}'.format(package_name)))

        with open(requirements_file, 'r') as read_file:
            packages = read_file.read().split('\n')
            if package_name not in packages:
                with open(requirements_file, 'a') as append_file:
                    append_file.write('\n{}'.format(package_name))

    elif kwargs.pop('requirements'):
        command = ['pip', 'install', '-r', requirements_file, '-t',
                   vendor_dir_path, '--upgrade']
        subprocess.call(command)
        botocore_path = '{}/botocore'.format(vendor_dir_path)
        boto3_path = '{}/boto3'.format(vendor_dir_path)
        if os.path.exists(botocore_path):
            shutil.rmtree(botocore_path)
            subprocess.call(['rm -rf {}-*'.format(botocore_path)], shell=True)
            click.echo(color(message='Removed botocore from {}'.format(vendor_dir_path)))
        if os.path.exists(boto3_path):
            shutil.rmtree(boto3_path)
            subprocess.call(['rm -rf {}-*'.format(boto3_path)], shell=True)
            click.echo(color(message='Removed boto3 from {}'.format(vendor_dir_path)))


@click.command()
@click.option('--target', default=CWD)
def env(*args, **kwargs):
    target = kwargs.pop('target')
    env_dist_path = '{}/env.dist.yml'.format(target)
    dist_env_vars = yaml.load(open(env_dist_path))
    for k, v in dist_env_vars.iteritems():
        if os.environ.get(k):
            dist_env_vars[k] = os.environ[k]
    stream = file('{}/env.yml'.format(target), 'w')
    dist_env_vars['NAME'] = get_config(target)['name'].replace('_', '-')
    yaml.safe_dump(dist_env_vars, stream)
    print yaml.dump(dist_env_vars)


@click.command()
@click.option('--target', default='{}/app/models'.format(CWD), help='Location to save model.')
@click.argument('name')
def model(target, **kwargs):
    model_name = kwargs.pop('name')
    class_name = INFLECTOR.camelize(model_name)
    table_name = INFLECTOR.tableize(class_name)
    table_name = table_name.replace('_', '-')
    template = get_template(LAMBDA_APP_TEMPLATES, 'flywheel_model.jinja2')
    with open('{}/{}.py'.format(target, class_name), 'w') as file:
        file.write(template.render(class_name=class_name, table_name=table_name))


def load_env(target):
    env_vars = yaml.load(open('{}/env.yml'.format(target)))
    if not env_vars:
        raise Exception('Could not load env.yml. Have you run `tight generate env`?')

    for k, v in env_vars.iteritems():
        os.environ[k] = str(v)

@click.group()
def dynamo():
    pass

@click.command()
@click.option('--target', default=CWD)
def generateschema(*args, **kwargs):
    target = kwargs.pop('target')
    load_env(target)
    generate_cf_dynamo_schema(target)

def write_schema_to_yaml(target, **kwargs):
    properties = kwargs.copy()
    table_name = "-".join(kwargs.pop('TableName').split('-')[3:])
    properties['TableName'] = '{}-{}-{}'.format(os.environ['NAME'], os.environ['STAGE'], table_name)
    table = {
        'Type': 'AWS::DynamoDB::Table',
        'Properties': properties
    }
    stream = file('{}/schemas/dynamo/{}.yml'
                  .format(target, table_name), 'w')
    yaml.safe_dump(table, stream)

def generate_cf_dynamo_schema(target):
    dynamo_connection = DynamoDBConnection()
    class FakeClient(object):
        def create_table(self, *args, **kwargs):
            write_schema_to_yaml(target, **kwargs)
            return {}

    client = FakeClient()
    dynamo_connection.client = client

    class FakeDynamo(object):
        def list_tables(self):
            return []
        def create_table(self, *args):
            result = dynamo_connection.create_table(*args)
        def describe_table(self, *args):
            StatusStruct = namedtuple('Status', 'status')
            return StatusStruct(status='ACTIVE')

    dynamo = FakeDynamo()
    engine = Engine()
    engine.dynamo = dynamo

    sys.path = ['{}/app/models'.format(target)] + sys.path
    modelModules = glob.glob('{}/app/models'.format(target) + '/*.py')
    models = [ basename(f)[:-3] for f in modelModules if isfile(f)]
    for modelName in models:
        if modelName != '__init__':
            engine.register(getattr(__import__(modelName), modelName))

    engine.create_schema()

@click.command()
def installdb():
    install_path = '{}/dynamo_db'.format(CWD)
    command = ['curl', '-LO', 'http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz']
    subprocess.call(command)
    if os.path.exists(install_path):
        shutil.rmtree(install_path)
    os.mkdir(install_path)
    extract = ['tar', '-xvzf', '{}/dynamodb_local_latest.tar.gz'.format(CWD), '-C', '{}/dynamo_db'.format(CWD)]
    subprocess.call(extract)
    remove_archive = ['rm', '{}/dynamodb_local_latest.tar.gz'.format(CWD)]
    subprocess.call(remove_archive)

@click.command()
def rundb():
    load_env()
    os.environ['AWS_REGION'] = 'us-west-2'
    shared_db = './dynamo_db/shared-local-instance.db'
    if os.path.exists(shared_db):
        os.remove(shared_db)
    dynamo_command = ['java', '-Djava.library.path={}/dynamo_db/DynamoDBLocal_lib'.format(CWD), '-jar', '{}/dynamo_db/DynamoDBLocal.jar'.format(CWD), '-sharedDb', '-dbPath', './dynamo_db']
    try:
        dynamo_process = subprocess.Popen(dynamo_command, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        pass
    try:
        '''
        Connect to DynamoDB and register and create tables for application models.
        '''
        engine = Engine()
        engine.connect(os.environ['AWS_REGION'], host='localhost',
                       port=8000,
                       access_key='anything',
                       secret_key='anything',
                       is_secure=False)
        # load models
        sys.path = ['./app/models'] + sys.path
        modelModules = glob.glob('./app/models' + "/*.py")
        models = [basename(f)[:-3] for f in modelModules if isfile(f)]
        for modelName in models:
            if modelName != '__init__':
                engine.register(getattr(__import__(modelName), modelName))
        engine.create_schema()
        tables = [table for table in engine.dynamo.list_tables()]
        print "This engine has the following tables " + str(tables)
        for table in tables:
            engine.dynamo.describe_table(table)
    except Exception as e:
        # IF anything goes wrong, then we self-destruct.
        dynamo_process.kill()
        raise e
    # Wait for process to finish.
    dynamo_process.wait()


@click.command()
@click.option('--target', default=CWD)
def artifact(*args, **kwargs):
    target = kwargs.pop('target')
    name = get_config(target)['name']
    zip_name = '{}/builds/{}-artifact-{}'.format(target, name, int(time.time()))
    builds_dir = '{}/builds'.format(target)
    if os.path.exists(builds_dir):
        shutil.rmtree(builds_dir)

    os.mkdir(builds_dir)
    os.mkdir('{}/{}-artifact'.format(builds_dir, name))

    directory_list = ['{}/app'.format(target)]
    file_list = ['{}/app_index.py'.format(target), '{}/env.dist.yml'.format(target), '{}/tight.yml'.format(target)]

    create_zip = ['zip', '-9', zip_name]
    subprocess.call(create_zip)
    artifact_dir =  '{}/builds/{}-artifact/'.format(target, name)

    for dir in directory_list:
        cp_dir_command = ['cp', '-R', dir, artifact_dir]
        subprocess.call(cp_dir_command)

    for file_name in file_list:
        cp_file_command = ['cp', file_name, artifact_dir]
        subprocess.call(cp_file_command)

    shutil.make_archive(zip_name, 'zip', root_dir=artifact_dir)


main.add_command(generate)
main.add_command(pip)
main.add_command(dynamo)
pip.add_command(install)
generate.add_command(app)
generate.add_command(function)
generate.add_command(env)
generate.add_command(model)
generate.add_command(artifact)
dynamo.add_command(generateschema)
dynamo.add_command(installdb)
dynamo.add_command(rundb)