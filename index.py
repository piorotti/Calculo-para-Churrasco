import PySimpleGUI as sg
import subprocess
import platform
from valida_cep import consultar_cep
from valida_cpf import validar_cpf
from calculo import calcular_itens
from gerar_pdf import gerar_pdf
from obter_opcoes_entrega import obter_opcoes_entrega

def main():
    layout = [
        [sg.Text("Digite o CEP:")],
        [sg.InputText(key="cep_input")],
        [sg.Text("Número da casa:")],  # Campo para obter o número da casa
        [sg.InputText(key="numero_casa_input")],
        [sg.Text("Digite o CPF:")],
        [sg.InputText(key="cpf_input")],
        [sg.Text("Número de convidados:")],
        [sg.InputText(key="convidados_input")],
        [sg.Button("Calcular")]
    ]

    window = sg.Window("Churrasco Planner", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Calcular":
            cep = values["cep_input"]
            numero_casa = values["numero_casa_input"]  # Obtenção do número da casa
            cpf = values["cpf_input"]
            convidados = values["convidados_input"]
            
            resultado_cep = consultar_cep(cep, numero_casa)  # Crie resultado_cep com o número da casa

            if not resultado_cep or not validar_cpf(cpf):
                sg.popup_error("CEP inválido ou CPF inválido. Verifique os campos e tente novamente.")
                continue

            opcoes_entrega = obter_opcoes_entrega(cep)

            tipo_entrega = ""

            if opcoes_entrega:
                layout_entrega = [
                    [sg.Text("Escolha o tipo de entrega:")],
                    [sg.Radio("Entrega padrão", "tipo_entrega", key="entrega_padrao", default=True)],
                    [sg.Radio("Entrega expressa", "tipo_entrega", key="entrega_expressa")],
                    [sg.Button("Gerar PDF")]
                ]
                
                window_entrega = sg.Window("Escolha o Tipo de Entrega", layout_entrega)

                event_entrega, values_entrega = window_entrega.read()

                if event_entrega == "Gerar PDF":
                    if values_entrega["entrega_padrao"]:
                        tipo_entrega = "Entrega Padrão"
                    elif values_entrega["entrega_expressa"]:
                        tipo_entrega = "Entrega Expressa"
                    window_entrega.close()
                else:
                    window_entrega.close()
                    continue
            else:
                sg.popup_error("Não há opções de entrega disponíveis para este CEP. O PDF será gerado sem tipo de entrega.")

            try:
                convidados = int(convidados)
                carne, bebida = calcular_itens(convidados)
                
                pdf_filename = gerar_pdf(cep, cpf, convidados, carne, bebida, tipo_entrega, resultado_cep)  # Passe resultado_cep para gerar_pdf

                if platform.system() == "Darwin":
                    subprocess.Popen(['open', pdf_filename], shell=True)
                elif platform.system() == "Windows":
                    subprocess.Popen(['start', pdf_filename], shell=True)

            except ValueError:
                sg.popup_error("Por favor, insira um número válido de convidados.")

    window.close()

if __name__ == "__main__":
    main()
