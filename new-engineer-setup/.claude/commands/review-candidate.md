---
allowed-tools: Read, Glob, Grep, Bash, Task, Write
description: Review ML candidate assessment submission with fair comparison template
argument-hint: [candidate-name]
model: sonnet
---

# Review ML Candidate Assessment

Review the ML candidate assessment submission for `$ARGUMENTS` using the standardized evaluation framework.

## Variables

CANDIDATE_NAME: $ARGUMENTS
ASSESSMENT_BASE_DIR: /path/to/assessments
REFERENCE_SOLUTION_REPO: reference-assessment
REFERENCE_SOLUTION_BRANCH: solution

## Workflow

1. **Locate Candidate Repository**
   - Find repo at `ASSESSMENT_BASE_DIR/assessment-CANDIDATE_NAME/`
   - Verify repo exists and has candidate's work

2. **Gather Submission Artifacts**
   - Check for notebooks, production code, tests
   - Check for experiment tracking (MLflow, etc.)
   - Check git history: number of commits, branches, PR if any
   - Check for documentation: README updates, reports

3. **Execute Critical Validation Checks**
   - **Data Leakage Check**: Search for preprocessing before train_test_split
   - **Cross-Validation Check**: Search for cross_val_score, StratifiedKFold usage
   - **Class Imbalance Check**: Search for SMOTE, class_weight handling
   - **Interpretability Check**: Search for SHAP, feature_importance usage

4. **Evaluate Against 5 Core Criteria** (with weights)

   | Criterion | Weight | Evaluation Focus |
   |-----------|--------|------------------|
   | Small-Data Handling | 25% | No leakage, stratified splits, class imbalance strategy |
   | Predictive Performance | 25% | Valid metrics, CV scores, confidence intervals |
   | Interpretability | 20% | SHAP, feature importance, prediction explanations |
   | Experiment Tracking | 15% | MLflow usage, logged params/metrics/models |
   | Code Quality | 15% | Production structure, tests, documentation |

5. **Score Each Criterion (0-5 scale)**

6. **Calculate Weighted Score**

7. **Determine Verdict**
   - **STRONG HIRE** (>80%): Exceptional work
   - **HIRE** (65-80%): Meets requirements
   - **HIRE WITH CONDITIONS** (55-65%): Minimum met, coaching needed
   - **BORDERLINE** (45-55%): Interview to clarify gaps
   - **NO HIRE** (<45%): Critical gaps

8. **Generate Review Report**
   - Save to: `ASSESSMENT_BASE_DIR/assessment-CANDIDATE_NAME/review_output/`

## Report

Generate a comprehensive review with: executive summary, requirements assessment table, solution quality analysis, problems identified, comparison to reference, and hiring recommendation with confidence level.
