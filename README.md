# AI-300 Lab Guide

Hands-on guide for the Microsoft AI-300: Operationalizing Machine Learning and Generative AI Solutions exam.

All 13 labs from the official Microsoft Learn curriculum, reorganized into a single linear path with architecture diagrams, cost estimates, and exam tips.

## Who This Is For

- Preparing for the AI-300 exam
- Have an Azure subscription (pay-as-you-go is fine)
- Comfortable with CLI basics

## Quick Start

1. Clone this repo: `git clone https://github.com/btriani/ai-300-lab-guide.git`
2. Complete the [prerequisites](prerequisites.md)
3. Start with [Lab 01](labs/01-automl-mlflow/workbook.md)

## Labs

| # | Lab | Track | Est. Cost | Est. Time |
|---|-----|-------|-----------|-----------|
| 01 | [AutoML & MLflow](labs/01-automl-mlflow/workbook.md) | MLOps | ~$1-2 | 45 min |
| 02 | [Sweep Jobs (Hyperparameter Tuning)](labs/02-sweep-jobs/workbook.md) | MLOps | ~$1-2 | 45 min |
| 03 | [Pipelines & Components](labs/03-pipelines/workbook.md) | MLOps | ~$1-2 | 60 min |
| 04 | [Managed Online Endpoints](labs/04-endpoints/workbook.md) | MLOps | ~$1-3 | 60 min |
| 05 | [Responsible AI Dashboard](labs/05-responsible-ai/workbook.md) | MLOps | ~$1-2 | 45 min |
| 06 | [CI/CD with GitHub Actions](labs/06-cicd/workbook.md) | MLOps | ~$1-2 | 60 min |
| 07 | [MLOps End-to-End](labs/07-mlops-e2e/workbook.md) | MLOps | ~$1-3 | 90 min |
| 08 | [Azure AI Foundry Basics](labs/08-foundry-basics/workbook.md) | GenAIOps | <$1 | 30 min |
| 09 | [Prompt Flow](labs/09-prompt-flow/workbook.md) | GenAIOps | ~$1-2 | 60 min |
| 10 | [Content Safety & Filters](labs/10-content-safety/workbook.md) | GenAIOps | <$1 | 30 min |
| 11 | [GenAI CI/CD with azd](labs/11-genai-cicd/workbook.md) | GenAIOps | ~$1-2 | 60 min |
| 12 | [RAG Evaluation](labs/12-rag-eval/workbook.md) | GenAIOps | ~$1-2 | 60 min |
| 13 | [GenAIOps End-to-End](labs/13-genaiops-e2e/workbook.md) | GenAIOps | ~$2-4 | 90 min |

Labs 01-07 = MLOps track, Labs 08-13 = GenAIOps track.

**Total estimated cost: ~$15-30** -- see [COST-GUIDE.md](COST-GUIDE.md)

## Cheatsheets

- [MLOps Cheatsheet](cheatsheets/mlops-cheatsheet.md) -- CLI commands, key concepts, common patterns
- [GenAIOps Cheatsheet](cheatsheets/genaiops-cheatsheet.md) -- azd commands, Foundry concepts, evaluation patterns

## Official Microsoft Resources

- [MLOps Labs](https://microsoftlearning.github.io/mslearn-mlops/)
- [GenAIOps Labs](https://microsoftlearning.github.io/mslearn-genaiops/)
- [AI-300 Exam Page](https://learn.microsoft.com/en-us/credentials/certifications/exams/ai-300/)

## Contributing

Found an error or have a suggestion? Open an issue or PR.

## License

[MIT](LICENSE)
