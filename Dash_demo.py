# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

pie_colors = ['LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenRodYellow',
          'LightGray', 'LightGreen', 'LightPink', 'LightSalmon', 'LightSteelBlue', 'LightSkyBlue'] #饼图的颜色，可自行修改
def pie_Figure(values,colors):
    '''
    用于生成饼图的函数
    :param values: 传入饼图中的值，格式为list
    :param colors: 饼图各个部分对应的颜色，传入一个list，list中的每个值对应HTML的颜色
    :return: 返回生成好的fig
    '''
    labels = ['Education','IT','Animals','Medicine','Famous','Poetry','Sensitives','Car_brand_part','Law','Finacial','Food'] # 在本项目中label固定，所以没有当做传参
    values = values
    index = values.index(max(values))
    pulls = [0,0,0,0,0,0,0,0,0,0,0]
    pulls[index] = 0.2
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pulls)])
    fig.update_layout(title_text="类别饼图") # 图的命名
    fig.update_traces(textinfo='label+percent', textfont_size=14,
                  marker=dict(colors=colors))
    return fig

bar_colors = ['lightCoral','lightCyan'] # 柱状图颜色，可自行修改
def bar_Figure(values,colors):
    '''
    用于生成情感分析柱状图的函数
    :param values:传入的柱状图数据
    :param colors:柱状图颜色
    :return:
    '''
    fig = go.Figure(data=[go.Bar(
        x=['positive','negative'],
        y=values,
        marker_color=colors  # marker color can be a single color value or an iterable
    )])
    fig.update_layout(title_text='情感分析柱状图') # 图的命名
    return fig

external_stylesheets = ['css_code.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('系统标题')
    ],className="header"),
    html.Div(children=[
        html.Div(children=[html.H1('新闻内容主题')],className='left'),
        html.Div(children=[dcc.Graph(
                                id='pie-graph',
                                figure=pie_Figure(values=None,colors=pie_colors) #这里需要传入一个数值列表
                )],className='right-up'),
        html.Div([dcc.Graph(
                        id='example-graph',
                        figure=bar_Figure(values=None,colors=bar_colors) # 这里需要传入一个数值列表
                    )
        ],className='right-down')
    ],className="main"),
], className="box")

if __name__ == '__main__':
    app.run_server(debug=True)