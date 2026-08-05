# Shift-Left Security in CI/CD — Estudo Experimental

Repositório de apoio à IC "Avaliação Comparativa e de Desempenho na Adoção de
Segurança Shift-Left em Esteiras CI/CD" (FHO — orientação Prof. Mateus Yamaguti).

## O que este repositório faz

Compara dois pipelines de CI/CD rodando sobre a mesma aplicação vulnerável
(OWASP Juice Shop).

- **`baseline.yml`** — pipeline "tradicional", sem nenhuma ferramenta de
  segurança embarcada (grupo controle).
- **`shift-left.yml`** — o mesmo pipeline, mas com SAST (Semgrep) e SCA
  (Trivy) embarcados como etapas do build.

Cada execução grava um JSON em `data/raw/` com tempo de build, tempo do
estágio de segurança e número de vulnerabilidades encontradas. Depois de
várias execuções, `analysis/analyze_results.py` consolida os dados, roda o
teste estatístico e gera os gráficos usados na seção de Resultados do artigo.

## Como usar

1. Clonar este repo e o Juice Shop como submódulo (ver `docker/Dockerfile`).
2. Rodar `baseline.yml` e `shift-left.yml` manualmente (workflow_dispatch)
   N vezes cada — sugestão: 30 execuções por grupo.
3. Baixar os artifacts JSON gerados (ou configurar um step que faz commit
   direto em `data/raw/`).
4. Rodar `python analysis/analyze_results.py` para consolidar e gerar os
   gráficos em `results/figures/`.
5. Usar os números e gráficos para preencher Metodologia, Resultados e
   Discussão do artigo (ver `docs/methodology.md` como ponto de partida).

## Limitação assumida (documentar no artigo)

O MTTD (Mean Time To Detect) aqui é operacionalizado como o **tempo que a
ferramenta leva para escanear e reportar as vulnerabilidades já presentes no
código**, não o tempo entre a introdução histórica de uma falha e sua
descoberta. Isso é uma simplificação razoável para um estudo de IC e deve ser
declarada explicitamente na Metodologia como escopo/limitação.
