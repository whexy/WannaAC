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
        'language': 'Java',
        'probInfo': 'test',
        'content': 'public class Main{public static void main(String[] args){for(;;);}}'
        }

file_type_list = {
        'C++': 'cpp',
        'Java': 'java',
        'Python': 'py'
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
    elif file_name == 'py':
        return ['python3', file_path + file_name + '.py']
    else:
        return []

def get_test_points(data_dir):
    file_list = os.listdir(data_dir)
    in_list = [f[:-3] for f in file_list if isfile(join(data_dir, f)) and f[-3:] == '.in']
    return [join(data_dir, f) for f in in_list if isfile(join(data_dir, f + '.out'))]

def j_compile(file_type, file_path, content):
    with open(file_path + 'Main.' + file_type, 'w') as src_file:
        src_file.write(config_dict['content'])
    compile_result = run(get_compile_cmd(file_type, file_path), stdout=PIPE, stderr=STDOUT)
    if compile_result.returncode != 0:
        return False, compile_result.stdout.decode('utf-8')
    else:
        return True, ''

def j_execute(test, file_type, file_path, timeout):
    if file_type == 'java':
        timeout += 2
    with open(test + '.in', 'r') as testin:
        try:
            stdin = testin.read()
            runtime_result = run(get_exec_cmd(file_type, file_path)), stdin=stdin, stdout=PIPE, stderr=PIPE, timeout=timeout)
            if runtime_result.returncode == 0:
                return 0, stdin, runtime_result.stdout, ''
            else:
                return 1, stdin, '', runtime_result.stderr
        except TimeoutExpired:
            return 2, stdin, '', ''

def basic_diff(text1, text2, *args):
    text1 = '\n'.join(map(lambda s : s.rstrip(), text1.splitlines())).rstrip()
    text2 = '\n'.join(map(lambda s : s.rstrip(), text2.splitlines())).rstrip()
    # NOTE Untested:
    return SequenceMatcher(None, text1, text2).ratio() == 1.0
    # return text1 == text2

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

def judge(config_dict):
    global info_dict
    update_info()

    serial = get_serial()
    response = {'runtimeStatus': 'AC'}
    file_type = file_type_list[config_dict['language']]
    file_path = 'run/%s/' % serial
    problem = config_dict['probInfo']
    data_dir = 'data/%s/' % problem
    timeout = int(info_dict[problem]['timeout'])

    os.mkdir(file_path)
    compile_flag, compile_message = j_compile(file_type, file_path, config_dict['content'])
    if compile_flag:
        test_list = get_test_points(data_dir)
        test_points = len(test_list)
        passed_points = 0
        for test in test_list:
            status, stdin, stdout, stderr = j_execute(test, file_type, file_path, timeout)
            with open(test + '.out', 'r') as testout:
                stdans = testout.read()
                if status == 0:
                    if info_dict[problem]['method'] == 'spj':
                        pass # TODO Special judge
                    else:
                        diff_flag = judge_dict[info_dict[problem]['method']](stdout, stdans, info_dict[problem]['precision'])
                        if diff_flag:
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

    else:
        response['runtimeStatus'] = 'CE'
        response['compileInfo'] = compile_message

    shutil.rmtree(file_path)
    return response

def beat_std(config_dict, cases_num = 20):
    pass # TODO

def beat(config_dict_1, config_dict_2, cases_num = 20):
    pass # TODO

'''

def execute(data_dir, test_file, file_type, file_path, timeout):
    result = {}
    std_file = file_path + 'std.out'
    user_file = file_path + 'user.out'
    with open(test_file, 'r') as testdata, open(std_file, 'w') as std_output:
        run([data_dir + 'std'], stdin=testdata, stdout=std_output, timeout=timeout)
    with open (test_file, 'r') as testdata, open(user_file, 'w') as user_output:
        add_time = 0
        if file_type == 'java':
            add_time = 2
        try:
            runtime = run(get_exec_cmd(file_type, file_path), stdin=testdata, stdout=user_output, timeout=timeout+add_time)
            if runtime.returncode != 0:
                result['runtimeStatus'] = 'RE'
            else:
                diff_status = run(['diff', '-Bbw', std_file, user_file], stdout=PIPE)
                if diff_status.returncode != 0:
                    result['runtimeStatus'] = 'WA'
        except TimeoutExpired:
            result['runtimeStatus'] = 'TLE'
    if result:
        with open(test_file, 'r') as testdata, open(std_file, 'r') as std_output, open(user_file, 'r') as user_output:
            result['testData'] = testdata.read()
            result['expectedOutput'] = std_output.read()
            result['actualOutput'] = user_output.read()
    return result

def save_data(data_dir, data):
    test_no = 1 + len([f for f in os.listdir(data_dir) if isfile(join(data_dir, f)) and f[-3:] == '.in'])
    with open(data_dir + 'data%d.in' % test_no, 'w') as new_test:
        new_test.write(data)

def judge_impl(config_dict, random_points=20):
    # Initialize
    serial = get_serial()
    response = {'runtimeStatus': 'AC'}
    file_type = file_type_list[config_dict['language']]
    file_path = 'run/%s/' % serial
    file_name = 'Main.' + file_type
    data_dir = 'data/%s/' % config_dict['probInfo']
    test_points = 0
    passed_points = 0
    timeout = 1
    with open('info.json', 'r') as f_info:
        timeout = int(json.loads(f_info.read())[config_dict['probInfo']]['timeout'])

    # Compile
    os.mkdir(file_path)
    with open(file_path + file_name, 'w') as src_file:
        src_file.write(config_dict['content'])
    compile_status = run(get_compile_cmd(file_type, file_path), stdout=PIPE, stderr=STDOUT)
    if compile_status.returncode != 0:
        response['runtimeStatus'] = 'CE'
        response['compileInfo'] = compile_status.stdout.decode('utf-8')
        return response

    # Saved data
    test_files = [f for f in os.listdir(data_dir) if isfile(join(data_dir, f)) and f[-3:] == '.in']
    test_files_cnt = len(test_files)
    test_points = test_files_cnt
    for test_file in test_files:
        result = execute(data_dir, join(data_dir, test_file), file_type, file_path, timeout)
        if result:
            response.update(result)
            break
        passed_points += 1

    # Random data
    if passed_points == test_points and isfile(data_dir + 'data.py'):
        test_points += random_points
        for i in range(random_points):
            test_file = file_path + 'test.in'
            with open(test_file, 'w') as testdata:
                run(['python3', data_dir + 'data.py'], stdout=testdata)
            result = execute(data_dir, test_file, file_type, file_path, timeout)
            if result:
                response.update(result)
                save_data(data_dir, result['testData'])
                break
            passed_points += 1

    # Return
    response['passedRatioPercent'] = passed_points * 100 // test_points
    return response

def judge(config_dict, random_points=20):
    try:
        return judge_impl(config_dict, random_points, False)
    except:
        return {'runtimeStatus': 'UE'}
        # raise

'''

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
    pass
    # print(judge_impl(test_config))
    # print(get_prob_list())
    # print(save_new_data({'probInfo': 'test', 'in': '1 3', 'out': '4'}))
    # print(save_new_data({'probInfo': 'test', 'in': '1 3', 'out': 'Hello'}))
