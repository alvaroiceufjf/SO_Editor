"""
A FAZER(por prioridade):
Localização do Cursor(Ediçao local ao invés de sobrescrever)
Buffer de Edição(Facilita o Desfazer/Refazer)
Desfazer/Refazer
Interface Gráfica(Facilita a visualização)

"""
import os

def abrir_arquivo(nome_arquivo):
    """Abre um arquivo e retorna seu conteúdo."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        return conteudo
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")
        return None

def salvar_arquivo(nome_arquivo, conteudo):
    """Salva o conteúdo em um arquivo."""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"Arquivo '{nome_arquivo}' salvo com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")
        return False

def editor_texto():
    """Função principal do editor de texto."""
    print("--- Editor de Texto Simples ---")
    print("Comandos: 'abrir <nome_arquivo>', 'novo <nome_arquivo>', 'sair'")

    nome_arquivo_atual = None
    conteudo_atual = ""

    while True:
        comando = input("\n> ").strip().split(maxsplit=1)
        acao = comando[0]

        if acao == "abrir":
            if len(comando) > 1:
                nome_arquivo_atual = comando[1]
                conteudo = abrir_arquivo(nome_arquivo_atual)
                if conteudo is not None:
                    conteudo_atual = conteudo
                    print("\n--- Conteúdo do Arquivo ---")
                    print(conteudo_atual)
                    print("--------------------------")
                else:
                    nome_arquivo_atual = None # Limpa se não conseguir abrir
            else:
                print("Uso: abrir <nome_arquivo>")

        elif acao == "novo":
            if len(comando) > 1:
                nome_arquivo_atual = comando[1]
                conteudo_atual = ""
                print(f"Novo arquivo '{nome_arquivo_atual}' criado (vazio).")
            else:
                print("Uso: novo <nome_arquivo>")

        elif acao == "editar":
            if nome_arquivo_atual:
                print(f"\n--- Editando '{nome_arquivo_atual}' ---")
                print("Digite seu texto. Pressione Enter em uma linha vazia para finalizar.")
                linhas = []
                while True:
                    linha = input()
                    if not linha:
                        break
                    linhas.append(linha)
                conteudo_atual = "\n".join(linhas)
                print("Edição finalizada. Use 'salvar' para gravar as alterações.")
            else:
                print("Nenhum arquivo aberto ou novo. Use 'abrir' ou 'novo' primeiro.")

        elif acao == "salvar":
            if nome_arquivo_atual:
                salvar_arquivo(nome_arquivo_atual, conteudo_atual)
            else:
                print("Nenhum arquivo para salvar. Abra ou crie um arquivo primeiro.")

        elif acao == "mostrar":
            if nome_arquivo_atual:
                print(f"\n--- Conteúdo atual de '{nome_arquivo_atual}' ---")
                print(conteudo_atual)
                print("---------------------------------------------")
            else:
                print("Nenhum arquivo aberto ou novo para mostrar.")

        elif acao == "sair":
            print("Saindo do editor. Até mais!")
            break

        else:
            print("Comando desconhecido. Comandos: 'abrir <nome_arquivo>', 'novo <nome_arquivo>', 'editar', 'salvar', 'mostrar', 'sair'")

if __name__ == "__main__":
    editor_texto()