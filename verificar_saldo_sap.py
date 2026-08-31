"""
Automação SAP GUI / OpenText VIM

Fluxo:

1. Alt + Tab para o SAP
2. Clicar em "Imposto calc. auto"
3. Duplo clique em "Montante de imposto"
4. O próprio SAP seleciona o conteúdo
5. Delete
6. Ctrl + S
7. Clicar em "Aplicar regras"
8. Esperar a próxima fatura
9. Repetir

Imagens necessárias na mesma pasta do script:

    imposto_calc_auto.png
    montante_imposto.png
    aplicar_regras.png
    titulo_processar_invoice.png
"""

import pyautogui
import time
import logging


# ==================================================
# CONFIGURAÇÕES
# ==================================================

pyautogui.PAUSE = 0.4

# Se você mover o mouse para o canto superior esquerdo,
# o PyAutoGUI interrompe a automação.
pyautogui.FAILSAFE = True

# Quanto maior, mais parecida a imagem precisa ser.
CONFIDENCE = 0.70


# ==================================================
# LOG
# ==================================================

logging.basicConfig(
    filename="sap_automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


# ==================================================
# LOCALIZAR IMAGEM NA TELA
# ==================================================

def localizar(img_name):

    print(f"Procurando: {img_name}")

    try:

        resultado = pyautogui.locateCenterOnScreen(
            img_name,
            confidence=CONFIDENCE
        )

        if resultado:
            print(f"Encontrado: {resultado}")
        else:
            print(f"Não encontrado: {img_name}")

        return resultado

    except pyautogui.ImageNotFoundException:

        print(f"Não encontrado: {img_name}")

        return None


# ==================================================
# VERIFICAR SE EXISTE UMA FATURA
# ==================================================

def fatura_disponivel():

    titulo = localizar(
        "titulo_processar_invoice.png"
    )

    return titulo is not None


# ==================================================
# PROCESSAR UMA FATURA
# ==================================================

def processar_fatura():

    # ------------------------------------------------
    # 1. IMPOSTO CALC. AUTO
    # ------------------------------------------------

    print()
    print("1 - Procurando 'Imposto calc. auto'...")

    checkbox = localizar(
        "imposto_calc_auto.png"
    )

    if not checkbox:

        raise Exception(
            "Checkbox 'Imposto calc. auto' não encontrado."
        )

    print("Clicando em 'Imposto calc. auto'...")

    pyautogui.click(checkbox)

    time.sleep(1)


    # ------------------------------------------------
    # 2. MONTANTE DE IMPOSTO
    # ------------------------------------------------

    print()
    print("2 - Procurando 'Montante de imposto'...")

    campo_imposto = localizar(
        "montante_imposto.png"
    )

    if not campo_imposto:

        raise Exception(
            "Campo 'Montante de imposto' não encontrado."
        )

    print(
        f"Campo encontrado em: {campo_imposto}"
    )

    # Duplo clique.
    #
    # O próprio SAP seleciona o conteúdo
    # do campo.
    print("Dando duplo clique no campo...")

    pyautogui.doubleClick(campo_imposto)

    time.sleep(1)

    # O SAP já selecionou os números.
    # Apenas apagamos.
    print("Apagando o conteúdo...")

    pyautogui.press("delete")
    time.sleep(1)
    pyautogui.press("0")

    time.sleep(1)


    # ------------------------------------------------
    # 3. SALVAR
    # ------------------------------------------------

    print()
    print("3 - Salvando com Ctrl + S...")

    pyautogui.hotkey(
        "ctrl",
        "s"
    )

    time.sleep(1.5)


    # ------------------------------------------------
    # 4. APLICAR REGRAS
    # ------------------------------------------------

    print()
    print("4 - Procurando 'Aplicar regras'...")

    aplicar_regras = localizar(
        "aplicar_regras.png"
    )

    if not aplicar_regras:

        raise Exception(
            "Botão 'Aplicar regras' não encontrado."
        )

    time.sleep(1)

    print("Clicando em 'Aplicar regras'...")

    pyautogui.click(aplicar_regras)

    # Espera a próxima fatura carregar
    time.sleep(9)

    print()
    print("Fatura processada com sucesso!")


# ==================================================
# LOOP PRINCIPAL
# ==================================================

def main(
    limite_seguranca=200,
    modo_teste=True
):

    contador = 0

    # No modo teste:
    # processa apenas uma fatura.
    if modo_teste:

        max_faturas = 1

    else:

        max_faturas = limite_seguranca


    while contador < max_faturas:

        print()
        print("=" * 50)
        print(
            f"Verificando fatura {contador + 1}..."
        )
        print("=" * 50)


        # ------------------------------------------------
        # VERIFICAR SE HÁ FATURA
        # ------------------------------------------------

        if not fatura_disponivel():

            logging.info(
                f"Fila vazia ou tela mudou. "
                f"Total processado: {contador}"
            )

            print()
            print(
                f"Concluído. "
                f"{contador} fatura(s) processada(s)."
            )

            break


        # ------------------------------------------------
        # PROCESSAR
        # ------------------------------------------------

        try:

            processar_fatura()

            contador += 1

            logging.info(
                f"Fatura {contador} processada com sucesso."
            )

            print(
                f"Fatura {contador} processada."
            )


        except Exception as e:

            logging.error(
                f"Erro na fatura {contador + 1}: "
                f"{type(e).__name__}: {e}"
            )

            print()
            print("=" * 50)
            print("ERRO!")
            print("=" * 50)
            print(
                f"{type(e).__name__}: {e}"
            )

            print()
            print(
                "Automação interrompida por segurança."
            )

            break


    # ------------------------------------------------
    # LIMITE DE SEGURANÇA
    # ------------------------------------------------

    if (
        contador >= limite_seguranca
        and not modo_teste
    ):

        logging.warning(
            "Limite de segurança atingido."
        )

        print(
            "Limite de segurança atingido."
        )


# ==================================================
# INÍCIO DO SCRIPT
# ==================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("       AUTOMAÇÃO SAP / OPEN TEXT VIM")
    print("=" * 50)
    print()

    print(
        "Você tem 5 segundos para preparar o SAP."
    )

    print(
        "O SAP deve estar pronto na primeira fatura."
    )

    print()

    time.sleep(5)


    # ------------------------------------------------
    # ALT + TAB PARA O SAP
    # ------------------------------------------------

    print("Alternando para o SAP...")

    pyautogui.hotkey(
        "alt",
        "tab"
    )

    time.sleep(1)


    # ------------------------------------------------
    # MODO TESTE
    # ------------------------------------------------

    # True = processa somente 1 fatura
    #
    # Depois de confirmar que funciona,
    # altere para:
    #
    # main(modo_teste=False)

    main(
        modo_teste=False
    )