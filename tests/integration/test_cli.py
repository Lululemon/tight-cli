# Copyright (c) 2016 Michael Orion McManus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml
import pytest
import click
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
    generate_function_result = runner.invoke(cli.function, ['my_controller', '--target={}'.format(app_root)])
    assert generate_function_result.output == u'Usage: function [OPTIONS] NAME\n\nError: Invalid value for NAME: Function already exists!\n'


def test_generate_model_and_schema(tmpdir):
    here = os.path.dirname(os.path.realpath(__file__))
    runner = CliRunner()
    app_dir = 'my_service'
    target = '{}/{}/app/models'.format(tmpdir, app_dir)
    runner.invoke(cli.app, [app_dir, '--target={}'.format(tmpdir)])
    runner.invoke(cli.env, ['--target={}/{}'.format(tmpdir, app_dir)])
    runner.invoke(cli.model, ['my_model', '--target={}'.format(target)])
    model_location = '{}/MyModel.py'.format(target)
    assert os.path.isfile(model_location)
    runner.invoke(cli.generateschema, ['--target={}/{}'.format(tmpdir, app_dir)])
    with open('{}/../fixtures/my-models.yml'.format(here)) as yaml_fixture:
        yaml_fixture_dict = yaml.load(yaml_fixture)
    with open('{}/{}/schemas/dynamo/my-models.yml'.format(tmpdir, app_dir)) as result_yaml:
        result_yaml_dict = yaml.load(result_yaml)
    assert yaml_fixture_dict == result_yaml_dict, 'Correct schema generated for model.'


def test_generate_artifact(tmpdir):
    runner = CliRunner()
    app_dir_name = 'my_service'
    app_dir_path = '{}/{}'.format(tmpdir, app_dir_name)
    runner.invoke(cli.app, [app_dir_name, '--target={}'.format(tmpdir)])
    runner.invoke(cli.artifact, ['--target={}/{}'.format(tmpdir, app_dir_name)])
    builds_dir_path = '{}/builds'.format(app_dir_path)
    service_artifact_path = '{}/{}'.format(builds_dir_path, 'my-service-artifact')
    app_artifact_path = '{}/app'.format(service_artifact_path)
    assert os.path.isdir(builds_dir_path), './builds dir created'
    assert os.path.isdir(service_artifact_path), './builds/artifact dir created'
    assert os.path.isdir(app_artifact_path), './builds/artifact/app dir copied'
    assert os.listdir(service_artifact_path) == ['app', 'app_index.py', 'env.dist.yml', 'tight.yml']
    assert os.listdir(app_artifact_path) == ['__init__.py', 'functions', 'lib', 'models', 'serializers', 'vendored']

def test_pip_install_requirements(tmpdir, monkeypatch):
    runner = CliRunner()
    app_dir_name = 'my_service'
    app_dir_path = '{}/{}'.format(tmpdir, app_dir_name)
    def mock_run_command(*args, **kwargs):
        pass
    monkeypatch.setattr(cli, 'run_command', mock_run_command)
    runner.invoke(cli.app, [app_dir_name, '--target={}'.format(tmpdir)])
    runner.invoke(cli.install, ['--requirements', '--target={}'.format(app_dir_path)])


def test_pip_install_package(tmpdir, monkeypatch):
    runner = CliRunner()
    app_dir_name = 'my_service'
    app_dir_path = '{}/{}'.format(tmpdir, app_dir_name)
    def mock_run_command(*args, **kwargs):
        pass
    monkeypatch.setattr(cli, 'run_command', mock_run_command)
    app_result = runner.invoke(cli.app, [app_dir_name, '--target={}'.format(tmpdir)])
    assert app_result.exit_code == 0, 'App created successfully.'
    install_result = runner.invoke(cli.install, ['PyYAML', '--target={}'.format(app_dir_path)])
    assert install_result.exit_code == 0, 'Install package command ran successfully.'
    with open('{}/requirements-vendor.txt'.format(app_dir_path)) as requirements_file:
        contents = requirements_file.read()
        assert contents.split('\n')[-1] == 'PyYAML', 'Package added to requirements file.'
