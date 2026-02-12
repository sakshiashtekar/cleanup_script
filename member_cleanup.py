import pandas as pd
import re

df = pd.read_excel("signups_clean.xlsx")

if len(df.columns) == 1:
    df = df.iloc[:, 0].str.split(",", expand=True)

if df.shape[1] > 5:
    df[0] = df[0] + ", " + df[1]
    df = df.drop(columns=[1]).reset_index(drop=True)

df.columns = ["name", "email", "signup_date", "plan", "notes"]

df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["signup_date"] = df["signup_date"].dt.strftime("%Y-%m-%d")

def is_low_quality(row):
    test_patterns = ["test", "asdf", "qwerty", "dummy"]
    name = str(row["name"]).lower()
    email = str(row["email"]).lower()

    if any(pattern in name for pattern in test_patterns):
        return True
    if any(pattern in email for pattern in test_patterns):
        return True
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    if pd.isna(row["email"]) or pd.isna(row["signup_date"]):
        return True
    return False

df["is_low_quality"] = df.apply(is_low_quality, axis=1)

quarantine = df[df["is_low_quality"]].copy()
clean_df = df[~df["is_low_quality"]].copy()

quarantine.to_csv("quarantine.csv", index=False)

plan_counts = clean_df.groupby("email")["plan"].nunique()
multi_plan_emails = plan_counts[plan_counts > 1].index

clean_df["is_multi_plan"] = clean_df["email"].isin(multi_plan_emails)

clean_df["signup_date"] = pd.to_datetime(clean_df["signup_date"])
clean_df = clean_df.sort_values("signup_date", ascending=False)
clean_df = clean_df.drop_duplicates(subset=["email"], keep="first")
clean_df["signup_date"] = clean_df["signup_date"].dt.strftime("%Y-%m-%d")

clean_df = clean_df.drop(columns=["is_low_quality"])

clean_df.to_csv("members_final.csv", index=False)

print("Cleanup complete")
