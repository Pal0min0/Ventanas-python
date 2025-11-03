from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk


class TiendaApp:
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("Tienda Virtual 🛒")
        self.raiz.geometry("700x550")
        self.raiz.config(bg="#f0f0f0")
        self.raiz.resizable(False, False)

        self.productos = {
            "Miku": {"precio": 1_200_000, "imagen": "img/figura py (1).jpg"},
            "Iron_Man": {"precio": 45_000, "imagen": "img/figura 2 py.jpg"},
            "Muñeca_inf": {"precio": 85_000, "imagen": "img/figura 3 py.jpg"}
        }

        self.carrito = {}

        self._crear_pestanas()
        self._crear_menu()

        self.raiz.mainloop()

    """_________________________________________"""

    def _crear_menu(self):
        barra = Menu(self.raiz)
        self.raiz.config(menu=barra)

        menu_tienda = Menu(barra, tearoff=0)
        menu_tienda.add_command(label="Ver Catálogo", command=lambda: self.notebook.select(0))
        menu_tienda.add_command(label="Ver Carrito", command=lambda: self.notebook.select(1))
        menu_tienda.add_command(label="Ver Factura", command=lambda: self.notebook.select(2))
        menu_tienda.add_separator()
        menu_tienda.add_command(label="Vaciar Carrito", command=self.vaciar_carrito)
        menu_tienda.add_separator()
        menu_tienda.add_command(label="Salir", command=self.salir)
        barra.add_cascade(label="Menú", menu=menu_tienda)

        menu_ayuda = Menu(barra, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.acerca_de)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

    """_________________________________________"""

    def _crear_pestanas(self):
        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(expand=True, fill='both', padx=15, pady=15)

        self._crear_pestana_catalogo()
        self._crear_pestana_carrito()
        self._crear_pestana_factura()

    """_________________________________________"""

    def _crear_pestana_catalogo(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛍️ Catálogo")

        Label(tab, text="CATÁLOGO DE PRODUCTOS", font=("Arial", 18, "bold"),
              bg="#4CAF50", fg="white", pady=15).pack(fill='x')

        canvas = Canvas(tab, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        contenedor = Frame(canvas, bg="#f0f0f0")

        contenedor.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=contenedor, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 🖼️ Mostrar productos
        for idx, (nombre, info) in enumerate(self.productos.items()):
            frame = Frame(contenedor, bg="white", relief="raised", bd=2)
            frame.pack(pady=10, padx=20, fill='x')

            # Mostrar imagen real
            try:
                img = Image.open(info["imagen"])
                img = img.resize((120, 120))
                img_tk = ImageTk.PhotoImage(img)
                lbl_img = Label(frame, image=img_tk, bg="white")
                lbl_img.image = img_tk  # evitar garbage collection
                lbl_img.pack(pady=10)
            except Exception as e:
                Label(frame, text="(Imagen no encontrada)", fg="red", bg="white").pack(pady=10)
                print(f"Error al cargar {info['imagen']}: {e}")

            Label(frame, text=nombre, font=("Arial", 14, "bold"), bg="white").pack()
            Label(frame, text=f"${info['precio']:,}", font=("Arial", 12),
                  fg="#4CAF50", bg="white").pack(pady=5)

            cantidad_frame = Frame(frame, bg="white")
            cantidad_frame.pack(pady=10)

            cantidad_var = IntVar(value=1)

            def crear_controles(n, c_var, f):
                def restar():
                    if c_var.get() > 1:
                        c_var.set(c_var.get() - 1)

                def sumar():
                    if c_var.get() < 99:
                        c_var.set(c_var.get() + 1)

                def agregar():
                    cant = c_var.get()
                    self.carrito[n] = self.carrito.get(n, 0) + cant
                    messagebox.showinfo("¡Listo!", f"Se agregaron {cant} {n}(s) al carrito")
                    self._actualizar_carrito()
                    c_var.set(1)

                Button(f, text="−", font=("Arial", 14, "bold"), width=2,
                       bg="#f44336", fg="white", command=restar, cursor="hand2").pack(side='left', padx=3)
                Label(f, textvariable=c_var, font=("Arial", 14, "bold"),
                      width=4, bg="#f0f0f0").pack(side='left', padx=5)
                Button(f, text="+", font=("Arial", 14, "bold"), width=2,
                       bg="#4CAF50", fg="white", command=sumar, cursor="hand2").pack(side='left', padx=3)
                Button(f, text="🛒 Agregar", bg="#2196F3", fg="white",
                       font=("Arial", 10, "bold"), command=agregar,
                       cursor="hand2", padx=15, pady=5).pack(side='left', padx=10)

            crear_controles(nombre, cantidad_var, cantidad_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        Button(tab, text="🛒 IR AL CARRITO", bg="#FF9800", fg="white",
               font=("Arial", 12, "bold"), command=lambda: self.notebook.select(1),
               cursor="hand2", padx=30, pady=12).pack(pady=15)

    """_________________________________________"""

    def _crear_pestana_carrito(self):
        self.tab_carrito = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_carrito, text="🛒 Carrito")

        Label(self.tab_carrito, text="CARRITO DE COMPRAS", font=("Arial", 18, "bold"),
              bg="#2196F3", fg="white", pady=15).pack(fill='x')

        self.canvas_carrito = Canvas(self.tab_carrito, bg="white")
        scrollbar_carrito = ttk.Scrollbar(self.tab_carrito, orient="vertical", command=self.canvas_carrito.yview)
        self.frame_carrito = Frame(self.canvas_carrito, bg="white")

        self.frame_carrito.bind(
            "<Configure>",
            lambda e: self.canvas_carrito.configure(scrollregion=self.canvas_carrito.bbox("all"))
        )

        self.canvas_carrito.create_window((0, 0), window=self.frame_carrito, anchor="nw")
        self.canvas_carrito.configure(yscrollcommand=scrollbar_carrito.set)

        self.canvas_carrito.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar_carrito.pack(side="right", fill="y")

        self._actualizar_carrito()

    """_________________________________________"""

    def _actualizar_carrito(self):
        for widget in self.frame_carrito.winfo_children():
            widget.destroy()

        if not self.carrito:
            Label(self.frame_carrito, text="🛒 El carrito está vacío",
                  font=("Arial", 14), fg="gray", bg="white").pack(pady=50)
            return

        total = 0
        for nombre, cantidad in self.carrito.items():
            info = self.productos[nombre]
            subtotal = info["precio"] * cantidad
            total += subtotal

            item = Frame(self.frame_carrito, bg="#f9f9f9", relief="groove", bd=1)
            item.pack(fill='x', pady=5, padx=10)

            # Mostrar imagen en carrito
            try:
                img = Image.open(info["imagen"])
                img = img.resize((70, 70))
                img_tk = ImageTk.PhotoImage(img)
                lbl = Label(item, image=img_tk, bg="#f9f9f9")
                lbl.image = img_tk
                lbl.pack(side='left', padx=10)
            except Exception as e:
                Label(item, text="[Img]", bg="#f9f9f9").pack(side='left', padx=10)
                print(f"Error cargando {info['imagen']}: {e}")

            info_frame = Frame(item, bg="#f9f9f9")
            info_frame.pack(side='left', fill='both', expand=True, pady=10)

            Label(info_frame, text=nombre, font=("Arial", 12, "bold"), bg="#f9f9f9", anchor='w').pack(fill='x')
            Label(info_frame, text=f"Cantidad: {cantidad} × ${info['precio']:,}",
                  font=("Arial", 10), bg="#f9f9f9", anchor='w').pack(fill='x')
            Label(info_frame, text=f"Subtotal: ${subtotal:,}", font=("Arial", 11, "bold"),
                  fg="#4CAF50", bg="#f9f9f9", anchor='w').pack(fill='x')

            Button(item, text="✕", bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                   command=lambda n=nombre: self._eliminar_del_carrito(n),
                   cursor="hand2").pack(side='right', padx=10)

        barra_total = Frame(self.frame_carrito, bg="#4CAF50")
        barra_total.pack(fill='x', pady=10, padx=10)
        Label(barra_total, text=f"TOTAL: ${total:,}", font=("Arial", 16, "bold"),
              fg="white", bg="#4CAF50", pady=10).pack()

        Button(self.frame_carrito, text="📄 GENERAR FACTURA", bg="#FF9800", fg="white",
               font=("Arial", 12, "bold"), command=self._generar_factura,
               cursor="hand2", padx=30, pady=12).pack(pady=20)

    """_________________________________________"""

    def _eliminar_del_carrito(self, nombre):
        if messagebox.askyesno("Eliminar", f"¿Quitar {nombre} del carrito?"):
            del self.carrito[nombre]
            self._actualizar_carrito()

    """_________________________________________"""

    def vaciar_carrito(self):
        if self.carrito and messagebox.askyesno("Vaciar", "¿Vaciar todo el carrito?"):
            self.carrito.clear()
            self._actualizar_carrito()
            messagebox.showinfo("Listo", "Carrito vaciado")

    """_________________________________________"""

    def _crear_pestana_factura(self):
        self.tab_factura = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_factura, text="📄 Factura")

        Label(self.tab_factura, text="FACTURA DE COMPRA", font=("Arial", 18, "bold"),
              bg="#673AB7", fg="white", pady=15).pack(fill='x')

        canvas_factura = Canvas(self.tab_factura, bg="white")
        scrollbar_factura = ttk.Scrollbar(self.tab_factura, orient="vertical", command=canvas_factura.yview)
        self.frame_factura = Frame(canvas_factura, bg="white")

        self.frame_factura.bind(
            "<Configure>",
            lambda e: canvas_factura.configure(scrollregion=canvas_factura.bbox("all"))
        )

        canvas_factura.create_window((0, 0), window=self.frame_factura, anchor="nw")
        canvas_factura.configure(yscrollcommand=scrollbar_factura.set)

        canvas_factura.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar_factura.pack(side="right", fill="y")

    """_________________________________________"""

    def _generar_factura(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacío", "Agrega productos antes de facturar")
            return

        for widget in self.frame_factura.winfo_children():
            widget.destroy()

        Label(self.frame_factura, text="🏪 TIENDA VIRTUAL", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        Label(self.frame_factura, text="NIT: 900.123.456-7", font=("Arial", 10), bg="white").pack()
        Label(self.frame_factura, text=f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}",
              font=("Arial", 10), bg="white").pack(pady=5)

        Frame(self.frame_factura, height=2, bg="#673AB7").pack(fill='x', pady=10, padx=20)

        total = sum(self.productos[n]["precio"] * c for n, c in self.carrito.items())
        for nombre, cantidad in self.carrito.items():
            info = self.productos[nombre]
            subtotal = info["precio"] * cantidad
            item = Frame(self.frame_factura, bg="white")
            item.pack(fill='x', pady=3, padx=20)

            # Imagen en factura
            try:
                img = Image.open(info["imagen"])
                img = img.resize((40, 40))
                img_tk = ImageTk.PhotoImage(img)
                lbl = Label(item, image=img_tk, bg="white")
                lbl.image = img_tk
                lbl.pack(side='left', padx=5)
            except:
                Label(item, text="[Img]", bg="white").pack(side='left', padx=5)

            Label(item, text=f"{nombre}", font=("Arial", 11), bg="white", anchor='w', width=25).pack(side='left')
            Label(item, text=f"x{cantidad}", font=("Arial", 11), bg="white", width=6).pack(side='left')
            Label(item, text=f"${subtotal:,}", font=("Arial", 11), bg="white").pack(side='right')

        Frame(self.frame_factura, height=2, bg="#673AB7").pack(fill='x', pady=10, padx=20)

        subtotal = total / 1.19
        iva = total - subtotal

        Label(self.frame_factura, text=f"Subtotal: ${subtotal:,.0f}", font=("Arial", 11), bg="white", anchor='e').pack(fill='x', padx=20)
        Label(self.frame_factura, text=f"IVA (19%): ${iva:,.0f}", font=("Arial", 11), bg="white", anchor='e').pack(fill='x', padx=20)

        barra_total = Frame(self.frame_factura, bg="#4CAF50")
        barra_total.pack(fill='x', pady=10, padx=20)
        Label(barra_total, text=f"TOTAL A PAGAR: ${total:,}", font=("Arial", 14, "bold"),
              fg="white", bg="#4CAF50", pady=10).pack()

        Label(self.frame_factura, text="¡Gracias por su compra!", font=("Arial", 12, "italic"),
              fg="#673AB7", bg="white").pack(pady=20)

        botones = Frame(self.frame_factura, bg="white")
        botones.pack(pady=10)
        Button(botones, text="✅ Finalizar Compra", bg="#4CAF50", fg="white",
               font=("Arial", 11, "bold"), command=self._confirmar_compra,
               cursor="hand2", padx=20, pady=10).pack(side='left', padx=5)
        Button(botones, text="❌ Cancelar", bg="#f44336", fg="white",
               font=("Arial", 11, "bold"), command=self._cancelar_factura,
               cursor="hand2", padx=20, pady=10).pack(side='left', padx=5)

        self.notebook.select(2)

    """_________________________________________"""

    def _confirmar_compra(self):
        if messagebox.askyesno("Confirmar compra", "¿de verdad me vas a comprar?, buenaaaa sos lo mejor"):
            messagebox.showinfo("ya listo compraste", "Gracias perrito por comprar, dios te bendiga\n¡Vuelve, vuelve pronto!")
            self.carrito.clear()
            self._actualizar_carrito()
            for widget in self.frame_factura.winfo_children():
                widget.destroy()
            Label(self.frame_factura, text="✅ Compra finalizada exitosamente",
                  font=("Arial", 14, "bold"), fg="#4CAF50", bg="white").pack(pady=50)
            self.notebook.select(0)

    """_________________________________________"""

    def _cancelar_factura(self):
        if messagebox.askyesno("Cancelar", "¿Deseas cancelar y volver al carrito?"):
            self.notebook.select(1)

    """_________________________________________"""

    def acerca_de(self):
        messagebox.showinfo("Acerca de", "si le diste al boton ayuda, mejor ayudame con esta")

    """_________________________________________"""

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Seguro que deseas salir?"):
            self.raiz.destroy()


"""_________________________________________"""

if __name__ == "__main__":
    app = TiendaApp()
