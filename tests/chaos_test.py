import pytest

from nemesis_monkey.chaos import Chaos
from nemesis_monkey.chaos import ChoiceStrategy


@pytest.mark.target
def test_target_node_list_generation_more_nemesis_than_targets():
    empty_chaos = Chaos(targets_choice_strategy=ChoiceStrategy.sequential())
    empty_chaos.targets = [1, 2, 3]
    targets = empty_chaos._create_list_of_targets(num_nemesis=4)
    expected_targets = [1, 2, 3, 1]
    assert targets == expected_targets


@pytest.mark.target
def test_target_node_list_generation_more_targets_than_nemesis():
    empty_chaos = Chaos(targets_choice_strategy=ChoiceStrategy.sequential())
    empty_chaos.targets = [1, 2, 3, 4, 5]
    targets = empty_chaos._create_list_of_targets(num_nemesis=2)
    expected_targets = [1, 2]
    assert targets == expected_targets


@pytest.mark.target
def test_target_node_list_generation_nemesis_num_same_as_targets():
    empty_chaos = Chaos(targets_choice_strategy=ChoiceStrategy.sequential())
    empty_chaos.targets = [1, 2, 3]
    targets = empty_chaos._create_list_of_targets(num_nemesis=3)
    expected_targets = [1, 2, 3]
    assert targets == expected_targets
