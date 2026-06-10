from __future__ import annotations

from src.application.graph.builders.interview_graph_builder import (
    InterviewGraphBuilder,
)
from src.scripts.helpers.graph_input_builder import (
    GraphInputBuilder,
)


def main() -> None:
    graph = InterviewGraphBuilder.build()

    result = graph.invoke(
        GraphInputBuilder.build(),
    )

    print(result)


if __name__ == "__main__":
    main()