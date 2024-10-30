logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_products():
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    products = cursor.fetchall()
    conn.close()
    return products

def abrir_janela_edicao(page):
    
    products = load_products()
    product_rows = []
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO)

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

    def delete_product_row(e, product_id):
        delete_product(product_id)
        for row in product_rows:
            if row['id'] == product_id:
                product_list.controls.remove(row['row'])
                product_rows.remove(row)
                break
        page.update()

    def filter_products(e):
        search_term = search_field.value.lower()
        product_list.controls.clear()
        for product in products:
            product_id, name, price, category, quantity = product
            if (search_term in name.lower() or
                search_term in category.lower() or
                search_term in str(price)):
                # Campos de edição do produto
                name_field = ft.TextField(value=name, max_length=25, bgcolor=ft.colors.GREEN_400)
                price_field = ft.TextField(value=str(price), max_length=10, bgcolor=ft.colors.GREEN_400)
                category_field = ft.TextField(value=category, max_length=15, bgcolor=ft.colors.GREEN_400)
                quantity_field = ft.TextField(value=str(quantity), max_length=3, bgcolor=ft.colors.GREEN_400)

                # Linha de produto
                row = {
                    'id': product_id,
                    'name': name_field,
                    'price': price_field,
                    'category': category_field,
                    'quantity': quantity_field,
                    'row': ft.Row(
                        [
                            ft.Text(value=product_id, width=50, text_align="center"),
                            name_field,
                            price_field,
                            category_field,
                            quantity_field,
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Excluir Produto",
                                on_click=lambda e, product_id=product_id: delete_product_row(e, product_id),
                            )
                        ],
                        alignment="center",
                        spacing=5,
                    )
                }
                product_rows.append(row)
                product_list.controls.append(row['row'])
        page.update()

    search_field = ft.TextField(
        label="Pesquisar produtos...",
        bgcolor="#f2f2f2",
        on_change=filter_products,
        icon=ft.icons.SEARCH
    )

    table_header = ft.Row(
        [
            ft.Text("ID", width=30),
            ft.Text("Nome", width=140),
            ft.Text("Preço", width=100),
            ft.Text("Categoria", width=150),
            ft.Text("Qtd", width=75),
            ft.Text("Ação", width=100),
        ],
        alignment="start",
        spacing=5,
    )

    save_button = ft.ElevatedButton(
        text="Salvar Alterações",
        icon=ft.icons.SAVE,
        on_click=save_changes
    )

    dialog = ft.AlertDialog(
        title=ft.Text("Editar Produtos", size=20, weight="bold"),
        content=ft.Column(
            [
                search_field,
                table_header,
                ft.Container(content=product_list,),
                save_button
            ],
            spacing=10
        ),
        on_dismiss=lambda e: page.update(),
        modal=True,
        open=True
    )

    page.dialog = dialog
    page.update()

#acima fica a tela edição 

