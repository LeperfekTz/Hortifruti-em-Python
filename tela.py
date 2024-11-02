import flet as ft
import sqlite3

name = "LineChart 2"

def get_sales_data():
    # Conectando ao banco de dados
    conn = sqlite3.connect('database_hortifruti-py.db')
    cursor = conn.cursor()
    
    # Executando a consulta para obter os dados
    cursor.execute("SELECT quantidade, preco_total FROM historico_vendas ORDER BY data_venda")
    rows = cursor.fetchall()
    
    conn.close()
    
    # Retorna os dados formatados para o gráfico
    return [(i + 1, row[0] * row[1]) for i, row in enumerate(rows)]  # (x, y) = (indice, quantidade * preco_total)

def example():
    class State:
        toggle = True

    s = State()

    # Obtendo dados da base de dados
    sales_data = get_sales_data()

    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(x, y) for x, y in sales_data
            ],
            stroke_width=5,
            color=ft.colors.DEEP_PURPLE,  # Linha em roxo profundo
            curved=True,
            stroke_cap_round=True,
        )
    ]

    # Exemplo de dados estáticos para comparação
    data_2 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, 3.44),
                ft.LineChartDataPoint(2.6, 3.44),
                ft.LineChartDataPoint(4.9, 3.44),
                ft.LineChartDataPoint(6.8, 3.44),
                ft.LineChartDataPoint(8, 3.44),
                ft.LineChartDataPoint(9.5, 3.44),
                ft.LineChartDataPoint(11, 3.44),
            ],
            stroke_width=5,
            color=ft.colors.TEAL,  # Linha em teal
            curved=True,
            stroke_cap_round=True,
        )
    ]

    chart = ft.LineChart(
        data_series=data_1,
        border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.BLACK)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.BLACK), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.BLACK), width=1
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=1, label=ft.Text("10K", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.DEEP_PURPLE)),
                ft.ChartAxisLabel(value=3, label=ft.Text("30K", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.DEEP_PURPLE)),
                ft.ChartAxisLabel(value=5, label=ft.Text("50K", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.DEEP_PURPLE)),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=2, label=ft.Text("MAR", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)),
                ft.ChartAxisLabel(value=5, label=ft.Text("JUN", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)),
                ft.ChartAxisLabel(value=8, label=ft.Text("SEP", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.GREY),
        min_y=0,
        max_y=max(y for _, y in sales_data) + 1,  # Ajustando o máximo dinamicamente
        min_x=0,
        max_x=len(sales_data),
        width=700,
        height=500,
    )

    def toggle_data(e):
        if s.toggle:
            chart.data_series = data_2
            chart.interactive = False
        else:
            chart.data_series = data_1
            chart.interactive = True
        s.toggle = not s.toggle
        chart.update()

    return ft.Column(controls=[
        ft.ElevatedButton("avg", on_click=toggle_data, bgcolor=ft.colors.CYAN, color="white"),
        chart
    ])
