import sqlite3
import flet as ft

# Função para carregar produtos do banco de dados
def load_products():
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    products = cursor.fetchall()
    conn.close()
    return products

# Função para atualizar um produto no banco de dados
def update_product(product_id, name, price, category, quantity):
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        UPDATE produtos 
        SET nome = ?, preco = ?, categoria = ?, quantidade = ? 
        WHERE id = ? 
    """, (name, price, category, quantity, product_id))
    conn.commit()
    conn.close()

# Função para excluir um produto no banco de dados
def delete_product(product_id):
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Função que inicializa a interface
def editar_produtos(page: ft.Page):
    page.title = "Editar Produtos"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 600
    page.window_maximizable = False 
    page.bgcolor = "#f2f2f2"

    # Carregar produtos da DB
    products = load_products()

    # Função para salvar mudanças
    def save_changes(e):
        for row in product_rows:
            product_id = row['id']
            name = row['name'].value
            price = float(row['price'].value)
            category = row['category'].value
            quantity = int(row['quantity'].value)
            update_product(product_id, name, price, category, quantity)

        page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"), bgcolor="green") 
        page.snack_bar.open = True
        page.update()

    # Função para excluir um produto
    def delete_product_row(e, product_id):
        delete_product(product_id)
        for row in product_rows:
            if row['id'] == product_id:
                product_list.controls.remove(row['row'])  # Remover da lista de produtos
                product_rows.remove(row)  # Remover do controle
                break
        page.update()

    # Função para filtrar produtos com base na pesquisa
    def filter_products(e):
        search_term = search_field.value.lower()
        product_list.controls.clear()  # Limpa a lista atual
        for product in products:
            product_id, name, price, category, quantity = product
            if (search_term in name.lower() or
                search_term in category.lower() or
                search_term in str(price)):
                
                name_field = ft.TextField(value=name, max_length=25, color="black", bgcolor=ft.colors.GREEN_400, width=140, height=60)
                price_field = ft.TextField(value=str(price), max_length=10, color="black", bgcolor=ft.colors.GREEN_400, width=100, height=60)
                category_field = ft.TextField(value=category, max_length=15, color="black", bgcolor=ft.colors.GREEN_400, width=100, height=60)
                quantity_field = ft.TextField(value=str(quantity), max_length=3, color="black", bgcolor=ft.colors.GREEN_400, width=100, height=60)

                row = {
                    'id': product_id,
                    'name': name_field,
                    'price': price_field,
                    'category': category_field,
                    'quantity': quantity_field,
                    'row': ft.Row(
                        [
                            ft.Text(value=product_id, color="black", width=50, size=15),
                            name_field,
                            price_field,
                            category_field,
                            quantity_field,
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED,
                                tooltip="Excluir Produto",
                                on_click=lambda e, product_id=product_id: delete_product_row(e, product_id),
                            )
                        ],
                        alignment="start",
                        spacing=5,
                    )
                }
                product_rows.append(row)
                product_list.controls.append(row['row'])  # Adicionar a linha ao contêiner de produtos
        page.update()  # Atualiza a interface após a filtragem

    # Cabeçalhos da tabela
    table_header = ft.Row(
        [
            ft.Text("ID", width=30, color="black", text_align="START"), 
            ft.Text("Nome", width=140, color="black", text_align="center"),
            ft.Text("Preço", width=100, color="black", text_align="center"),
            ft.Text("Categoria", width=150, color="black", text_align="center"), 
            ft.Text("Qtd", width=75, color="black", text_align="start"),    
            ft.Text("Ação", width=100, color="black", text_align="start"),
        ],
        alignment="start",
        spacing=5,
    )

    # Container para os produtos
    product_rows = []
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO)   

    # Campo de pesquisa
    search_field = ft.TextField(
        label="Pesquisar produtos...",
        width=300,
        bgcolor="#f2f2f2",
        label_style=ft.TextStyle(color=ft.colors.BLACK),
        border_color=ft.colors.GREEN,
        color=ft.colors.BLACK,
        autofocus=True,
        on_change=filter_products,
        icon=ft.icons.SEARCH
    )

    # Gerar linhas para cada produto inicialmente
    filter_products(None)  # Carrega todos os produtos inicialmente

    # Botão para salvar
    save_button = ft.ElevatedButton(
        text="Salvar Alterações",
        icon_color=ft.colors.GREEN,
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        color="WHITE",
        on_click=save_changes
    )

    # Adicionar cabeçalhos, campo de pesquisa, lista de produtos e botão de salvar à página
    page.add(
        ft.Column(
            [
                search_field,
                table_header,
                ft.Container(content=product_list, height=400, width=650),
                save_button
            ],
            alignment="center",
            spacing=10
        )
    )


