import os
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tabulate import tabulate
import json # Para guardar/cargar configuración

# --- Configuración de CustomTkinter ---
# Estos se establecerán al cargar la configuración
# ctk.set_appearance_mode("System")
# ctk.set_default_color_theme("blue")

class InvestmentCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora Avanzada de Inversiones 🚀")
        self.geometry("1200x800")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Variables de configuración predeterminadas ---
        self.moneda_simbolo = "€"
        self.decimal_places = 2
        self.current_appearance_mode = "System"
        self.current_color_theme = "blue"

        # --- Frames principales ---
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.home_frame = ctk.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.analysis_frame = ctk.CTkFrame(self, corner_radius=0)
        self.analysis_frame.grid_columnconfigure(1, weight=1) # Columna para resultados/gráficos

        self.guide_frame = ctk.CTkFrame(self, corner_radius=0)
        self.guide_frame.grid_columnconfigure(0, weight=1)
        self.guide_frame.grid_rowconfigure(1, weight=1)

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.grid_columnconfigure(0, weight=1)

        self.about_frame = ctk.CTkFrame(self, corner_radius=0)
        self.about_frame.grid_columnconfigure(0, weight=1)
        self.about_frame.grid_rowconfigure(1, weight=1)

        # --- Elementos del Frame de Navegación ---
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Menú Principal",
                                                    compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, text="Inicio", command=self.select_frame_by_name("home"))
        self.home_button.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        self.analysis_button = ctk.CTkButton(self.navigation_frame, text="Análisis de Inversión", command=self.select_frame_by_name("analysis"))
        self.analysis_button.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.guide_button = ctk.CTkButton(self.navigation_frame, text="Guía para Novatos", command=self.select_frame_by_name("guide"))
        self.guide_button.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        self.settings_button = ctk.CTkButton(self.navigation_frame, text="Configuración", command=self.select_frame_by_name("settings"))
        self.settings_button.grid(row=4, column=0, sticky="ew", padx=20, pady=10)

        self.about_button = ctk.CTkButton(self.navigation_frame, text="Acerca de", command=self.select_frame_by_name("about"))
        self.about_button.grid(row=5, column=0, sticky="ew", padx=20, pady=10)

        self.exit_button = ctk.CTkButton(self.navigation_frame, text="Salir", fg_color="red", command=self.quit)
        self.exit_button.grid(row=7, column=0, sticky="ew", padx=20, pady=10)

        # --- Elementos del Frame de Inicio ---
        self.home_label = ctk.CTkLabel(self.home_frame, text="Bienvenido a la Calculadora de Inversiones", font=ctk.CTkFont(size=24, weight="bold"))
        self.home_label.grid(row=0, column=0, padx=20, pady=20)
        self.home_text = ctk.CTkTextbox(self.home_frame, wrap="word", width=600, height=300)
        self.home_text.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.home_text.insert("end", "Esta aplicación te ayuda a responder preguntas típicas de Shark Tank México de forma simple: cuánto valora tu empresa, cuánto porcentaje cedes y si una oferta parece razonable.\n\n"
                                     "También puedes hacer un análisis más completo de inversión, pero el modo rápido está pensado para decisiones ágiles y claras.\n\n"
                                     "Utiliza el menú de la izquierda para navegar por las diferentes secciones.")
        self.home_text.configure(state="disabled")

        self.shark_tank_frame = ctk.CTkFrame(self.home_frame, corner_radius=10)
        self.shark_tank_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.shark_tank_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.shark_tank_frame, text="Análisis rápido para Shark Tank México", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        self.shark_label_inversion_solicitada = ctk.CTkLabel(self.shark_tank_frame, text=f"Inversión que piden ({self.moneda_simbolo}):")
        self.shark_label_inversion_solicitada.grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.entry_inversion_solicitada = ctk.CTkEntry(self.shark_tank_frame)
        self.entry_inversion_solicitada.grid(row=1, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self.shark_tank_frame, text="Porcentaje que ofrecen (%):").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.entry_porcentaje_ofrecido = ctk.CTkEntry(self.shark_tank_frame)
        self.entry_porcentaje_ofrecido.grid(row=2, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self.shark_tank_frame, text="Ingresos anuales estimados (opcional):").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.entry_ingresos_anuales = ctk.CTkEntry(self.shark_tank_frame)
        self.entry_ingresos_anuales.grid(row=3, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self.shark_tank_frame, text="Modo de respuesta:").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.shark_mode_var = ctk.StringVar(value="Ambos")
        self.shark_mode_optionmenu = ctk.CTkOptionMenu(self.shark_tank_frame, values=["Emprendedor", "Inversionista", "Ambos"], variable=self.shark_mode_var)
        self.shark_mode_optionmenu.grid(row=4, column=1, sticky="ew", padx=10, pady=4)

        self.shark_tank_button = ctk.CTkButton(self.shark_tank_frame, text="Evaluar oferta rápida", command=self.evaluar_oferta_shark_tank)
        self.shark_tank_button.grid(row=5, column=0, columnspan=2, pady=(10, 8))

        self.shark_tank_result = ctk.CTkTextbox(self.shark_tank_frame, height=140, wrap="word")
        self.shark_tank_result.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        self.shark_tank_result.insert("end", "Completa los datos para ver una respuesta breve y clara para una posible negociación.")
        self.shark_tank_result.configure(state="disabled")

        # --- Elementos del Frame de Análisis ---
        self.analysis_input_frame = ctk.CTkFrame(self.analysis_frame)
        self.analysis_input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.analysis_input_frame.grid_columnconfigure(0, weight=1)

        self.analysis_title = ctk.CTkLabel(self.analysis_input_frame, text="Datos de la Inversión", font=ctk.CTkFont(size=18, weight="bold"))
        self.analysis_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.label_valor_participacion = ctk.CTkLabel(self.analysis_input_frame, text=f"Valor de la Participación ({self.moneda_simbolo}):")
        self.label_valor_participacion.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_valor_participacion = ctk.CTkEntry(self.analysis_input_frame)
        self.entry_valor_participacion.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.label_porcentaje_adquirido = ctk.CTkLabel(self.analysis_input_frame, text="Porcentaje Adquirido (%):")
        self.label_porcentaje_adquirido.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_porcentaje_adquirido = ctk.CTkEntry(self.analysis_input_frame)
        self.entry_porcentaje_adquirido.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.label_tipo_data_financiera = ctk.CTkLabel(self.analysis_input_frame, text="Tipo de Datos Financieros:")
        self.label_tipo_data_financiera.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.tipo_data_financiera_var = ctk.StringVar(value="BN")
        self.radio_bn = ctk.CTkRadioButton(self.analysis_input_frame, text="Beneficio Neto (BN)", variable=self.tipo_data_financiera_var, value="BN")
        self.radio_bn.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.radio_fcl = ctk.CTkRadioButton(self.analysis_input_frame, text="Flujo de Caja Libre (FCL)", variable=self.tipo_data_financiera_var, value="FCL")
        self.radio_fcl.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Entradas para datos históricos
        self.historical_data_entries = {}
        self.historical_labels = {}
        for i in range(5, 0, -1):
            año_label = f"Año -{i}"
            label = ctk.CTkLabel(self.analysis_input_frame, text=f"{año_label} ({self.moneda_simbolo} o N/A):")
            label.grid(row=4+i, column=0, sticky="w", padx=5, pady=2)
            entry = ctk.CTkEntry(self.analysis_input_frame)
            entry.grid(row=4+i, column=1, sticky="ew", padx=5, pady=2)
            self.historical_data_entries[año_label] = entry
            self.historical_labels[año_label] = label # Guardar referencia al label para actualizar moneda

        self.label_tasa_crecimiento = ctk.CTkLabel(self.analysis_input_frame, text="Tasa de Crecimiento Anual (Base - %):")
        self.label_tasa_crecimiento.grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.entry_tasa_crecimiento = ctk.CTkEntry(self.analysis_input_frame)
        self.entry_tasa_crecimiento.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        self.label_anios_proyeccion = ctk.CTkLabel(self.analysis_input_frame, text="Años Futuros a Proyectar:")
        self.label_anios_proyeccion.grid(row=11, column=0, sticky="w", padx=5, pady=5)
        self.entry_anios_proyeccion = ctk.CTkEntry(self.analysis_input_frame)
        self.entry_anios_proyeccion.grid(row=11, column=1, sticky="ew", padx=5, pady=5)

        self.label_tasa_descuento = ctk.CTkLabel(self.analysis_input_frame, text="Tasa de Descuento (Base - %):")
        self.label_tasa_descuento.grid(row=12, column=0, sticky="w", padx=5, pady=5)
        self.entry_tasa_descuento = ctk.CTkEntry(self.analysis_input_frame)
        self.entry_tasa_descuento.grid(row=12, column=1, sticky="ew", padx=5, pady=5)

        # Escenario Optimista
        self.scenario_opt_frame = ctk.CTkFrame(self.analysis_input_frame)
        self.scenario_opt_frame.grid(row=13, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        self.scenario_opt_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.scenario_opt_frame, text="Escenario Optimista", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        ctk.CTkLabel(self.scenario_opt_frame, text="Tasa de Crecimiento (%):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_tasa_crecimiento_opt = ctk.CTkEntry(self.scenario_opt_frame)
        self.entry_tasa_crecimiento_opt.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkLabel(self.scenario_opt_frame, text="Tasa de Descuento (%):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_tasa_descuento_opt = ctk.CTkEntry(self.scenario_opt_frame)
        self.entry_tasa_descuento_opt.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        # Escenario Pesimista
        self.scenario_pes_frame = ctk.CTkFrame(self.analysis_input_frame)
        self.scenario_pes_frame.grid(row=14, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        self.scenario_pes_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.scenario_pes_frame, text="Escenario Pesimista", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        ctk.CTkLabel(self.scenario_pes_frame, text="Tasa de Crecimiento (%):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_tasa_crecimiento_pes = ctk.CTkEntry(self.scenario_pes_frame)
        self.entry_tasa_crecimiento_pes.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ctk.CTkLabel(self.scenario_pes_frame, text="Tasa de Descuento (%):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_tasa_descuento_pes = ctk.CTkEntry(self.scenario_pes_frame)
        self.entry_tasa_descuento_pes.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        
        # Un solo botón para realizar todos los análisis
        self.run_all_analysis_button = ctk.CTkButton(self.analysis_input_frame, text="Realizar Análisis Completo", command=self.run_all_scenarios)
        self.run_all_analysis_button.grid(row=15, column=0, columnspan=2, pady=20)


        # --- Área de resultados con pestañas ---
        self.results_tabview = ctk.CTkTabview(self.analysis_frame)
        self.results_tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.results_tabview.grid_columnconfigure(0, weight=1) # Make content inside tabs expandable

        # Crear pestañas
        self.tab_historical = self.results_tabview.add("Desglose Anual Histórico")
        self.tab_base_projection = self.results_tabview.add("Proyección Base (VAN/TIR)")
        self.tab_optimistic = self.results_tabview.add("Escenario Optimista")
        self.tab_pessimistic = self.results_tabview.add("Escenario Pesimista")

        # Configurar contenido de cada pestaña
        self.historical_scroll_frame = self.setup_results_tab_content(self.tab_historical)
        self.base_projection_scroll_frame = self.setup_results_tab_content(self.tab_base_projection, include_graph=True)
        self.optimistic_scroll_frame = self.setup_results_tab_content(self.tab_optimistic)
        self.pessimistic_scroll_frame = self.setup_results_tab_content(self.tab_pessimistic)
        
        # Referencia al frame del canvas del gráfico dentro de la pestaña base
        self.base_graph_canvas_frame = self.base_projection_scroll_frame.children["!ctkframe"] # Access the graph frame directly

        # Graph type selection for the base projection tab
        self.graph_type_var = ctk.StringVar(value="Barras")
        self.graph_type_optionmenu = ctk.CTkOptionMenu(self.base_projection_scroll_frame, values=["Barras", "Líneas"],
                                                        variable=self.graph_type_var, command=self.update_graph_type)
        self.graph_type_optionmenu.pack(pady=10) # Place above the graph frame within the scrollable frame

        # Store graph data to redraw when type changes
        self.last_graph_data = None


        # --- Elementos del Frame de Guía ---
        self.guide_title = ctk.CTkLabel(self.guide_frame, text="Guía para Inversores Novatos", font=ctk.CTkFont(size=24, weight="bold"))
        self.guide_title.grid(row=0, column=0, padx=20, pady=20)
        self.guide_textbox = ctk.CTkTextbox(self.guide_frame, wrap="word", width=800, height=600)
        self.guide_textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.load_guide_content()
        self.guide_textbox.configure(state="disabled")

        # --- Elementos del Frame de Configuración ---
        self.settings_title = ctk.CTkLabel(self.settings_frame, text="Configuración", font=ctk.CTkFont(size=24, weight="bold"))
        self.settings_title.grid(row=0, column=0, padx=20, pady=20)

        # Moneda
        self.label_moneda = ctk.CTkLabel(self.settings_frame, text="Símbolo de Moneda Actual:")
        self.label_moneda.grid(row=1, column=0, sticky="w", padx=20, pady=5)
        self.entry_moneda = ctk.CTkEntry(self.settings_frame)
        self.entry_moneda.grid(row=1, column=1, sticky="ew", padx=20, pady=5)

        # Modo de Apariencia
        self.label_appearance = ctk.CTkLabel(self.settings_frame, text="Modo de Apariencia:")
        self.label_appearance.grid(row=2, column=0, sticky="w", padx=20, pady=5)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=1, sticky="ew", padx=20, pady=5)

        # Tema de Color
        self.label_color_theme = ctk.CTkLabel(self.settings_frame, text="Tema de Color:")
        self.label_color_theme.grid(row=3, column=0, sticky="w", padx=20, pady=5)
        self.color_theme_optionemenu = ctk.CTkOptionMenu(self.settings_frame, values=["blue", "dark-blue", "green"],
                                                            command=self.change_color_theme_event)
        self.color_theme_optionemenu.grid(row=3, column=1, sticky="ew", padx=20, pady=5)

        # Decimales
        self.label_decimal_places = ctk.CTkLabel(self.settings_frame, text="Decimales en Resultados:")
        self.label_decimal_places.grid(row=4, column=0, sticky="w", padx=20, pady=5)
        self.entry_decimal_places = ctk.CTkEntry(self.settings_frame)
        self.entry_decimal_places.grid(row=4, column=1, sticky="ew", padx=20, pady=5)

        # Información de la aplicación en configuración
        self.info_label_settings = ctk.CTkLabel(self.settings_frame, text="Información de la Aplicación:", font=ctk.CTkFont(weight="bold"))
        self.info_label_settings.grid(row=7, column=0, columnspan=2, pady=(20, 5))
        self.info_text_settings = ctk.CTkLabel(self.settings_frame, text="Versión: 1.2\nAutor: José Manuel Caamaño González\nÚltima Actualización: Julio 2025", justify="left")
        self.info_text_settings.grid(row=8, column=0, columnspan=2, padx=20, pady=5, sticky="w")


        self.save_settings_button = ctk.CTkButton(self.settings_frame, text="Guardar Configuración", command=self.save_settings)
        self.save_settings_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.reset_settings_button = ctk.CTkButton(self.settings_frame, text="Restablecer Configuración", command=self.reset_settings, fg_color="orange")
        self.reset_settings_button.grid(row=6, column=0, columnspan=2, pady=10)

        # --- Elementos del Frame de Acerca de ---
        self.about_title = ctk.CTkLabel(self.about_frame, text="Acerca de esta Aplicación", font=ctk.CTkFont(size=24, weight="bold"))
        self.about_title.grid(row=0, column=0, padx=20, pady=20)
        self.about_textbox = ctk.CTkTextbox(self.about_frame, wrap="word", width=800, height=400)
        self.about_textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.about_textbox.insert("end", "Esta Calculadora Avanzada de Inversiones ha sido desarrollada por José Manuel Caamaño González.\n\n"
                                        "El objetivo de este programa es proporcionar una herramienta robusta y fácil de usar para analizar la viabilidad financiera de diversas inversiones, utilizando métricas estándar de valoración.\n\n"
                                        "La aplicación utiliza librerías de Python como `CustomTkinter` para la interfaz gráfica, `NumPy` y `NumPy-Financial` para los cálculos financieros, `Matplotlib` para la visualización de gráficos y `Tabulate` para el formato de tablas en los resultados.\n\n"
                                        "¡Espero que te sea de gran utilidad en tus decisiones de inversión!")
        self.about_textbox.configure(state="disabled")

        # Cargar y aplicar configuración después de que todos los widgets existan
        self._load_settings_from_file()
        self._apply_settings_to_gui()

        # Seleccionar frame inicial
        self.select_frame_by_name("home")

    def setup_results_tab_content(self, parent_tab, include_graph=False):
        """Configura un CTkScrollableFrame dentro de una pestaña y opcionalmente un frame para el gráfico."""
        scroll_frame = ctk.CTkScrollableFrame(parent_tab, corner_radius=10)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1) # Allow content inside to expand

        if include_graph:
            graph_frame = ctk.CTkFrame(scroll_frame, corner_radius=10, fg_color="transparent") # Transparent for graph background
            graph_frame.pack(fill="both", expand=True, padx=5, pady=5)
            graph_frame.grid_columnconfigure(0, weight=1)
            graph_frame.grid_rowconfigure(0, weight=1)
            # Store a reference to this specific graph frame for the base projection tab
            # This is accessed via self.base_projection_scroll_frame.children["!ctkframe"]
            
        return scroll_frame # Return the scrollable frame to add content to it

    def create_data_box(self, parent_frame, title, metrics_dict, is_highlight=False):
        """Crea una caja de datos con título y métricas."""
        box_frame = ctk.CTkFrame(parent_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        box_frame.pack(fill="x", padx=10, pady=5, expand=True)
        box_frame.grid_columnconfigure(1, weight=1) # Allow values column to expand

        title_font = ctk.CTkFont(weight="bold", size=14)
        if is_highlight:
            title_font = ctk.CTkFont(weight="bold", size=16)
            box_frame.configure(fg_color=("lightblue", "darkblue")) # Highlight color

        ctk.CTkLabel(box_frame, text=title, font=title_font).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        row_idx = 1
        for label_text, value_text in metrics_dict.items():
            ctk.CTkLabel(box_frame, text=f"{label_text}:", anchor="w").grid(row=row_idx, column=0, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(box_frame, text=value_text, anchor="e", font=ctk.CTkFont(weight="bold")).grid(row=row_idx, column=1, padx=10, pady=2, sticky="ew")
            row_idx += 1
        return box_frame

    def select_frame_by_name(self, name):
        """Muestra el frame seleccionado y oculta los demás."""
        def switch_frame():
            # set button color for selected button
            self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
            self.analysis_button.configure(fg_color=("gray75", "gray25") if name == "analysis" else "transparent")
            self.guide_button.configure(fg_color=("gray75", "gray25") if name == "guide" else "transparent")
            self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
            self.about_button.configure(fg_color=("gray75", "gray25") if name == "about" else "transparent")

            # show selected frame
            if name == "home":
                self.home_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.home_frame.grid_forget()
            if name == "analysis":
                self.analysis_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.analysis_frame.grid_forget()
            if name == "guide":
                self.guide_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.guide_frame.grid_forget()
            if name == "settings":
                self.settings_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.settings_frame.grid_forget()
            if name == "about":
                self.about_frame.grid(row=0, column=1, sticky="nsew")
            else:
                self.about_frame.grid_forget()
        return switch_frame

    def show_message(self, title, message, is_error=False):
        """Muestra un cuadro de mensaje simple."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.transient(self) # Make dialog appear on top of the main window
        dialog.grab_set() # Disable interaction with the main window

        label_color = "red" if is_error else "green"
        ctk.CTkLabel(dialog, text=message, text_color=label_color, wraplength=350, font=ctk.CTkFont(size=14)).pack(pady=20)
        ctk.CTkButton(dialog, text="Aceptar", command=dialog.destroy).pack(pady=10)

    def analizar_oferta_shark_tank(self, inversion_solicitada, porcentaje_ofrecido, ingresos_anuales=None):
        """Devuelve una respuesta simple y útil para una oferta tipo Shark Tank México."""
        if inversion_solicitada is None or porcentaje_ofrecido is None:
            return None

        if porcentaje_ofrecido <= 0 or porcentaje_ofrecido > 100:
            return None

        valoracion_implícita = inversion_solicitada / (porcentaje_ofrecido / 100)
        porcentaje_que_mantienes = 100 - porcentaje_ofrecido
        multiplo_ingresos = None
        if ingresos_anuales is not None and ingresos_anuales > 0:
            multiplo_ingresos = valoracion_implícita / ingresos_anuales

        if porcentaje_ofrecido <= 10:
            mensaje = "Oferta relativamente razonable: no cedes demasiado del negocio."
        elif porcentaje_ofrecido <= 20:
            mensaje = "Oferta bastante agresiva: el inversor está pidiendo una parte importante."
        else:
            mensaje = "Oferta muy agresiva: probablemente conviene negociar mejor el porcentaje."

        if multiplo_ingresos is not None:
            if multiplo_ingresos <= 5:
                mensaje += " La valoración está cerca de los ingresos anuales."
            elif multiplo_ingresos <= 10:
                mensaje += " La valoración es alta, pero todavía razonable para un negocio en crecimiento."
            else:
                mensaje += " La valoración parece muy alta respecto a los ingresos actuales."

        contraoferta_sugerida = None
        if porcentaje_ofrecido > 10:
            contraoferta_sugerida = max(5.0, porcentaje_ofrecido - 5.0)
        elif porcentaje_ofrecido <= 5:
            contraoferta_sugerida = porcentaje_ofrecido

        if contraoferta_sugerida is not None:
            mensaje += f" Sugiero intentar una contraoferta cercana al {contraoferta_sugerida:.1f}% de participación."

        if porcentaje_ofrecido <= 10:
            mensaje += " La oferta está en un rango más defendible."
        elif porcentaje_ofrecido <= 20:
            mensaje += " La oferta es fuerte y merece negociación."
        else:
            mensaje += " La oferta es muy agresiva; conviene rechazar o pedir condiciones mejores."

        if porcentaje_ofrecido <= 8:
            tono_pitch = "confianza"
            respuesta_pitch = (
                f"Estoy viendo una propuesta bastante respetuosa. Mi empresa tiene una valoración de {valoracion_implícita:,.0f} {self.moneda_simbolo} y creo que este nivel de inversión es razonable. "
                f"Quiero mantener un buen control del negocio, pero sí veo valor en contar con un aliado que aporte experiencia y red."
            )
            respuesta_inversionista = (
                f"Esta oferta parece razonable. La valoración implícita es de {valoracion_implícita:,.0f} {self.moneda_simbolo}, y el porcentaje pedido no parece excesivo. "
                f"Si el negocio tiene potencial real, esta puede ser una entrada interesante para un inversor que busque crecimiento con control razonable."
            )
        elif porcentaje_ofrecido <= 15:
            tono_pitch = "equilibrado"
            respuesta_pitch = (
                f"Esta propuesta tiene un punto medio interesante. Mi empresa está valorada en {valoracion_implícita:,.0f} {self.moneda_simbolo} y entiendo que el inversionista busca una participación relevante. "
                f"Estoy abierto a conversar, pero quiero que la relación sea justa y que el apoyo estratégico sea real, no solo financiero."
            )
            respuesta_inversionista = (
                f"La oferta está en un punto medio. La valoración implícita es de {valoracion_implícita:,.0f} {self.moneda_simbolo}, por lo que el porcentaje solicitado empieza a ser relevante. "
                f"Hay espacio para negociar, pero también hay que valorar si el inversor aporta algo más que capital."
            )
        else:
            tono_pitch = "defensivo"
            respuesta_pitch = (
                f"Creo que esta propuesta es demasiado agresiva para el valor que estamos construyendo. Con una valoración de {valoracion_implícita:,.0f} {self.moneda_simbolo}, "
                f"pedir una participación tan alta me obliga a defender mejor el control de la empresa. Quiero que la negociación sea más equilibrada y que el valor del inversionista sea claro."
            )
            respuesta_inversionista = (
                f"Esta propuesta parece demasiado agresiva. Con una valoración implícita de {valoracion_implícita:,.0f} {self.moneda_simbolo}, el porcentaje solicitado puede dejar al emprendedor con muy poco control. "
                f"Yo pediría mejores condiciones o una participación menor si el riesgo sigue siendo alto."
            )

        return {
            "valoracion_implícita": valoracion_implícita,
            "porcentaje_que_mantienes": porcentaje_que_mantienes,
            "multiplo_ingresos": multiplo_ingresos,
            "mensaje": mensaje,
            "contraoferta_sugerida": contraoferta_sugerida,
            "respuesta_pitch": respuesta_pitch,
            "respuesta_inversionista": respuesta_inversionista,
            "tono_pitch": tono_pitch,
        }

    def evaluar_oferta_shark_tank(self):
        """Muestra una respuesta rápida para la oferta ingresada en la pantalla principal."""
        inversion_solicitada = self.obtener_numero_gui(self.entry_inversion_solicitada, solo_positivo=True, permite_cero=False, field_name="Inversión que piden")
        if inversion_solicitada is None:
            return

        porcentaje_ofrecido = self.obtener_numero_gui(self.entry_porcentaje_ofrecido, solo_positivo=True, permite_cero=False, min_val=0.01, max_val=100.0, field_name="Porcentaje que ofrecen")
        if porcentaje_ofrecido is None:
            return

        ingresos_anuales = None
        if self.entry_ingresos_anuales.get().strip():
            ingresos_anuales = self.obtener_numero_gui(self.entry_ingresos_anuales, solo_positivo=True, permite_cero=True, field_name="Ingresos anuales estimados")
            if ingresos_anuales is None:
                return

        resultado = self.analizar_oferta_shark_tank(inversion_solicitada, porcentaje_ofrecido, ingresos_anuales)
        if resultado is None:
            self.show_message("Error de Entrada", "Revisa los valores para obtener una respuesta rápida.", is_error=True)
            return

        self.shark_tank_result.configure(state="normal")
        self.shark_tank_result.delete("1.0", "end")
        texto = (
            f"Respuesta rápida:\n\n"
            f"• Valoración implícita: {resultado['valoracion_implícita']:,.{self.decimal_places}f} {self.moneda_simbolo}\n"
            f"• Porcentaje que cedes: {porcentaje_ofrecido:,.{self.decimal_places}f}%\n"
            f"• Porcentaje que mantienes: {resultado['porcentaje_que_mantienes']:,.{self.decimal_places}f}%\n"
        )
        if resultado['multiplo_ingresos'] is not None:
            texto += f"• Múltiplo sobre ingresos: {resultado['multiplo_ingresos']:,.{self.decimal_places}f}x\n"
        if resultado['contraoferta_sugerida'] is not None:
            texto += f"• Contraoferta sugerida: ~{resultado['contraoferta_sugerida']:.1f}%\n"
        texto += f"\n{resultado['mensaje']}\n\n"
        modo_respuesta = self.shark_mode_var.get()
        if modo_respuesta in ["Emprendedor", "Ambos"]:
            texto += "Respuesta tipo pitch (emprendedor):\n"
            texto += resultado['respuesta_pitch']
        if modo_respuesta in ["Inversionista", "Ambos"]:
            if modo_respuesta == "Ambos":
                texto += "\n\n"
            texto += "Respuesta tipo pitch (inversionista):\n"
            texto += resultado['respuesta_inversionista']
        self.shark_tank_result.insert("end", texto)
        self.shark_tank_result.configure(state="disabled")

    def obtener_numero_gui(self, entry_widget, tipo=float, solo_positivo=False, permite_cero=True, min_val=None, max_val=None, field_name=""):
        """Obtiene y valida un número de un widget de entrada."""
        try:
            entrada_str = entry_widget.get().strip()
            if not entrada_str:
                self.show_message("Error de Entrada", f"Por favor, introduce un valor para '{field_name}'.", is_error=True)
                return None
            
            # Reemplazar comas por puntos para asegurar la correcta conversión a float
            numero = tipo(entrada_str.replace('.', '').replace(',', '.'))

            if solo_positivo and numero < 0:
                self.show_message("Error de Validación", f"'{field_name}' no puede ser negativo.", is_error=True)
                return None
            if solo_positivo and not permite_cero and numero == 0:
                self.show_message("Error de Validación", f"'{field_name}' debe ser positivo y distinto de cero.", is_error=True)
                return None
            if min_val is not None and numero < min_val:
                self.show_message("Error de Validación", f"'{field_name}' no puede ser menor que {min_val}.", is_error=True)
                return None
            if max_val is not None and numero > max_val:
                self.show_message("Error de Validación", f"'{field_name}' no puede ser mayor que {max_val}.", is_error=True)
                return None
            
            return numero
        except ValueError:
            self.show_message("Error de Entrada", f"Entrada inválida para '{field_name}'. Por favor, introduce solo números válidos.", is_error=True)
            return None

    def get_historical_financial_data_gui(self, data_type_label="beneficio neto"):
        """Obtiene los datos financieros históricos de los widgets de entrada."""
        data = {}
        for año_key, entry in self.historical_data_entries.items():
            data_str = entry.get().strip().upper()
            if data_str in ['N', 'NO', 'N/A', '']:
                data[año_key] = None
            else:
                try:
                    valor = float(data_str.replace('.', '').replace(',', '.'))
                    data[año_key] = valor
                except ValueError:
                    self.show_message("Error de Entrada", f"Entrada inválida para {data_type_label} del {año_key}. Introduce un número o 'N/A'.", is_error=True)
                    return None
        return data

    def generar_grafico_flujos(self, años, flujos_empresa, flujos_inversor, titulo, y_label, tipo_data_financiera, target_frame, graph_type="Barras"):
        """Genera y muestra un gráfico de barras/líneas de flujos en la GUI en un frame específico."""
        try:
            # Limpiar el canvas anterior si existe en el target_frame
            for widget in target_frame.winfo_children():
                widget.destroy()
            plt.close('all') # Close all existing matplotlib figures to prevent memory leaks

            # Apply dark mode style if enabled
            if self.current_appearance_mode == "Dark":
                plt.style.use('dark_background')
            else:
                plt.style.use('default')

            fig, ax = plt.subplots(figsize=(10, 6)) # Ajustar tamaño para la GUI
            
            indices = np.arange(len(años))
            
            if graph_type == "Barras":
                bar_width = 0.35
                ax.bar(indices - bar_width/2, flujos_empresa, bar_width, label=f'{tipo_data_financiera.capitalize()} Empresa', color='skyblue', alpha=0.8)
                ax.bar(indices + bar_width/2, flujos_inversor, bar_width, label=f'Ganancia Inversor', color='lightcoral', alpha=0.8)
            elif graph_type == "Líneas":
                ax.plot(indices, flujos_empresa, marker='o', linestyle='-', label=f'{tipo_data_financiera.capitalize()} Empresa', color='skyblue')
                ax.plot(indices, flujos_inversor, marker='o', linestyle='-', label=f'Ganancia Inversor', color='lightcoral')
            
            ax.set_xlabel('Periodo (Años)')
            ax.set_ylabel(f'{y_label} ({self.moneda_simbolo})')
            ax.set_title(titulo)
            ax.set_xticks(indices)
            ax.set_xticklabels(años, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Ajustar límites del eje Y automáticamente para asegurar que las barras/líneas sean visibles
            all_flujos = flujos_empresa + flujos_inversor
            if all_flujos:
                min_val = min(all_flujos)
                max_val = max(all_flujos)
                # Asegurar que el límite inferior sea 0 si todos los valores son positivos
                y_bottom = min(0, min_val * 1.1) if min_val < 0 else 0
                y_top = max_val * 1.1 if max_val > 0 else 0.1 # Añadir un 10% de margen superior, o un pequeño valor si todo es 0/negativo
                if y_bottom == y_top: # Evitar que los límites sean iguales si todos los valores son 0
                    y_top += 1 # Add a small range if all values are zero
                ax.set_ylim(bottom=y_bottom, top=y_top)

            plt.tight_layout()

            # Incrustar el gráfico en CustomTkinter
            canvas = FigureCanvasTkAgg(fig, master=target_frame)
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(fill="both", expand=True)
            canvas.draw()
            plt.close(fig) # Close the figure to free up memory
        except Exception as e:
            self.show_message("Error de Gráfico", f"Ocurrió un error al intentar generar el gráfico: {e}", is_error=True)

    def calcular_van_tir(self, valor_participacion_inversor, porcentaje_adquirido_inversor, ultimo_data_historica, tasa_crecimiento_anual, num_anios_proyeccion, tasa_descuento):
        """
        Calcula el Valor Actual Neto (VAN) y la Tasa Interna de Retorno (TIR).
        Returns:
            tuple: (VAN, TIR, flujos_proyectados_empresa, flujos_proyectados_inversor, años_grafico_proyectado)
        """
        cash_flows = [-valor_participacion_inversor] # La inversión inicial es un flujo de salida
        
        flujos_proyectados_empresa = [ultimo_data_historica] # Incluimos el último histórico para la base del gráfico
        flujos_proyectados_inversor = [(porcentaje_adquirido_inversor / 100) * ultimo_data_historica]
        años_grafico_proyectado = [f"Año 0 (Base)"] # Etiqueta para el último año histórico
        
        for i in range(1, num_anios_proyeccion + 1):
            if i == 1:
                flujo_anual_empresa = ultimo_data_historica * (1 + tasa_crecimiento_anual)
            else:
                flujo_anual_empresa = flujos_proyectados_empresa[-1] * (1 + tasa_crecimiento_anual)
            
            flujo_anual_inversor = (porcentaje_adquirido_inversor / 100) * flujo_anual_empresa
            cash_flows.append(flujo_anual_inversor)
            flujos_proyectados_empresa.append(flujo_anual_empresa)
            flujos_proyectados_inversor.append(flujo_anual_inversor)
            años_grafico_proyectado.append(f"Año +{i}")
        
        van = None
        tir = None
        try:
            np_cash_flows = np.array(cash_flows)
            van = npf.npv(tasa_descuento, np_cash_flows)
            try:
                tir = npf.irr(np_cash_flows)
            except Exception:
                pass # TIR no calculable, se manejará en la impresión
        except Exception as e:
            self.show_message("Error de Cálculo", f"Ocurrió un error al calcular VAN/TIR: {e}", is_error=True)

        return van, tir, flujos_proyectados_empresa, flujos_proyectados_inversor, años_grafico_proyectado

    def populate_historical_tab(self, valor_participacion_inversor, porcentaje_adquirido_inversor, tipo_data_financiera, data_financiera_historica):
        """Popula la pestaña de desglose anual histórico con cajas de datos."""
        # Clear previous content
        for widget in self.historical_scroll_frame.winfo_children():
            widget.destroy()

        # Resumen de la Inversión
        self.create_data_box(self.historical_scroll_frame, "Resumen de la Inversión", {
            "Valor de la Participación": f"{valor_participacion_inversor:,.{self.decimal_places}f} {self.moneda_simbolo}",
            "Porcentaje Adquirido": f"{porcentaje_adquirido_inversor:,.{self.decimal_places}f}%"
        }, is_highlight=True)

        valoracion_total_empresa_implicita = valor_participacion_inversor / (porcentaje_adquirido_inversor / 100)
        self.create_data_box(self.historical_scroll_frame, "Valoración Implícita de la Empresa", {
            "Valoración Total": f"{valoracion_total_empresa_implicita:,.{self.decimal_places}f} {self.moneda_simbolo}",
            "Explicación": "El valor estimado para el 100% de la empresa, derivado de tu inversión."
        })

        # Desglose Anual Histórico y Múltiplos (como tabla en un textbox dentro de una caja)
        table_data_historica = []
        datos_financieros_reales = []

        for año_key, valor in data_financiera_historica.items():
            if valor is None:
                table_data_historica.append([año_key, "N/A", "N/A", "N/A", "N/A"])
                continue

            ganancia_anual_inversor = (porcentaje_adquirido_inversor / 100) * valor
            
            multiplo_str = "N/A"
            if valor > 0 and valoracion_total_empresa_implicita > 0:
                multiplo_actual = valoracion_total_empresa_implicita / valor
                multiplo_str = f"{multiplo_actual:,.{self.decimal_places}f}x"

            payback_str = "N/A"
            if ganancia_anual_inversor > 0 and valor_participacion_inversor > 0:
                retorno_inversion_anios = valor_participacion_inversor / ganancia_anual_inversor
                payback_str = f"{retorno_inversion_anios:,.{self.decimal_places}f} años"
            
            table_data_historica.append([
                año_key,
                f"{valor:,.{self.decimal_places}f} {self.moneda_simbolo}",
                f"{ganancia_anual_inversor:,.{self.decimal_places}f} {self.moneda_simbolo}",
                multiplo_str,
                payback_str
            ])
            datos_financieros_reales.append(valor)

        headers_historicos = ["Año", f"{tipo_data_financiera.capitalize()} Empresa", "Ganancia Inversor", f"Múltiplo VE/{tipo_data_financiera.upper()}", "Payback Period (Solo este año)"]
        
        table_frame = ctk.CTkFrame(self.historical_scroll_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        table_frame.pack(fill="x", padx=10, pady=5, expand=True)
        ctk.CTkLabel(table_frame, text="Desglose Anual Histórico y Múltiplos", font=ctk.CTkFont(weight="bold", size=14)).pack(padx=10, pady=5, anchor="w")
        
        table_textbox = ctk.CTkTextbox(table_frame, wrap="word", height=200)
        table_textbox.insert("end", tabulate(table_data_historica, headers=headers_historicos, tablefmt="grid"))
        table_textbox.configure(state="disabled")
        table_textbox.pack(fill="both", expand=True, padx=10, pady=10)


        # Resumen Promedio (Payback Period)
        datos_positivos_para_promedio = [d for d in datos_financieros_reales if d is not None and d > 0]
        if datos_positivos_para_promedio:
            promedio_data_empresa = sum(datos_positivos_para_promedio) / len(datos_positivos_para_promedio)
            promedio_ganancia_inversor = (porcentaje_adquirido_inversor / 100) * promedio_data_empresa
            
            payback_metrics = {
                f"{tipo_data_financiera.capitalize()} Promedio Empresa": f"{promedio_data_empresa:,.{self.decimal_places}f} {self.moneda_simbolo}",
                "Ganancia Promedio Inversor": f"{promedio_ganancia_inversor:,.{self.decimal_places}f} {self.moneda_simbolo}"
            }
            if promedio_ganancia_inversor > 0:
                payback_period_promedio = valor_participacion_inversor / promedio_ganancia_inversor
                payback_metrics["Payback Period (Promedio)"] = f"{payback_period_promedio:,.{self.decimal_places}f} años"
                if payback_period_promedio <= 3:
                    payback_metrics["Comentario"] = "¡Excelente! Recuperación rápida."
                elif payback_period_promedio <= 5:
                    payback_metrics["Comentario"] = "Bueno. Recuperación aceptable."
                else:
                    payback_metrics["Comentario"] = "Recuperación lenta. Considerar riesgo."
            else:
                payback_metrics["Comentario"] = "Payback Period no calculable (ganancia promedio <= 0)."
            
            self.create_data_box(self.historical_scroll_frame, "Resumen de Payback Period Promedio", payback_metrics)
        else:
            self.create_data_box(self.historical_scroll_frame, "Resumen de Payback Period Promedio", {
                "Estado": "No hay datos positivos para calcular el Payback Period promedio."
            })
        
        return datos_financieros_reales # Return real historical data for projection

    def populate_projection_tab(self, parent_scroll_frame, valor_participacion_inversor, porcentaje_adquirido_inversor, tipo_data_financiera, ultimo_data_historica, tasa_crecimiento_anual, num_anios_proyeccion, tasa_descuento, escenario_nombre=""):
        """Popula una pestaña de proyección con cajas de datos y gráfico."""
        # Clear previous content
        for widget in parent_scroll_frame.winfo_children():
            widget.destroy()
        
        # Re-add graph type option menu if it's the base projection tab
        if parent_scroll_frame == self.base_projection_scroll_frame:
            self.graph_type_optionmenu.pack(pady=10)
            self.base_graph_canvas_frame.pack(fill="both", expand=True, padx=5, pady=5) # Repack the graph frame

        if ultimo_data_historica is None:
            self.create_data_box(parent_scroll_frame, f"Análisis {escenario_nombre}", {
                "Estado": "No hay datos históricos válidos para iniciar la proyección. VAN y TIR no calculables."
            })
            return

        # Proyección de Flujos
        van, tir, flujos_proyectados_empresa, flujos_proyectados_inversor, años_grafico_proyectado = \
            self.calcular_van_tir(valor_participacion_inversor, porcentaje_adquirido_inversor, ultimo_data_historica, tasa_crecimiento_anual, num_anios_proyeccion, tasa_descuento)

        projection_metrics = {
            f"Último {tipo_data_financiera.capitalize()} Histórico": f"{ultimo_data_historica:,.{self.decimal_places}f} {self.moneda_simbolo}",
            "Tasa de Crecimiento": f"{tasa_crecimiento_anual*100:,.{self.decimal_places}f}%",
            "Años Proyectados": f"{num_anios_proyeccion}"
        }
        self.create_data_box(parent_scroll_frame, f"Parámetros de Proyección {escenario_nombre}", projection_metrics)

        # Tabla de flujos proyectados
        table_data_proyeccion = []
        for i in range(len(años_grafico_proyectado)):
            table_data_proyeccion.append([
                años_grafico_proyectado[i],
                f"{flujos_proyectados_empresa[i]:,.{self.decimal_places}f} {self.moneda_simbolo}",
                f"{flujos_proyectados_inversor[i]:,.{self.decimal_places}f} {self.moneda_simbolo}"
            ])
        headers_proyeccion = ["Periodo", f"{tipo_data_financiera.capitalize()} Proyectado Empresa", "Flujo para Inversor"]
        
        table_frame = ctk.CTkFrame(parent_scroll_frame, corner_radius=10, fg_color=("gray85", "gray15"))
        table_frame.pack(fill="x", padx=10, pady=5, expand=True)
        ctk.CTkLabel(table_frame, text="Tabla de Flujos Proyectados", font=ctk.CTkFont(weight="bold", size=14)).pack(padx=10, pady=5, anchor="w")
        
        table_textbox = ctk.CTkTextbox(table_frame, wrap="word", height=200)
        table_textbox.insert("end", tabulate(table_data_proyeccion, headers=headers_proyeccion, tablefmt="grid"))
        table_textbox.configure(state="disabled")
        table_textbox.pack(fill="both", expand=True, padx=10, pady=10)


        # VAN y TIR
        van_tir_metrics = {
            "Tasa de Descuento": f"{tasa_descuento*100:,.{self.decimal_places}f}%"
        }
        if van is not None:
            van_tir_metrics["Valor Actual Neto (VAN)"] = f"{van:,.{self.decimal_places}f} {self.moneda_simbolo}"
            van_tir_metrics["Comentario VAN"] = "(Positivo: Inversión rentable)" if van > 0 else "(Negativo/Cero: Inversión no rentable)"
        else:
            van_tir_metrics["Valor Actual Neto (VAN)"] = "No calculable"

        if tir is not None:
            van_tir_metrics["Tasa Interna de Retorno (TIR)"] = f"{tir*100:,.{self.decimal_places}f}%"
            van_tir_metrics["Comentario TIR"] = "(Mayor que Tasa de Descuento: Atractiva)" if tir > tasa_descuento else "(Menor/Igual que Tasa de Descuento: Poco atractiva)"
        else:
            van_tir_metrics["Tasa Interna de Retorno (TIR)"] = "No calculable"
            van_tir_metrics["Comentario TIR"] = "No se pudo calcular la TIR (posibles flujos inadecuados)."
        
        self.create_data_box(parent_scroll_frame, f"Resultados VAN y TIR {escenario_nombre}", van_tir_metrics, is_highlight=True)

        # Store graph data for later redraw if type changes
        # Only store for the base projection tab, as other tabs don't have their own graph
        if parent_scroll_frame == self.base_projection_scroll_frame:
            self.last_graph_data = {
                "años": años_grafico_proyectado,
                "flujos_empresa": flujos_proyectados_empresa,
                "flujos_inversor": flujos_proyectados_inversor,
                "titulo": f'Evolución del {tipo_data_financiera.capitalize()} (Empresa vs. Inversor) con Crecimiento del {tasa_crecimiento_anual*100:,.{self.decimal_places}f}%',
                "y_label": tipo_data_financiera.capitalize(),
                "tipo_data_financiera": tipo_data_financiera,
            }

            # Generar Gráfico de Flujos Proyectados
            self.generar_grafico_flujos(
                años_grafico_proyectado,
                flujos_proyectados_empresa,
                flujos_inversor,
                f'Evolución del {tipo_data_financiera.capitalize()} (Empresa vs. Inversor) con Crecimiento del {tasa_crecimiento_anual*100:,.{self.decimal_places}f}%',
                tipo_data_financiera.capitalize(),
                tipo_data_financiera,
                self.base_graph_canvas_frame, # Always use the base graph frame
                self.graph_type_var.get() # Pass current graph type
            )

    def run_all_scenarios(self):
        """Ejecuta el análisis de inversión para todos los escenarios (Base, Optimista, Pesimista)."""
        try:
            # Limpiar todos los scrollable frames de resultados
            for frame in [self.historical_scroll_frame, self.base_projection_scroll_frame, self.optimistic_scroll_frame, self.pessimistic_scroll_frame]:
                for widget in frame.winfo_children():
                    widget.destroy()
            
            # Limpiar el canvas del gráfico y cerrar figuras de matplotlib
            for widget in self.base_graph_canvas_frame.winfo_children():
                widget.destroy()
            plt.close('all')
            self.last_graph_data = None # Reset graph data

            # Validar entradas comunes
            valor_participacion_inversor = self.obtener_numero_gui(self.entry_valor_participacion, solo_positivo=True, permite_cero=False, field_name="Valor de la Participación")
            if valor_participacion_inversor is None: return

            porcentaje_adquirido_inversor = self.obtener_numero_gui(self.entry_porcentaje_adquirido, solo_positivo=True, permite_cero=False, min_val=0.01, max_val=100.0, field_name="Porcentaje Adquirido")
            if porcentaje_adquirido_inversor is None: return

            tipo_data_financiera = self.tipo_data_financiera_var.get()
            
            data_financiera_historica = self.get_historical_financial_data_gui(
                "beneficio neto" if tipo_data_financiera == 'BN' else "flujo de caja libre"
            )
            if data_financiera_historica is None: return

            num_anios_proyeccion = self.obtener_numero_gui(self.entry_anios_proyeccion, tipo=int, solo_positivo=True, permite_cero=False, min_val=1, field_name="Años Futuros a Proyectar")
            if num_anios_proyeccion is None: return

            # --- Desglose Anual Histórico ---
            datos_financieros_reales = self.populate_historical_tab(
                valor_participacion_inversor, porcentaje_adquirido_inversor, tipo_data_financiera, data_financiera_historica
            )

            ultimo_data_historica = None
            if datos_financieros_reales:
                ultimo_data_historica = datos_financieros_reales[-1] # El último elemento de la lista

            if ultimo_data_historica is None:
                self.show_message("Advertencia", "No hay datos históricos válidos para iniciar las proyecciones. VAN y TIR no calculables.", is_error=False)
                return # Salir si no hay datos para proyectar

            # --- Escenario Base ---
            tasa_crecimiento_base = self.obtener_numero_gui(self.entry_tasa_crecimiento, solo_positivo=False, permite_cero=True, field_name="Tasa de Crecimiento Anual (Base)")
            if tasa_crecimiento_base is None: return
            tasa_crecimiento_base /= 100

            tasa_descuento_base = self.obtener_numero_gui(self.entry_tasa_descuento, solo_positivo=True, permite_cero=False, min_val=0.01, field_name="Tasa de Descuento (Base)")
            if tasa_descuento_base is None: return
            tasa_descuento_base /= 100

            self.populate_projection_tab(
                self.base_projection_scroll_frame,
                valor_participacion_inversor, porcentaje_adquirido_inversor, tipo_data_financiera,
                ultimo_data_historica, tasa_crecimiento_base, num_anios_proyeccion, tasa_descuento_base, " (Base)"
            )
            
            # --- Escenario Optimista ---
            tasa_crecimiento_opt = self.obtener_numero_gui(self.entry_tasa_crecimiento_opt, solo_positivo=False, permite_cero=True, field_name="Tasa de Crecimiento Optimista")
            if tasa_crecimiento_opt is None: return
            tasa_crecimiento_opt /= 100

            tasa_descuento_opt = self.obtener_numero_gui(self.entry_tasa_descuento_opt, solo_positivo=True, permite_cero=False, min_val=0.01, field_name="Tasa de Descuento Optimista")
            if tasa_descuento_opt is None: return
            tasa_descuento_opt /= 100

            self.populate_projection_tab(
                self.optimistic_scroll_frame,
                valor_participacion_inversor, porcentaje_adquirido_inversor, tipo_data_financiera,
                ultimo_data_historica, tasa_crecimiento_opt, num_anios_proyeccion, tasa_descuento_opt, " (Optimista)"
            )

            # --- Escenario Pesimista ---
            tasa_crecimiento_pes = self.obtener_numero_gui(self.entry_tasa_crecimiento_pes, solo_positivo=False, permite_cero=True, field_name="Tasa de Crecimiento Pesimista")
            if tasa_crecimiento_pes is None: return
            tasa_crecimiento_pes /= 100

            tasa_descuento_pes = self.obtener_numero_gui(self.entry_tasa_descuento_pes, solo_positivo=True, permite_cero=False, min_val=0.01, field_name="Tasa de Descuento Pesimista")
            if tasa_descuento_pes is None: return
            tasa_descuento_pes /= 100

            self.populate_projection_tab(
                self.pessimistic_scroll_frame,
                valor_participacion_inversor, porcentaje_adquirido_inversor, tipo_data_financiera,
                ultimo_data_historica, tasa_crecimiento_pes, num_anios_proyeccion, tasa_descuento_pes, " (Pesimista)"
            )
            
            self.show_message("Análisis Completado", "El análisis de inversión completo ha sido finalizado. Revisa las pestañas de resultados.", is_error=False)
        except Exception as e:
            self.show_message("Error Inesperado", f"Ocurrió un error inesperado durante el análisis: {e}\nPor favor, revisa tus entradas.", is_error=True)
            print(f"ERROR INESPERADO: {e}") # Print to console for deeper debugging


    def update_graph_type(self, new_type):
        """Redibuja el gráfico con el nuevo tipo seleccionado."""
        if self.last_graph_data:
            self.generar_grafico_flujos(
                self.last_graph_data["años"],
                self.last_graph_data["flujos_empresa"],
                self.last_graph_data["flujos_inversor"],
                self.last_graph_data["titulo"],
                self.last_graph_data["y_label"],
                self.last_graph_data["tipo_data_financiera"],
                self.base_graph_canvas_frame,
                new_type
            )
        else:
            self.show_message("Gráfico", "No hay datos de análisis para generar el gráfico.", is_error=False)


    def load_guide_content(self):
        """Carga el contenido de la guía para novatos."""
        explicaciones = {
            "valor_participacion": "Es el monto de dinero que el inversor pagaría para adquirir un porcentaje específico de la empresa.",
            "porcentaje_adquirido": "Es el porcentaje del total de la empresa que el inversor obtendría con su inversión.",
            "beneficio_neto": "Es la ganancia o pérdida total de una empresa después de restar todos los gastos, incluyendo impuestos e intereses.",
            "flujo_caja_libre": "Es el efectivo que genera una empresa después de contabilizar los gastos de capital. Representa el efectivo que una empresa tiene disponible para pagar deudas, dividendos, etc. Es una métrica crucial para inversores.",
            "tasa_crecimiento": "Es el porcentaje en que se espera que los beneficios o el flujo de caja de la empresa crezcan anualmente en el futuro.",
            "anios_proyeccion": "Es la cantidad de años futuros para los cuales se realizará una estimación de los beneficios/flujos de caja para calcular VAN y TIR.",
            "tasa_descuento": "También conocida como Coste de Oportunidad del Capital. Es la tasa de retorno mínima que un inversor espera obtener de una inversión para compensar el riesgo y el valor del dinero en el tiempo. Se usa para traer flujos de caja futuros a su valor presente.",
            "payback_period": "Es el tiempo que tarda una inversión en recuperar su costo inicial a partir de los flujos de caja generados. Un payback period más corto suele ser más atractivo.",
            "van": "Valor Actual Neto. Es el valor presente de los flujos de efectivo futuros de una inversión menos el costo inicial de la inversión. Un VAN POSITIVO indica que la inversión es rentable a la tasa de descuento utilizada.",
            "tir": "Tasa Interna de Retorno. Es la tasa de descuento que hace que el Valor Actual Neto (VAN) de todos los flujos de efectivo de una inversión sea igual a cero. Si la TIR es MAYOR que la tasa de descuento, la inversión se considera atractiva.",
            "valoracion_implicita": "Es el valor total de la empresa que se deriva del precio que el inversor está pagando por un determinado porcentaje de la misma."
        }
        self.guide_textbox.configure(state="normal")
        self.guide_textbox.delete("1.0", "end")
        self.guide_textbox.insert("end", "Aquí te explicamos los conceptos clave que usamos en la calculadora:\n\n")
        for concepto, explicacion in explicaciones.items():
            self.guide_textbox.insert("end", f"💡 {concepto.replace('_', ' ').upper()}:\n")
            self.guide_textbox.insert("end", f"    {explicacion}\n\n")
        self.guide_textbox.configure(state="disabled")

    def _load_settings_from_file(self):
        """Carga la configuración de un archivo JSON en los atributos internos."""
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.moneda_simbolo = settings.get("moneda_simbolo", "€")
                self.decimal_places = settings.get("decimal_places", 2)
                self.current_appearance_mode = settings.get("appearance_mode", "System")
                self.current_color_theme = settings.get("color_theme", "blue")
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está corrupto, se usan los valores predeterminados
            pass 
        # Aplicar el tema inmediatamente (antes de que se actualicen los widgets)
        ctk.set_appearance_mode(self.current_appearance_mode)
        ctk.set_default_color_theme(self.current_color_theme)

    def _apply_settings_to_gui(self):
        """Aplica los valores de configuración a los widgets de la GUI."""
        self.entry_moneda.delete(0, "end")
        self.entry_moneda.insert(0, self.moneda_simbolo)
        self.entry_decimal_places.delete(0, "end")
        self.entry_decimal_places.insert(0, str(self.decimal_places))
        self.appearance_mode_optionemenu.set(self.current_appearance_mode)
        self.color_theme_optionemenu.set(self.current_color_theme)

        # Actualizar labels que muestran la moneda
        self.label_valor_participacion.configure(text=f"Valor de la Participación ({self.moneda_simbolo}):")
        if hasattr(self, "shark_label_inversion_solicitada"):
            self.shark_label_inversion_solicitada.configure(text=f"Inversión que piden ({self.moneda_simbolo}):")
        for año_key, label in self.historical_labels.items():
            label.configure(text=f"{año_key} ({self.moneda_simbolo} o N/A):")

    def save_settings(self):
        """Guarda la configuración en un archivo JSON."""
        # Validar y actualizar variables internas antes de guardar
        new_moneda = self.entry_moneda.get().strip()
        if new_moneda:
            self.moneda_simbolo = new_moneda
        else:
            self.show_message("Advertencia", "El símbolo de moneda no puede estar vacío. Se mantendrá el actual.", is_error=True)
            self.entry_moneda.insert(0, self.moneda_simbolo) # Reinsert current value

        try:
            new_decimal_places = int(self.entry_decimal_places.get().strip())
            if new_decimal_places < 0:
                self.show_message("Error de Configuración", "El número de decimales no puede ser negativo.", is_error=True)
                self.entry_decimal_places.delete(0, "end")
                self.entry_decimal_places.insert(0, str(self.decimal_places))
            else:
                self.decimal_places = new_decimal_places
        except ValueError:
            self.show_message("Error de Configuración", "El número de decimales debe ser un entero válido.", is_error=True)
            self.entry_decimal_places.delete(0, "end")
            self.entry_decimal_places.insert(0, str(self.decimal_places)) # Reset to current valid value

        self.current_appearance_mode = self.appearance_mode_optionemenu.get()
        self.current_color_theme = self.color_theme_optionemenu.get()

        settings = {
            "moneda_simbolo": self.moneda_simbolo,
            "decimal_places": self.decimal_places,
            "appearance_mode": self.current_appearance_mode,
            "color_theme": self.current_color_theme
        }
        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            self.show_message("Configuración Guardada", f"Configuración actualizada y guardada.", is_error=False)
            
            # Aplicar cambios inmediatamente
            ctk.set_appearance_mode(self.current_appearance_mode)
            ctk.set_default_color_theme(self.current_color_theme)

            # Actualizar labels que muestran la moneda (si se cambió)
            self.label_valor_participacion.configure(text=f"Valor de la Participación ({self.moneda_simbolo}):")
            for año_key, label in self.historical_labels.items():
                label.configure(text=f"{año_key} ({self.moneda_simbolo} o N/A):")

        except Exception as e:
            self.show_message("Error al Guardar", f"No se pudo guardar la configuración: {e}", is_error=True)

    def reset_settings(self):
        """Restablece la configuración a los valores predeterminados y los guarda."""
        self.moneda_simbolo = "€"
        self.decimal_places = 2
        self.current_appearance_mode = "System"
        self.current_color_theme = "blue"

        # Actualizar los widgets de entrada con los valores predeterminados
        self.entry_moneda.delete(0, "end")
        self.entry_moneda.insert(0, self.moneda_simbolo)
        self.entry_decimal_places.delete(0, "end")
        self.entry_decimal_places.insert(0, str(self.decimal_places))
        self.appearance_mode_optionemenu.set(self.current_appearance_mode)
        self.color_theme_optionemenu.set(self.current_color_theme)

        # Guardar los valores predeterminados en el archivo
        self.save_settings() 
        self.show_message("Configuración Restablecida", "La configuración ha sido restablecida a los valores predeterminados.", is_error=False)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Cambia el modo de apariencia de la aplicación."""
        ctk.set_appearance_mode(new_appearance_mode)
        self.current_appearance_mode = new_appearance_mode
        # Redraw graph if data exists to apply new theme
        if self.last_graph_data:
            self.generar_grafico_flujos(
                self.last_graph_data["años"],
                self.last_graph_data["flujos_empresa"],
                self.last_graph_data["flujos_inversor"],
                self.last_graph_data["titulo"],
                self.last_graph_data["y_label"],
                self.last_graph_data["tipo_data_financiera"],
                self.base_graph_canvas_frame,
                self.graph_type_var.get()
            )


    def change_color_theme_event(self, new_color_theme: str):
        """Cambia el tema de color de la aplicación."""
        ctk.set_default_color_theme(new_color_theme)
        self.current_color_theme = new_color_theme


if __name__ == "__main__":
    app = InvestmentCalculatorApp()
    app.mainloop()
