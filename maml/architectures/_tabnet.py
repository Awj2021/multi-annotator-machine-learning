from torch import nn
from typing import Union
from collections.abc import Iterable


def gt_tabnet(
    n_classes: int, n_features: int, n_hidden_neurons: Union[int, Iterable] = 128, dropout_rate: float = 0.0
):
    """
    Creates a ground truth (GT) model as multi-layer perceptron, suited for learning with tabular data or as
    classification head to a backbone.

    Parameters
    ----------
    n_classes : int
        Number of classes used for the classification head implemented as multi-layer perceptron (MLP) or linear layer.
    n_features : int
        Number of features of the input data.
    n_hidden_neurons : int or list, default=129
        Number of hidden neurons of the classification head. In case of an empty list, a linear layer is used as
        classification head.
    dropout_rate : float, default=True
        Dropout rate used, if the classification head is an MLP.

    Returns
    -------
    gt_embed_x : nn.Module
        Architecture of the MLP excluding its last layer.
    gt_output : nn.Module
        Last layer of the created MLP.
    n_hidden_neurons : int
        Number of neurons in the MLP's penultimate layer.
    """
    # Set list of neuron numbers.
    neuron_list = [n_features]
    if isinstance(n_hidden_neurons, int) and n_hidden_neurons > 0:
        n_hidden_neurons = [n_hidden_neurons]
    for neurons in n_hidden_neurons:
        neuron_list.append(neurons)
    n_last_layer_neurons = neuron_list[-1]

    def gt_embed_x():
        # Create list of modules for given numbers of neurons.
        module_list = []
        for i in range(len(neuron_list) - 1):
            module_list.append(nn.Linear(in_features=neuron_list[i], out_features=neuron_list[i + 1]))
            module_list.append(nn.BatchNorm1d(num_features=neuron_list[i + 1]))
            module_list.append(nn.ReLU())
            module_list.append(nn.Dropout(dropout_rate))
        if len(module_list) > 0:
            return nn.Sequential(*module_list)
        else:
            return nn.Identity()

    def gt_output():
        return nn.Linear(in_features=n_last_layer_neurons, out_features=n_classes)

    return gt_embed_x, gt_output, n_last_layer_neurons
