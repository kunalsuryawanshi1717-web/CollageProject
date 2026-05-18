import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from db import add_expense, get_expenses, delete_expense
import io

def expense_ui(page):
    username = st.session_state.username

    # Initialize monthly budget in session state
    if "monthly_budget" not in st.session_state:
        st.session_state.monthly_budget = 0.0

    # ----------------- ADD EXPENSE -----------------
    if page == "Add Expense":
        st.subheader("➕ Add Expense")

        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount (₹)", min_value=0.0)
        note = st.text_input("Note (Optional)")

        if st.button("Save Expense"):
            add_expense(username, str(date), category, amount, note)
            st.success("✅ Expense Added Successfully!")
            st.rerun()

    # ----------------- VIEW EXPENSES -----------------
    elif page == "View Expenses":
        st.subheader("📄 Your Expenses")

        data = get_expenses(username)

        if data:
            df = pd.DataFrame(data, columns=["ID", "User", "Date", "Category", "Amount", "Note"])
            df = df.drop(columns=["User"])

            # Filter by date range
            with st.expander("📅 Filter by Date Range"):
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                if st.button("Apply Filter"):
                    df["Date"] = pd.to_datetime(df["Date"])
                    df = df[(df["Date"] >= pd.Timestamp(start_date)) & (df["Date"] <= pd.Timestamp(end_date))]

            st.dataframe(df)

            # Export options
            st.download_button("📤 Export as CSV", df.to_csv(index=False), "expenses.csv", "text/csv")

            to_excel = io.BytesIO()
            with pd.ExcelWriter(to_excel, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Expenses")
            st.download_button("📥 Export as Excel", to_excel.getvalue(), "expenses.xlsx")

            # Delete expense
            delete_id = st.number_input("Enter Expense ID to delete", min_value=0, step=1)
            if st.button("Delete Expense"):
                if delete_id > 0:
                    delete_expense(int(delete_id))
                    st.success("🗑️ Expense Deleted Successfully!")
                    st.rerun()
        else:
            st.info("No expenses found.")

    # ----------------- ANALYTICS -----------------
    elif page == "Analytics":
        st.subheader("📊 Expense Analytics")

        data = get_expenses(username)

        if data:
            df = pd.DataFrame(data, columns=["ID", "User", "Date", "Category", "Amount", "Note"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Month"] = df["Date"].dt.to_period("M")

            # --- Dynamic Monthly Line Chart (Plotly) ---
            monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()
            st.subheader("📅 Monthly Expense Trend")

            if not monthly_summary.empty:
                monthly_summary["Month"] = monthly_summary["Month"].astype(str)
                monthly_summary = monthly_summary.sort_values("Month")

                fig = px.line(
                    monthly_summary,
                    x="Month",
                    y="Amount",
                    markers=True,
                    text="Amount",
                    title="📈 Monthly Expense Trend"
                )

                fig.update_traces(
                    line_color="#0073e6",
                    line_width=3,
                    texttemplate="₹%{y:.0f}",
                    textposition="top center",
                    marker=dict(size=9, color="#00bfa6", line=dict(width=2, color="#004d99"))
                )

                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Total Expense (₹)",
                    template="plotly_white",
                    hovermode="x unified",
                    title_font=dict(size=18, color="#0073e6"),
                    xaxis=dict(showgrid=True, gridcolor="lightgrey"),
                    yaxis=dict(showgrid=True, gridcolor="lightgrey"),
                    margin=dict(l=50, r=50, t=80, b=50)
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available to display monthly trend.")

            # --- Category-wise Spending (Matplotlib Bar Chart) ---
            st.subheader("📊 Category-wise Spending")
            summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

            if not summary.empty:
                fig, ax = plt.subplots(figsize=(8, 4))
                bars = ax.bar(summary.index, summary.values, color="#00bfa6")
                ax.set_xlabel("Category")
                ax.set_ylabel("Total Amount (₹)")
                ax.set_title("Spending by Category")
                ax.bar_label(bars, fmt="₹%.0f", padding=3)
                ax.grid(True, linestyle="--", alpha=0.3)
                st.pyplot(fig)
            else:
                st.info("No expenses found to display category chart.")

            # --- Monthly Budget Section ---
            st.subheader("💡 Monthly Budget")

            st.write(f"🎯 Current Budget: ₹{st.session_state.monthly_budget:.2f}")
            new_budget = st.number_input("Set New Monthly Budget", min_value=0.0)
            if st.button("Update Budget"):
                st.session_state.monthly_budget = new_budget
                st.success("✅ Budget Updated")

            # Budget Progress
            current_month = str(pd.Timestamp.now().to_period("M"))
            spent_this_month = df[df["Month"] == current_month]["Amount"].sum()

            if st.session_state.monthly_budget > 0:
                percent = (spent_this_month / st.session_state.monthly_budget) * 100
                st.progress(min(int(percent), 100))
                st.write(f"💰 You’ve spent ₹{spent_this_month:.2f} of ₹{st.session_state.monthly_budget:.2f} ({percent:.1f}%)")

                if percent > 80 and percent < 100:
                    st.warning("⚠ You’ve reached 80% of your monthly budget!")
                elif percent >= 100:
                    st.error("🚨 Budget limit exceeded!")
            else:
                st.info("Set a monthly budget to track your spending progress.")
        else:
            st.info("No expenses available for analysis.")
