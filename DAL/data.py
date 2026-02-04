from typing import Any, Literal, Iterable
from os.path import isfile


def load_data(file_path: str) -> dict:
    func_res = {'success': None, 'err_msg': {}, 'success_msg': {}, 'returndata': None}

    if not isfile(file_path):

        try:
            file_object = open(file=file_path, mode='x')

        except BaseException as err:
            func_res['success'] = False
            func_res['returndata'] = err
            return func_res

        else:
            func_res['success'] = True
            func_res['returndata'] = []
            return func_res

        finally:
            if 'file_object' in locals() and (not file_object.closed):
                file_object.close()

    try:
        file_object = open(file=file_path)
        res = file_object.readlines()

    except BaseException as err:
        func_res['success'] = False
        func_res['returndata'] = err
        return func_res

    else:
        func_res['success'] = True
        func_res['returndata'] = res
        return func_res

    finally:
        if 'file_object' in locals() and (not file_object.closed):
            file_object.close()


def save_data(data: str, file_path: str, mode: Literal['a', 'w'] = 'a') -> Literal[True] | BaseException:
    func_res = {'success': None, 'err_msg': {}, 'success_msg': {}, 'returndata': None}

    try:
        file_object = open(file=file_path, mode=mode)
        file_object.write(data)

    except BaseException as err:
        func_res['success'] = False
        func_res['returndata'] = err
        return func_res
    else:
        func_res['success'] = True
        return func_res
    finally:
        if 'file_object' in locals() and (not file_object.closed):
            file_object.close()


def save_data_list(data: Iterable[str], file_path: str, mode: Literal['a', 'w'] = 'a') -> Literal[True] | BaseException:
    func_res = {'success': None, 'err_msg': {}, 'success_msg': {}, 'returndata': None}

    try:
        file_object = open(file=file_path, mode=mode)
        file_object.writelines(data)

    except BaseException as err:
        func_res['success'] = False
        func_res['returndata'] = err
        return func_res

    else:
        func_res['success'] = True
        return func_res

    finally:
        if 'file_object' in locals() and (not file_object.closed):
            file_object.close()