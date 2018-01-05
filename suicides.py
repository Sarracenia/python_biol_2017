import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas
import plotly.graph_objs as graph
import os

suicides = dash.Dash()

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

suicides.layout = html.Div(children=[
    html.H1(children='Data o sebevraždách'),

    html.Div(children='''
        ... aneb jaký je nejlepší způsob smrti
    '''),

    dcc.Graph(
        id='example-graph',
    ),
    html.H3("""
    Vyberte graf:"""),
    dcc.Dropdown(
        options=[
            {'label': '1. Frekvence sebevražd v rámci pohlaví - součet', 'value': 'gender'},
            {'label': '2. Frekvence sebevražd v rámci věkových kategorií - součet', 'value': 'age_group'},
            {'label': '3. Frekvence jednotlivých metod - součet', 'value': 'method'},
            {'label': '4. Frekvence jednotlivých metod v rámci pohlaví a věku', 'value': 'gender_methods'}
        ],
        value='gender',
        id='drop-input'
    ),
    
    html.Details([
        html.Summary('Pokročilá nastavení'),
        html.Div(children=[        
            dcc.RadioItems(
                options=[
                    {'label': 'Sloupcový graf', 'value':'bar'},
                    {'label': 'Bodový graf', 'value': 'scat'},
                ],
                value='bar',
                id='radio-input'
            ),
            html.Div("Poznámka: u grafů 1-3 má smysl pouze sloupcový graf",style={'fontSize': 14}),
            
            dcc.Markdown("**Následující položky jsou určeny pro graf č.4:**"),
            dcc.Checklist(
                options=[
                    {'label': 'jed muži', 'value': 'm_poison'},
                    {'label': 'jed ženy', 'value': 'f_poison'},
                    {'label': 'oběšení muži', 'value': 'm_hang'},
                    {'label': 'oběšení ženy', 'value': 'f_hang'},
                    {'label': 'plyn muži', 'value': 'm_gas'},
                    {'label': 'plyn_ženy', 'value': 'f_gas'},
                    {'label': 'zastřelení muži', 'value': 'm_gun'},
                    {'label': 'zastřelení ženy', 'value': 'f_gun'},
                    {'label': 'utopení muži', 'value': 'm_drown'},
                    {'label': 'utopení ženy', 'value': 'f_drown'},
                    {'label': 'skok muži', 'value': 'm_jump'},
                    {'label': 'skok ženy', 'value': 'f_jump'},
                    {'label': 'nůž muži', 'value': 'm_knife'},
                    {'label': 'nůž ženy', 'value': 'f_knife'},
                    {'label': 'ostatní muži', 'value': 'm_other'},
                    {'label': 'ostatní ženy', 'value': 'f_other'}
                    
                ],
                values=['m_poison','f_poison'],
                id='check-input'
                
            )
            
        
        ])
    ])
    
])

@suicides.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='drop-input', component_property='value'),
    Input(component_id='radio-input', component_property='value'),
    Input(component_id='check-input', component_property='values')]
)
def update_figure(graph_type,plot_type,traces):
    
    if graph_type =="gender":
        traces=0
        plot_function = graph.Bar if plot_type == 'bar' else graph.Scatter
        trace1 = plot_function(y=genders[genders.sex=="male"].Freq, name = 'muži')
        trace2 = plot_function(y=genders[genders.sex=="female"].Freq, name = 'ženy')
        data = [trace1, trace2]
        layout = graph.Layout(
            title = 'Frequence v rámci pohlaví',
            titlefont={'size':24, 'family':'Raleway'},
            xaxis={'title':'Pohlaví'}, yaxis={'title':'Frekvence'}
            )
    
    elif graph_type=="age_group": 
        traces=0
        plot_function = graph.Bar if plot_type == 'bar' else graph.Scatter
        trace1 = plot_function(y=suicide_age_group[suicide_age_group.age_group=="10-20"].Freq, name = '10-20')
        trace2 = plot_function(y=suicide_age_group[suicide_age_group.age_group=="25-35"].Freq, name = '25-35')
        trace3 = plot_function(y=suicide_age_group[suicide_age_group.age_group=="40-50"].Freq, name = '40-50')
        trace4 = plot_function(y=suicide_age_group[suicide_age_group.age_group=="55-65"].Freq, name = '55-65')
        trace5 = plot_function(y=suicide_age_group[suicide_age_group.age_group=="70-90"].Freq, name = '70-90')
        data = [trace1, trace2, trace3,trace4,trace5]
        layout = graph.Layout(
            title = 'Frequence podle věkových skupin',
            titlefont={'size':24, 'family':'Raleway'},
            xaxis={'title':'Věková skupina'}, yaxis={'title':'Frekvence'}
            )
    elif graph_type=="method":
        traces=0
        plot_function = graph.Bar if plot_type == 'bar' else graph.Scatter
        trace1 = plot_function(y=suicide_method[suicide_method.method2=="poison"].Freq, name = 'jed')
        trace2 = plot_function(y=suicide_method[suicide_method.method2=="hang"].Freq, name = 'oběšení')
        trace3 = plot_function(y=suicide_method[suicide_method.method2=="gas"].Freq, name = 'plyn')
        trace4 = plot_function(y=suicide_method[suicide_method.method2=="gun"].Freq, name = 'zastřelení')
        trace5 = plot_function(y=suicide_method[suicide_method.method2=="drown"].Freq, name = 'utopení')
        trace6 = plot_function(y=suicide_method[suicide_method.method2=="jump"].Freq, name = 'skok')
        trace7 = plot_function(y=suicide_method[suicide_method.method2=="knife"].Freq, name = 'nůž')
        trace8 = plot_function(y=suicide_method[suicide_method.method2=="other"].Freq, name = 'ostatní')
        data = [trace1, trace2, trace3,trace4,trace5,trace6,trace7,trace8]
        layout = graph.Layout(
            title = 'Frequency by method',
            titlefont={'size':24, 'family':'Raleway'},
            xaxis={'title':'Metoda'}, yaxis={'title':'Frequence'}
            )
     
    elif graph_type=="gender_methods":
        plot_function = graph.Bar if plot_type == 'bar' else graph.Scatter
        trace1 = plot_function(y=male_poison.Freq, x=male_poison.age, name = 'jed muži'
                              ) if 'm_poison' in traces else plot_function(y=0, x=0)
        trace2 = plot_function(y=female_poison.Freq, x=female_poison.age, name = 'jed ženy'
                              ) if 'f_poison' in traces else plot_function(y=0, x=0)
                               
        trace3 = plot_function(y=male_hang.Freq, x=male_hang.age, name = 'oběšení muži'
                              ) if 'm_hang' in traces else plot_function(y=0, x=0)
        trace4 = plot_function(y=female_hang.Freq, x=female_hang.age, name = 'oběšení ženy'
                              ) if 'f_hang' in traces else plot_function(y=0, x=0)
                               
        trace5 = plot_function(y=male_gas.Freq, x=male_gas.age, name = 'plyn muži'
                              ) if 'm_gas' in traces else plot_function(y=0, x=0)
        trace6 = plot_function(y=female_gas.Freq, x=female_gas.age, name = 'plyn ženy'
                              ) if 'f_gas' in traces else plot_function(y=0, x=0)
        
        trace7 = plot_function(y=male_gun.Freq, x=male_gun.age, name = 'zastřelení muži'
                              ) if 'm_gun' in traces else plot_function(y=0, x=0)
        trace8 = plot_function(y=female_gun.Freq, x=female_gun.age, name = 'zastřelení ženy'
                              ) if 'f_gun' in traces else plot_function(y=0, x=0)
                               
        trace9 = plot_function(y=male_drown.Freq, x=male_drown.age, name = 'utopení muži'
                              ) if 'm_drown' in traces else plot_function(y=0, x=0)
        trace10 = plot_function(y=female_drown.Freq, x=female_drown.age, name = 'utopení ženy'
                              ) if 'f_drown' in traces else plot_function(y=0, x=0)
        
        trace11 = plot_function(y=male_jump.Freq, x=male_jump.age, name = 'skok muži'
                              ) if 'm_jump' in traces else plot_function(y=0, x=0) 
        trace12 = plot_function(y=female_jump.Freq, x=female_jump.age, name = 'skok ženy'
                              ) if 'f_jump' in traces else plot_function(y=0, x=0)
        
        trace13 = plot_function(y=male_knife.Freq, x=male_knife.age, name = 'nůž muži'
                              ) if 'm_knife' in traces else plot_function(y=0, x=0)
        trace14 = plot_function(y=female_knife.Freq, x=female_knife.age, name = 'nůž ženy'
                              )if 'f_knife' in traces else plot_function(y=0, x=0)
                               
        trace15 = plot_function(y=male_other.Freq, x=male_other.age, name = 'ostatní muži'
                              ) if 'm_other' in traces else plot_function(y=0, x=0)
        trace16 = plot_function(y=female_other.Freq, x=female_other.age, name = 'ostatní ženy'
                              ) if 'f_other' in traces else plot_function(y=0, x=0)
        
        data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15,trace16]
        layout = graph.Layout( 
            title = 'Frekvence jednotlivých metod v rámci pohlaví',
            titlefont={'size':24, 'family':'Raleway'},
            xaxis={'title':'Věk'},yaxis={'title':'Frekvence'}
        )
        

    figure={'data':data,'layout':layout}
    return figure

suicide = pandas.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/vcd/Suicide.csv',index_col=0)
suicide.rename(columns={'age.group':'age_group'}, inplace=True)
suicide_method=suicide.groupby('method2').sum().reset_index()
suicide_age_group=suicide.groupby("age_group").sum().reset_index()

female = suicide.groupby("sex").get_group("female")
male = suicide.groupby("sex").get_group("male")

# frekvence metod pro určité pohlaví
male_poison=male.groupby("method").get_group("poison")
male_cgas=male.groupby("method").get_group("cookgas")
male_tgas=male.groupby("method").get_group("toxicgas")
male_hang=male.groupby("method").get_group("hang")
male_drown=male.groupby("method").get_group("drown")
male_gun=male.groupby("method").get_group("gun")
male_knife=male.groupby("method").get_group("knife")
male_jump=male.groupby("method").get_group("jump")
male_other=male.groupby("method").get_group("other")

female_poison=female.groupby("method").get_group("poison")
female_cgas=female.groupby("method").get_group("cookgas")
female_tgas=female.groupby("method").get_group("toxicgas")
female_hang=female.groupby("method").get_group("hang")
female_drown=female.groupby("method").get_group("drown")
female_gun=female.groupby("method").get_group("gun")
female_knife=female.groupby("method").get_group("knife")
female_jump=female.groupby("method").get_group("jump")
female_other=female.groupby("method").get_group("other")

female_gasx=female.groupby("method2").get_group("gas")
female_gas=female_gasx.groupby("age").sum().reset_index()
male_gasx=male.groupby("method2").get_group("gas")
male_gas=male_gasx.groupby("age").sum().reset_index()

#frekvence sebevražd podle věkových skupin a pohlaví
male_10_20=male.groupby("age_group").get_group("10-20")
male_25_35=male.groupby("age_group").get_group("25-35")
male_40_50=male.groupby("age_group").get_group("40-50")
male_55_65=male.groupby("age_group").get_group("55-65")
male_70_90=male.groupby("age_group").get_group("70-90")

female_10_20=female.groupby("age_group").get_group("10-20")
female_25_35=female.groupby("age_group").get_group("25-35")
female_40_50=female.groupby("age_group").get_group("40-50")
female_55_65=female.groupby("age_group").get_group("55-65")
female_70_90=female.groupby("age_group").get_group("70-90")

genders = suicide.groupby("sex").sum().reset_index()

if __name__ == '__main__':
    suicides.run_server()