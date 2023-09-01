<!-- cheminformatics, computationsl drug design, machine learning, programming, blog, blog posts, samuel homberg, academia, research, Münster, graphgym, pytorch-geometric, gnn, graph -->
<!-- Samuel Homberg, --.---.---- -->

# Using GraphGym with custom datasets and models

[GraphGym](https://pytorch-geometric.readthedocs.io/en/2.0.1/notes/graphgym.html) is a platform for designing and evaluating Graph Neural networks (GNNs) and supported officially as a part of [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/2.0.1/index.html) (PyG).
Through the use of config-files (as `.yaml`), experiments become repeatable and hyperparameter tuning (in form of grid searches) are possible.

I assume that this is great if you start with a blank project, however, I ran into some difficulties when using GraphGym with existing data and models. (I want to switch to GraphGym instead of coding every training routine myself and to have config-files that I can easily refer back to.) **In this blog post, I describe the problems I ran into, when using GraphGym with a preexisting project and how I solved them.**

## Getting started

*Using PyG version 2.3.0* <!-- -->

### Running an example experiment (as in the docs)

Provided PyG and PyTorch are installed, GraphGym also expects `pandas`, `yacs`, `pytorch_lightning`, `ogb` and  `tensorboardx`. Which can be installed with conda/mamba or pip.

Then, it was possible to execute the `run_single.sh` script, as described in the docs.

## Using a custom dataset (for a regression task)

To register a custom dataset, create a `custom_dataset.py` file at `graphgym/custom_graphgym/loader/custom_dataset.py`. Due to a bug [[Issue #4230](https://github.com/pyg-team/pytorch_geometric/issues/4230)] it is necessary to have a dataset with the split names `['train_graph_index', 'val_graph_index', 'test_graph_index']`, at least in my case.

To resolve this issue, in the `custom_datasety.py` file, create a loader function, which you register with the decorator according to the example. The dataset can be crated in the same file, inheriting from `torch_geometric.data.InMemoryDataset`. The file for customization could look like this:

```py
# %% loader 
from torch_geometric.graphgym.register import register_loader
from torch_geometric.graphgym.config import cfg
from torch_geometric.graphgym.loader import set_dataset_attr


@register_loader('custom_dataset')
def load_custom_dataset(format, name, dataset_dir):
    dataset_dir = f'{dataset_dir}/{name}'
    if name == 'custom_dataset':
        dataset = custom_dataset(root=dataset_dir,
                                 custom_option,
                                 train_val_test=cfg.dataset.split)
        # this has to be added because of Issue #4230
        splits = dataset.get_idx_split()
        split_names = ['train_graph_index',
                       'val_graph_index',
                       'test_graph_index']
        for i, key in enumerate(splits.keys()):
            id = splits[key]
            set_dataset_attr(dataset, split_names[i], id, len(id))
        return dataset

# %% dataset
import torch
import torch_geometric

class custom_dataset(torch_geometric.data.InMemoryDataset):
    def __init__(self, root, 
                 custom_option,
                 train_val_test=[0.8, 0.1, 0.1]):

        self.root = root
        self.custom_option = self.custom_option
        self.train_val_test = train_val_test

        super().__init__(root)
        self.data, self.slices = torch.load(self.processed_paths[0])

    # add this function because of Issue #4230
    def get_idx_split(self):
        train_idx = [i for i,x in enumerate(self.split) if x == 'train']
        valid_idx = [i for i,x in enumerate(self.split) if x == 'val']
        test_idx = [i for i,x in enumerate(self.split) if x == 'test']

        return {'train': torch.tensor(train_idx, dtype = torch.long),
                'valid': torch.tensor(valid_idx, dtype = torch.long),
                'test': torch.tensor(test_idx, dtype = torch.long)}

    @property
    def raw_file_names(self):
        return ['raw_file.csv']

    @property
    def processed_file_names(self):
        return ['processed_file.pt']

    def download(self):
        # download or copy from other location
        pass

    def process(self):
        # process raw data, possibly using rdkit, networkx, ...
        # ...
        # split according to self.train_val_test with names ['train', 'val', 'test']
        # for element in raw data:
            data_list[idx] = torch_geometric.data.Data(x=x, 
                                                  edge_index=edge_index, 
                                                  y=label,
                                                  split=split)

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])
```

Additionally, in the config file, change the `metric_best` from `auto` (which seems to default to accuracy, even for regression tasks) to `mse` or another usable metric.

### Adding customization options to the config file

To use config options in dataset processing and loading, default options can be added to the config. For that, the file `graphgym/custom_graphgym/config/example.py` can be modified, which is straightforward. **However, the `main.py` file has to be modified by adding the line `set_cfg(cfg)` to the main function after parsing the arguments.** (Also import the `set_cfg` function first.)

## Using a custom model

Here, the folder names lead to some confusion. To use a custom model (inherited from `torch.nn.module`), save this model at `graphgym/custom_graphgym/network/modelname.py` and add the `@register_network(modelname)` decorator (as in the provided example).
To then use the model, the `modelname` (from the decorator) has to be added as follows:

```yaml
model:
    type: modelname
```

Here it is important again that the line `load_cfg(cfg)` is added to `main.py` to actually register customized modules.

Another caveat ist that, while you can supply a model this way, the model is expected to do only message passing (MP), and you can specify pre- and post-MP layers in the config:

```yaml
gnn:
    layers_pre_mp: 0
    layers_post_mp: 1
```

I do not know how to use pre-MP couldn't find any examples, but for post-MP the `__init__` function of the model should register the post-MP, along with any layer-initialization (taken from the example):

```py
class modelname(torch.nn.Module):
    def __init__(self, dim_in, dim_out):
        super().__init__()
        # layer initialization
        self.conv = GCNConv(dim_in, dim_in) # example
        # ...

        GNNHead = register.head_dict[cfg.dataset.task]
        self.post_mp = GNNHead(dim_in=dim_in, dim_out=dim_out)
```

The message passing, i.e. the `forward` function is expected to look like this, where the `batch` attributes is expected and a modified `batch` is returned:

```py
def forward(self, batch):
    x, edge_index = batch.x, batch.edge_index
    
    # message passing:
    # x = self.conv1(x, edge_index)
    # x = F.relu(x)
    # x = F.dropout(x, p=0.1, training=self.training)

    batch.x = x
    batch = self.post_mp(batch)
    return batch
```

**The pooling before the post-MP is handled by the config:**

```yaml
model:
    graph_pooling: add # mean, sum
```

## Suppressing warnings

The following warnings with my setup and version were suppressed:

- Directly accessing the internal storage format
  - `/home/username/mambaforge/envs/envname/lib/python3.10/site-packages/torch_geometric/data/in_memory_dataset.py:157: UserWarning: It is not recommended to directly access the internal storage format 'data' of an 'InMemoryDataset'. If you are absolutely certain what you are doing, access the internal storage via 'InMemoryDataset._data' instead to suppress this warning. Alternatively, you can access stacked individual attributes of every graph via 'dataset.{attr_name}'.`
  - I assume the creators of graphgym know what they are doing, so I changed the `.data` to `._data` in the torch_geometric package (`.data` was used multiple times in `/home/username/mambaforge/envs/envname/lib/python3.10/site-packages/torch_geometric/graphgym/loader.py`).

- Dataloader workers
  - `/home/username/mambaforge/envs/env_name/lib/python3.10/site-packages/pytorch_lightning/trainer/connectors/data_connector.py:432: PossibleUserWarning: The dataloader, val_dataloader, does not have many workers which may be a bottleneck. Consider increasing the value of the 'num_workers' argument' (try 64 which is the number of cpus on this machine) in the 'DataLoader' init to improve performance.`
  - This could be resolved by a config argument:

    ```yaml
    num_workers: 64
    ```

  - But results in a bunch of warnings `UserWarning: TypedStorage is deprecated.` within PyG, so I did not add the config argument.

- Properly use tensor cores
  - `You are using a CUDA device ('NVIDIA GeForce RTX 3090') that has Tensor Cores. To properly utilize them, you should set 'torch.set_float32_matmul_precision('medium' | 'high')' which will trade-off precision for performance. For more details, read https://pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html#torch.set_float32_matmul_precision`
  - Solved by adding this line to the main function in `graphgym/main.py`: `torch.set_float32_matmul_precision('medium')`
