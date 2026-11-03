import socket
import sys
from datetime import datetime

# Validacion de IP
def validar_ip(direccion_ip: str) -> bool:
    try:
        socket.getaddrinfo(direccion_ip, None)
        return True
    except socket.gaierror:
        return False

# Solicitud de datos al usuario (IP y puerto inicial y final a escanear)
def solicitar_datos() -> tuple[str, int, int]:
    print("=" * 40)
    print("        ESCÁNER DE PUERTOS TCP")
    print("=" * 40)

    #  Dirección IP
    while True:
        ip = input("Ingrese la dirección IP o host a escanear: ").strip()
        if validar_ip(ip):
            break
        print("  [Error] Dirección IP/host no válida. Intente nuevamente.\n")

    # Puerto inicial
    while True:
        try:
            puerto_inicio = int(input("Ingrese el puerto inicial (1-65535): "))
            if 1 <= puerto_inicio <= 65535:
                break
            print("  [Error] El puerto debe estar entre 1 y 65535.\n")
        except ValueError:
            print("  [Error] Debe ingresar un número entero.\n")

    # Puerto final
    while True:
        try:
            puerto_fin = int(input("Ingrese el puerto final (1-65535): "))
            if puerto_fin < puerto_inicio:
                print("  [Error] El puerto final debe ser >= al puerto inicial.\n")
            elif not (1 <= puerto_fin <= 65535):
                print("  [Error] El puerto debe estar entre 1 y 65535.\n")
            else:
                break
        except ValueError:
            print("  [Error] Debe ingresar un número entero.\n")

    return ip, puerto_inicio, puerto_fin

# Escanear puerto especificado - Retorna True si esta abierto
def escanear_puerto(ip: str, puerto: int, timeout: float = 0.5) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        resultado = sock.connect_ex((ip, puerto))
        return resultado == 0

# Escanea los puertos desde el inicial hasta el final indicados por el usuario
def escanear_rango(ip: str, puerto_inicio: int, puerto_fin: int) -> list[int]:
    puertos_abiertos = []

    print(f"\nIP: {ip}")
    print(f"Desde: {puerto_inicio}")
    print(f"Hasta: {puerto_fin}")
    print("Escaneando...\n")

    inicio_tiempo = datetime.now()

    for puerto in range(puerto_inicio, puerto_fin + 1):
        try:
            if escanear_puerto(ip, puerto):
                print(f"Puerto {puerto} - ABIERTO")
                puertos_abiertos.append(puerto)
        except socket.error:
            # Host inalcanzable u otro error de red: se detiene el escaneo
            print(f"\n[Error] No se pudo establecer conexión con {ip}.")
            sys.exit(1)

    fin_tiempo = datetime.now()
    duracion = (fin_tiempo - inicio_tiempo).total_seconds()

    mostrar_resumen(puerto_inicio, puerto_fin, puertos_abiertos, duracion)
    return puertos_abiertos

# Informe final de resultados del escaneo de puertos
def mostrar_resumen(puerto_inicio: int, puerto_fin: int,
                     puertos_abiertos: list[int], duracion: float) -> None:
    total_analizados = puerto_fin - puerto_inicio + 1

    print("\n" + "=" * 40)
    print("           RESUMEN DEL ESCANEO")
    print("=" * 40)
    print(f"Puertos analizados: {total_analizados}")
    print(f"Puertos abiertos: {len(puertos_abiertos)}")
    if puertos_abiertos:
        print(f"Lista de puertos abiertos: {', '.join(map(str, puertos_abiertos))}")
    else:
        print("No se encontraron puertos abiertos en el rango indicado.")
    print(f"Tiempo total de escaneo: {duracion:.2f} segundos")
    print("=" * 40)


def main():
    ip, puerto_inicio, puerto_fin = solicitar_datos()
    escanear_rango(ip, puerto_inicio, puerto_fin)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEscaneo interrumpido por el usuario.")
        sys.exit(0)