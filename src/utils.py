

def get_model_fun(model, train):
    import sys
    sys.path.insert(0, get_top_level_path())
    if model == 'iwge':
        if train:
            from IWGE.src.train import train
            return train
        else:
            from IWGE.src.test import test
            return test
    else:
        raise RuntimeError('Not recognized model %s' % model)

def get_data(data, train):
    if data == 'syn':
        from data import SynData
        return SynData(train)
    else:
        raise RuntimeError('Not recognized data %s' % data)

def get_top_level_path():
    import os
    return os.path.dirname(os.path.abspath(__file__)) + '/../'