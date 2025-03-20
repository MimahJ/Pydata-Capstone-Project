import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Streamlit App Title
st.title("📊 Gender Gap Analysis in Kenya’s Tech Industry")

# Load dataset
file_path = "Kenya_Data_Professionals_Compensation_data.xlsx"
df = pd.read_excel(file_path)

# Rename columns for easier reference
df.rename(columns={
    "What is your gender": "Gender",
    "What is your Level?": "Job_Level",
    "What is your monthly Gross Salary in Kes per month?": "Salary"
}, inplace=True)

# Drop missing values in critical columns
df_cleaned = df.dropna(subset=["Gender", "Salary"])

# Function to clean salary values
def clean_salary(value):
    if isinstance(value, str):
        value = re.sub(r"[^\d.]", "", value)  # Remove non-numeric characters
        try:
            return float(value)
        except ValueError:
            return None
    return value

# Apply salary cleaning function
df_cleaned["Salary"] = df_cleaned["Salary"].apply(clean_salary)

# Drop rows where Salary couldn't be converted
df_cleaned = df_cleaned.dropna(subset=["Salary"])

# Standardize gender labels
df_cleaned["Gender"] = df_cleaned["Gender"].str.strip().str.capitalize()

# --- Salary Gap Analysis ---
st.subheader("💰 Salary Gap Analysis")

# Ensure at least one male and one female record exists
if "Male" in df_cleaned["Gender"].unique() and "Female" in df_cleaned["Gender"].unique():
    salary_gap = df_cleaned.groupby("Gender")["Salary"].mean()

    male_avg_salary = salary_gap.get("Male", 0)
    female_avg_salary = salary_gap.get("Female", 0)

    if male_avg_salary > 0:
        salary_gap_percentage = ((male_avg_salary - female_avg_salary) / male_avg_salary) * 100
    else:
        salary_gap_percentage = None

    # Display Salary Gap Percentage
    st.write(f"**Average Salary for Men:** KES {male_avg_salary:,.2f}")
    st.write(f"**Average Salary for Women:** KES {female_avg_salary:,.2f}")

    if salary_gap_percentage is not None:
        st.write(f"**Salary Gap:** Women earn **{abs(salary_gap_percentage):.2f}%** {'less' if salary_gap_percentage > 0 else 'more'} than men.")
    else:
        st.write("Salary gap could not be calculated.")

    # Visualization: Salary Comparison
    st.subheader("📊 Salary Comparison by Gender")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=salary_gap.index, y=salary_gap.values, palette=["pink", "blue"], ax=ax)
    ax.set_title("Average Salary Comparison by Gender")
    ax.set_ylabel("Average Salary (KES)")
    ax.set_xlabel("Gender")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

else:
    st.write("⚠️ Not enough gender data to compute salary gap.")

# --- Women in Leadership Representation ---
st.subheader("👩‍💼 Women in Leadership Roles")

# Define leadership roles to filter
leadership_roles = [
    "Manager eg Manager of Analytics",
    "Senior Level  eg Senior Data Analyst",
    "Lead eg Lead Analyst"
]

leadership_df = df_cleaned[df_cleaned["Job_Level"].isin(leadership_roles)]

# Gender distribution in leadership roles
leadership_gender_count = leadership_df["Gender"].value_counts(normalize=True) * 100  

# Display leadership representation
if not leadership_gender_count.empty:
    st.write("**Percentage of Women in Leadership Roles:**")
    st.write(leadership_gender_count)

    # Visualization: Leadership Representation
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.pie(
        leadership_gender_count, 
        labels=leadership_gender_count.index, 
        autopct="%1.1f%%", 
        colors=["pink", "blue"],
        startangle=140,
    )
    ax2.set_title("Gender Representation in Leadership Roles")
    st.pyplot(fig2)
else:
    st.write("⚠️ No leadership data available in the dataset.")

# Footer
st.markdown("---")
st.write("🔍 **Developed by:** Jemmimah Kavyu")
st.write("📅 **Project:** Gender Gap Analysis in Kenya Tech Industry")
