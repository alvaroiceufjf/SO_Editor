"""
A FAZER(por prioridade):
Localização do Cursor(Ediçao local ao invés de sobrescrever)
Buffer de Edição(Facilita o Desfazer/Refazer)
Desfazer/Refazer
Interface Gráfica(Facilita a visualização)

"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("Editor de Texto Simples (Tkinter)")
        master.geometry("800x600") # Define o tamanho inicial da janela

        self.current_file = None # Armazena o caminho do arquivo atualmente aberto

        # --- Widget de Texto Principal ---
        # Usamos scrolledtext.ScrolledText para ter barras de rolagem automáticas
        self.text_area = scrolledtext.ScrolledText(master, wrap='word', undo=True)
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)

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
        self.file_menu.add_command(label="Sair", command=master.quit)

        # Menu 'Editar' (opcional, mas bom para desfazer/refazer)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Desfazer", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Refazer", command=self.text_area.edit_redo)

        # --- Status Bar ---
        self.status_bar = tk.Label(master, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_title()

    def update_title(self):
        """Atualiza o título da janela para mostrar o nome do arquivo."""
        if self.current_file:
            self.master.title(f"Editor de Texto Simples - {self.current_file.split('/')[-1]}")
        else:
            self.master.title("Editor de Texto Simples - Sem Título")

    def new_file(self):
        """Cria um novo arquivo (limpa a área de texto)."""
        if self.text_area.get(1.0, tk.END).strip() and \
           not messagebox.askyesno("Novo Arquivo", "Deseja salvar as alterações antes de criar um novo arquivo?"):
            # Se o texto não estiver vazio e o usuário não quiser salvar, continua
            pass
        else:
            self.save_file() # Tenta salvar se o usuário quiser
        
        self.text_area.delete(1.0, tk.END) # Limpa todo o texto
        self.current_file = None
        self.update_title()
        self.status_bar.config(text="Novo arquivo criado.")

    def open_file(self):
        """Abre um arquivo existente."""
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
                self.update_title()
                self.status_bar.config(text=f"Arquivo '{filepath.split('/')[-1]}' aberto.")
            except Exception as e:
                messagebox.showerror("Erro ao Abrir Arquivo", f"Não foi possível abrir o arquivo:\n{e}")
                self.status_bar.config(text="Erro ao abrir arquivo.")

    def save_file(self):
        """Salva o arquivo atual. Se for um novo arquivo, chama 'Salvar Como'."""
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                self.status_bar.config(text=f"Arquivo '{self.current_file.split('/')[-1]}' salvo.")
                return True
            except Exception as e:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Não foi possível salvar o arquivo:\n{e}")
                self.status_bar.config(text="Erro ao salvar arquivo.")
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
                self.update_title()
                self.status_bar.config(text=f"Arquivo '{filepath.split('/')[-1]}' salvo como.")
                return True
            except Exception as e:
                messagebox.showerror("Erro ao Salvar Arquivo", f"Não foi possível salvar o arquivo:\n{e}")
                self.status_bar.config(text="Erro ao salvar arquivo.")
                return False
        return False # Retorna False se o usuário cancelar a caixa de diálogo

# --- Execução do Editor ---
if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()