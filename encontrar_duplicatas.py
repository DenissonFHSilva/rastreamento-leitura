import os
import hashlib
import shutil
from collections import defaultdict

PASTAS_IGNORADAS = {'.git', 'venv', '__pycache__', '.mypy_cache', '.idea'}
EXTENSOES_VALIDAS = {'.py', '.html', '.txt', '.csv', '.json', '.md', '.db'}
PASTA_DESTINO = "duplicatas"

def gerar_hash(caminho_arquivo, parcial=False, chunk_size=1024):
    hash_md5 = hashlib.md5()
    try:
        with open(caminho_arquivo, 'rb') as f:
            if parcial:
                hash_md5.update(f.read(chunk_size))
            else:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
    except Exception as e:
        print(f"⚠️ Erro ao ler {caminho_arquivo}: {e}")
        return None
    return hash_md5.hexdigest()

def encontrar_duplicatas(diretorio_raiz):
    arquivos_por_tamanho = defaultdict(list)
    arquivos_por_hash_parcial = defaultdict(list)
    arquivos_por_hash_total = {}
    duplicatas = []

    for dirpath, dirnames, arquivos in os.walk(diretorio_raiz):
        dirnames[:] = [d for d in dirnames if d not in PASTAS_IGNORADAS]

        for nome in arquivos:
            caminho = os.path.join(dirpath, nome)
            _, ext = os.path.splitext(nome)
            if ext.lower() not in EXTENSOES_VALIDAS:
                continue
            try:
                tamanho = os.path.getsize(caminho)
                arquivos_por_tamanho[tamanho].append(caminho)
            except:
                continue

    for tamanho, lista in arquivos_por_tamanho.items():
        if len(lista) < 2:
            continue
        for caminho in lista:
            hash_parcial = gerar_hash(caminho, parcial=True)
            if hash_parcial:
                arquivos_por_hash_parcial[(tamanho, hash_parcial)].append(caminho)

    for _, lista in arquivos_por_hash_parcial.items():
        if len(lista) < 2:
            continue
        for caminho in lista:
            hash_total = gerar_hash(caminho, parcial=False)
            if not hash_total:
                continue
            if hash_total in arquivos_por_hash_total:
                original = arquivos_por_hash_total[hash_total]
                duplicatas.append((caminho, original))
            else:
                arquivos_por_hash_total[hash_total] = caminho

    if duplicatas:
        os.makedirs(PASTA_DESTINO, exist_ok=True)
        with open("duplicatas.txt", "w", encoding="utf-8") as f:
            for dup, original in duplicatas:
                f.write(f"{dup}\nDUPLICADO DE:\n{original}\n\n")
                try:
                    novo_nome = os.path.join(PASTA_DESTINO, os.path.basename(dup))
                    shutil.move(dup, novo_nome)
                    print(f"📦 Movido: {dup} → {novo_nome}")
                except Exception as e:
                    print(f"❌ Erro ao mover {dup}: {e}")
        print(f"\n✅ {len(duplicatas)} duplicatas movidas para a pasta '{PASTA_DESTINO}' e listadas em 'duplicatas.txt'.")
    else:
        print("\n🎉 Nenhuma duplicata encontrada!")

if __name__ == "__main__":
    pasta = input("📂 Caminho da pasta para verificar duplicatas: ").strip()
    if os.path.isdir(pasta):
        encontrar_duplicatas(pasta)
    else:
        print("❌ Caminho inválido.")
