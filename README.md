# Shark Tank México: Análisis de Inversión 🦈📈

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-2fa5d6.svg)
![NumPy](https://img.shields.io/badge/Data-NumPy_Financial-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

(Arquitecto Técnico_JMC) Herramienta de escritorio desarrollada en Python orientada al análisis de viabilidad financiera y valoración de empresas. Inspirada en las métricas exigidas en escenarios de inversión de capital riesgo (como Shark Tank), permite calcular el rendimiento esperado de una aportación de capital frente a la adquisición de un porcentaje empresarial.

## 🚀 Características Principales

* **Valoración Implícita:** Calcula automáticamente el valor real de la empresa (Post-money) en base a la inversión inicial y el capital cedido.
* **Métricas Financieras Clave:** Cálculo algorítmico del Valor Actual Neto (VAN), Tasa Interna de Retorno (TIR) y Payback Period sobre los flujos de caja libre o beneficios netos.
* **Análisis Multi-Escenario:** Proyección de flujos futuros en tres variables simultáneas: Escenario Base, Optimista y Pesimista, aplicando distintas tasas de crecimiento y descuento.
* **Visualización de Datos:** Generación de gráficos dinámicos integrados (barras y líneas) para comparar visualmente el rendimiento de la empresa vs. la ganancia del inversor a lo largo del tiempo.
* **Persistencia de Configuración:** Guarda tus preferencias de entorno (moneda, número de decimales y temas claro/oscuro) localmente en un archivo `.json`.
* **Guía Integrada:** Incluye un glosario y guía de conceptos financieros básicos para inversores novatos.

## 🛠️ Stack Tecnológico

* **CustomTkinter:** Interfaz gráfica moderna, responsive y con soporte nativo para Dark Mode.
* **NumPy & NumPy-Financial:** Motor matemático para el cálculo de matrices de flujos y funciones financieras complejas (NPV, IRR).
* **Matplotlib:** Renderizado de gráficos financieros directamente sobre los frames de Tkinter (`FigureCanvasTkAgg`).
* **Tabulate:** Estructuración y formateo de tablas de resultados históricos y proyectados.

## ⚙️ Instalación y Uso

1. Clona este repositorio en tu equipo:
   ```bash
   git clone [https://github.com/TU_USUARIO/shark-tank-mx-analisis-inversion.git](https://github.com/TU_USUARIO/shark-tank-mx-analisis-inversion.git)

2. Accede a la carpeta del proyecto:
   ```bash
   cd shark-tank-mx-analisis-inversion

3. Instala las dependencias necesarias. Se recomienda usar un entorno virtual:
   ```bash
   pip install customtkinter numpy numpy-financial matplotlib tabulate

4. Ejecuta la aplicación:
   ```bash
   python 008calculadora.py

## 👨‍💻 Autor

Jose Manuel Caamaño González | Arquitecto Técnico & BIM Manager.
Digital Product Lead | ConTech & Digital Twin SaaS | BIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)

Hecho con código y café desde A Coruña. ☕

Jose Manuel Caamaño González | [LinkedIn](https://www.linkedin.com/in/jmcaamanog/)

¡Pégalo en el proyecto y a por el siguiente! Ya tienes un arsenal de herramientas impresionante en tu perfil.
