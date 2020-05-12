import os
import argparse
from subprocess import run
from .one_pass_auth import OnePassAuth
from .one_pass import OnePass
from .one_pass_parser.one_pass_parser_factory import OnePassParserFactory


def exec(profile, execute, op_obj_dict):
    if profile is None:
        raise Exception('argument profile should not be none')
    if execute is None:
        raise Exception('argument --execute should not be none')

    OnePassAuth(profile)
    if op_obj_dict:
        for op_type, op_objects_list in op_obj_dict.items():
            for op_object in op_objects_list:
                response = getattr(OnePass(), f'get_{op_type}')(op_object)
                op_parser = OnePassParserFactory(op_type).build_parser()
                parsed_response = op_parser.parse_response(response)
                spawn_parsed_response(
                    parsed_response=parsed_response,
                    op_object=op_object
                )
    run(execute)


def one_pass_vault():
    parser = argparse.ArgumentParser(description='One Pass Vault')
    parser.add_argument('job_option', help='options: exec', nargs=1)
    parser.add_argument('profile', help="The profile you want to use", nargs=1)
    parser.add_argument('--item', '-i')
    parser.add_argument('execute', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.item:
        op_obj_dict = {'item': args.item.split(',')}
    else:
        op_obj_dict = None

    if args.job_option[0] == 'exec':
        exec(
            profile=args.profile[0],
            execute=args.execute,
            op_obj_dict=op_obj_dict
        )
    else:
        raise Exception('Invalid job_option, should be: exec')


def spawn_parsed_response(parsed_response, op_object):
    object_name = op_object
    for key, value in parsed_response.items():
        os.environ[f'{object_name}_{key}'] = value
