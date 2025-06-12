# LLM Evaluation Based on World Values Survey Data: Quantifying Cultural Bias Across Model Architectures

---

![GitHub last commit](https://img.shields.io/github/last-commit/anchauha/CultureEval)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

## 🚀 Overview

This project introduces a novel quantitative framework for evaluating **cultural bias in Large Language Models (LLMs)** using empirical data from the **World Values Survey (WVS)**. As LLMs become integrated into global digital infrastructure, understanding and mitigating their inherent cultural biases is crucial for equitable AI development.

Our research reveals significant and varied cultural biases across leading LLMs (Llama 2 13B, Gemma 3 12B, and Phi 4 14B), including a consistent underestimation of **Religious-Traditional Values** in Non-Western contexts. This repository provides the complete methodology, code, and data for reproducing our findings and extending this analysis.

## ✨ Key Contributions

* **Novel Evaluation Framework:** A rigorous, quantitative method for assessing LLM cultural bias using real-world survey data.
* **Empirically Derived Cultural Dimensions:** Extraction and validation of five distinct cultural dimensions from WVS Wave 7 data.
* **Cross-Model Bias Quantification:** Detailed, dimension-specific cultural bias evaluation across multiple LLMs.
* **Actionable Insights:** Identifies specific patterns of bias (e.g., secularizing bias in Non-Western profiles, Western-leaning tendencies) to inform the development of more culturally inclusive AI systems.

## 📊 Key Findings at a Glance

* **All tested LLMs show significant cultural biases** compared to WVS empirical data.
* **Poor Factor Structure Congruence:** LLM outputs failed to adequately reproduce the underlying cultural factor structure of the ground truth data.
* **Consistent Underestimation of Religious-Traditional Values:** Particularly pronounced for Non-Western demographic profiles (Cohen's d from -0.89 to -1.17), suggesting a secularizing bias.
* **Model-Specific Bias Patterns:**
    * **Llama 2 13B:** Showed the strongest Western Bias (WBI=0.789) but a lower Overall Cultural Bias Index (OCBI=0.64).
    * **Gemma 3 12B:** Exhibited extreme biases in specific dimensions (e.g., overestimating Openness to Diversity, OCBI=0.66, WBI=0.724).
    * **Phi 4 14B:** Demonstrated the highest overall bias magnitude (OCBI=0.78) but a less pronounced Western orientation (WBI=0.512).
* **Cultural Flattening:** LLMs tend to homogenize cultural differences, often pushing responses towards a moderate, Western-influenced perspective.

## 🛠️ Methodology Overview

Our multi-stage pipeline processes WVS data, extracts cultural dimensions, generates LLM responses, and quantifies cultural bias:

1.  **Data Source:** World Values Survey (WVS) Wave 7 (2017-2022) data.
2.  **Preprocessing & Imputation:** Comprehensive data cleaning, variable selection, and advanced iterative imputation (MICE) for missing data.
3.  **Data Aggregation:** Individual-level imputed WVS data aggregated to 2,250 unique demographic profiles using the mode for ground truth.
4.  **Cultural Dimension Extraction (EFA):** Exploratory Factor Analysis (PCA with Promax rotation, 5 factors) performed on the aggregated data to identify five latent cultural dimensions:
    * Religious-Traditional Values
    * Institutional Trust
    * Democratic Values
    * Social Conservatism
    * Openness to Diversity
5.  **LLM Response Generation:** Llama 2 (13B-chat-fp16), Gemma 3 (12B-it-fp16), and Phi 4 (14B-fp16) predict responses for the same demographic profiles.
6.  **Cultural Bias Evaluation:** Comparison of LLM-generated data with WVS ground truth using statistical techniques like Tucker’s Congruence Coefficient, Cohen’s d, and custom bias indices (Overall Cultural Bias Index - OCBI, and Western Bias Index - WBI).

## 📂 Repository Structure

The repository is organized as follows:

```text
.
├── 01_pre-processing.ipynb         # Data loading, cleaning, and initial exploration
├── 02_imputation.ipynb             # Primary imputation pipeline
├── 02_imputationalternate.ipynb    # Alternate imputation strategies/checks
├── 03_aggregation.ipynb            # Aggregation of imputed data by demographic profiles
├── 04_EFA.ipynb                    # Exploratory Factor Analysis model selection
├── 05_DimenReduc.ipynb             # Detailed EFA, diagnostics, and dimension interpretation
├── 06_EFA_Comparison.ipynb         # Comparison of LLM outputs with ground truth EFA
├── 07_visualizations.ipynb         # Generation of charts and visualizations
├── data/                           # Input datasets and metadata
│   ├── gemma3-12b_output_inferred.csv # Inferred output from gemma3-12b
│   ├── llama2-13b_output_inferred.csv # Inferred output from gemma3-12b
│   ├── phi4-14b_output_inferred.csv # Inferred output from gemma3-12b
│   ├── variable_info.csv # Variables info metadata file
│   ├── wvs_wave7_imputed.csv # Imputed data
│   └── ...
├── output/                         # Generated results from analyses
│   ├── communalities_varimax_5factors.csv
│   ├── efa_comparison_all_models/  # Detailed model comparison outputs
│   │   ├── T1_EFA_results/         # Factor loadings and scores for ground truth (T1)
│   │   │   └── ...                 # (contains T1 factor analysis outputs)
│   │   ├── visualizations/         # Visualizations from EFA comparisons
│   │   │   └── ...                 # (contains plots and charts)
│   │   ├── ...
│   ├── factor_loadings_varimax_5factors.csv
│   ├── factor_scores_varimax_5factors.csv
│   ├── kmo_per_variable.csv
│   └── pearson_correlation_matrix.csv
└── README.md                       # This file
```

### Notebook Pipeline

The Jupyter notebooks are designed to be run sequentially, forming a complete data processing and analysis pipeline:

1.  **`01_pre-processing.ipynb`**: Imports raw WVS Wave 7 data, performs initial cleaning, variable selection, and exploratory data analysis.
2.  **`02_imputation.ipynb`** (and **`02_imputationalternate.ipynb`**): Implements the demographic-grouped imputation strategy using `IterativeImputer` (MICE) with custom estimators (Logistic Regression, Ordered Logit) and manual, evidence-based imputations.
3.  **`03_aggregation.ipynb`**: Aggregates the imputed survey data by demographic profiles, primarily computing modal responses to create the T1 dataset.
4.  **`04_EFA.ipynb`**: Tests multiple EFA configurations (different extraction methods and rotation techniques) to select the optimal model.
5.  **`05_DimenReduc.ipynb`**: Performs a detailed EFA using the selected model (PCA with Promax, 5 factors), including diagnostic tests like KMO and Scree plots, and interprets the resulting cultural dimensions.
6.  **`06_EFA_Comparison.ipynb`**: Compares the factor structure and scores of the ground truth WVS data (T1) with LLM-simulated datasets (T2) using techniques like Tucker’s Congruence Coefficient and Cohen’s d.
7.  **`07_visualizations.ipynb`**: Generates various visualizations (heatmaps, radar charts, etc.) using `pandas` and `seaborn` to illustrate the findings from the EFA and comparative analyses.

### Data Files (`data/` directory)

* **Raw/Processed WVS Data:**
    * `wvs_wave7_preprocessed.csv`: Output of `01_pre-processing.ipynb`.
    * `wvs_wave7_imputed.csv`: Output of `02_imputation.ipynb` (primary imputation).
    * `wvs_wave7_imputed_alternate.csv`: Output of `02_imputationalternate.ipynb`.
    * `new_mode_wvs_wave7_aggregated_by_demographics.csv`: Aggregated ground truth (T1) using mode, output of `03_aggregation.ipynb`.
    * `new_median_wvs_wave7_aggregated_by_demographics.csv`: Aggregated ground truth (T1) using median.
* **LLM Generated Data:**
    * `gemma3-12b_output_inferred.csv`: Responses generated by Gemma 3 12B.
    * `llama2-13b_output_inferred.csv`: Responses generated by Llama 2 13B.
    * `phi4-14b_output_inferred.csv`: Responses generated by Phi 4 14B.
* **Metadata:**
    * `selected_vars.csv`: List of WVS variables selected for the analysis.
    * `variable_info.csv`: Detailed information about the WVS variables used.

### Output Files (`output/` directory)

This directory contains the results of the EFA and comparative analyses:

* **Main EFA Results (from `05_DimenReduc.ipynb` on T1 data):**
    * `communalities_varimax_5factors.csv`: Communalities for variables from the EFA.
    * `factor_loadings_varimax_5factors.csv`: Factor loadings for the 5-factor solution.
    * `factor_scores_varimax_5factors.csv`: Factor scores for demographic profiles on the T1 data.
    * `kmo_per_variable.csv`: KMO measure per variable for the T1 data.
    * `pearson_correlation_matrix.csv`: Pearson correlation matrix of the variables in T1 data.
* **EFA Comparison and LLM Evaluation Results (from `06_EFA_Comparison.ipynb` stored in `output/efa_comparison_all_models/`):**
    * `T1_EFA_results/`: Contains detailed factor analysis outputs (loadings, scores) specifically for the ground truth (T1) dataset, used as a baseline.
    * `visualizations/`: Stores plots and charts generated during the comparison of LLM outputs against the ground truth.
    * `cohens_d_T1_vs_<model_name>_projected.csv`: Cohen's d effect sizes comparing T1 factor scores with LLM-projected scores for each model.
    * `country_mean_factor_change_<model_name>.csv`: Mean factor score differences at the country level for each model.
    * `diff_scores_T1_vs_<model_name>_projected.csv`: Raw difference scores between T1 and LLM-projected factor scores.
    * `region_mean_factor_change_<model_name>.csv`: Mean factor score differences aggregated by region (e.g., Western vs. Non-Western) for each model.
    * `scores_<model_name>_projected_on_T1.csv`: Factor scores for each LLM's data when projected onto the T1 factor structure.
    * `ttest_T1_vs_<model_name>_projected.csv`: Results of paired t-tests comparing T1 factor scores with LLM-projected scores.

## 🤝 Contributing

Contributions are welcome! If you find a bug, have suggestions for improvements, or want to add new features, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📧 Contact

Ankit Singh Chauhan - [ankichau.1718@gmail.com](mailto:ankichau.1718@gmail.com)
