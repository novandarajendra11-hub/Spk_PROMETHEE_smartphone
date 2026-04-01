from flask import Flask, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Data Alternatif Smartphone
    alternatives = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10']
    names = [
        'Apple iPhone 15 Pro Max', 'Samsung Galaxy S24 Ultra', 'Google Pixel 8 Pro', 
        'Xiaomi 14 Ultra', 'OnePlus 12', 'Oppo Find X7 Pro', 
        'Huawei Mate 60 Pro', 'Vivo X100 Pro', 'Asus ROG Phone 7', 'Sony Xperia 1 V'
    ]
    
    # Generate Link YouTube Review Otomatis
    urls = [f'https://www.youtube.com/results?search_query=Review+{name.replace(" ", "+")}' for name in names]
    
    # 2. Matriks Keputusan Awal (Sesuai Jurnal)
    data = np.array([
        [5, 5, 5, 3, 1], # A1 - iPhone 15 Pro Max (>15jt)
        [4, 5, 5, 4, 1], # A2 - S24 Ultra (>15jt)
        [4, 4, 4, 4, 2], # A3 - Pixel 8 Pro (11-15jt)
        [4, 4, 4, 5, 2], # A4 - Xiaomi 14 Ultra (11-15jt)
        [4, 4, 3, 4, 3], # A5 - OnePlus 12 (7-11jt)
        [3, 4, 4, 3, 4], # A6 - Oppo Find X7 Pro (3-7jt)
        [3, 5, 4, 4, 2], # A7 - Huawei Mate 60 Pro (11-15jt)
        [4, 4, 4, 3, 3], # A8 - Vivo X100 Pro (7-11jt)
        [4, 5, 4, 4, 2], # A9 - Asus ROG Phone 7 (11-15jt)
        [4, 4, 4, 3, 2]  # A10 - Sony Xperia 1 V (11-15jt)
    ], dtype=float)
    
    # Bobot: C1(Layar)=30%, C2(Simpan)=30%, C3(RAM)=20%, C4(Kamera)=10%, C5(Harga)=10%
    weights = np.array([0.3, 0.3, 0.2, 0.1, 0.1])
    n = len(alternatives)

    # Format Tampilan Bintang untuk Tabel Matriks di Web
    matriks_keputusan = []
    for i in range(n):
        matriks_keputusan.append({
            'kode': alternatives[i], 'nama': names[i],
            'c1': "⭐" * int(data[i][0]), 'c2': "⭐" * int(data[i][1]),
            'c3': "⭐" * int(data[i][2]), 'c4': "⭐" * int(data[i][3]), 'c5': "⭐" * int(data[i][4])
        })

    # ==========================================
    # 3. PERHITUNGAN METODE PROMETHEE II
    # ==========================================
    pi = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                diff = data[i] - data[j]
                p_val = (diff > 0).astype(float) # Usual Criterion
                pi[i, j] = np.sum(p_val * weights)
                
    leaving_flow = np.sum(pi, axis=1) / (n - 1)
    entering_flow = np.sum(pi, axis=0) / (n - 1)
    net_flow = leaving_flow - entering_flow 
    # ==========================================

    # 4. Format Hasil Akhir untuk Web
    hasil = []
    for i in range(n):
        hasil.append({
            'kode': alternatives[i],
            'nama': names[i],
            'url': urls[i],
            'lf': round(leaving_flow[i], 4),
            'ef': round(entering_flow[i], 4),
            'nf': round(net_flow[i], 4)
        })

    # Urutkan berdasarkan Net Flow (Ranking PROMETHEE)
    hasil.sort(key=lambda x: x['nf'], reverse=True)

    labels_grafik = []
    data_grafik = []
    for idx, item in enumerate(hasil):
        item['ranking'] = idx + 1
        labels_grafik.append(item['nama'])
        data_grafik.append(item['nf'])

    return render_template('index.html', 
                           matriks=matriks_keputusan, 
                           hasil=hasil, 
                           labels=labels_grafik, 
                           data_grafik=data_grafik)

if __name__ == '__main__':
    app.run(debug=True)
