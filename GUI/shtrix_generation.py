from barcode import generate
from barcode.writer import ImageWriter

# Список валидных штрих-кодов
barcodes = ["VALID_BARCODE1", "VALID_BARCODE2", "VALID_BARCODE3"]

for code in barcodes:
    # Создаем штрих-код и сохраняем его в PNG
    generate('code128', code, writer=ImageWriter(), output=f'{code}')