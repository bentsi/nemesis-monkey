from nemesis_collection.scylla import FillScyllaDataPartition
from nemesis_collection.scylla import RebootScyllaNode
from nemesis_collection.scylla import RestartScyllaService

from nemesis_monkey.chaos import Chaos


with Chaos(repeat_cycles=5) as sequential_chaos:
    sequential_chaos.apply(
        list_of_nemesis=[
            RestartScyllaService(),
            RebootScyllaNode(),
            FillScyllaDataPartition(),
        ],
    )
