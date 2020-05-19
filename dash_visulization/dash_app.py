# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from dash_visulization.datasource import DataLoader

pie_colors = ['LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenRodYellow',
              'LightGray', 'LightGreen', 'LightPink', 'LightSalmon', 'LightSteelBlue', 'LightSkyBlue']  # 饼图的颜色，可自行修改


def pie_Figure(values, colors):
    """
    用于生成饼图的函数
    :param values: 传入饼图中的值，格式为list
    :param colors: 饼图各个部分对应的颜色，传入一个list，list中的每个值对应HTML的颜色
    :return: 返回生成好的fig
    """
    labels = ['Education', 'IT', 'Animals', 'Medicine', 'Famous', 'Poetry', 'Sensitives', 'Car_brand_part', 'Law',
              'Finacial', 'Food']  # 在本项目中label固定，所以没有当做传参
    values = values
    index = values.index(max(values))
    pulls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pulls[index] = 0.2
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pulls)])
    fig.update_layout(title_text="类别饼图")  # 图的命名
    fig.update_traces(textinfo='label+percent', textfont_size=14,
                      marker=dict(colors=colors))
    return fig


bar_colors = ['lightCoral', 'lightCyan']  # 柱状图颜色，可自行修改


def bar_Figure(values, colors):
    """
    用于生成情感分析柱状图的函数
    :param values:传入的柱状图数据
    :param colors:柱状图颜色
    :return:
    """
    fig = go.Figure(data=[go.Bar(
        x=['positive', 'negative'],
        y=values,
        marker_color=colors  # marker color can be a single color value or an iterable
    )])
    fig.update_layout(title_text='情感分析柱状图')  # 图的命名
    return fig


# 初始化工作
loader = DataLoader()
# loader.batch_size = 100 # 缓存批大小默认100

# 界面布局
external_stylesheets = ['css_code.css', 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('网易新闻')
    ], className="header"),
    # dcc.Input(id="user_input"),
    html.Div(children=[

        dcc.Loading([
            # 上一个按钮
            html.Div([html.Img(src="https://zty-pic-bed.oss-cn-shenzhen.aliyuncs.com/left.png")], id="previous",
                     className='veryleft'),
            # 左侧文章
            html.Div([
                html.H2(id="title"),
                html.H6(id="tag"),
                html.Div(id="content"),
                html.Hr(),
                html.A("原文链接", id="url")
            ], id="article", className='left'),
            # 饼图
            html.Div(children=[dcc.Graph(
                id='pie-graph',
                # figure=pie_Figure(values=[1,2,3,4,5], colors=pie_colors)  # 这里需要传入一个数值列表
                # figure=pie
            )], className='right-up'),

            # 条形图
            html.Div([dcc.Graph(
                id='bar-graph',
                # figure=bar_Figure(values=[1,2,3,4,5], colors=bar_colors)  # 这里需要传入一个数值列表
                # figure=bar
            )], className='right-down'),
            # 下一个按钮
            html.Div([html.Img(src="https://zty-pic-bed.oss-cn-shenzhen.aliyuncs.com/right.png")], id="next",
                     className='veryright'),
        ], type="circle"
        ),

        # 文章id
        html.Div(id='article_id', style={'display': 'none'}, children=1)
    ], className="main"),

], className="box")


# 根据文章id更新页面数据的回调
@app.callback(output=[Output("pie-graph", "figure"),
                      Output("bar-graph", "figure"),
                      Output("title", "children"),
                      Output("tag", "children"),
                      Output("content", "children"),
                      Output("url", "href")],
              inputs=[Input("article_id", "children")])
def load_data(article_id):
    pie_data, bar_data, tag, title, content, url = loader.get(article_id)
    pie = pie_Figure(pie_data, pie_colors)
    bar = bar_Figure(bar_data, bar_colors)

    if len(content) > 1500:
        content = content[:1500] + "......"

    return pie, bar, title, tag, content, url


# 根据文章id更新左侧按钮的回调
@app.callback(Output("previous", "className"), [Input("article_id", "children")])
def change_button(art_id):
    if art_id == 1:
        return "invisible"
    else:
        return "veryleft"


ltime, rtime = 0, 0


# 根据点击两侧按钮改变访问一个文章的回调
@app.callback(Output("article_id", "children"),
              [Input("previous", "n_clicks"), Input("next", "n_clicks")],
              [State("article_id", "children")])
def next_article(l, r, art_id):
    global ltime, rtime
    if l is None:
        l = 0
    if r is None:
        r = 0

    if l > ltime:
        ltime = l
        return max(1, art_id - 1)
    elif r > rtime:
        rtime = r
        return art_id + 1
    else:
        return art_id


if __name__ == '__main__':
    app.run_server(debug=True)
