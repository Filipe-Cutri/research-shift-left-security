"""
Lê os JSONs de saída do Semgrep e do Trivy e soma o total de achados
(vulnerabilidades detectadas). Escreve o resultado no formato esperado
pelo GitHub Actions ($GITHUB_OUTPUT).

Uso: python3 parse_scan_results.py semgrep-results.json trivy-results.json
"""
import json
import os
import sys


def count_semgrep_findings(path: str) -> int:
    try:
        with open(path) as f:
            data = json.load(f)
        return len(data.get("results", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def count_trivy_findings(path: str) -> int:
    try:
        with open(path) as f:
            data = json.load(f)
        total = 0
        for result in data.get("Results", []):
            total += len(result.get("Vulnerabilities", []) or [])
        return total
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def main():
    semgrep_path = sys.argv[1] if len(sys.argv) > 1 else "semgrep-results.json"
    trivy_path = sys.argv[2] if len(sys.argv) > 2 else "trivy-results.json"

    semgrep_count = count_semgrep_findings(semgrep_path)
    trivy_count = count_trivy_findings(trivy_path)
    total = semgrep_count + trivy_count

    print(f"Semgrep findings: {semgrep_count}")
    print(f"Trivy findings: {trivy_count}")
    print(f"Total findings: {total}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"total_findings={total}\n")
            f.write(f"semgrep_findings={semgrep_count}\n")
            f.write(f"trivy_findings={trivy_count}\n")


if __name__ == "__main__":
    main()
