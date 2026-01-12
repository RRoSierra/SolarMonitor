import pandas as pd
import matplotlib.pyplot as plt
import os

# Obtener directorio del script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, "historico_voltaje.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "graficos_diarios")

# Crear carpeta para los gráficos si no existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Cargar datos
if not os.path.exists(FILE_NAME):
    print(f"❌ Error: El archivo {FILE_NAME} no existe.")
    exit()

df = pd.read_csv(FILE_NAME)
# Asegurar que timestamp sea objeto fecha/hora
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Obtener lista de días únicos presentes en el archivo
dias_unicos = df['fecha'].unique()

print(f"✅ Se encontraron datos de {len(dias_unicos)} días.")

for dia in dias_unicos:
    # Filtrar datos de ese día específico
    df_dia = df[df['fecha'] == dia].copy()
    
    # Crear la figura
    plt.figure(figsize=(12, 6))
    
    # Graficar Voltaje 5.5V vs Hora
    # Usamos la columna 'hora' para el eje X
    plt.plot(df_dia['hora'], df_dia['v55'], color='orange', linewidth=2, label=f'Voltaje 5.5V ({dia})')
    
    # Configurar etiquetas y títulos
    plt.title(f"Ciclo de Voltaje LDR - Fecha: {dia}", fontsize=14)
    plt.xlabel("Hora del Día (HH:MM:SS)", fontsize=12)
    plt.ylabel("Voltaje (V)", fontsize=12)
    
    # Optimizar el eje X (mostrar una etiqueta cada N puntos para que no se amontonen)
    n = len(df_dia) // 10 if len(df_dia) > 10 else 1
    plt.xticks(df_dia['hora'][::n], rotation=45)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.ylim(0, 6) # Limitar eje Y a 6V para ver bien las variaciones
    
    plt.tight_layout()
    
    # Guardar gráfico con el nombre del día
    nombre_archivo = f"grafico_{dia}.png"
    save_path = os.path.join(OUTPUT_DIR, nombre_archivo)
    plt.savefig(save_path, dpi=150)
    plt.close() # Cerrar para liberar memoria
    
    print(f"📊 Gráfico generado: {nombre_archivo}")

print(f"\n🚀 Proceso terminado. Revisa la carpeta: {OUTPUT_DIR}")