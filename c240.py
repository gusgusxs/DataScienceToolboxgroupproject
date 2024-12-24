import plotly.graph_objects as go

# สร้างกราฟแท่ง
fig = go.Figure(data=go.Bar(y=[10, 20, 15, 25]))
fig.update_layout(
    title="ตัวอย่างกราฟแท่ง",
    xaxis_title="หมวดหมู่",
    yaxis_title="จำนวน"
)

# แสดงกราฟ
fig.show()