import click
import os
from click.testing import CliRunner
from tight_cli import cli

def test_generate_app_verify_structure(tmpdir):
    runner = CliRunner()
    result = runner.invoke(cli.app, ['my_service', '--target={}'.format(tmpdir)])
    app_root = '{}/{}'.format(tmpdir, 'my_service')
    assert os.path.isdir(app_root), 'Directory was created with correct name.'
    # Verify top level structure
    dirs = ['app', 'tests', 'schemas']
    for dir in dirs:
        assert os.path.isdir('{}/{}'.format(app_root, dir)), '{} directory exists'.format(dir)

    files = ['.gitignore', 'app_index.py', 'conftest.py', 'env.dist.yml', 'requirements.txt', 'requirements-vendor.txt', 'tight.yml']
    for file in files:
        assert os.path.isfile('{}/{}'.format(app_root, file)), '{} file exists'.format(file)

def test_generate_function_verify_structure(tmpdir):
    runner = CliRunner()
    """ generate app """
    runner.invoke(cli.app, ['my_service', '--target={}'.format(tmpdir)])
    app_root = '{}/{}'.format(tmpdir, 'my_service')
    """ generate function """
    generate_function_result = runner.invoke(cli.function, ['my_controller', '--target={}'.format(app_root)])
    assert generate_function_result.exit_code == 0
    function_root = '{}/app/functions/my_controller'.format(app_root)
    """ function structure """
    assert os.path.isdir(function_root)
    assert os.path.isfile('{}/handler.py'.format(function_root))
    assert os.path.isfile('{}/__init__.py'.format(function_root))
    """ tests structure """
    function_integration_test_root = '{}/tests/functions/integration/my_controller'.format(app_root)
    function_unit_test_root = '{}/tests/functions/unit/my_controller'.format(app_root)
    assert os.path.isdir(function_integration_test_root), 'Integration test directory exists'
    assert os.path.isdir('{}/placebos'.format(function_integration_test_root)), 'Integration test expectations directory exists'
    assert os.path.isdir('{}/expectations'.format(function_integration_test_root)), 'Integration test placebos directory exists'
    assert os.path.isdir(function_unit_test_root)
    assert os.path.isfile('{}/test_integration_my_controller.py'.format(function_integration_test_root))
    assert os.path.isfile('{}/test_unit_my_controller.py'.format(function_unit_test_root))



