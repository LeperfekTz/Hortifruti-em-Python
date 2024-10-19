import flet as ft

def criar_navigation_rail(on_change):
    """Cria o NavigationRail."""
    return ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor=ft.colors.GREEN,
        min_extended_width=200,
        leading=ft.FloatingActionButton(icon=ft.icons.EXIT_TO_APP, text="Sair", bgcolor=ft.colors.RED_400, on_click=lambda e: page.window.destroy()),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.ADD,
                selected_icon=ft.icons.ADD,
                label="Cadasto",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PAYMENT),
                selected_icon_content=ft.Icon(ft.icons.PAYMENT),
                label="Vendas",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.RECEIPT_LONG,
                selected_icon_content=ft.Icon(ft.icons.RECEIPT_LONG),
                label_content=ft.Text("Relatórios"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.POINT_OF_SALE,
                selected_icon_content=ft.Icon(ft.icons.POINT_OF_SALE),
                label_content=ft.Text("Caixa"),
            ),
        ],
        on_change=on_change,
    )
