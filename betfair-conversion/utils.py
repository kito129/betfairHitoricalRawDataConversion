from rich.progress import BarColumn, Progress, TimeRemainingColumn


def getProgress() -> Progress:
    return Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "{task.completed}/{task.total}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )
