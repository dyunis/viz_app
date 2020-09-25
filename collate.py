import json
import os.path as osp
import sys

def collate(paths):
    for p in paths:
        assert osp.exists(p)

    collated = {}
    for p in paths:

        if osp.isdir(p):
            prefix = osp.basename(p)
            with open(osp.join(p, 'stats.json'), 'r') as f: 
                json_dict = json.load(f)
        elif osp.isfile(p):
            prefix = osp.basename(osp.dirname(p))
            with open(p, 'r') as f:
                json_dict = json.load(f)

        for key in json_dict.keys():
            if key != 'step':
                collated[f'{prefix}_{key}'] = json_dict[key]
            else:
                collated['step'] = json_dict[key]

    with open('data/data.json', 'w') as f:
        json.dump(collated, f)

    return collated

if __name__=='__main__':
    assert len(sys.argv) > 0
    collate(sys.argv[1:])
