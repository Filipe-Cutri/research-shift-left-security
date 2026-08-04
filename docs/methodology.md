# Metodologia

> Rascunho técnico para apoiar a redação da seção METODOLOGIA do artigo.
> Ajustar linguagem/formatação para o modelo FHO antes de colar no docx.

## 1. Desenho experimental

Estudo comparativo de dois grupos, com a mesma aplicação-alvo e a mesma
infraestrutura de execução, variando apenas a presença de ferramentas de
segurança embarcadas na esteira de CI/CD:

- **Grupo controle (baseline)** — pipeline sem nenhuma etapa de segurança
  (`baseline.yml`): checkout, build da imagem Docker, registro de tempo.
- **Grupo experimental (shift-left)** — mesmo pipeline, acrescido de SAST
  (Semgrep, `--config=auto`) e SCA (Trivy, escaneamento de filesystem +
  imagem) como etapas do build (`shift-left.yml`).

Ambos os pipelines rodam sobre o **OWASP Juice Shop**, aplicação
intencionalmente vulnerável, [DECIDIR: imagem oficial `bkimminich/juice-shop`
vs. fork travado em commit específico como submódulo — documentar a escolha
e a justificativa aqui].

## 2. Amostra

- N = 30 execuções por grupo (60 no total), disparadas manualmente via
  `workflow_dispatch` no GitHub Actions.
- [DECIDIR: execuções em blocos sequenciais por grupo ou intercaladas —
  justificar a escolha em termos de controle de variação do runner
  GitHub-hosted ao longo do tempo].
- Ambiente: GitHub-hosted runner `ubuntu-latest`, mesma especificação de
  hardware para todas as execuções.

## 3. Métricas coletadas

Cada execução grava um registro JSON (`data/raw/`) com:

| Campo | Descrição |
|---|---|
| `pipeline_type` | `baseline` ou `shift-left` |
| `build_time_seconds` | tempo total do pipeline |
| `security_stage_seconds` | tempo da etapa de segurança (0 no baseline) |
| `vulnerabilities_detected` | soma de achados do Semgrep + Trivy |
| `false_positives` | [DECIDIR: como será classificado/validado manualmente] |

## 4. Análise estatística

- Teste **Mann-Whitney U** (não paramétrico, não assume normalidade —
  adequado ao N moderado deste estudo) para comparar `build_time_seconds`
  entre os grupos.
- Nível de significância: α = 0,05.
- Overhead relatado como variação percentual da média
  (shift-left vs. baseline).
- Script: `analysis/analyze_results.py`, saída em
  `results/figures/*.png` e `data/processed/summary.csv`.

## 5. Limitações assumidas

- **MTTD operacionalizado como tempo de escaneamento**, não como tempo
  entre a introdução histórica de uma falha e sua descoberta — o Semgrep/
  Trivy reportam vulnerabilidades já presentes no código no momento do
  scan. Simplificação razoável para o escopo de uma IC; deve ser declarada
  explicitamente aqui.
- [Adicionar outras limitações à medida que surgirem: falsos positivos não
  validados manualmente, N=30 por grupo, ambiente de runner compartilhado
  do GitHub Actions, etc.]
