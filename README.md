# Shark Tank México: Análisis de Inversión 🦈📈

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-2fa5d6.svg)
![NumPy](https://img.shields.io/badge/Data-NumPy_Financial-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Herramienta de escritorio desarrollada en Python para el análisis de viabilidad financiera y valoración de empresas, inspirada en las métricas exigidas en escenarios de inversión como Shark Tank México.

## 🚀 Características Principales

* **Evaluación rápida de ofertas:** Mide valoración implícita, porcentaje cedido, porcentaje retenido, múltiplo de ingresos y sugiere contraoferta.
* **Modos de respuesta personalizados:** Respuestas tipo "emprendedor", "inversionista" o "ambos" para negociar con mayor claridad.
* **Análisis completo de inversión:** Permite cargar datos históricos y proyectar flujos financieros.
* **Proyección multi-escenario:** Calcula análisis Base, Optimista y Pesimista con tasas de crecimiento y descuento independientes.
* **Cálculos financieros estándar:** VAN (Valor Actual Neto), TIR (Tasa Interna de Retorno) y Payback Period de manera automática.
* **Tablas con resultados:** Desglose anual histórico, múltiplos y flujos proyectados presentados en tablas legibles.
* **Gráficos dinámicos:** Visualiza resultados en barras o líneas según prefieras.
* **Configuración persistente:** Guarda símbolo de moneda, decimales, tema de color y modo de apariencia en `settings.json`.
* **Guía integrada para novatos:** Incluye explicaciones de conceptos clave como VAN, TIR, flujo de caja libre y valoración implícita.

## 🧩 Estructura de la aplicación

La interfaz contiene varias secciones:

* `Inicio`: Explicación rápida y acceso a la evaluación Shark Tank.
* `Análisis de Inversión`: Datos de inversión, histórico financiero y proyección multi-escenario.
* `Guía para Novatos`: Glosario de conceptos financieros.
* `Configuración`: Ajustes de moneda, decimales, apariencia y tema.
* `Acerca de`: Información del desarrollador y las librerías usadas.

## 🛠️ Stack Tecnológico

* **CustomTkinter**: Interfaz moderna con modo claro/oscuro y temas de color.
* **NumPy**: Operaciones numéricas y soporte de arrays.
* **NumPy-Financial**: Cálculo de VAN y TIR.
* **Matplotlib**: Gráficos integrados en la app.
* **Tabulate**: Formato de tablas para los resultados.

## ⚙️ Instalación y Ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/shark-tank-mx-analisis-inversion.git
   ```
2. Entra en la carpeta del proyecto:
   ```bash
   cd shark-tank-mx-analisis-inversion
   ```
3. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Instala las dependencias:
   ```bash
   pip install customtkinter numpy numpy-financial matplotlib tabulate
   ```
5. Ejecuta la aplicación:
   ```bash
   python CODE\008calculadora.py
   ```

## 📁 Archivo de configuración

La aplicación usa `settings.json` para guardar:

* símbolo de moneda
* número de decimales
* modo de apariencia (`Light`, `Dark`, `System`)
* tema de color (`blue`, `dark-blue`, `green`)

Si no existe, la app carga valores predeterminados y crea el archivo al guardar la configuración.

## ✅ Revisión del código

* El archivo `CODE/008calculadora.py` está estructurado en clases y métodos claros.
* Tiene validación de entradas numéricas con soporte para comas y puntos.
* Crea controles para análisis de datos históricos y escenarios futuros.
* Genera gráficos que funcionan en modo barras o líneas.
* Incluye manejo de errores básico para entrada inválida y cálculo de gráficos.

## 👨‍💻 Autor

Jose Manuel Caamaño González | Arquitecto Técnico & BIM Manager.
Digital Product Lead | ConTech & Digital Twin SaaS | BIM, Energy Modeling & Sustainability | Data Analytics (SQL, Power BI)

Hecho con código y café desde A Coruña. ☕

Jose Manuel Caamaño González | [LinkedIn](https://www.linkedin.com/in/jmcaamanog/)
