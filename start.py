#!/usr/bin/env python3

import sys
import os

def show_startup_menu():
    """Mostrar menu de inicialização"""
    print("=" * 60)
    print("TERMINALTEC - FERRAMENTA PARA TECNICOS")
    print("=" * 60)
    print()
    print("Modo de execução:")
    print()
    print("1. 💻 Modo Terminal")
    print("2. 🖼️  Modo GUI (experimental)")
    print("3. Sair")
    print()
    
    while True:
        choice = input("Digite sua escolha (1-3): ").strip()
        
        if choice == "1":
            print("Iniciando modo terminal...")
            os.system(f"{sys.executable} main.py")
            break
            
        elif choice == "2":
            print("Iniciando modo GUI...")
            os.system(f"{sys.executable} gui.py")
            break
            
        elif choice == "3":
            print("Saindo...")
            sys.exit(0)
            
        else:
            print("Opcao invalida. Tente novamente.")

def main():
    """Função principal"""
    try:
        show_startup_menu()
    except KeyboardInterrupt:
        print("\n\nSaindo...")
        sys.exit(0)

if __name__ == "__main__":
    main() 