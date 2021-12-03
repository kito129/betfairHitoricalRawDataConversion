from rich.progress import BarColumn, Progress, TimeRemainingColumn


def get_progress() -> Progress:
    return Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "{task.completed}/{task.total}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )