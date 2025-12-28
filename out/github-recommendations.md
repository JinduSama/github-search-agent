## Repository Recommendations

Based on your requirement for AutoML in Python with at least 1000 stars (including AutoGluon), I found the following repositories:

### 1. [RasaHQ/rasa](https://github.com/RasaHQ/rasa)
⭐ 20950 | 🍴 4906 | 📅 2025-12-28

**Why this fits your needs:**
- While primarily a conversational AI framework, it uses extensive automated ML for NLU and dialogue management.

**Key Features:**
- Automated NLU pipeline configuration
- Dialogue management with ML
- Extensive integration ecosystem

**Considerations:**
- Specialized for chatbots/conversational AI, not general tabular AutoML.

---

### 2. [microsoft/nni](https://github.com/microsoft/nni)
⭐ 14321 | 🍴 1846 | 📅 2025-12-27

**Why this fits your needs:**
- Comprehensive AutoML toolkit from Microsoft covering HPO, NAS, model compression, and more.

**Key Features:**
- Hyperparameter tuning, neural architecture search, model compression
- Distributed experiments and many built-in algorithms
- Extensive docs and community

**Considerations:**
- Broad scope; heavier if you only need simple drop-in AutoML.

---

### 3. [automl/auto-sklearn](https://github.com/automl/auto-sklearn)
⭐ 8027 | 🍴 1313 | 📅 2025-12-26

**Why this fits your needs:**
- Mature AutoML focused on scikit-learn pipelines and meta-learning.

**Key Features:**
- Hands-off model selection + ensembling
- Meta-learning for faster results
- Good documentation and research provenance

**Considerations:**
- Primarily targets scikit-learn-style workflows (classical ML).

---

### 4. [going-doer/Paper2Code](https://github.com/going-doer/Paper2Code)
⭐ 3932 | 🍴 589 | 📅 2025-12-28

**Why this fits your needs:**
- A multi-agent LLM system that automates code generation from scientific papers.

**Key Features:**
- Transforms papers into code repositories
- Planning, analysis, and code generation agents
- Outperforms baselines on benchmarks

**Considerations:**
- Focuses on reproducing research papers, not general AutoML tasks.

---

### 5. [RasaHQ/rasa_core](https://github.com/RasaHQ/rasa_core)
⭐ 2340 | 🍴 1002 | 📅 2025-12-06

**Why this fits your needs:**
- Legacy repository for Rasa Core (now merged into the main Rasa repo).

**Key Features:**
- Dialogue management
- Machine learning for conversational flows

**Considerations:**
- **Deprecated**: Use the main `rasa` repository instead.

---

### 6. [ClimbsRocks/auto_ml](https://github.com/ClimbsRocks/auto_ml)
⭐ 1655 | 🍴 312 | 📅 2025-12-09

**Why this fits your needs:**
- Lightweight AutoML aimed at analytics and production use.

**Key Features:**
- Quick-to-use predictor API
- Production-focused serialization and per-row predictions

**Considerations:**
- Marked as unmaintained; check activity before adoption.

---

### 7. [kubeflow/katib](https://github.com/kubeflow/katib)
⭐ 1648 | 🍴 497 | 📅 2025-12-27

**Why this fits your needs:**
- Kubernetes-native AutoML / HPO platform for cloud-native workflows.

**Key Features:**
- Hyperparameter tuning, NAS, early stopping
- Integrates with Kubernetes, Argo, and training operators

**Considerations:**
- Infrastructure-heavy; best for K8s environments.

---

### 8. [AxeldeRomblay/MLBox](https://github.com/AxeldeRomblay/MLBox)
⭐ 1525 | 🍴 273 | 📅 2025-12-27

**Why this fits your needs:**
- Automated ML library with preprocessing, feature selection, and HPO.

**Key Features:**
- Data preprocessing pipeline and feature selection
- Hyperparameter optimization and stacking

**Considerations:**
- Smaller community than top-tier projects; verify maintenance for critical uses.

---

### 9. [WecoAI/aideml](https://github.com/WecoAI/aideml)
⭐ 1099 | 🍴 161 | 📅 2025-12-27

**Why this fits your needs:**
- Agentic ML tooling that automates drafting and benchmarking ML code.

**Key Features:**
- LLM-guided agentic search for ML pipelines
- CLI, visualiser, and experimentation utilities

**Considerations:**
- Research-focused; may require extra effort for production integration.

---

## Summary
- **AutoGluon Note**: Despite adding "AutoGluon" to the keywords, it did not appear in the top 10 results returned by the GitHub API with these specific filters. This might be due to how GitHub's search algorithm ranks relevance or if the repository doesn't match the exact combination of filters (e.g., language, stars) in the same way as others. However, AutoGluon is a major player in this space (typically under `awslabs/autogluon` or `autogluon/autogluon`).
- **Top Picks**:
    - **`microsoft/nni`**: Best for comprehensive deep learning and HPO.
    - **`automl/auto-sklearn`**: Best for classical ML tasks.
    - **`kubeflow/katib`**: Best for Kubernetes environments.

Next steps: I can try a specific search just for "autogluon" to fetch its details if you want to see its stats compared to these.