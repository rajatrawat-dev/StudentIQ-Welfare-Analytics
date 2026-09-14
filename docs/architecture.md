# StudentIQ Architectural Blueprint

StudentIQ is architected to address the official **TransOrg AgentIQ Datathon** business challenge for the **Education & EdTech Track: "Student Retention & Welfare Efficacy Tracker"**.

## Core Problem Statement
The State Education Department needs to monitor and evaluate the correlation between:
1. Mid-Day Meal scheme
2. School infrastructure
3. Student dropout risks

## 4-Layer Architecture

```mermaid
flowchart TD
    subgraph Layer1[Layer 1: Data Rescue Engine]
        A[Raw Organizer Dataset / Demo CSV] --> B[Data Profiler: Inspect Schema & Types]
        B --> C[Synonym Schema Matcher: Candidate Mapping]
        C --> D[Boolean Normalizer: Yes/Hai/Nahi/0/1 -> True/False]
        D --> E[Unit Normalizer: Quintals/Qtl/Tons -> Standard KG]
        E --> F[Attendance Bounds & Proxy Anomaly Detector]
        F --> G[District-Median Missing Imputer]
        G --> H[Composite Quality Scorer & Audit JSON Report]
    end

    subgraph Layer2[Layer 2: DuckDB Columnar OLAP Analytics]
        H --> I[(Embedded DuckDB Store)]
        I --> J[Analytical Views: district_summary, risk_summary]
        I --> K[Dynamic Executive Findings Generator]
    end

    subgraph Layer3[Layer 3: Machine Learning Risk Classifier]
        H --> L[Scikit-Learn Preprocessing & Random Forest]
        L --> M[Dropout Risk Model & Calibration Fallback]
        M --> N[School Risk Factor Explainer]
    end

    subgraph Layer4[Layer 4: Controlled AI Analyst & UI]
        O[Natural Language Question] --> P[Intent Detection]
        P --> Q[Query Generator: Ollama LLM / Rule Engine]
        Q --> R{AI Safety Gatekeeper}
        R -- "Unsafe Command / Multi-stmt" --> S[Security Rejection]
        R -- "Validated SELECT" --> T[DuckDB Execution]
        T --> U[Deterministic Chart Selector]
        T --> V[Text Summary & Business Insight]
        U --> W[Plotly Visualization]
    end

    subgraph Presentation[Presentation & API Microservices]
        X[Streamlit Multi-Page Executive Dashboard]
        Y[FastAPI REST API Service]
        I --> X
        I --> Y
        M --> X
        M --> Y
        W --> X
        V --> X
    end
```

## Adaptability Guarantee
When the organizer dataset arrives:
1. Copy raw file into `data/raw/`
2. Run `python scripts/inspect_data.py --file data/raw/<file>.csv`
3. Run `python scripts/run_pipeline.py --file data/raw/<file>.csv`
The fuzzy schema matcher automatically detects column aliases and regenerates clean ground truth without touching UI or backend code.