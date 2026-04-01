import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats
import webbrowser
from pathlib import Path


data = {
    'experience': [1, 2, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 10, 10, 11, 12, 12, 15, 15, 18, 20],
    'salary': [35000, 40000, 42000, 48000, 50000, 55000, 62000, 60000, 68000, 75000, 73000, 
               82000, 88000, 90000, 95000, 98000, 105000, 110000, 115000, 130000, 135000, 150000, 160000]
}

df = pd.DataFrame(data)


slope, intercept, r_value, p_value, std_err = stats.linregress(df['experience'], df['salary'])
line_x = np.array([df['experience'].min(), df['experience'].max()])
line_y = slope * line_x + intercept

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['experience'],
    y=df['salary'],
    mode='markers',
    name='Data Points',
    marker=dict(
        size=10,
        color='#667eea',
        opacity=0.7,
        line=dict(
            color='#764ba2',
            width=2
        )
    ),
    text=[f"<b>Experience:</b> {exp} years<br><b>Salary:</b> ₹{sal:,.0f}" 
          for exp, sal in zip(df['experience'], df['salary'])],
    hovertemplate='%{text}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=line_x,
    y=line_y,
    mode='lines',
    name='Trend Line',
    line=dict(
        color='#ff6b6b',
        width=2,
        dash='dash'
    ),
    hovertemplate='Trend: ₹%{y:,.0f}<extra></extra>'
))

fig.update_layout(
    title={
        'text': 'Salary Growth by Years of Experience',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#333'}
    },
    xaxis=dict(
        title='<b>Years of Experience</b>',
        showgrid=True,
        gridwidth=1,
        gridcolor='#e0e0e0',
        zeroline=False,
        title_font={'size': 14}
    ),
    yaxis=dict(
        title='<b>Annual Salary (₹)</b>',
        showgrid=True,
        gridwidth=1,
        gridcolor='#e0e0e0',
        zeroline=False,
        tickformat=',.0f',
        title_font={'size': 14}
    ),
    plot_bgcolor='#f9f9f9',
    paper_bgcolor='white',
    hovermode='closest',
    showlegend=True,
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='#ddd',
        borderwidth=1,
        font={'size': 12}
    ),
    width=1000,
    height=600,
    margin=dict(l=80, r=80, t=100, b=80)
)

r_squared = r_value ** 2
fig.add_annotation(
    text=f"<b>R² = {r_squared:.3f}</b><br>Correlation strength",
    xref="paper", yref="paper",
    x=0.98, y=0.02,
    showarrow=False,
    bgcolor="rgba(255, 255, 255, 0.8)",
    bordercolor="#ddd",
    borderwidth=1,
    font=dict(size=12),
    align="right"
)


output_path = Path(__file__).parent / 'visualization.html'
fig.write_html(str(output_path))

print(f"✓ Visualization saved to: {output_path}")
print(f"✓ Data Summary:")
print(f"  - Number of data points: {len(df)}")
print(f"  - Experience range: {df['experience'].min()} - {df['experience'].max()} years")
print(f"  - Salary range: ₹{df['salary'].min():,.0f} - ₹{df['salary'].max():,.0f}")
print(f"  - Correlation coefficient (R): {r_value:.3f}")
print(f"  - R² value: {r_squared:.3f}")
print(f"\n✓ Opening visualization in browser...")


webbrowser.open(f'file://{output_path.absolute()}')
