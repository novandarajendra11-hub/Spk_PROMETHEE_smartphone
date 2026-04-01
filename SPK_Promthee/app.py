from flask import Flask, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Data Kriteria & Sub-Kriteria (Sesuai Gambar)
    criteria_info = [
        {
            'id': 'C1', 'name': 'Resolusi Layar', 'weight': '30%', 'type': 'Benefit',
            'details': '1:IPS 720p, 2:IPS 1080p, 3:OLED FHD, 4:OLED 2K, 5:OLED 4K'
        },
        {
            'id': 'C2', 'name': 'Penyimpanan', 'weight': '30%', 'type': 'Benefit',
            'details': '1:32GB, 2:64GB, 3:128GB, 4:256GB, 5:512GB'
        },
        {
            'id': 'C3', 'name': 'RAM', 'weight': '20%', 'type': 'Benefit',
            'details': '1:2GB, 2:4GB, 3:6GB, 4:8GB, 5:12GB'
        },
        {
            'id': 'C4', 'name': 'Kamera', 'weight': '10%', 'type': 'Benefit',
            'details': '1:8MP, 2:12MP, 3:48MP, 4:64MP, 5:108MP'
        },
        {
            'id': 'C5', 'name': 'Harga', 'weight': '10%', 'type': 'Cost',
            'details': '1:>15jt, 2:11-15jt, 3:7-11jt, 4:3-6jt, 5:<3jt'
        }
    ]

    # 2. Nama Alternatif
    names = [
        'Apple iPhone 15 Pro Max', 'Samsung Galaxy S24 Ultra', 'Google Pixel 8 Pro', 
        'Xiaomi 14 Ultra', 'OnePlus 12', 'Oppo Find X7 Pro', 
        'Huawei Mate 60 Pro', 'Vivo X100 Pro', 'Asus ROG Phone 7', 'Sony Xperia 1 V'
    ]
    
    # 3. Matriks Keputusan (Skor 1-5 berdasarkan Sub-Kriteria di Gambar)
    data = np.array([
        [5, 5, 5, 3, 1], # A1 (iPhone 15 Pro Max)
        [4, 5, 5, 4, 1], # A2 (S24 Ultra)
        [4, 4, 4, 4, 2], # A3
        [4, 4, 4, 5, 2], # A4
        [4, 4, 4, 4, 3], # A5
        [3, 4, 4, 3, 4], # A6
        [3, 5, 4, 4, 2], # A7
        [4, 4, 4, 3, 3], # A8
        [4, 5, 4, 4, 2], # A9
        [4, 4, 4, 3, 2]  # A10
    ], dtype=float)
    
    weights = np.array([0.3, 0.3, 0.2, 0.1, 0.1])
    n = len(names)

    # Format Tampilan Bintang
    matriks_view = []
    for i in range(n):
        matriks_view.append({
            'kode': f'A{i+1}', 'nama': names[i],
            'c1': "⭐" * int(data[i][0]), 'c2': "⭐" * int(data[i][1]),
            'c3': "⭐" * int(data[i][2]), 'c4': "⭐" * int(data[i][3]), 'c5': "⭐" * int(data[i][4])
        })

    # 4. LOGIKA PROMETHEE II
    pi = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                diff = data[i] - data[j]
                p_val = (diff > 0).astype(float) 
                pi[i, j] = np.sum(p_val * weights)
                
    leaving_flow = np.sum(pi, axis=1) / (n - 1)
    entering_flow = np.sum(pi, axis=0) / (n - 1)
    net_flow = leaving_flow - entering_flow 

    # 5. Penyiapan Hasil Akhir
    hasil = []
    for i in range(n):
        hasil.append({
            'nama': names[i],
            'lf': round(leaving_flow[i], 4),
            'ef': round(entering_flow[i], 4),
            'nf': round(net_flow[i], 4),
            'url': f'https://www.youtube.com/results?search_query=Review+{names[i].replace(" ", "+")}'
        })

    hasil.sort(key=lambda x: x['nf'], reverse=True)

    labels = [h['nama'] for h in hasil]
    values = [h['nf'] for h in hasil]

    return render_template('index.html', 
                           kriteria=criteria_info,
                           matriks=matriks_view, 
                           hasil=hasil, 
                           labels=labels, 
                           data_grafik=values)

if __name__ == '__main__':
    app.run(debug=True)
