import PyPDF2
import pyttsx3
import os


def converter_pdf_para_audio(caminho_pdf, pagina_inicial=0):
    """
    Lê um PDF e salva o áudio em MP3.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_pdf):
        print("[ERRO] Arquivo não encontrado.")
        return

    # Inicializa o leitor de PDF
    try:
        pdf_file = open(caminho_pdf, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_paginas = len(pdf_reader.pages)

        print(f"[INFO] PDF carregado com {num_paginas} páginas.")

        # Inicializa o motor de voz (Offline)
        engine = pyttsx3.init()

        # Configura velocidade e volume
        engine.setProperty("rate", 200)  # Velocidade da fala
        engine.setProperty("volume", 1.0)  # Volume (0.0 a 1.0)

        # Escolhe voz em português (se disponível)
        voices = engine.getProperty("voices")
        for voice in voices:
            if "brazil" in voice.id.lower() or "portuguese" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        texto_completo = ""

        print("[PROCESSANDO] Extraindo texto e convertendo...")

        # Loop pelas páginas
        for num in range(pagina_inicial, num_paginas):
            pagina = pdf_reader.pages[num]
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + " "

        # Salva o arquivo de áudio
        nome_saida = os.path.splitext(caminho_pdf)[0] + ".mp3"
        print(f"[GRAVANDO] Salvando em: {nome_saida}")

        engine.save_to_file(texto_completo, nome_saida)
        engine.runAndWait()

        print(f"[SUCESSO] Audiobook criado: {nome_saida}")
        os.startfile(nome_saida)  # Toca o áudio ao terminar

    except Exception as e:
        print(f"[ERRO] Falha na conversão: {e}")


if __name__ == "__main__":
    # Teste rápido se rodar direto
    arquivo = input("Arraste o PDF para cá: ").strip('"')
    converter_pdf_para_audio(arquivo)
