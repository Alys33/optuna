import pytest

from typing import List
from typing import Optional

import itertools

import optuna
from optuna.multi_objective.visualization import plot_pareto_front


@pytest.mark.parametrize("include_dominated_trials", [False, True])
@pytest.mark.parametrize("axis_order", [None, [0, 1], [1, 0]])
def test_plot_pareto_front_2d(
    include_dominated_trials: bool, axis_order: Optional[List[int]]
) -> None:
    # Test with no trial.
    study = optuna.multi_objective.create_study(["minimize", "minimize"])
    figure = plot_pareto_front(
        study,
        include_dominated_trials=include_dominated_trials,
        axis_order=axis_order,
    )
    assert len(figure.data) == 1
    assert figure.data[0]["x"] == ()
    assert figure.data[0]["y"] == ()

    # Test with three trials.
    study.enqueue_trial({"x": 1, "y": 1})
    study.enqueue_trial({"x": 1, "y": 0})
    study.enqueue_trial({"x": 0, "y": 1})
    study.optimize(lambda t: [t.suggest_int("x", 0, 1), t.suggest_int("y", 0, 1)], n_trials=3)

    figure = plot_pareto_front(
        study,
        include_dominated_trials=include_dominated_trials,
        axis_order=axis_order,
    )
    assert len(figure.data) == 1
    if include_dominated_trials:
        # The last elements come from dominated trial that is enqueued firstly.
        data = [(1, 0, 1), (0, 1, 1)]
        if axis_order is None:
            assert figure.data[0]["x"] == data[0]
            assert figure.data[0]["y"] == data[1]
        else:
            assert figure.data[0]["x"] == data[axis_order[0]]
            assert figure.data[0]["y"] == data[axis_order[1]]
    else:
        data = [(1, 0), (0, 1)]
        if axis_order is None:
            assert figure.data[0]["x"] == data[0]
            assert figure.data[0]["y"] == data[1]
        else:
            assert figure.data[0]["x"] == data[axis_order[0]]
            assert figure.data[0]["y"] == data[axis_order[1]]

    titles = ["Objective {}".format(i) for i in range(2)]
    if axis_order is None:
        assert figure.layout.xaxis.title.text == titles[0]
        assert figure.layout.yaxis.title.text == titles[1]
    else:
        assert figure.layout.xaxis.title.text == titles[axis_order[0]]
        assert figure.layout.yaxis.title.text == titles[axis_order[1]]

    # Test with `names` argument.
    with pytest.raises(ValueError):
        plot_pareto_front(study, names=[], include_dominated_trials=include_dominated_trials)

    with pytest.raises(ValueError):
        plot_pareto_front(study, names=["Foo"], include_dominated_trials=include_dominated_trials)

    with pytest.raises(ValueError):
        plot_pareto_front(
            study,
            names=["Foo", "Bar", "Baz"],
            include_dominated_trials=include_dominated_trials,
            axis_order=axis_order,
        )

    names = ["Foo", "Bar"]
    figure = plot_pareto_front(
        study,
        names=names,
        include_dominated_trials=include_dominated_trials,
        axis_order=axis_order,
    )
    if axis_order is None:
        assert figure.layout.xaxis.title.text == names[0]
        assert figure.layout.yaxis.title.text == names[1]
    else:
        assert figure.layout.xaxis.title.text == names[axis_order[0]]
        assert figure.layout.yaxis.title.text == names[axis_order[1]]


@pytest.mark.parametrize("include_dominated_trials", [False, True])
@pytest.mark.parametrize("axis_order", [None] + list(itertools.permutations(range(3), 3)))
def test_plot_pareto_front_3d(
    include_dominated_trials: bool, axis_order: Optional[List[int]]
) -> None:
    # Test with no trial.
    study = optuna.multi_objective.create_study(["minimize", "minimize", "minimize"])
    figure = plot_pareto_front(
        study,
        include_dominated_trials=include_dominated_trials,
        axis_order=axis_order,
    )
    assert len(figure.data) == 1
    assert figure.data[0]["x"] == ()
    assert figure.data[0]["y"] == ()
    assert figure.data[0]["z"] == ()

    # Test with three trials.
    study.enqueue_trial({"x": 1, "y": 1, "z": 1})
    study.enqueue_trial({"x": 1, "y": 0, "z": 1})
    study.enqueue_trial({"x": 1, "y": 1, "z": 0})
    study.optimize(
        lambda t: [t.suggest_int("x", 0, 1), t.suggest_int("y", 0, 1), t.suggest_int("z", 0, 1)],
        n_trials=3,
    )

    figure = plot_pareto_front(
        study,
        include_dominated_trials=include_dominated_trials,
        axis_order=axis_order,
    )
    assert len(figure.data) == 1
    if include_dominated_trials:
        # The last elements come from dominated trial that is enqueued firstly.
        data = [(1, 1, 1), (0, 1, 1), (1, 0, 1)]
        if axis_order is None:
            assert figure.data[0]["x"] == data[0]
            assert figure.data[0]["y"] == data[1]
            assert figure.data[0]["z"] == data[2]
        else:
            assert figure.data[0]["x"] == data[axis_order[0]]
            assert figure.data[0]["y"] == data[axis_order[1]]
            assert figure.data[0]["z"] == data[axis_order[2]]
    else:
        data = [(1, 1), (0, 1), (1, 0)]
        if axis_order is None:
            assert figure.data[0]["x"] == data[0]
            assert figure.data[0]["y"] == data[1]
            assert figure.data[0]["z"] == data[2]
        else:
            assert figure.data[0]["x"] == data[axis_order[0]]
            assert figure.data[0]["y"] == data[axis_order[1]]
            assert figure.data[0]["z"] == data[axis_order[2]]

    titles = ["Objective {}".format(i) for i in range(3)]
    if axis_order is None:
        assert figure.layout.scene.xaxis.title.text == titles[0]
        assert figure.layout.scene.yaxis.title.text == titles[1]
        assert figure.layout.scene.zaxis.title.text == titles[2]
    else:
        assert figure.layout.scene.xaxis.title.text == titles[axis_order[0]]
        assert figure.layout.scene.yaxis.title.text == titles[axis_order[1]]
        assert figure.layout.scene.zaxis.title.text == titles[axis_order[2]]

    # Test with `names` argument.
    with pytest.raises(ValueError):
        plot_pareto_front(
            study,
            names=[],
            include_dominated_trials=include_dominated_trials,
            axis_order=axis_order,
        )

    with pytest.raises(ValueError):
        plot_pareto_front(
            study,
            names=["Foo"],
            include_dominated_trials=include_dominated_trials,
            axis_order=axis_order,
        )

    with pytest.raises(ValueError):
        plot_pareto_front(
            study,
            names=["Foo", "Bar"],
            include_dominated_trials=include_dominated_trials,
            axis_order=axis_order,
        )

    with pytest.raises(ValueError):
        plot_pareto_front(
            study,
            names=["Foo", "Bar", "Baz", "Qux"],
            include_dominated_trials=include_dominated_trials,
            axis_order=axis_order,
        )

    names = ["Foo", "Bar", "Baz"]
    figure = plot_pareto_front(study, names=names, axis_order=axis_order)
    if axis_order is None:
        assert figure.layout.scene.xaxis.title.text == names[0]
        assert figure.layout.scene.yaxis.title.text == names[1]
        assert figure.layout.scene.zaxis.title.text == names[2]
    else:
        assert figure.layout.scene.xaxis.title.text == names[axis_order[0]]
        assert figure.layout.scene.yaxis.title.text == names[axis_order[1]]
        assert figure.layout.scene.zaxis.title.text == names[axis_order[2]]


@pytest.mark.parametrize("include_dominated_trials", [False, True])
def test_plot_pareto_front_unsupported_dimensions(include_dominated_trials: bool) -> None:
    # Unsupported: n_objectives == 1.
    with pytest.raises(ValueError):
        study = optuna.multi_objective.create_study(["minimize"])
        study.optimize(lambda t: [0], n_trials=1)
        plot_pareto_front(study, include_dominated_trials=include_dominated_trials)

    # Supported: n_objectives == 2.
    study = optuna.multi_objective.create_study(["minimize", "minimize"])
    study.optimize(lambda t: [0, 0], n_trials=1)
    plot_pareto_front(study, include_dominated_trials=include_dominated_trials)

    # Supported: n_objectives == 3.
    study = optuna.multi_objective.create_study(["minimize", "minimize", "minimize"])
    study.optimize(lambda t: [0, 0, 0], n_trials=1)
    plot_pareto_front(study, include_dominated_trials=include_dominated_trials)

    # Unsupported: n_objectives == 4.
    with pytest.raises(ValueError):
        study = optuna.multi_objective.create_study(
            ["minimize", "minimize", "minimize", "minimize"]
        )
        study.optimize(lambda t: [0, 0, 0, 0], n_trials=1)
        plot_pareto_front(study, include_dominated_trials=include_dominated_trials)
