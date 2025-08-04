import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os # Importar para verificar existência de arquivos/diretórios

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("Editor de Texto Simples (Tkinter)")
        master.geometry("800x600") # Define o tamanho inicial da janela

        self.current_file = None # Armazena o caminho do arquivo atualmente aberto
        self.text_changed = False # Flag para indicar se o texto foi modificado

        # --- Widget de Texto Principal ---
        self.text_area = scrolledtext.ScrolledText(master, wrap='word', undo=True)
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        # Binda um evento para detectar quando o texto foi modificado
        self.text_area.bind("<<Modified>>", self._on_text_modified)

        # --- Menu Bar ---
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # Menu 'Arquivo'
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Novo", command=self.new_file)
        self.file_menu.add_command(label="Abrir...", command=self.open_file)
        self.file_menu.add_command(label="Salvar", command=self.save_file)
        self.file_menu.add_command(label="Salvar Como...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.exit_editor) # Chamar um método customizado para sair

        # Menu 'Editar'
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Desfazer", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Refazer", command=self.text_area.edit_redo)

        # --- Status Bar ---
        self.status_bar = tk.Label(master, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_title()
        # Binda o protocolo de fechar janela para verificar alterações
        self.master.protocol("WM_DELETE_WINDOW", self.exit_editor)

    def _on_text_modified(self, event=None):
        """Callback quando o texto é modificado."""
        self.text_changed = True
        # Limpa o flag de modificação do widget Text
        self.text_area.edit_modified(False)
        self.update_title() # Atualiza o título para indicar que há alterações não salvas

    def update_title(self):
        """Atualiza o título da janela para mostrar o nome do arquivo e um asterisco se houver alterações."""
        title_text = "Editor de Texto Simples"
        if self.current_file:
            title_text += f" - {os.path.basename(self.current_file)}"
        else:
            title_text += " - Sem Título"

        if self.text_changed:
            title_text += " *" # Adiciona um asterisco se houver mudanças não salvas

        self.master.title(title_text)

    def _ask_save_changes(self):
        """Pergunta ao usuário se deseja salvar as alterações."""
        if self.text_changed:
            response = messagebox.askyesnocancel(
                "Salvar Alterações",
                "Existem alterações não salvas. Deseja salvar antes de continuar?"
            )
            if response is True: # Sim, quer salvar
                return self.save_file()
            elif response is False: # Não, não quer salvar (descarta)
                return True
            else: # Cancelar
                return False
        return True # Não há alterações, pode continuar

    def new_file(self):
        """Cria um novo arquivo (limpa a área de texto)."""
        if self._ask_save_changes():
            self.text_area.delete(1.0, tk.END) # Limpa todo o texto
            self.current_file = None
            self.text_changed = False # Resetar o flag de alteração
            self.update_title()
            self.status_bar.config(text="Novo arquivo criado.")

    def open_file(self):
        """Abre um arquivo existente."""
        if not self._ask_save_changes():
            return # Se o usuário cancelar salvar, não abre um novo arquivo

        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END) # Limpa o conteúdo atual
                self.text_area.insert(1.0, content) # Insere o novo conteúdo
                self.current_file = filepath
                self.text_changed = False # Resetar o flag de alteração
                self.update_title()
                self.status_bar.config(text=f"Arquivo '{os.path.basename(filepath)}' aberto.")
            except FileNotFoundError:
                messagebox.showerror("Erro ao Abrir Arquivo", f"O arquivo '{os.path.basename(filepath)}' não foi encontrado.")
                self.status_bar.config(text="Erro: arquivo não encontrado.")
            except PermissionError:
                messagebox.showerror("Erro ao Abrir Arquivo", f"Permissão negada para acessar o arquivo '{os.path.basename(filepath)}'.")
                self.status_bar.config(text="Erro: permissão negada.")
            except UnicodeDecodeError:
                messagebox.showerror("Erro de Codificação", f"Não foi possível decodificar o arquivo '{os.path.basename(filepath)}'. Tente abrir com outra codificação (não suportado neste editor).")
                self.status_bar.config(text="Erro de codificação.")
            except Exception as e:
                messagebox.showerror("Erro ao Abrir Arquivo", f"Ocorreu um erro inesperado ao abrir o arquivo:\n{e}")
                self.status_bar.config(text="Erro inesperado ao abrir arquivo.")

    def save_file(self):
        """Salva o arquivo atual. Se for um novo arquivo, chama 'Salvar Como'."""
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                self.text_changed = False # Marcar como não modificado após salvar
                self.update_title()
                self.status_bar.config(text=f"Arquivo '{os.path.basename(self.current_file)}' salvo.")
                return True
            except PermissionError:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Permissão negada para salvar o arquivo em '{os.path.basename(self.current_file)}'.")
                self.status_bar.config(text="Erro: permissão negada ao salvar.")
                return False
            except IOError as e:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Erro de I/O ao salvar o arquivo '{os.path.basename(self.current_file)}':\n{e}")
                self.status_bar.config(text="Erro de I/O ao salvar.")
                return False
            except Exception as e:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Ocorreu um erro inesperado ao salvar o arquivo:\n{e}")
                self.status_bar.config(text="Erro inesperado ao salvar arquivo.")
                return False
        else:
            return self.save_file_as() # Se não há arquivo atual, chama Salvar Como

    def save_file_as(self):
        """Salva o conteúdo em um novo arquivo ou em um local diferente."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if filepath:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)
                self.current_file = filepath
                self.text_changed = False # Marcar como não modificado após salvar
                self.update_title()
                self.status_bar.config(text=f"Arquivo '{os.path.basename(filepath)}' salvo como.")
                return True
            except PermissionError:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Permissão negada para salvar o arquivo em '{os.path.basename(filepath)}'.")
                self.status_bar.config(text="Erro: permissão negada ao salvar como.")
                return False
            except IOError as e:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Erro de I/O ao salvar o arquivo '{os.path.basename(filepath)}':\n{e}")
                self.status_bar.config(text="Erro de I/O ao salvar como.")
                return False
            except Exception as e:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Ocorreu um erro inesperado ao salvar o arquivo:\n{e}")
                self.status_bar.config(text="Erro inesperado ao salvar como.")
                return False
        return False # Retorna False se o usuário cancelar a caixa de diálogo

    def exit_editor(self):
        """Trata a saída do editor, perguntando para salvar se houver alterações."""
        if self._ask_save_changes():
            self.master.quit() # Sai do aplicativo se as alterações foram salvas ou descartadas

# --- Execução do Editor ---
if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()