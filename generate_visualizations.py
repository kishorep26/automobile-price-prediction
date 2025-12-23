import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import json
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('dark_background')
sns.set_palette("husl")

# Create output directory
import os
os.makedirs('static/visualizations', exist_ok=True)

# Load the dataset
df = pd.read_csv('Automobile price data _Raw_.csv')
df = df.replace('?', np.nan)

# Handle missing values
numeric_cols = ['normalized-losses', 'bore', 'stroke', 'horsepower', 'peak-rpm', 'price']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(df[col].mean(), inplace=True)

# Load model stats
with open('model_stats.pkl', 'rb') as f:
    model_stats = pickle.load(f)

# 1. Feature Importance Plot
print("Generating feature importance plot...")
feature_importance = model_stats['feature_importance']
sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:15]
features, importances = zip(*sorted_features)

plt.figure(figsize=(12, 8))
colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(features)))
bars = plt.barh(range(len(features)), importances, color=colors)
plt.yticks(range(len(features)), features)
plt.xlabel('Importance Score', fontsize=12, fontweight='bold')
plt.title('Top 15 Features Influencing Car Price', fontsize=16, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('static/visualizations/feature_importance.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()

# 2. Correlation Heatmap
print("Generating correlation heatmap...")
numeric_features = ['wheel-base', 'length', 'width', 'height', 'curb-weight', 
                   'engine-size', 'bore', 'stroke', 'compression-ratio', 
                   'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price']
corr_df = df[numeric_features].corr()

plt.figure(figsize=(14, 12))
mask = np.triu(np.ones_like(corr_df, dtype=bool))
sns.heatmap(corr_df, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Feature Correlation Matrix\nHow Different Car Attributes Relate to Each Other', 
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('static/visualizations/correlation_heatmap.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()

# 3. Price Distribution
print("Generating price distribution plot...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
ax1.hist(df['price'], bins=30, color='#ff6b6b', alpha=0.7, edgecolor='white')
ax1.axvline(df['price'].mean(), color='#4ecdc4', linestyle='--', linewidth=2, label=f'Mean: ${df["price"].mean():.0f}')
ax1.axvline(df['price'].median(), color='#ffe66d', linestyle='--', linewidth=2, label=f'Median: ${df["price"].median():.0f}')
ax1.set_xlabel('Price ($)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('Distribution of Automobile Prices', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3, linestyle='--')

# Box plot
bp = ax2.boxplot(df['price'], vert=True, patch_artist=True, widths=0.5)
bp['boxes'][0].set_facecolor('#ff6b6b')
bp['boxes'][0].set_alpha(0.7)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp[element], color='white', linewidth=2)
ax2.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
ax2.set_title('Price Range & Outliers', fontsize=14, fontweight='bold')
ax2.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('static/visualizations/price_distribution.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()

# 4. Key Features vs Price
print("Generating scatter plots...")
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
key_features = ['engine-size', 'horsepower', 'curb-weight', 'highway-mpg', 'length', 'width']
colors_scatter = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#95e1d3', '#f38181', '#aa96da']

for idx, (feature, color) in enumerate(zip(key_features, colors_scatter)):
    ax = axes[idx // 3, idx % 3]
    ax.scatter(df[feature], df['price'], alpha=0.6, s=50, color=color, edgecolors='white', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(df[feature].dropna(), df[df[feature].notna()]['price'], 1)
    p = np.poly1d(z)
    ax.plot(df[feature].sort_values(), p(df[feature].sort_values()), 
            "r--", alpha=0.8, linewidth=2, label='Trend')
    
    ax.set_xlabel(feature.replace('-', ' ').title(), fontsize=11, fontweight='bold')
    ax.set_ylabel('Price ($)', fontsize=11, fontweight='bold')
    ax.set_title(f'{feature.replace("-", " ").title()} Impact on Price', fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend()

plt.tight_layout()
plt.savefig('static/visualizations/features_vs_price.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()

# 5. Categorical Features Analysis
print("Generating categorical analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Body style
body_style_prices = df.groupby('body-style')['price'].mean().sort_values(ascending=False)
axes[0, 0].barh(range(len(body_style_prices)), body_style_prices.values, 
                color=plt.cm.plasma(np.linspace(0.2, 0.8, len(body_style_prices))))
axes[0, 0].set_yticks(range(len(body_style_prices)))
axes[0, 0].set_yticklabels(body_style_prices.index)
axes[0, 0].set_xlabel('Average Price ($)', fontweight='bold')
axes[0, 0].set_title('Average Price by Body Style', fontsize=14, fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3, linestyle='--')

# Fuel type
fuel_prices = df.groupby('fuel-type')['price'].mean().sort_values(ascending=False)
axes[0, 1].bar(range(len(fuel_prices)), fuel_prices.values, 
               color=['#ff6b6b', '#4ecdc4'])
axes[0, 1].set_xticks(range(len(fuel_prices)))
axes[0, 1].set_xticklabels(fuel_prices.index, rotation=0)
axes[0, 1].set_ylabel('Average Price ($)', fontweight='bold')
axes[0, 1].set_title('Average Price by Fuel Type', fontsize=14, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3, linestyle='--')

# Drive wheels
drive_prices = df.groupby('drive-wheels')['price'].mean().sort_values(ascending=False)
axes[1, 0].barh(range(len(drive_prices)), drive_prices.values, 
                color=['#ffe66d', '#95e1d3', '#f38181'])
axes[1, 0].set_yticks(range(len(drive_prices)))
axes[1, 0].set_yticklabels(drive_prices.index)
axes[1, 0].set_xlabel('Average Price ($)', fontweight='bold')
axes[1, 0].set_title('Average Price by Drive Wheels', fontsize=14, fontweight='bold')
axes[1, 0].grid(axis='x', alpha=0.3, linestyle='--')

# Make (top 10)
make_prices = df.groupby('make')['price'].mean().sort_values(ascending=False).head(10)
axes[1, 1].barh(range(len(make_prices)), make_prices.values, 
                color=plt.cm.viridis(np.linspace(0.2, 0.9, len(make_prices))))
axes[1, 1].set_yticks(range(len(make_prices)))
axes[1, 1].set_yticklabels(make_prices.index)
axes[1, 1].set_xlabel('Average Price ($)', fontweight='bold')
axes[1, 1].set_title('Top 10 Most Expensive Car Brands', fontsize=14, fontweight='bold')
axes[1, 1].grid(axis='x', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('static/visualizations/categorical_analysis.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()

# 6. Model Performance Visualization
print("Generating model performance plot...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Accuracy comparison
metrics = ['Training\nAccuracy', 'Testing\nAccuracy']
scores = [model_stats['train_score'] * 100, model_stats['test_score'] * 100]
colors_bar = ['#4ecdc4', '#ff6b6b']

bars = ax1.bar(metrics, scores, color=colors_bar, alpha=0.8, edgecolor='white', linewidth=2)
ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax1.set_title('Model Performance Metrics', fontsize=14, fontweight='bold')
ax1.set_ylim([0, 100])
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bar, score in zip(bars, scores):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{score:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')

# Feature importance pie (top 5)
top_5_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
other_importance = sum([v for k, v in feature_importance.items() if k not in dict(top_5_features)])
labels = [k.replace('-', ' ').title() for k, v in top_5_features] + ['Others']
sizes = [v for k, v in top_5_features] + [other_importance]
colors_pie = plt.cm.Set3(np.linspace(0, 1, len(sizes)))

wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90,
                                     textprops={'fontsize': 10, 'fontweight': 'bold'})
ax2.set_title('Top 5 Features Contribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('static/visualizations/model_performance.png', dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
plt.close()

# Helper functions
def get_feature_description(feature):
    descriptions = {
        'curb-weight': 'Heavier vehicles often indicate luxury or larger size, commanding higher prices',
        'engine-size': 'Larger engines typically mean more power and performance, increasing value',
        'horsepower': 'Higher horsepower directly correlates with performance and price',
        'width': 'Wider vehicles often indicate luxury or sports models',
        'length': 'Longer vehicles may indicate luxury sedans or SUVs',
        'highway-mpg': 'Better fuel efficiency can increase value, especially for economy cars',
        'city-mpg': 'Urban fuel efficiency is a key factor for daily drivers',
        'bore': 'Engine bore affects displacement and power output',
        'wheel-base': 'Longer wheelbase often indicates larger, more expensive vehicles',
        'height': 'Vehicle height affects aerodynamics and utility'
    }
    return descriptions.get(feature, 'This feature contributes to the overall vehicle valuation')

def get_strongest_correlation(corr_matrix, target, positive=True):
    correlations = corr_matrix[target].drop(target).sort_values(ascending=not positive)
    strongest = correlations.iloc[0] if positive else correlations.iloc[-1]
    return {
        "feature": correlations.index[0] if positive else correlations.index[-1],
        "value": float(strongest)
    }

# Generate insights JSON
insights = {
    "top_features": [
        {
            "name": feature.replace('-', ' ').title(),
            "importance": float(importance),
            "description": get_feature_description(feature)
        }
        for feature, importance in sorted_features[:5]
    ],
    "price_stats": {
        "mean": float(df['price'].mean()),
        "median": float(df['price'].median()),
        "min": float(df['price'].min()),
        "max": float(df['price'].max()),
        "std": float(df['price'].std())
    },
    "correlations": {
        "strongest_positive": get_strongest_correlation(corr_df, 'price', positive=True),
        "strongest_negative": get_strongest_correlation(corr_df, 'price', positive=False)
    }
}

with open('static/visualizations/insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print("\n✅ All visualizations generated successfully!")
print("📊 Files created in static/visualizations/:")
print("   - feature_importance.png")
print("   - correlation_heatmap.png")
print("   - price_distribution.png")
print("   - features_vs_price.png")
print("   - categorical_analysis.png")
print("   - model_performance.png")
print("   - insights.json")

