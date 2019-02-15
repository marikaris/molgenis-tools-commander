from mcmd import arguments as arg_parser
from mcmd import io
from mcmd.config.home import get_scripts_folder
from mcmd.executor import execute

# =========
# Arguments
# =========
from mcmd.utils.utils import McmdError


def arguments(subparsers):
    p_run = subparsers.add_parser('run',
                                  help='Run an mcmd script')
    p_run.set_defaults(write_to_history=False)
    p_run.add_argument('script',
                       type=str,
                       help='The .mcmd script to run')
    p_run.add_argument('--ignore-errors', '-i',
                       action='store_true',
                       help='Let the script continue when one or more commands throw an error')


# =======
# Methods
# =======

def run(args):
    script = get_scripts_folder().joinpath(args.script)
    lines = _read_script(script)
    _run_script(not args.ignore_errors, lines)


def _run_script(exit_on_error, lines):
    for line in lines:
        if _is_comment(line) or _is_empty(line):
            continue

        _run_command(exit_on_error, line)


def _run_command(exit_on_error, line):
    sub_args = arg_parser.parse_args(line.split(' '))
    setattr(sub_args, 'arg_string', line)
    if sub_args.command == 'run':
        io.error("Can't use the run command in a script: %s" % line)
        if exit_on_error:
            exit(1)
        else:
            return

    execute(sub_args, exit_on_error)


def _read_script(script):
    try:
        with open(script) as file:
            lines = [line.rstrip('\n') for line in file]
    except OSError as e:
        raise McmdError('Error reading script: {}'.format(str(e)))
    return lines


def _is_comment(line):
    return line.strip().startswith('#')


def _is_empty(line):
    return line.isspace() or len(line) == 0
