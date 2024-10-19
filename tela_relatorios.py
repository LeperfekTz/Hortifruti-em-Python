import flet as ft

def mostrar_tela_relatorios(page):
    return ft.Column(
        [
            ft.Text("Relatórios", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text("Aqui você poderá visualizar relatórios de vendas e estoque.", color="black"),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
