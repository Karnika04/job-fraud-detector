from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns


def plot_metric_comparison(metrics: Dict[str, Dict[str, float]], output_path: str) -> None:
    """Plot comparison of model metrics and save to file."""

    sns.set(style="whitegrid")
    metric_names = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    fig, axes = plt.subplots(1, len(metric_names), figsize=(18, 4))

    for idx, metric in enumerate(metric_names):
        values = [metrics[m][metric] for m in metrics]
        model_names = list(metrics.keys())
        ax = axes[idx]
        sns.barplot(x=model_names, y=values, ax=ax)
        ax.set_title(metric)
        ax.set_ylim(0, 1)
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

