#!/usr/bin/env bash
# -----------------------------------------------------------
# Script de execução do projeto "Calculadora Inteligente"
# -----------------------------------------------------------

echo "==============================================="
echo " Iniciando a Calculadora Inteligente em Python"
echo "==============================================="

# Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null
then
    echo " Python3 não encontrado. Instale o Python 3 para continuar."
    exit 1
fi

# Cria um arquivo temporário com o código da calculadora
cat << 'EOF' > calculadora_inteligente_temp.py
# Primeiro Projeto - Calculadora Inteligente

# Inicio do Programa e apresentação

print("Bem vindo a calculadora inteligente")
print("Você gostaria de fazer qual tipo de calculo? ")
dado1 = input()
dado1 = dado1.strip().lower()

# Identificar qual será cálculo

if dado1 == "soma":
  print("você escolheu Soma!")

elif dado1 == "subtração":
  print("você escolheu Subtração!")

elif dado1 == "multiplicação":
  print("Você escolheu Multiplicação!")

elif dado1 == "divisão":
  print("Você escolheu Divisão!")

elif dado1 == "potenciação":
  print("Você escolheu Potenciação!")

elif dado1 == "raiz quadrada":
  print("Você escolheu raiz Quadrada!")

elif dado1 != "soma" != "subtração" != "multiplicação" != "divisão" != "potenciação" != "raiz Quadrada":
   print("Você Não escolheu nenhuma opção.")


# Cálculo

if dado1 == "soma":
  print("Digite um numero")
  numero1 = int(input()) #converte para inteiro
  print("Digite outro numero")
  numero2 = int(input()) #Converte para inteiro

  soma = numero1 + numero2
  print("A Soma dos dois numeros é: ", soma,".")

elif dado1 == "subtração":
  print("Digite um numero")
  numero1 = int(input()) #converte para inteiro
  print("Digite outro numero")
  numero2 = int(input()) #converte para inteiro

  subtração = numero1 - numero2
  print("A Subtração dos dois numeros é: ", subtração,".")

elif dado1 == "multiplicação":
  print("Digite um numero")
  numero1 = int(input()) #converte para inteiro
  print("Digite outro numero")
  numero2 = int(input()) #Converte para inteiro

  multiplicação = numero1 * numero2
  print("A multiplicação dos dois numeros é: ", multiplicação,".")

elif dado1 == "divisão":
  print("Digite um numero")
  numero1 = int(input()) #converte para inteiro
  print("Digite outro numero")
  numero2 = int(input()) #Converte para inteiro

  divisão = numero1 / numero2
  print("A divisão dos dois numeros é: ", divisão,".")

elif dado1 == "potenciação":
  print("Digite um numero")
  numero1 = int(input()) #converte para inteiro
  print("Digite outro numero")
  numero2 = int(input()) #Converte para inteiro

  potenciação = numero1 ** numero2
  print("A potenciação dos dois numeros é: ", potenciação,".")


elif dado1 == "raiz quadrada":
  numero = int(input("Digite um número para calcular a raiz quadrada: "))
  raiz_quadrada = numero ** (1/2)
  print("a raiz quadrada é: ", raiz_quadrada,".")
EOF

# Executa o código temporário
python3 calculadora_inteligente_temp.py

# Remove o arquivo temporário após execução
rm calculadora_inteligente_temp.py

echo "==============================================="
echo "Execução finalizada com sucesso!"
echo "==============================================="
