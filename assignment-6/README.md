# 🏠 Unlocking Real Estate Value: Exploratory Data Analysis of House Prices

## 📊 Project Overview
This project performs an Exploratory Data Analysis (EDA) on the Ames Housing dataset to identify the key factors influencing house prices. The analysis includes data inspection, cleaning, transformation, multivariate analysis, and business insights to better understand property value drivers.

The goal is to uncover meaningful patterns in housing data and translate them into actionable insights for decision-making and future predictive modeling.

---

## 🎯 Objectives
- Understand the dataset structure and feature types
- Analyze the distribution of the target variable (SalePrice)
- Detect and remove outliers using the IQR method
- Identify key factors affecting house prices
- Explore relationships between features
- Generate business insights through visualizations

---

## 📁 Dataset
**Source:** Kaggle — House Prices: Advanced Regression Techniques  

The dataset contains information about residential homes including property characteristics, location, quality ratings, and sale prices.

---

## 🧪 Analysis Workflow

### Phase 1 — Data Inspection
- Loaded dataset and examined structure
- Categorized numerical and categorical features
- Analyzed SalePrice distribution
- Applied log transformation to normalize target variable

### Phase 2 — Data Cleaning
- Detected outliers using the Interquartile Range (IQR)
- Removed extreme SalePrice values
- Visualized impact using boxplots

### Phase 3 — Multivariate Analysis
- Generated correlation matrix heatmap
- Identified top features correlated with SalePrice
- Analyzed relationship between OverallQual and SalePrice
- Performed neighborhood price comparison

### Phase 4 — Insights & Reporting
- Identified top drivers of house prices
- Reviewed missing data impact
- Summarized key visual insights

---

## 🔑 Key Findings

### Top Drivers of Price
- Overall Quality (OverallQual)
- Living Area (GrLivArea)
- Garage Capacity (GarageCars)

### Location Impact
The neighborhood **NoRidge** has the highest average house prices, indicating it is the most premium area in the dataset.

### Distribution Insights
SalePrice was highly right-skewed and became approximately normal after log transformation.

### Outlier Insights
IQR filtering removed extreme high-price outliers, resulting in a more compact distribution.

---

## 📈 Key Visualizations
- SalePrice Distribution Histogram
- Log-transformed Q-Q Plot
- Boxplot Before and After Outlier Removal
- Correlation Heatmap
- OverallQual vs SalePrice Boxplot
- Neighborhood Average Price Bar Chart

---

## ⚠️ Missing Data Considerations
Features such as PoolQC, Alley, Fence, and MiscFeature contain significant missing values, often representing absence of the feature. These will require careful handling during modeling.

---

## 🛠️ Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy

---

## ⚙️ Environment Setup

### Using Conda (Recommended)

```bash
conda create -n pandaenv python=3.11 -y
conda activate pandaenv
pip install -r requirements.txt
```

### Using pip only

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Project

1. Clone the repository

```bash
git clone <your-repo-link>
```

2. Navigate into project folder

```bash
cd <project-folder>
```

3. Open the notebook

```
main.ipynb
```

4. Run all cells sequentially

---

## 📌 Project Structure

```
├── data/
│   ├── train.csv
│   ├── test.csv
│   ├── data_description.txt
│
├── main.ipynb
├── requirements.txt
└── README.md
```

---

## 🧠 Business Insights
The analysis confirms that house prices are primarily driven by quality, size, amenities, and location. These insights can support real estate valuation, pricing strategy, and predictive modeling.

---

## 🚀 Future Work
- Feature engineering
- Build regression models
- Hyperparameter tuning
- Model evaluation
- Deployment

---

## 👤 Author
Riasat Raihan Noor  

---

## 📜 License
This project is for educational and research purposes.