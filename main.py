import flet as ft
import sqlite3
import logging


# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pesquisa_input = ft.Ref[ft.TextField]()

def main(page: ft.Page):
    page.title = "ERP Hortifruti"
    page.bgcolor = "#f2f2f2"  # Cor de fundo do app

        # Conectar ao banco de dados
    def conectar_db():
        try:
            conn = sqlite3.connect('database_hortifruti-py.db')
            logging.info("Conexão ao banco de dados estabelecida com sucesso.")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None  # Retorna None em caso de erro

    # Função para obter produtos do banco de dados
    # Função para obter produtos do banco de dados
    def obter_produtos(pesquisa=None, id_produto=None):
        conn = conectar_db()  # Conecta ao banco de dados
        if conn is None:
            return []  # Retorna uma lista vazia se a conexão falhar

        cursor = conn.cursor()  # Cria o cursor a partir da conexão

        if id_produto is not None:
            query = "SELECT * FROM produtos WHERE id = ?"
            parametros = (id_produto,)  # Busca pelo ID específico

        elif pesquisa:
            query = "SELECT * FROM produtos WHERE nome LIKE ?"
            parametros = (f"%{pesquisa}%",)  # Wildcards para busca pelo nome
        
        else:
            query = "SELECT * FROM produtos"
            parametros = ()
        
        try:
            cursor.execute(query, parametros)  # Execute a consulta
            produtos = cursor.fetchall()  # Obtenha todos os resultados
        except sqlite3.Error as e:
            logging.error(f"Erro ao obter produtos: {e}")
            produtos = []  # Retorna uma lista vazia em caso de erro
        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco de dados
        
        return produtos  # Retorna os produtos encontrados

    # Função para listar produtos na tabela
    def listar_produtos(pesquisa=None):
        produtos = obter_produtos(pesquisa)  # Função que busca produtos no banco de dados
        data_rows = []  # Lista para armazenar as linhas da tabela

        for produto in produtos:
            quantidade_input = ft.TextField(
                hint_text="Qtd.",
                width=80,
                keyboard_type=ft.KeyboardType.NUMBER,
                color=ft.colors.BLACK,
                border_color=ft.colors.BLACK,
            )
            
            # Captura os valores de 'produto' e 'quantidade_input'
            venda_button = ft.ElevatedButton(
                "Vender",
                on_click=lambda e, p=produto, q=quantidade_input: vender_produto(e, p, q)
            )
            
            # Adiciona uma linha de dados para a tabela
            data_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(produto[0]), color=ft.colors.BLACK)),  # ID do produto
                    ft.DataCell(ft.Text(produto[1], color=ft.colors.BLACK)),  # Nome do produto
                    ft.DataCell(ft.Text(f"R$ {float(produto[2]):.2f}", color=ft.colors.BLACK)),  # Preço do produto
                    ft.DataCell(ft.Text(str(produto[4]), color=ft.colors.BLACK)),  # Quantidade em estoque
                    ft.DataCell(quantidade_input),  # Campo de entrada de quantidade
                    ft.DataCell(venda_button),  # Botão de venda
                ])
            )

        # Atualiza a tabela com as novas linhas
        produtos_table.rows = data_rows
        page.update()

    # Função para buscar produtos
    def buscar_produtos():
        pesquisa = pesquisa_input.value  # Certifique-se de que 'pesquisa_input' é um campo de entrada definido corretamente
        listar_produtos(pesquisa)

    # Botão de busca
    search_button = ft.ElevatedButton("Buscar", on_click=lambda e: buscar_produtos())

    # Função para processar a venda de um produto
    def vender_produto(e, produto, quantidade_input):
        try:
            quantidade = int(quantidade_input.value)
            if quantidade > 0 and quantidade <= produto[4]: 
                conn = conectar_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",  # Corrigido para usar o ID
                        (quantidade, produto[0])  # Usando o ID do produto
                    )
                    conn.commit()
                    conn.close()

                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"{quantidade} unidades de {produto[1]} vendidas!", color=ft.colors.GREEN)
                    )
                    page.snack_bar.open = True
                    page.update()

                    # Atualiza a tabela de produtos após a venda
                    listar_produtos()  # Atualiza a listagem
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Erro ao conectar ao banco de dados.", color=ft.colors.RED)
                    )
                    page.snack_bar.open = True
                    page.update()
            else:
                show_popup(
                    "Erro",
                    "Quantidade inválida ou maior que o estoque disponível."
                )
                page.snack_bar.open = True
                page.update()
        except ValueError:
            show_popup(
                "Erro", 
            "Insira um valor numérico válido para a quantidade.",
            color=ft.colors.RED
            )
                
            page.snack_bar.open = True
            page.update()

    # Cria uma tabela para listar produtos
    produtos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Produto", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Preço", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Estoque", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Quantidade", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Ação", color=ft.colors.BLACK)),
        ],
        rows=[],  # Inicialmente vazio
        border_radius=10,
    )

    # Adiciona a tabela ao corpo da tela de vendas
    def mostrar_tela_vendas():
        listar_produtos()  # Preenche a tabela com produtos
        return ft.Column(
            [
                ft.Text("Tela de Vendas", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK,),
                ft.Divider(height=5, thickness=1),
                ft.Row([
                    ft.TextField(label="Pesquisar", color=ft.colors.BLACK, width=200, ref=pesquisa_input),
                    ft.ElevatedButton("Buscar", on_click=lambda e: listar_produtos(pesquisa_input.current.value)),  # Corrigido
                ]),
                ft.Container(
                    content=ft.ListView(
                        controls=[produtos_table],
                        width=800,  # Defina a largura desejada para a tabela
                        height=500,  # Defina a altura desejada para a tabela (opcional)
                    ),
                    padding=5,
                    border=ft.Border(
                        top=ft.BorderSide(color=ft.colors.GREEN, width=2),
                        bottom=ft.BorderSide(color=ft.colors.GREEN, width=2),
                        left=ft.BorderSide(color=ft.colors.GREEN, width=2),
                        right=ft.BorderSide(color=ft.colors.GREEN, width=2)
                    ),
                    border_radius=10,  # Borda arredondada
                    bgcolor="#f2f2f2",  # Cor de fundo do contêiner
                ),
            ]
        )

# Certifique-se de que produtos_table esteja definido corretamente antes de chamar mostrar_tela_vendas


    # Funções para exibir diferentes telas
    def mostrar_tela_caixa():
        return ft.Column(
            [
                ft.Text("Tela de Caixa", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Aqui você poderá gerenciar o caixa.", color="black"),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_cadastro():
        return ft.Column(
            [
                ft.Text("Cadastro de Produtos", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.TextField(label="Nome do Produto", hint_text="Insira o nome",color=ft.colors.BLACK, width=300),
                ft.TextField(label="Preço", width=300, keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK, hint_text="Digite o valor"),
                ft.TextField(label="Quantidade em Estoque", width=300, keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK, hint_text="Digite a quantidade"),
                ft.ElevatedButton(
                    "Adicionar Produto",
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.GREEN_300,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_relatorios():
        return ft.Column(
            [
                ft.Text("Relatórios", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Aqui você poderá visualizar relatórios de vendas e estoque.", color="black"),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
    def show_popup(title, message, color=ft.colors.RED):
        # Cria o conteúdo do dialog
        dialog = ft.AlertDialog(
            title=ft.Text(title, color=ft.colors.BLACK),  # Título do popup
            content=ft.Text(message, color=ft.colors.WHITE),  # Mensagem do popup
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_popup(dialog)),  # Botão de fechar o popup
            ],
            actions_alignment=ft.MainAxisAlignment.END,  # Alinha o botão à direita
            bgcolor=color,  # Cor de fundo do popup
            shape=ft.RoundedRectangleBorder(radius=10),  # Forma arredondada
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Função para fechar o AlertDialog
    def close_popup(dialog):
        dialog.open = False
        page.update()


    # Função para fechar o SnackBar
    def close_snack_bar():
        page.snack_bar.open = False
        page.update()


    # Função para alternar entre telas com base na seleção da NavigationRail
    def trocar_tela(e):
        if rail.selected_index == 0:
            corpo.content = mostrar_tela_cadastro()
        elif rail.selected_index == 1:
            corpo.content = mostrar_tela_vendas()  # Chama a função que mostra a tela de vendas
        elif rail.selected_index == 2:
            corpo.content = mostrar_tela_relatorios()
        elif rail.selected_index == 3:
            corpo.content = mostrar_tela_caixa()
        page.update()

    # NavigationRail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor=ft.colors.GREEN,
        indicator_color=ft.colors.GREEN_ACCENT,
        min_extended_width=200,
        leading=ft.FloatingActionButton(icon=ft.icons.EXIT_TO_APP,width=70,height=40, text="Sair", bgcolor=ft.colors.RED_500, on_click=lambda e: page.window_destroy()),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.ADD,
                selected_icon=ft.icons.ADD,
                label="Cadastro"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PAYMENT,
                selected_icon=ft.icons.PAYMENT,
                label="Vendas",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.RECEIPT_LONG,
                selected_icon=ft.icons.RECEIPT_LONG,
                label="Relatórios",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.POINT_OF_SALE,
                selected_icon=ft.icons.POINT_OF_SALE,
                label="Caixa",
            ),
        ],
        on_change=trocar_tela,
    )

    # Conteúdo inicial do corpo da página
    corpo = ft.Container(content=mostrar_tela_cadastro(), expand=True)

    # Layout da página
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                corpo,
            ],
            expand=True
        )
    )

# Executa a aplicação
if __name__ == "__main__":
    ft.app(target=main)
