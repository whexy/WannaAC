#!/usr/bin/python3

import os
from os.path import isfile, join
import json
from subprocess import run, PIPE, TimeoutExpired, STDOUT
import time
import sys
import shutil
from difflib import SequenceMatcher

test_config = {
        'language': 'java',
        'probInfo': 'test',
        'content': 'public class Main{public static void main(String[] args){for(;;);}}'
        }

test_config_2 = {
        'language': 'c++',
        'probInfo': 'test',
        'content': '#include <iostream>\n int main() { int a, b; std::cin >> a >> b; std::cout << a + b; return 0; }'
        }

beat_test_config = {
        'probInfo': 'test',
        'language': ['java', 'c++'],
        'content': [ '''
            import java.util.Scanner; 
            public class Main { 
                public static void main(String[] args) {
                    Scanner sc = new Scanner(System.in); 
                    int a = sc.nextInt(); 
                    System.out.println(a+sc.nextInt());
                }
            }
            ''',
            '''#include <iostream>
            int main() { 
                int a, b; 
                std::cin >> a >> b; 
                std::cout << a + b; 
                return 0; 
            }
            ''' ]
        }

file_type_list = {
        'c++': 'cpp',
        'java': 'java',
        'python': 'py'
        }

info_dict = {}

def update_info():
    global info_dict
    with open('info.json', 'r') as f_info:
        info_dict = json.load(f_info)

def get_serial():
    return str(int(time.time() * 1000))

def get_compile_cmd(file_type, file_path):
    if file_path[-1] != '/':
        file_path += '/'
    if file_type == 'cpp':
        return ['g++', file_path + 'Main.cpp', '-o', file_path + 'Main', '-std=c++14', '-lm']
    elif file_type == 'java':
        return ['javac', file_path + 'Main.java']
    else:
        return []

def get_exec_cmd(file_type, file_path, file_name = 'Main'):
    if file_path[-1] != '/':
        file_path += '/'
    if file_type == 'cpp':
        return [file_path + file_name]
    elif file_type == 'java':
        return ['java', '-cp', file_path, file_name]
    elif file_type == 'py':
        return ['python3', file_path + file_name + '.py']
    else:
        return []

def get_test_points(data_dir):
    file_list = os.listdir(data_dir)
    in_list = [f[:-3] for f in file_list if isfile(join(data_dir, f)) and f[-3:] == '.in']
    return [join(data_dir, f) for f in in_list if isfile(join(data_dir, f + '.out'))]

def j_compile(file_type, file_path, content):
    with open(file_path + 'Main.' + file_type, 'w') as src_file:
        src_file.write(content)
    compile_result = run(get_compile_cmd(file_type, file_path), stdout=PIPE, stderr=STDOUT)
    if compile_result.returncode != 0:
        return False, compile_result.stdout.decode('utf-8')
    else:
        return True, ''

def j_execute(file_type, file_path, stdin, timeout):
    if file_type == 'java':
        timeout += 2
    try:
        runtime_result = run(get_exec_cmd(file_type, file_path), input=stdin, stdout=PIPE, timeout=timeout)
        if runtime_result.returncode == 0:
            return 0, runtime_result.stdout.decode('utf-8')
        else:
            return 1, ''
    except TimeoutExpired:
        return 2, ''

def basic_diff(text1, text2, *args):
    text1 = '\n'.join(map(lambda s : s.rstrip(), text1.splitlines())).rstrip()
    text2 = '\n'.join(map(lambda s : s.rstrip(), text2.splitlines())).rstrip()
    # NOTE Untested:
    return SequenceMatcher(None, text1, text2).ratio() == 1.0
    # return text1 == text2

# NOTE Untested:
def real_diff(text1, text2, precision):
    seq1 = list(map(float, text1.split()))
    seq2 = list(map(float, text2.split()))
    if len(seq1) != len(seq2):
        return False
    else:
        n = len(seq1)
        for i in range(n):
            if abs(seq1[i] - seq2[i]) > precision:
                return False
        return True

judge_dict = {
        'diff': basic_diff,
        'real': real_diff,
        'spj': None
        }

def judge_impl(config_dict, file_path):
    response = {'runtimeStatus': 'AC'}
    file_type = file_type_list[config_dict['language']]
    problem = config_dict['probInfo']
    data_dir = 'data/%s/' % problem
    timeout = int(info_dict[problem]['timeout'])

    compile_flag, compile_message = j_compile(file_type, file_path, config_dict['content'])
    if not compile_flag:
        response['runtimeStatus'] = 'CE'
        response['compileInfo'] = compile_message
        return response

    test_list = get_test_points(data_dir)
    test_points = len(test_list)
    passed_points = 0
    for test in test_list:
        stdin = ''
        with open(test + '.in', 'r') as testin:
            stdin = testin.read()
        status, stdout = j_execute(file_type, file_path, stdin.encode('utf-8'), timeout)
        with open(test + '.out', 'r') as testout:
            stdans = testout.read()
            if status == 0:
                if info_dict[problem]['method'] == 'spj':
                    pass # TODO Special judge
                else:
                    if judge_dict[info_dict[problem]['method']](stdout, stdans, info_dict[problem]['precision']):
                        passed_points += 1
                    else:
                        response['runtimeStatus'] = 'WA'
                        response['expectedOutput'] = stdans
                        response['actualOutput'] = stdout
            else:
                if status == 1:
                    response['runtimeStatus'] = 'RE'
                else:
                    response['runtimeStatus'] = 'TLE'
                response['testData'] = stdin
                response['expectedOutput'] = stdans
                response['actualOutput'] = ''
                break
    response['passedRatioPercent'] = passed_points * 100 // test_points
    return response

def check_data(data_dir, data_type):
    data = data_dir + 'Data'
    if data_type == 'java':
        data += '.class'
    elif data_type == 'py':
        data += '.py'
    if isfile(data):
        return True
    else:
        return False

def beat_impl(config_dict, file_path, cases_num):
    response = {'runtimeStatus': ['N/A', 'N/A']}
    problem = config_dict['probInfo']
    data_dir = 'data/%s/' % problem
    timeout = int(info_dict[problem]['timeout'])
    file_type = list(map(lambda f : file_type_list[f], config_dict['language']))
    data_type = file_type_list[info_dict[problem]['data_type']]
    if not check_data(data_dir, data_type):
        response['errorMessage'] = 'Data generator not found!'
        return response

    os.mkdir(file_path + '0/')
    os.mkdir(file_path + '1/')
    compile_flag_0, compile_message_0 = j_compile(file_type[0], file_path + '0/', config_dict['content'][0])
    compile_flag_1, compile_message_1 = j_compile(file_type[1], file_path + '1/', config_dict['content'][1])
    compile_messages = ['', '']
    if not compile_flag_0:
        response['runtimeStatus'][0] == 'CE'
        compile_messages[0] = compile_message_0
    if not compile_flag_1:
        response['runtimeStatus'][1] == 'CE'
        compile_messages[1] = compile_message_1

    if compile_flag_0 and compile_flag_1:
        for i in range(cases_num):
            test_data = run(get_exec_cmd(data_type, data_dir, 'Data'), stdout=PIPE).stdout
            status_0, stdout_0 = j_execute(file_type[0], file_path + '0/', test_data, timeout)
            status_1, stdout_1 = j_execute(file_type[1], file_path + '1/', test_data, timeout)
            if status_0 == 0 and status_1 == 0:
                if not judge_dict[info_dict[problem]['method']](stdout_0, stdout_1, info_dict[problem]['precision']):
                    response['runtimeStatus'] = ['DIFF', 'DIFF']
                    response['testData'] = stdin
                    response['outputs'] = [stdout_0, stdout_1]
                    break
            else:
                if status_0 == 1:
                    response['runtimeStatus'][0] = 'RE'
                elif status_0 == 2:
                    response['runtimeStatus'][0] = 'TLE'
                if status_1 == 1:
                    response['runtimeStatus'][1] = 'RE'
                elif status_1 == 2:
                    response['runtimeStatus'][1] = 'TLE'
                break

    if response['runtimeStatus'] == ['N/A', 'N/A']:
        response['runtimeStatus'] = ['IDT', 'IDT']
    return response

def judge(config_dict):
    global info_dict
    update_info()

    serial = get_serial()
    file_path = 'run/%s/' % serial
    os.mkdir(file_path)
    response = {}
    try:
        return judge_impl(config_dict, file_path)
    except:
        return {'runtimeStatus': 'UE'}
    finally:
        shutil.rmtree(file_path)

def beat_std(config_dict, cases_num = 20):
    pass # TODO

def beat(config_dict, cases_num = 20):
    global info_dict
    update_info()

    serial = get_serial()
    file_path = 'run/%s/' % serial
    os.mkdir(file_path)
    response = {}
    try:
        return beat_impl(config_dict, file_path, cases_num)
    # except:
        # return {'runtimeStatus': ['UE', 'UE']}
    finally:
        shutil.rmtree(file_path)

def get_prob_list():
    try:
        with open('info.json', 'r') as info:
            raw_info = json.loads(info.read())
            prob_list = []
            for key, val in raw_info.items():
                prob_list.append({'value': key, 'label': val['title']})
            return prob_list
    except:
        return []

def save_new_data(new_data):
    data_dir = 'data/%s/' % new_data['probInfo']
    test_in = new_data['in']
    if '"' in test_in or "'" in test_in:
        return {'testStatus': 'Rejected'}
    timeout = 1
    with open('info.json', 'r') as info:
        timeout = int(json.loads(info.read())[new_data['probInfo']]['timeout'])
    r = run([data_dir + 'std'], input=test_in, encoding='ascii', stdout=PIPE, timeout=timeout)
    test_out = r.stdout
    check = run(['bash', '-c', 'diff -Bbwsq <(echo -e "%s") <(echo -e "%s")' % (test_out, new_data['out'])], stdout=PIPE)
    if check.returncode == 0:
        save_data(data_dir, new_data['in'])
        return {'testStatus': 'Accepted'}
    return {'testStatus': 'Rejected'}

if __name__ == '__main__':
    print(beat(beat_test_config))
