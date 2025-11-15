#!/usr/bin/env python3
"""
Script para executar testes E2E de forma controlada
"""
import subprocess
import time
import sys
import signal
import os

def start_django_server():
    """Inicia o servidor Django"""
    print("Iniciando servidor Django...")
    proc = subprocess.Popen(
        ['python', 'manage.py', 'runserver', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Esperar o servidor iniciar
    time.sleep(3)
    
    # Verificar se o servidor está rodando
    try:
        import requests
        response = requests.get('http://localhost:8000/')
        if response.status_code == 200:
            print("✅ Servidor Django iniciado com sucesso!")
            return proc
        else:
            print("❌ Servidor Django não respondeu corretamente")
            return None
    except Exception as e:
        print(f"❌ Erro ao verificar servidor: {e}")
        return None

def run_tests():
    """Executa os testes E2E"""
    print("Executando testes E2E...")
    result = subprocess.run(
        ['pytest', 'tests_e2e.py', '-v', '--tb=short'],
        capture_output=False
    )
    return result.returncode

def stop_django_server(proc):
    """Para o servidor Django"""
    if proc:
        print("Parando servidor Django...")
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        proc.wait()
        print("✅ Servidor Django parado")

def main():
    """Função principal"""
    django_proc = None
    
    try:
        # Iniciar servidor Django
        django_proc = start_django_server()
        if not django_proc:
            print("❌ Não foi possível iniciar o servidor Django")
            sys.exit(1)
        
        # Executar testes
        exit_code = run_tests()
        
        if exit_code == 0:
            print("✅ Todos os testes passaram!")
        else:
            print(f"❌ Alguns testes falharam (código: {exit_code})")
        
        return exit_code
        
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário")
        return 130
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1
        
    finally:
        # Sempre parar o servidor Django
        stop_django_server(django_proc)

if __name__ == '__main__':
    sys.exit(main())