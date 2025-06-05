# LLM Evaluation Based on World Values Survey Data: Quantifying Cultural Bias Across Model Architectures

**Authors:** Ankit Singh Chauhan

## Abstract

Artificial intelligence systems, particularly Large Language Models (LLMs), increasingly serve as global digital infrastructure. As their deployment expands worldwide, concerns about cultural bias have grown urgent, yet quantitative evaluation of such bias has remained elusive. This research develops a novel framework for evaluating cultural bias in LLMs using World Values Survey (WVS) data as an empirical benchmark. We extract five cultural dimensions from WVS Wave 7 data through factor analysis, then evaluate how well three different LLMs (Llama 2 13B, Gemma 3 12B, and Phi 4 14B) represent these dimensions across diverse demographic profiles. Our findings reveal significant cultural biases across all three models, though with important variations in both magnitude and pattern. Most notably, all models significantly underestimate Religious-Traditional Values for Non-Western profiles while slightly overestimating them for Western profiles, suggesting a consistent secular bias in representing Non-Western cultures. For other dimensions, the models show varying patterns, with Llama 2 exhibiting the strongest Western bias despite lower overall bias magnitude, Gemma 3 showing extreme biases in specific dimensions, and Phi 4 demonstrating higher overall bias magnitude but less Western orientation. These insights aim to inform more targeted approaches to developing culturally inclusive AI systems.

**Keywords:** cultural bias, large language models, exploratory factor analysis, world values survey, cross-cultural analysis

## Research Context and Objectives

This research addresses the pressing need for robust, quantitative methods to evaluate cultural bias in Large Language Models (LLMs). As LLMs become more integrated into global information ecosystems, understanding their cultural alignment is crucial for equitable AI development.

### Key Research Questions

This study seeks to answer the following core questions:

1.  What latent cultural dimensions can be extracted from the World Values Survey (WVS) Wave 7 data, and do these dimensions correspond to known cultural theories?
2.  How well do the WVS-derived cultural dimensions align with existing cultural models or indicators (such as Hofstede's country indices or the Inglehart-Welzel map)?
3.  To what extent do LLM-generated responses reflect the cultural value profiles of different demographic groups, and are certain cultural dimensions systematically over- or under-represented in LLM outputs?
4.  How does the cultural alignment of LLM responses vary across different subsets of demographic groups, in particular between Western and Non-Western profiles?

### Key Contributions

This research contributes to the field in several ways:

1.  **Methodological Framework:** We develop a novel quantitative framework for evaluating cultural bias in LLMs using empirical survey data, providing a more rigorous approach than existing qualitative or anecdotal assessments.
2.  **Cultural Dimension Extraction:** We extract and validate five distinct cultural dimensions from WVS Wave 7 data, offering a contemporary, empirically-grounded alternative to established cultural frameworks.
3.  **Cross-Model Bias Evaluation:** We provide a comprehensive, dimension-specific quantification of cultural bias across multiple LLMs (Llama 2 13B, Gemma 3 12B, and Phi 4 14B), identifying both consistent patterns and model-specific variations in bias.
4.  **Practical Implications:** We discuss concrete implications for AI development, deployment, and governance, offering actionable insights for creating more culturally inclusive AI systems, including model-specific approaches based on observed bias patterns. Part of report (To be uploaded)

## Methodology Overview

The research employs a multi-stage pipeline to quantify cultural bias in LLMs:

1.  **Data Source:** The primary data is the inverted World Values Survey (WVS) Wave 7 (2017-2022), covering 66 countries and 97,220 respondents.
2.  **Data Preprocessing (`01_pre-processing.ipynb`):**
    * Selection of 97 survey variables and 5 demographic variables.
    * Thorough missing data analysis (overall and country-specific).
3.  **Imputation (`02_imputation.ipynb`, `02_imputationalternate.ipynb`):**
    * **Manual Imputation:** For systematic country-specific missing data (25 variables), values were imputed based on extensive literature review, comparative data analysis (e.g., previous WVS waves, regional barometers, Pew surveys), and cultural/political context assessment.
    * **Advanced Iterative Imputation (MICE):** Remaining random missing values were handled using `sklearn`'s `IterativeImputer` within demographic groups (unique combinations of country, urban/rural status, sex, age, education). Custom estimators (Logistic Regression for binary, Ordered Logit Regression (`mord.LogisticIT`) for ordinal variables) were used to respect variable types.
4.  **Data Aggregation (`03_aggregation.ipynb`):**
    * Individual-level imputed WVS data was aggregated to 2,250 unique demographic profiles.
    * The primary aggregation method used the **mode** for each survey question within each demographic group to create the ground truth dataset (T1). An alternative median-based aggregation was also performed.
5.  **Exploratory Factor Analysis (EFA) & Dimension Reduction (`04_EFA.ipynb`, `05_DimenReduc.ipynb`):**
    * EFA was performed on the aggregated ground truth data (T1) to extract latent cultural dimensions.
    * After comparing various EFA models, Principal Components Analysis (PCA) with Promax rotation and 5 factors was selected. This model explained 35.22% of the variance.
    * Diagnostics included Bartlett’s test of sphericity ($\chi^2=115635.21, p<0.001$) and Kaiser-Meyer-Olkin (KMO) measure (overall KMO=0.943).
    * The five extracted dimensions are: Religious-Traditional Values, Institutional Trust, Democratic Values, Social Conservatism, and Openness to Diversity.
6.  **LLM Response Generation:**
    * Three LLMs were evaluated: Llama 2 (13B-chat-fp16), Gemma 3 (12B-it-fp16), and Phi 4 (14B-fp16), accessed via the Ollama API.
    * Prompts were designed to provide demographic context (country, urban/rural, sex, age, education) and the survey question, asking the LLM to predict the most likely response code.
    * LLM-generated responses formed the T2 datasets for each model.
7.  **Cultural Bias Evaluation & Comparison (`06_EFA_Comparison.ipynb`):**
    * **Factor Structure Comparison:** Tucker’s Congruence Coefficient was used to compare factor loading matrices of T1 and T2 for each LLM.
    * **Factor Score Comparison:** T2 data was projected onto the T1 factor structure. Paired t-tests and Cohen’s d were calculated to assess differences in factor scores.
    * **Group Difference Analysis:** Differences were analyzed between Western and Non-Western country profiles.
    * **Overall Cultural Bias Index (OCBI)** and **Western Bias Index (WBI)** were calculated.
8.  **Visualizations (`07_visualizations.ipynb`):**
    * Heatmaps, radar charts, and other plots were generated using `pandas` and `seaborn` to visualize findings.

## Key Findings

This research uncovered several critical insights into cultural bias in LLMs:

* **Significant Cultural Misalignment:** All three evaluated LLMs (Llama 2 13B, Gemma 3 12B, Phi 4 14B) exhibit substantial cultural biases when compared to empirical WVS data.
* **Poor Factor Structure Congruence:** LLM-generated data failed to adequately reproduce the underlying cultural factor structure of the ground truth data (Tucker's Congruence Coefficients were below the acceptable threshold of 0.85).
* **Underrepresentation of Religious-Traditional Values:** A consistent pattern across all models was the significant underestimation of Religious-Traditional Values, particularly for Non-Western demographic profiles (Cohen's d from -0.89 to -1.17), suggesting a secularizing bias.
* **Model-Specific Bias Patterns:**
    * **Llama 2 13B:** Showed the strongest Western Bias (WBI=0.789) but a lower Overall Cultural Bias Index (OCBI=0.64).
    * **Gemma 3 12B:** Exhibited extreme biases in specific dimensions (e.g., overestimating Openness to Diversity, OCBI=0.66, WBI=0.724).
    * **Phi 4 14B:** Demonstrated the highest overall bias magnitude (OCBI=0.78) but a less pronounced Western orientation (WBI=0.512).
* **Cultural Flattening:** LLMs tend to homogenize cultural differences, often pushing responses towards a moderate, Western-influenced perspective rather than accurately reflecting diverse cultural viewpoints.
* **Differential Regional Bias:** Models often showed contrasting directional biases for Western versus Non-Western profiles, for instance, underestimating certain values for Non-Western groups while overestimating them for Western groups.

## Repository Structure

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
│   ├── gemma3-12b_output_inferred.csv
│   ├── llama2-13b_output_inferred.csv
│   ├── new_median_wvs_wave7_aggregated_by_demographics.csv
│   ├── new_mode_wvs_wave7_aggregated_by_demographics.csv
│   ├── phi4-14b_output_inferred.csv
│   ├── selected_vars.csv
│   ├── variable_info.csv
│   ├── wvs_wave7_imputed.csv
│   ├── wvs_wave7_imputed_alternate.csv
│   └── wvs_wave7_preprocessed.csv
├── output/                         # Generated results from analyses
│   ├── communalities_varimax_5factors.csv
│   ├── efa_comparison_all_models/  # Detailed model comparison outputs
│   │   ├── T1_EFA_results/         # Factor loadings and scores for ground truth (T1)
│   │   │   └── ...                 # (contains T1 factor analysis outputs)
│   │   ├── visualizations/         # Visualizations from EFA comparisons
│   │   │   └── ...                 # (contains plots and charts)
│   │   ├── cohens_d_T1_vs_gemma3-12b_projected.csv
│   │   ├── cohens_d_T1_vs_llama2-13b_projected.csv
│   │   ├── cohens_d_T1_vs_phi4-14b_projected.csv
│   │   ├── country_mean_factor_change_gemma3-12b.csv
│   │   ├── country_mean_factor_change_llama2-13b.csv
│   │   ├── country_mean_factor_change_phi4-14b.csv
│   │   ├── diff_scores_T1_vs_gemma3-12b_projected.csv
│   │   ├── diff_scores_T1_vs_llama2-13b_projected.csv
│   │   ├── diff_scores_T1_vs_phi4-14b_projected.csv
│   │   ├── region_mean_factor_change_gemma3-12b.csv
│   │   ├── region_mean_factor_change_llama2-13b.csv
│   │   ├── region_mean_factor_change_phi4-14b.csv
│   │   ├── scores_gemma3-12b_projected_on_T1.csv
│   │   ├── scores_llama2-13b_projected_on_T1.csv
│   │   ├── scores_phi4-14b_projected_on_T1.csv
│   │   ├── ttest_T1_vs_gemma3-12b_projected.csv
│   │   ├── ttest_T1_vs_llama2-13b_projected.csv
│   │   └── ttest_T1_vs_phi4-14b_projected.csv
│   ├── factor_loadings_varimax_5factors.csv
│   ├── factor_scores_varimax_5factors.csv
│   ├── kmo_per_variable.csv
│   └── pearson_correlation_matrix.csv
└── README.md                       # This file

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

