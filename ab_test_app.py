import streamlit as st
import numpy as np
from scipy.stats import norm

def perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    # Calculate conversion rates
    control_conversion_rate = control_conversions / control_visitors
    treatment_conversion_rate = treatment_conversions / treatment_visitors
    
    # Calculate standard errors
    control_standard_error = np.sqrt(control_conversion_rate * (1 - control_conversion_rate) / control_visitors)
    treatment_standard_error = np.sqrt(treatment_conversion_rate * (1 - treatment_conversion_rate) / treatment_visitors)
    
    # Calculate the pooled standard error
    pooled_standard_error = np.sqrt(control_standard_error**2 + treatment_standard_error**2)
    
    # Calculate the Z-score
    z_score = (treatment_conversion_rate - control_conversion_rate) / pooled_standard_error
    
    # Determine the critical value based on the confidence level
    if confidence_level == 90:
        critical_value = norm.ppf(0.95)
    elif confidence_level == 95:
        critical_value = norm.ppf(0.975)
    elif confidence_level == 99:
        critical_value = norm.ppf(0.995)
    else:
        raise ValueError("Invalid confidence level. Please choose from 90, 95, or 99.")
    
    # Compare the Z-score with the critical value
    if z_score > critical_value:
        return "Experiment Group is Better"
    elif z_score < -critical_value:
        return "Control Group is Better"
    else:
        return "Indeterminate"

def main():
    st.title("A/B Test Hypothesis Test")

    st.write("Enter the following inputs to perform the hypothesis test:")

    control_visitors = st.number_input("Control Group Visitors", min_value=0)
    control_conversions = st.number_input("Control Group Conversions", min_value=0)
    treatment_visitors = st.number_input("Treatment Group Visitors", min_value=0)
    treatment_conversions = st.number_input("Treatment Group Conversions", min_value=0)
    confidence_level = st.selectbox("Confidence Level", [90, 95, 99])

    if st.button("Perform Hypothesis Test"):
        result = perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)
        st.write("Result of A/B test:", result)

if __name__ == "__main__":
    main()
