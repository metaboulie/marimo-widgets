import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __():
    from mowidget.layout.header import NotebookHeader

    return (NotebookHeader,)


@app.cell
def __(mo) -> None:
    mo.md(r"""## Testing NotebookHeader""")


@app.cell
def __(mo) -> None:
    mo.md(r"""test standard format""")


@app.cell(hide_code=True)
def __(NotebookHeader) -> None:
    NotebookHeader(
        metadata={
            "Title": "Comprehensive E-Commerce Customer Behavior Analysis",
            "Author": '<a href="https://github.com/Haleshot/marimo-tutorials">Dr. Jane Smith, PhD</a>',
            "Affiliation": '<a href="https://www.datascience.university.edu">University of Data Science</a>',
            "Version": "1.2.3.4",
            "Description": "This advanced notebook presents a multi-faceted analysis of <b>customer behavior patterns</b> across various e-commerce platforms. The primary goal is to derive actionable insights that can significantly enhance customer engagement, optimize conversion rates, and ultimately drive business growth in the competitive e-commerce landscape.",
            "Keywords": "E-Commerce Analytics, Customer Behavior Modeling, Predictive Analytics, Machine Learning, Natural Language Processing, Data Visualization, Time Series Analysis",
            "Data Sources": "1. Customer transaction logs (5 years, 10M+ records)<br>2. Website clickstream data (real-time, 1B+ events)<br>3. CRM records (customer demographics, purchase history)<br>4. Social media interactions (Twitter, Facebook, Instagram)<br>5. Customer support tickets and chat logs<br>6. Product catalog and inventory data",
            "Prerequisites": "Intermediate to advanced knowledge in statistics, machine learning, and Python programming. Familiarity with e-commerce concepts and business metrics is beneficial.",
            "Acknowledgements": "This work was supported by a grant from the National Science Foundation (NSF-1234567). Special thanks to the E-Commerce Research Consortium for providing anonymized datasets.",
            "License": '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>',
            "Last Updated": "November 3, 2024",
        },
        banner="https://raw.githubusercontent.com/Haleshot/marimo-tutorials/main/community-tutorials-banner.png",
    )


@app.cell
def __(mo) -> None:
    mo.md(r"""test with no banner""")


@app.cell(hide_code=True)
def __(NotebookHeader) -> None:
    NotebookHeader(
        metadata={
            "Title": "Comprehensive E-Commerce Customer Behavior Analysis",
            "Author": '<a href="https://github.com/Haleshot/marimo-tutorials">Dr. Jane Smith, PhD</a>',
            "Affiliation": '<a href="https://www.datascience.university.edu">University of Data Science</a>',
            "Version": "1.2.3.4",
            "Description": "This advanced notebook presents a multi-faceted analysis of <b>customer behavior patterns</b> across various e-commerce platforms. The primary goal is to derive actionable insights that can significantly enhance customer engagement, optimize conversion rates, and ultimately drive business growth in the competitive e-commerce landscape.",
            "Keywords": "E-Commerce Analytics, Customer Behavior Modeling, Predictive Analytics, Machine Learning, Natural Language Processing, Data Visualization, Time Series Analysis",
            "Data Sources": "1. Customer transaction logs (5 years, 10M+ records)<br>2. Website clickstream data (real-time, 1B+ events)<br>3. CRM records (customer demographics, purchase history)<br>4. Social media interactions (Twitter, Facebook, Instagram)<br>5. Customer support tickets and chat logs<br>6. Product catalog and inventory data",
            "Prerequisites": "Intermediate to advanced knowledge in statistics, machine learning, and Python programming. Familiarity with e-commerce concepts and business metrics is beneficial.",
            "Acknowledgements": "This work was supported by a grant from the National Science Foundation (NSF-1234567). Special thanks to the E-Commerce Research Consortium for providing anonymized datasets.",
            "License": '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>',
            "Last Updated": "November 3, 2024",
        },
    )


@app.cell
def __(mo) -> None:
    mo.md(r"""test metadata auto-refresh""")


@app.cell
def __(mo):
    version = mo.ui.text(value="0.1.0")
    version
    return (version,)


@app.cell
def __(NotebookHeader, version) -> None:
    NotebookHeader(
        metadata={
            "Title": "Comprehensive E-Commerce Customer Behavior Analysis",
            "Author": '<a href="https://github.com/Haleshot/marimo-tutorials">Dr. Jane Smith, PhD</a>',
            "Affiliation": '<a href="https://www.datascience.university.edu">University of Data Science</a>',
            "Version": version.value,
        },
    )


if __name__ == "__main__":
    app.run()
