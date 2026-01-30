"""Interactive tutorial for first-time users."""

import streamlit as st
from typing import List, Dict
from datetime import datetime


class TutorialStep:
    """Represents a single tutorial step."""

    def __init__(
        self,
        step_id: str,
        title: str,
        content: str,
        action_type: str = "info",
        checkpoint: bool = False
    ):
        self.step_id = step_id
        self.title = title
        self.content = content
        self.action_type = action_type  # info, action, quiz
        self.checkpoint = checkpoint


class InteractiveTutorial:
    """Interactive tutorial for Metric View Builder."""

    def __init__(self):
        """Initialize the tutorial."""
        self.steps = self._create_steps()
        self.current_step = 0

    def _create_steps(self) -> List[TutorialStep]:
        """Create tutorial steps.

        Returns:
            List of TutorialStep objects
        """
        return [
            TutorialStep(
                "welcome",
                "Welcome to Metric View Builder! 👋",
                """
                **What are we going to learn?**

                In this tutorial, you'll learn how to create a **Databricks Metric View** - a powerful
                way to define business metrics that can be used consistently across your organization.

                **What is a Metric View?**

                A Metric View is like a smart view that separates **measures** (calculations like SUM, COUNT)
                from **dimensions** (categories like region, product, time). This means you define
                your metrics once, then can group them by ANY dimension at query time!

                **Example:**
                - Define: `total_revenue = SUM(order_amount)`
                - Query by: day, week, month, region, product - whatever you need!
                - No need to redefine the metric for each grouping.

                **Tutorial Duration:** ~10 minutes

                **Prerequisites:**
                - Databricks workspace access
                - Basic understanding of tables and columns

                Let's get started!
                """,
                "info"
            ),

            TutorialStep(
                "connect",
                "Step 1: Connect to Databricks 🔌",
                """
                **Why Connect?**

                To create metric views, we need access to your Databricks workspace so we can:
                - Browse your data catalog
                - Select tables to use
                - Preview column information

                **How to Connect:**

                1. Look at the **sidebar** on the left
                2. You'll see connection options
                3. Choose one:
                   - **Service Account**: If your admin configured one
                   - **User Credentials**: Your personal Databricks token

                **Getting Your Token:**
                - Go to your Databricks workspace
                - Click your name → Settings → Developer
                - Generate a new personal access token
                - Copy and paste it into the sidebar

                **SQL Warehouse ID:**
                - Go to SQL → SQL Warehouses in Databricks
                - Click on your warehouse
                - Copy the Warehouse ID from the details panel

                ✅ **Action:** Connect to Databricks using the sidebar, then click "I'm Connected" below.
                """,
                "action",
                checkpoint=True
            ),

            TutorialStep(
                "understand_components",
                "Step 2: Understand the Components 🧩",
                """
                **Metric Views Have 4 Main Parts:**

                **1. Sources (Tables) 📊**
                - The tables containing your data
                - Can be one table or multiple joined tables
                - Example: `orders`, `customers`, `products`

                **2. Dimensions (Grouping) 📏**
                - Categories you want to group BY
                - Examples: date, region, product category, customer segment
                - Can be direct columns OR calculated values

                **3. Measures (Calculations) 📈**
                - The actual metrics you want to calculate
                - Use aggregate functions: SUM, COUNT, AVG, MIN, MAX
                - Examples: total_revenue, order_count, average_order_value

                **4. Joins (Connections) 🔗**
                - How to connect multiple tables
                - Define primary/foreign key relationships
                - Example: orders.customer_id → customers.id

                **Quick Quiz:** 📝

                Which of these would be a good **measure**?
                - A) Customer region
                - B) Total revenue (SUM of all order amounts)
                - C) Product category

                **Answer:** B! It's a calculation (aggregation).
                A and C are dimensions (categories).

                Click "Next" when you're ready to see a real example!
                """,
                "quiz"
            ),

            TutorialStep(
                "example",
                "Step 3: See a Real Example 💡",
                """
                **Let's Look at a Complete Example:**

                **Sales Metrics Metric View**

                **Sources:**
                - `orders` table (transaction data)
                - `customers` table (customer info)
                - `products` table (product catalog)

                **Joins:**
                - orders.customer_id → customers.id
                - orders.product_id → products.id

                **Dimensions:**
                - `order_date` - When the order was placed
                - `customer_region` - Customer's geographic region
                - `product_category` - Type of product
                - `order_month` - Extracted from date (custom)

                **Measures:**
                - `total_revenue` = SUM(order_amount)
                - `order_count` = COUNT(*)
                - `unique_customers` = COUNT(DISTINCT customer_id)
                - `avg_order_value` = AVG(order_amount)
                - `revenue_per_customer` = SUM(order_amount) / COUNT(DISTINCT customer_id)

                **Why This is Powerful:**

                Once defined, you can query:

                ```sql
                -- Revenue by month
                SELECT order_month, MEASURE(total_revenue)
                FROM sales_metrics
                GROUP BY order_month

                -- Revenue by region
                SELECT customer_region, MEASURE(total_revenue)
                FROM sales_metrics
                GROUP BY customer_region

                -- Revenue by product category
                SELECT product_category, MEASURE(total_revenue)
                FROM sales_metrics
                GROUP BY product_category
                ```

                Same metric view, flexible analysis! 🎉

                Click "Next" to learn how to create your own!
                """,
                "info"
            ),

            TutorialStep(
                "wizard_intro",
                "Step 4: Meet the Wizard 🧙‍♂️",
                """
                **The Wizard is Your Guide!**

                The Metric View Builder has a **6-step wizard** that guides you through
                creating your first metric view:

                1. **Connect** 🔌 - Connect to your Databricks workspace
                2. **Sources** 📊 - Select the tables you need
                3. **Joins** 🔗 - Connect tables if using multiple tables
                4. **Dimensions** 📏 - Define how you want to group data
                5. **Measures** 📈 - Define what you want to calculate
                6. **Review** ✅ - Preview and generate your YAML

                **Key Features:**
                - **Progress bar** shows where you are
                - **Previous/Next** buttons to navigate
                - **Validation** catches errors before you finish
                - **Live YAML preview** shows what you're building

                **Tips:**
                - Use the **Help** buttons (❓) throughout for guidance
                - You can go **back** to change anything
                - Your work is **auto-saved** as you go
                - Download YAML anytime, even if incomplete

                Ready to try it out?

                ✅ **Action:** Click the "Create New" button on the home page to start the wizard!
                """,
                "action",
                checkpoint=True
            ),

            TutorialStep(
                "templates",
                "Step 5: Start with Templates 🎨",
                """
                **Templates Are Your Friends!**

                Don't want to start from scratch? No problem!

                We have **3 pre-built templates** to help you get started fast:

                **1. 💰 Sales Revenue**
                - Track sales performance
                - Dimensions: date, region, product, customer segment
                - Measures: revenue, orders, customers, average order value
                - Perfect for: Sales dashboards, revenue reports

                **2. 📦 Order Analytics**
                - Monitor order pipeline
                - Dimensions: status, priority, shipping method
                - Measures: orders, fulfillment rate, open orders value
                - Perfect for: Operations teams, order tracking

                **3. 👥 Customer Metrics**
                - Understand customer value
                - Dimensions: tier, channel, region
                - Measures: customers, lifetime value, repeat purchase rate
                - Perfect for: Marketing, customer analytics

                **Using Templates:**

                Templates give you a **complete starting point**:
                - All sources defined
                - Joins configured
                - Dimensions and measures pre-built
                - Just customize the table names to match your data!

                ✅ **Action:** Go to the **Load/Edit** page and explore the templates!
                """,
                "info"
            ),

            TutorialStep(
                "next_steps",
                "Step 6: What's Next? 🚀",
                """
                **Congratulations! 🎉**

                You now know the basics of Metric Views!

                **Your Next Steps:**

                1. **Create Your First Metric View**
                   - Use the Wizard with your own data
                   - Start simple - one table, a few dimensions, one measure
                   - Download the YAML

                2. **Deploy to Databricks**
                   - Use the Deploy page
                   - Follow the manual deployment instructions
                   - Query your new metric view!

                3. **Explore Advanced Features**
                   - Custom dimensions with SQL expressions
                   - Complex measures (ratios, distinct counts)
                   - Multiple table joins
                   - Save and load your work

                **Helpful Resources:**

                - 📖 **Databricks Documentation:** [Metric Views](https://docs.databricks.com/aws/en/metric-views/)
                - 💡 **Templates page:** Start from pre-built examples
                - ✏️ **Editor page:** Load, edit, and save your work
                - 🚀 **Deploy page:** Export and deploy to Databricks

                **Remember:**
                - Start simple, then add complexity
                - Use templates to learn by example
                - Your work is auto-saved
                - Download YAML anytime

                **You're Ready!** 🚀

                Go create your first metric view now!
                """,
                "info",
                checkpoint=True
            )
        ]

    def get_current_step(self) -> TutorialStep:
        """Get current tutorial step.

        Returns:
            Current TutorialStep
        """
        return self.steps[self.current_step]

    def next_step(self):
        """Move to next step."""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            return True
        return False

    def previous_step(self):
        """Move to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False

    def is_complete(self) -> bool:
        """Check if tutorial is complete.

        Returns:
            True if on last step
        """
        return self.current_step == len(self.steps) - 1


def render_tutorial():
    """Render the interactive tutorial in Streamlit."""
    st.title("🎓 Interactive Tutorial")

    # Initialize tutorial in session state
    if "tutorial" not in st.session_state:
        st.session_state.tutorial = InteractiveTutorial()

    tutorial = st.session_state.tutorial
    step = tutorial.get_current_step()

    # Progress bar
    progress = (tutorial.current_step + 1) / len(tutorial.steps)
    st.progress(progress)
    st.caption(f"Step {tutorial.current_step + 1} of {len(tutorial.steps)}")

    # Step content
    st.markdown(f"### {step.title}")

    # Render content based on type
    if step.action_type == "info":
        st.markdown(step.content)

    elif step.action_type == "action":
        st.markdown(step.content)

        if step.checkpoint:
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Completed", type="primary", use_container_width=True):
                    if tutorial.next_step():
                        st.rerun()

            with col2:
                st.info("💡 Tip: Come back anytime to review!")

    elif step.action_type == "quiz":
        st.markdown(step.content)

        if step.checkpoint:
            st.markdown("---")
            if st.button("Next →", type="primary"):
                if tutorial.next_step():
                    st.rerun()

    # Navigation buttons at bottom
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if tutorial.current_step > 0:
            if st.button("⬅️ Previous"):
                tutorial.previous_step()
                st.rerun()

    with col2:
        st.markdown(f"<div style='text-align: center;'>{tutorial.current_step + 1} / {len(tutorial.steps)}</div>",
                    unsafe_allow_html=True)

    with col3:
        if not tutorial.is_complete():
            if st.button("Next ➡️", type="primary"):
                tutorial.next_step()
                st.rerun()
        else:
            st.success("🎉 Tutorial Complete!")
            if st.button("🏠 Back to Home"):
                st.switch_page("pages/0_welcome.py")


def render_tutorial_button():
    """Render a button to start the tutorial."""
    if st.button("🎓 Take Tutorial", use_container_width=True):
        # Switch to tutorial
        # For now, we'll show it inline in the main app
        st.session_state.show_tutorial = True
        st.rerun()


def show_tutorial_if_active():
    """Show tutorial if activated in session state."""
    if st.session_state.get("show_tutorial", False):
        st.markdown("---")
        render_tutorial()

        if st.button("❌ Close Tutorial"):
            st.session_state.show_tutorial = False
            st.rerun()
