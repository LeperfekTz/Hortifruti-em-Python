import flet as ft


def mostrar_tela_vendas(page):
    return ft.Column(
        [
            ft.Text("Tela de Vendas", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text("Aqui você poderá registrar as vendas e visualização histórico.", color="black"),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
