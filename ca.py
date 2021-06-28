#!/usr/bin/env python3
import sys
import os
import getopt
import yaml

BASE_CMD = os.path.basename(sys.argv[0])

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
CA_DIR = os.path.join(BASE_DIR, 'ca')
ROOT_DIR = os.path.join(CA_DIR, 'root')
CFG_DIR = os.path.join(CA_DIR, 'cfg')
KEY_DIR = os.path.join(CA_DIR, 'key')
REQ_DIR = os.path.join(CA_DIR, 'req')
CRT_DIR = os.path.join(CA_DIR, 'crt')

KEY_EXT = '.key'
REQ_EXT = '.csr'
CRT_EXT = '.crt'

ROOT_KEY = os.path.join(ROOT_DIR, 'ca' + KEY_EXT)
ROOT_CRT = os.path.join(ROOT_DIR, 'ca' + CRT_EXT)

SUBJ_CFG = os.path.join(CFG_DIR, 'subj.yaml')

def usage(command = ''):
    print('USAGE')

    if command == '':
        print('  ' + BASE_CMD + ' help')
    else:
        print('  ' + BASE_CMD + ' ' + command + ' help')

    if command == '':
        print('  ' + BASE_CMD + ' <COMMAND> help')
        print('  ' + BASE_CMD + ' <COMMAND> <SUBCOMMAND> help')
        print('')
        print('COMMANDS')
        print('  init            Generate root key and root certificate')
        print('  key             Manage private keys')
        print('  request         Manage certificate requests')
        print('  certificate     Manage certificates')
    elif command == 'init':
        print('  ' + BASE_CMD + ' ' + command +  ' [OPTIONS] <country> <state> <city> <organization>')
        print('')
        print('OPTIONS')
        print('  -f, --force     Force initialize')
        print('  -d, --days      Valid for number of days (default: 36500)')
        print('')
        print('ARGUMENTS')
        print('  country         Uppercase two letter country code')
        print('  state           The state, either as string or short')
        print('  city            City of origin')
        print('  organization    Name of the CA')
    elif command == 'key':
        print('  ' + BASE_CMD + ' ' + command + ' <COMMAND> help')
        print('')
        print('COMMANDS')
        print('  list            List all keys')
        print('  create          Create a new key')
        print('  delete          Delete existing key')
    elif command == 'key create':
        print('  ' + BASE_CMD + ' ' + command + ' [OPTIONS] <domain>')
        print('')
        print('OPTIONS')
        print('  -f, --force     Overwrite existing files')
        print('  -l, --length    Key length (default: 2048)')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')
    elif command == 'key delete':
        print('  ' + BASE_CMD + ' ' + command + ' <domain>')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')
    elif command == 'request':
        print('  ' + BASE_CMD + ' ' + command + ' <COMMAND>')
        print('')
        print('COMMANDS')
        print('  list            List all request')
        print('  create          Create a new request')
        print('  delete          Delete existing request')
    elif command == 'request create':
        print('  ' + BASE_CMD + ' ' + command + ' [OPTIONS] <domain>')
        print('')
        print('OPTIONS')
        print('  -f, --force     Overwrite existing files')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')
    elif command == 'request delete':
        print('  ' + BASE_CMD + ' ' + command + ' <domain>')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')
    elif command == 'certificate':
        print('  ' + BASE_CMD + ' ' + command + ' <COMMAND> help')
        print('')
        print('COMMANDS')
        print('  list            List all certificates')
        print('  create          Create a new certificate')
        # print('  revoke          Revoke existing certificate')
        print('  delete          Delete existing certificate')
    elif command == 'certificate create':
        print('  ' + BASE_CMD + ' ' + command + ' [OPTIONS] <domain>')
        print('')
        print('OPTIONS')
        print('  -f, --force     Overwrite existing files')
        print('  -d, --days      Valid for number of days (default: 730)')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')
    elif command == 'certificate revoke':
        print('  ' + BASE_CMD + ' ' + command + ' <domain>')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')
    elif command == 'certificate delete':
        print('  ' + BASE_CMD + ' ' + command + ' <domain>')
        print('')
        print('OPTIONS')
        print('  -a, --all       Delete key and request as well')
        print('  -k, --key       Delete key as well')
        print('  -r, --request   Delete request as well')
        print('')
        print('ARGUMENTS')
        print('  domain          Domain name')

def init(args):
    if len(args) and args[0] == 'help':
        usage('init')
        return 0

    opts, args = getopt.getopt(args, 'fd:', ['force', 'days='])

    force = False
    days = 36500 # 100 years

    for k,v in opts:
        if k == '-f' or k == '--force':
            force = True
        elif k == '-d' or k == '--days':
            days = int(v)

    if len(args) < 3:
        print('\033[31mError: Required argument missing!\033[39m')
        print('')
        usage('init')
        return 1

    country = args[0]
    state = args[1]
    city = args[2]
    organization = args[3]

    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)

    if not os.path.exists(CFG_DIR):
        os.makedirs(CFG_DIR)

    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

    if not os.path.exists(REQ_DIR):
        os.makedirs(REQ_DIR)

    if not os.path.exists(CRT_DIR):
        os.makedirs(CRT_DIR)

    if os.path.exists(ROOT_KEY) and not force:
        print('\033[31mError: Root key already exists! Use --force to overwrite it.\033[39m')
        return 1

    with open(SUBJ_CFG, 'w') as file:
        subj = yaml.dump({'country': country, 'state': state, 'city': city, 'organization': organization}, file)

    os.system('openssl genrsa -out "' + ROOT_KEY + '" 4096')
    os.system('openssl req -x509 -new -nodes -key "' + ROOT_KEY + '" -sha512 -days ' + str(days) + ' -out "' + ROOT_CRT + '" -subj "/C=' + country + '/ST=' + state + '/L=' + city + '/O=' + organization + '"')

    return 0

def key_list(args):
    print('KEYS')
    for key in os.listdir(KEY_DIR):
        print('  ' + key.replace(KEY_EXT, ''))
    return 0

def key_create(args):
    opts, args = getopt.getopt(args, 'l:', ['length='])

    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('key create')
        return 0

    force = False
    domain = args[0]
    length = 2048

    for k,v in opts:
        if k == '-f' or k == '--force':
            force = True
        if k == '-l' or k == '--length':
            length = int(v)

    key_file = os.path.join(KEY_DIR, domain + KEY_EXT)

    if os.path.exists(key_file) and not force:
        print('\033[31mError: Key file already exists! Use --force to overwrite it.\033[39m')
        print('')
        usage('key create')
        return 1

    os.system('openssl genrsa -out "' + key_file + '" ' + str(length))
    return 0

def key_delete(args):
    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('key delete')
        return 0

    domain = args[0]

    try:
        os.remove(os.path.join(KEY_DIR, domain + KEY_EXT))
    except FileNotFoundError:
        print('\033[31mError: Key not found!\033[39m')
        print('')
        usage('key delete')
        return 1
    return 0

def key(args):
    if not len(args) or args[0] == 'help':
        usage('key')
        return 0
    elif args[0] == 'list':
        return key_list(args[1:])
    elif args[0] == 'create':
        return key_create(args[1:])
    elif args[0] == 'delete':
        return key_delete(args[1:])
    return 0

def request_list(args):
    print('REQUESTS')
    for req in os.listdir(REQ_DIR):
        print('  ' + req.replace(REQ_EXT, ''))
    return 0

def request_create(args):
    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('request create')
        return 0

    opts, args = getopt.getopt(args, 'f', ['force'])

    force = False
    domain = args[0]
    key_file = os.path.join(KEY_DIR, domain + KEY_EXT)
    req_file = os.path.join(REQ_DIR, domain + REQ_EXT)

    for k,v in opts:
        if k == '-f' or k == '--force':
            force = True

    if os.path.exists(req_file) and not force:
        print('\033[31mError: Request file already exists! Use --force to overwrite it.\033[39m')
        print('')
        usage('request create')
        return 1

    if not os.path.exists(key_file):
        os.system('openssl genrsa -out "' + key_file + '" 2048')

    with open(SUBJ_CFG, 'r') as file:
        subj = yaml.full_load(file)
        os.system('openssl req -new -sha512 -key "' + key_file + '" -subj "/C=' + subj['country'] + '/ST=' + subj['state'] + '/L=' + subj['city'] + '/O=' + subj['organization'] + '/CN=' + domain + '" -out ' + req_file)

    return 0

def request_delete(args):
    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('request delete')
        return 0

    domain = args[0]

    try:
        os.remove(os.path.join(REQ_DIR, domain + REQ_EXT))
    except FileNotFoundError:
        print('\033[31mError: Request not found!\033[39m')
        print('')
        usage('request delete')
        return 1

    return 0

def request(args):
    if not len(args) or args[0] == 'help':
        usage('request')
        return 0
    elif args[0] == 'list':
        return request_list(args[1:])
    elif args[0] == 'create':
        return request_create(args[1:])
    elif args[0] == 'delete':
        return request_delete(args[1:])
    return 0

def certificate_list(args):
    print('CERTIFICATES')
    for crt in os.listdir(CRT_DIR):
        print('  ' + crt.replace(CRT_EXT, ''))
    return 0

def certificate_create(args):
    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('certificate create')
        return 0

    opts, args = getopt.getopt(args, 'fd:', ['force', 'days'])

    force = False
    days = 730

    domain = args[0]

    key_file = os.path.join(KEY_DIR, domain + KEY_EXT)
    req_file = os.path.join(REQ_DIR, domain + REQ_EXT)
    crt_file = os.path.join(CRT_DIR, domain + CRT_EXT)

    for k,v in opts:
        if k == '-f' or k == '--force':
            force = True
        if k == '-d' or k == '--days':
            days = int(v)

    if os.path.exists(crt_file) and not force:
        print('\033[31mError: Request file already exists! Use --force to overwrite it.\033[39m')
        print('')
        usage('request create')
        return 1

    if not os.path.exists(key_file):
        os.system('openssl genrsa -out "' + key_file + '" 2048')

    if not os.path.exists(req_file):
        with open(SUBJ_CFG, 'r') as file:
            subj = yaml.full_load(file)
            os.system('openssl req -new -sha512 -key "' + key_file + '" -subj "/C=' + subj['country'] + '/ST=' + subj['state'] + '/L=' + subj['city'] + '/O=' + subj['organization'] + '/CN=' + domain + '" -out ' + req_file)

    os.system('openssl x509 -req -sha512 -in "' + req_file + '" -CA "' + ROOT_CRT + '" -CAkey "' + ROOT_KEY + '" -CAcreateserial -days ' + str(days) + ' -out "' + crt_file + '" -extfile <(printf "subjectAltName=DNS:' + domain + '")')

    return 0

def certificate_revoke(args):
    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('certificate revoke')
        return 0
        # TODO: Implement
    return 0

def certificate_delete(args):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        return 2

    if not len(args) or args[0] == 'help':
        if not len(args):
            print('\033[31mError: Required argument missing!\033[39m')
            print('')
        usage('certificate delete')
        return 0

    domain = args[0]

    delete_key = False
    delete_request = False

    for k,v in opts:
        if k == '-a' or k == '--all':
            delete_key = True
            delete_request = True
        if k == '-k' or k == '--key':
            delete_key = True
        if k == '-r' or k == '--request':
            delete_request = True

        if delete_key:
            os.system('rm "' + os.path.join(KEY_DIR, domain + KEY_EXT) + '"')
        if delete_request:
            os.system('rm "' + os.path.join(REQ_DIR, domain + REQ_EXT) + '"')
        os.system('rm "' + os.path.join(CRT_DIR, domain + CRT_EXT) + '"')

    return 0

def certificate(args):
    if not len(args) or args[0] == 'help':
        usage('certificate')
        return 0
    elif args[0] == 'list':
        return certificate_list(args[1:])
    elif args[0] == 'create':
        return certificate_create(args[1:])
    # elif args[0] == 'revoke':
    #     return certificate_revoke(args[1:])
    elif args[0] == 'delete':
        return certificate_delete(args[1:])
    return 0

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        return 2

    if not len(args) or args[0] == 'help':
        usage()
        return 0
    elif args[0] == 'init':
        return init(args[1:])

    if not os.path.exists(SUBJ_CFG):
        print('\033[31mError: CA not yet initialized!\033[39m')
        print('')
        usage()
        return 1

    if args[0] == 'key':
        return key(args[1:])
    elif args[0] == 'request':
        return request(args[1:])
    elif args[0] == 'certificate':
        return certificate(args[1:])

if __name__ == '__main__':
    sys.exit(main())