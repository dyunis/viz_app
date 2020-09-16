import json
import os.path as osp
import sys

def collate(dirs):
    for d in dirs:
        assert osp.exists(d)

    collated = {}
    for d in dirs:
        with open(osp.join(d, 'stats.json'), 'r') as f: 
            json_dict = json.load(f)

            for key in json_dict.keys():
                if key != 'step':
                    collated[f'{osp.basename(d)}_{key}'] = json_dict[key]
                else:
                    collated['step'] = json_dict[key]

    with open('data.json', 'w') as f:
        json.dump(collated, f)

if __name__=='__main__':
    assert len(sys.argv) > 0
    collate(sys.argv[1:])
