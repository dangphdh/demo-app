"""Educational content and help documentation for Metric View Builder."""

EDUCATIONAL_CONTENT = {
    "what_is_metric_view": {
        "title": "What is a Metric View?",
        "icon": "📊",
        "content": """
        ## What is a Metric View?

        A **Metric View** is a centralized way to define and manage business metrics in Databricks.
        Think of it as a **smart, reusable view** that separates your **measures** (calculations)
        from your **dimensions** (grouping categories).

        ### Why Use Metric Views?

        **Traditional Views:**
        - Lock in both aggregations AND dimensions at creation time
        - Need separate views for each grouping
        - Can lead to metric inconsistency

        **Metric Views:**
        - Define metrics once, query by ANY dimension
        - Flexible analysis without redefining
        - Consistent metrics across the organization

        ### Example

        **Define once:**
        ```
        total_revenue = SUM(order_amount)
        unique_customers = COUNT(DISTINCT customer_id)
        ```

        **Query multiple ways:**
        ```sql
        -- Revenue by month
        SELECT month, MEASURE(total_revenue)
        FROM sales_metrics
        GROUP BY month

        -- Revenue by region
        SELECT region, MEASURE(total_revenue)
        FROM sales_metrics
        GROUP BY region

        -- Revenue by product
        SELECT product, MEASURE(total_revenue)
        FROM sales_metrics
        GROUP BY product
        ```

        ### Key Benefits

        ✅ **Consistency** - Same metric definition everywhere
        ✅ **Flexibility** - Group by any dimension at query time
        ✅ **Governance** - Managed in Unity Catalog
        ✅ **Performance** - Optimized query execution
        """
    },

    "understanding_dimensions": {
        "title": "Understanding Dimensions",
        "icon": "📏",
        "content": """
        ## What are Dimensions?

        **Dimensions** are categorical attributes that you use to **group and filter** your data.
        Think of them as the "BY" part of your analysis.

        ### Types of Dimensions

        **1. Column-Based Dimensions**
        Directly reference a column in your table:
        - `region` - Customer's geographic area
        - `product_category` - Type of product
        - `order_status` - Status of an order

        **2. Custom/Calculated Dimensions**
        Use SQL expressions to create derived dimensions:
        - `order_month` = `DATE_FORMAT(order_date, 'yyyy-MM')`
        - `price_tier` = `CASE WHEN price > 100 THEN 'High' ELSE 'Low' END`
        - `customer_age_group` = `FLOOR(DATEDIFF(day, birth_date, CURRENT_DATE) / 365)`

        ### Examples

        **Time-Based Dimensions:**
        ```
        order_date          → Direct column
        order_month         → DATE_FORMAT(order_date, 'yyyy-MM')
        order_quarter       → QUARTER(order_date)
        order_year          → YEAR(order_date)
        day_of_week         → DATE_FORMAT(order_date, 'EEEE')
        ```

        **String-Based Dimensions:**
        ```
        customer_region     → Direct column
        customer_segment     → Direct column
        product_category     → Direct column
        email_domain         → SUBSTRING(email, POSITION('@' IN email))
        ```

        **Bucketing Dimensions:**
        ```
        revenue_tier     → CASE
                             WHEN revenue < 1000 THEN 'Low'
                             WHEN revenue < 10000 THEN 'Medium'
                             ELSE 'High'
                           END
        ```

        ### Tips for Good Dimensions

        ✅ **Use meaningful names** - `order_month` not `om`
        ✅ **Add descriptions** - Document what the dimension represents
        ✅ **Consider cardinality** - Too many unique values = slow queries
        ✅ **Be consistent** - Use same naming across metric views
        """
    },

    "understanding_measures": {
        "title": "Understanding Measures",
        "icon": "📈",
        "content": """
        ## What are Measures?

        **Measures** are the actual calculations/metrics you want to perform.
        They use **aggregate functions** to summarize your data.

        ### Common Aggregate Functions

        **Basic Aggregates:**
        - `SUM(column)` - Total of all values
        - `COUNT(*)` - Number of rows
        - `COUNT(column)` - Number of non-null values
        - `AVG(column)` - Average value
        - `MIN(column)` - Minimum value
        - `MAX(column)` - Maximum value

        **Advanced Aggregates:**
        - `COUNT(DISTINCT column)` - Number of unique values
        - `STDDEV(column)` - Standard deviation
        - `VARIANCE(column)` - Statistical variance
        - `PERCENTILE(column, 0.5)` - Median

        ### Examples

        **Simple Measures:**
        ```
        total_revenue       = SUM(order_amount)
        order_count         = COUNT(*)
        average_order_value = AVG(order_amount)
        max_quantity        = MAX(quantity)
        ```

        **Distinct Counts:**
        ```
        unique_customers     = COUNT(DISTINCT customer_id)
        unique_products       = COUNT(DISTINCT product_id)
        active_days           = COUNT(DISTINCT order_date)
        ```

        **Ratios:**
        ```
        revenue_per_customer = SUM(revenue) / COUNT(DISTINCT customer_id)
        profit_margin         = SUM(profit) / SUM(revenue) * 100
        conversion_rate       = COUNT(CASE WHEN status = 'purchased' THEN 1 END)
                              * 100.0 / COUNT(*)
        ```

        **Conditional Aggregates:**
        ```
        high_value_orders    = SUM(CASE WHEN value > 1000 THEN value ELSE 0 END)
        fulfilled_orders     = COUNT(DISTINCT CASE
                             WHEN status = 'fulfilled' THEN order_id
                             END)
        ```

        ### Best Practices

        ✅ **Use descriptive names** - `total_revenue` not `sum1`
        ✅ **Handle division by zero** - Use CASE WHEN or NULLIF
        ✅ **Add descriptions** - Document what the measure calculates
        ✅ **Test your measures** - Verify results make sense

        ### Handling Division by Zero

        ❌ **Bad:**
        ```
        revenue_per_customer = SUM(revenue) / COUNT(DISTINCT customer_id)
        -- Fails if customer count is 0!
        ```

        ✅ **Good:**
        ```
        revenue_per_customer = SUM(revenue) / NULLIF(COUNT(DISTINCT customer_id), 0)
        -- Returns NULL instead of error
        ```

        ✅ **Also Good:**
        ```
        revenue_per_customer = CASE
          WHEN COUNT(DISTINCT customer_id) = 0 THEN 0
          ELSE SUM(revenue) / COUNT(DISTINCT customer_id)
        END
        -- Returns 0 instead of NULL
        ```
        """
    },

    "understanding_joins": {
        "title": "Understanding Joins",
        "icon": "🔗",
        "content": """
        ## What are Joins?

        **Joins** allow you to combine data from multiple tables. When creating a metric view
        with multiple sources, you need to specify how they relate to each other.

        ### Types of Joins

        **INNER JOIN** ← Default
        - Only matching rows from both tables
        - Use when: You only want data that exists in BOTH tables
        - Example: orders + customers (only orders with valid customer info)

        **LEFT JOIN**
        - All rows from left table + matching from right
        - Use when: Left table is primary, right is optional info
        - Example: orders + customer_tiers (all orders, tier if available)

        **RIGHT JOIN**
        - All rows from right table + matching from left
        - Use when: Right table is primary
        - Example: products + orders (all products, orders if available)

        **FULL JOIN**
        - All rows from both tables
        - Use when: You want everything from both tables
        - Example: customers + suppliers (all relationships)

        ### Example

        **Tables:**
        - `orders` - Order transactions
        - `customers` - Customer information
        - `products` - Product catalog

        **Joins:**
        ```
        orders.customer_id → customers.id (inner join)
        orders.product_id → products.id (inner join)
        ```

        **Result:**
        - One row per order
        - Enriched with customer details (region, segment, etc.)
        - Enriched with product details (category, name, etc.)

        ### Join Configuration

        For each join, you need:
        - **Left table** - Primary table
        - **Right table** - Table to join with
        - **Left key** - Column in left table (e.g., customer_id)
        - **Right key** - Column in right table (e.g., id)
        - **Join type** - inner, left, right, or full

        ### Best Practices

        ✅ **Start with INNER JOIN** - Most common use case
        ✅ **Join on indexed columns** - Better performance
        ✅ **Limit to 2-3 tables** - Keep it manageable
        ✅ **Validate join keys** - Ensure data types match
        ❌ **Avoid circular joins** - They cause errors

        ### Detecting Issues

        **Signs of join problems:**
        - Fewer rows than expected → Inner join filtering too much
        - More rows than expected → Need inner join, not full/left
        - Duplicate rows → Multiple join paths, need distinct
        - Very slow query → Missing indexes or circular joins
        """
    },

    "querying_metric_views": {
        "title": "Querying Metric Views",
        "icon": "🔍",
        "content": """
        ## How to Query Metric Views

        Once deployed, you query metric views using the special **MEASURE()** function.

        ### Basic Query Pattern

        ```sql
        SELECT
            dimension1,
            dimension2,
            MEASURE(measure_name) AS alias
        FROM catalog.schema.metric_view_name
        GROUP BY dimension1, dimension2
        ORDER BY dimension1
        ```

        ### Important Notes

        ⚠️ **No SELECT ***
        Metric views don't support `SELECT *` - you must specify columns explicitly

        ⚠️ **MEASURE() Function**
        All measures must be wrapped in `MEASURE()` function

        ⚠️ **No Runtime Joins**
        Can't join at query time - define joins in the metric view

        ### Examples

        **Single Dimension, Single Measure:**
        ```sql
        SELECT
            order_month,
            MEASURE(total_revenue) AS revenue
        FROM main.analytics.sales_metrics
        GROUP BY order_month
        ORDER BY order_month
        ```

        **Multiple Dimensions, Multiple Measures:**
        ```sql
        SELECT
            customer_region,
            product_category,
            MEASURE(total_revenue) AS revenue,
            MEASURE(order_count) AS orders,
            MEASURE(unique_customers) AS customers
        FROM main.analytics.sales_metrics
        GROUP BY customer_region, product_category
        ORDER BY revenue DESC
        ```

        **Filtering:**
        ```sql
        SELECT
            order_month,
            MEASURE(total_revenue) AS revenue
        FROM main.analytics.sales_metrics
        WHERE order_month >= '2024-01-01'
        GROUP BY order_month
        ORDER BY order_month
        ```

        **Time-Based Analysis:**
        ```sql
        -- Quarterly trend
        SELECT
            order_quarter,
            MEASURE(total_revenue) AS revenue,
            MEASURE(average_order_value) AS avg_order
        FROM main.analytics.sales_metrics
        WHERE order_quarter >= '2024-Q1'
        GROUP BY order_quarter
        ORDER BY order_quarter
        ```

        ### Using in BI Tools

        **Power BI:**
        - Connect via Databricks SQL endpoint
        - Metric views appear as tables
        - Drag dimensions to rows
        - Drag measures to values
        - Power BI automatically wraps measures in MEASURE()

        **Tableau:**
        - Use Databricks connector
        - Select your metric view
        - Dimensions go to Rows shelf
        - Measures go to Columns shelf

        **Looker:**
        - Native Databricks connection
        - Measures appear as dimensions in LookML
        - Use `measure: field_name` syntax

        **Databricks SQL:**
        - Query directly in SQL editor
        - Use MEASURE() function
        - Create visualizations from results

        ### Performance Tips

        ✅ **Limit dimensions** - Only group by what you need
        ✅ **Filter early** - Use WHERE clause before GROUP BY
        ✅ **Limit results** - Use LIMIT for testing
        ✅ **Use appropriate warehouse** - Size for your workload
        """
    },

    "troubleshooting": {
        "title": "Troubleshooting",
        "icon": "🔧",
        "content": """
        ## Common Issues and Solutions

        ### Issue 1: "Table not found"

        **Error:**
        ```
        Table not found: catalog.schema.table_name
        ```

        **Solutions:**
        - Check table name spelling
        - Verify you have access to the catalog/schema
        - Use Catalog Explorer to browse to the table
        - Check Unity Catalog permissions

        ### Issue 2: "Division by zero"

        **Error:**
        ```
        DIVISION_BY_ZERO error
        ```

        **Solution:**
        ```sql
        -- Wrap denominator in NULLIF or CASE
        measure = numerator / NULLIF(denominator, 0)
        -- OR
        measure = CASE WHEN denominator = 0 THEN 0
                    ELSE numerator / denominator
                END
        ```

        ### Issue 3: "Circular join detected"

        **Error:**
        ```
        Circular join: A → B → C → A
        ```

        **Solution:**
        - Remove one of the joins breaking the cycle
        - Reorganize your table relationships
        - Use 2 tables instead of 3

        ### Issue 4: "No results returned"

        **Possible Causes:**
        - INNER JOIN filtering too much → Try LEFT JOIN
        - WHERE clause too restrictive → Loosen filters
        - No data in date range → Check your data

        ### Issue 5: "Query very slow"

        **Solutions:**
        - Reduce number of dimensions
        - Add filters to reduce data volume
        - Check for circular joins
        - Use larger SQL warehouse
        - Check table has indexes on join columns

        ### Issue 6: "Wrong aggregation"

        **Example: Sum of averages is wrong**

        ❌ **Don't do this:**
        ```sql
        -- This is WRONG!
        SELECT
            SUM(AVG(order_amount))  -- Sum of averages
        FROM orders
        ```

        ✅ **Do this instead:**
        ```sql
        -- Calculate from raw data
        SUM(order_amount) / COUNT(DISTINCT order_id)
        ```

        ### Getting Help

        **Documentation:**
        - [Databricks Metric Views](https://docs.databricks.com/aws/en/metric-views/)
        - [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)

        **Community:**
        - [Databricks Community](https://community.databricks.com/)
        - Stack Overflow: Tag with `databricks` and `metric-views`

        **Support:**
        - Contact your Databricks admin
        - Check Databricks status page
        - Review SQL warehouse logs
        """
    },

    "best_practices": {
        "title": "Best Practices",
        "icon": "⭐",
        "content": """
        ## Metric View Best Practices

        ### Design Principles

        **1. Start Simple**
        - Begin with 1 table, 2-3 dimensions, 1-2 measures
        - Add complexity gradually
        - Test at each step

        **2. Use Meaningful Names**
        ✅ `total_revenue`, `average_order_value`
        ❌ `sum1`, `measure2`, `calculation_3`

        **3. Document Everything**
        - Add descriptions to dimensions
        - Add descriptions to measures
        - Comment your custom expressions

        **4. Validate Your Work**
        - Use the built-in validator
        - Test queries with sample data
        - Check measure calculations make sense

        ### Naming Conventions

        **Dimensions:**
        - Use lowercase with underscores: `order_date`, `customer_region`
        - Prefix with source if ambiguous: `customer_region`, `product_region`
        - Date/time suffixes: `_date`, `_month`, `_quarter`, `_year`

        **Measures:**
        - Use descriptive action names: `total_`, `average_`, `count_of_`, `unique_`
        - Examples: `total_revenue`, `average_order_value`, `unique_customers`

        ### Performance Tips

        **Optimize Dimensions:**
        - Keep cardinality reasonable (< 1000 unique values)
        - Avoid high-cardinality columns (like IDs)
        - Use calculated dimensions for bucketing

        **Optimize Measures:**
        - Pre-filter in WHERE clause, not in measure
        - Use COUNT(DISTINCT) sparingly
        - Avoid nested aggregations

        **Optimize Joins:**
        - Join on indexed columns
        - Start with INNER JOIN, use others only when needed
        - Limit to 2-3 tables maximum

        ### Governance

        **Ownership:**
        - Assign metric owners
        - Document business purpose
        - Review and approve changes

        **Versioning:**
        - Track metric view versions
        - Document what changed and why
        - Communicate changes to consumers

        **Testing:**
        - Validate calculations against source data
        - Test with various dimension combinations
        - Performance test with realistic data volumes

        ### Examples to Follow

        **Good Metric View:**
        - Clear purpose (documented)
        - 1-3 sources (join when needed)
        - 3-7 dimensions (grouping flexibility)
        - 3-5 measures (core KPIs)
        - Descriptive names
        - Comprehensive documentation

        **Needs Improvement:**
        - Vague purpose
        - Too many sources (>3)
        - Too many dimensions (>10)
        - Complex nested measures
        - Cryptic names
        - No documentation
        """
    }
}


def get_help_content(topic: str) -> dict:
    """Get help content for a topic.

    Args:
        topic: Topic key (e.g., 'what_is_metric_view')

    Returns:
        Dictionary with title, icon, and content
    """
    return EDUCATIONAL_CONTENT.get(topic, {
        "title": "Help Not Found",
        "icon": "❓",
        "content": f"No help content available for '{topic}'"
    })


def list_help_topics() -> list:
    """List all available help topics.

    Returns:
        List of topic keys
    """
    return list(EDUCATIONAL_CONTENT.keys())


def render_help_center():
    """Render the help center UI in Streamlit."""
    st.title("📚 Help Center")

    # Search
    search = st.text_input("Search for help...", placeholder="e.g., measures, joins, querying")

    # List topics
    topics = list_help_topics()

    if search:
        # Filter topics by search term
        search_lower = search.lower()
        topics = [
            t for t in topics
            if search_lower in t.lower() or
            search_lower in EDUCATIONAL_CONTENT[t]["title"].lower()
        ]

    # Display topics
    for topic_key in topics:
        content = get_help_content(topic_key)

        with st.expander(f"{content['icon']} {content['title']}"):
            st.markdown(content["content"])
