# StudentIQ Methodology & Risk Scoring Formulation

## 1. Mid-Day Meal & Infrastructure Correlation Hypothesis

Educational policy research demonstrates that school dropouts in rural and semi-urban jurisdictions are heavily driven by welfare deficits:
- **Nutritional Anchor**: A functioning Mid-Day Meal scheme prevents midday attrition and incentivizes consistent daily attendance.
- **Gender Retention Threshold**: The absence of dedicated, functional toilets for female students correlates with an exponential rise in adolescent dropouts.
- **Learning Infrastructure**: Electrification facilitates modern classroom delivery, evening study, and digital literacy, directly impacting exam scores.

## 2. Retention Risk Scoring Algorithm

Each institution is evaluated on a continuous composite risk formulation:

$$\text{Risk Points} = (100 - \text{Infrastructure Score}) \times 0.45 + (100 - \text{Attendance}) \times 0.40 + \text{Meal Deficit Penalty}$$

Where:
- $\text{Infrastructure Score} = (\text{Electricity} \times 30) + (\text{Water} \times 30) + (\text{Girls Toilet} \times 25) + (\text{Boys Toilet} \times 15)$
- $\text{Meal Deficit Penalty} = 15.0$ if Mid-Day Meal is disrupted/inactive, else $0.0$.

### Retention Risk Tiers:
- **CRITICAL**: Risk Points $\ge 50$ OR Dropout Rate $\ge 20\%$ OR (Attendance $< 50\%$ AND Infrastructure Score $< 40$)
- **HIGH**: Risk Points $\ge 35$ OR Dropout Rate $\ge 12\%$ OR Infrastructure Score $< 50\%$
- **MEDIUM**: Risk Points $\ge 20$ OR Dropout Rate $\ge 6\%$
- **LOW**: Baseline operations satisfying institutional standards.

*Disclaimer: Strictly framed as an administrative early-warning decision support metric, not a psychological evaluation.*