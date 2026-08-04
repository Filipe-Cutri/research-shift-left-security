"""
Consolida os JSONs de data/raw/, roda o teste estatístico comparando
baseline vs shift-left, e gera os gráficos usados na seção de Resultados
do artigo.

Uso: python analysis/analyze_results.py
Saída: results/figures/*.png + resumo estatístico impresso no terminal
"""
import glob
import json
import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "figures")


def load_data() -> pd.DataFrame:
    records = []
    for path in glob.glob(os.path.join(RAW_DIR, "*.json")):
        with open(path) as f:
            records.append(json.load(f))
    if not records:
        raise SystemExit(
            f"Nenhum JSON encontrado em {RAW_DIR}. "
            "Rode os workflows baseline.yml e shift-left.yml antes."
        )
    return pd.DataFrame(records)


def compare_build_times(df: pd.DataFrame):
    baseline = df[df.pipeline_type == "baseline"]["build_time_seconds"]
    shiftleft = df[df.pipeline_type == "shift-left"]["build_time_seconds"]

    print(f"\nN baseline = {len(baseline)}, N shift-left = {len(shiftleft)}")
    print(f"Média baseline: {baseline.mean():.2f}s (dp {baseline.std():.2f})")
    print(f"Média shift-left: {shiftleft.mean():.2f}s (dp {shiftleft.std():.2f})")

    overhead_pct = (shiftleft.mean() - baseline.mean()) / baseline.mean() * 100
    print(f"Overhead médio: {overhead_pct:.1f}%")

    # Mann-Whitney U: não assume distribuição normal, apropriado para
    # amostras pequenas/moderadas típicas de estudos de IC.
    stat, p_value = stats.mannwhitneyu(baseline, shiftleft, alternative="two-sided")
    print(f"Mann-Whitney U: estatística={stat:.2f}, p-valor={p_value:.4f}")
    if p_value < 0.05:
        print("→ Diferença estatisticamente significativa (p < 0.05)")
    else:
        print("→ Diferença NÃO significativa ao nível de 0.05")

    return baseline, shiftleft


def plot_build_time_comparison(baseline: pd.Series, shiftleft: pd.Series):
    os.makedirs(FIG_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot([baseline, shiftleft], labels=["Baseline", "Shift-Left"])
    ax.set_ylabel("Tempo de build (segundos)")
    ax.set_title("Comparação de tempo de build: baseline vs shift-left")
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "build_time_comparison.png")
    fig.savefig(out_path, dpi=150)
    print(f"\nGráfico salvo em {out_path}")


def plot_detection_summary(df: pd.DataFrame):
    shiftleft = df[df.pipeline_type == "shift-left"]
    if shiftleft.empty:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(
        ["Vulnerabilidades\ndetectadas", "Falsos\npositivos"],
        [
            shiftleft["vulnerabilities_detected"].mean(),
            shiftleft["false_positives"].mean(),
        ],
    )
    ax.set_ylabel("Média por execução")
    ax.set_title("Detecção de vulnerabilidades — pipeline shift-left")
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "detection_summary.png")
    fig.savefig(out_path, dpi=150)
    print(f"Gráfico salvo em {out_path}")


def main():
    df = load_data()
    baseline, shiftleft = compare_build_times(df)
    plot_build_time_comparison(baseline, shiftleft)
    plot_detection_summary(df)

    processed_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed", "summary.csv"
    )
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.groupby("pipeline_type").agg(
        {
            "build_time_seconds": ["mean", "std", "count"],
            "vulnerabilities_detected": "mean",
            "false_positives": "mean",
        }
    ).to_csv(processed_path)
    print(f"\nResumo consolidado salvo em {processed_path}")


if __name__ == "__main__":
    main()
