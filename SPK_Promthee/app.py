from flask import Flask, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    # 1. Data Kriteria & Sub-Kriteria (Dibuat List agar rapi)
    criteria_info = [
        {
            'id': 'C1', 'name': 'Resolusi Layar', 'weight': '30%', 'type': 'Benefit',
            'scores': ['IPS 720p', 'IPS 1080p', 'OLED FHD', 'OLED 2K', 'OLED 4K']
        },
        {
            'id': 'C2', 'name': 'Penyimpanan', 'weight': '30%', 'type': 'Benefit',
            'scores': ['32 GB', '64 GB', '128 GB', '256 GB', '512 GB']
        },
        {
            'id': 'C3', 'name': 'RAM', 'weight': '20%', 'type': 'Benefit',
            'scores': ['2 GB', '4 GB', '6 GB', '8 GB', '12 GB']
        },
        {
            'id': 'C4', 'name': 'Kamera', 'weight': '10%', 'type': 'Benefit',
            'scores': ['8 MP', '12 MP', '48 MP', '64 MP', '108 MP']
        },
        {
            'id': 'C5', 'name': 'Harga', 'weight': '10%', 'type': 'Cost',
            'scores': ['> 15 Juta', '11-15 Juta', '7-11 Juta', '3-6 Juta', '< 3 Juta']
        }
    ]

    # 2. Data Alternatif & Matriks Skor (1-5)
    names = [
        'Apple iPhone 15 Pro Max', 'Samsung Galaxy S24 Ultra', 'Google Pixel 8 Pro', 
        'Xiaomi 14 Ultra', 'OnePlus 12', 'Oppo Find X7 Pro', 
        'Huawei Mate 60 Pro', 'Vivo X100 Pro', 'Asus ROG Phone 7', 'Sony Xperia 1 V'
    ]
    
    data = np.array([
        [5, 5, 5, 3, 1], [4, 5, 5, 4, 1], [4, 4, 4, 4, 2], [4, 4, 4, 5, 2], [4, 4, 4, 4, 3],
        [3, 4, 4, 3, 4], [3, 5, 4, 4, 2], [4, 4, 4, 3, 3], [4, 5, 4, 4, 2], [4, 4, 4, 3, 2]
    ], dtype=float)
    
    weights = np.array([0.3, 0.3, 0.2, 0.1, 0.1])
    n = len(names)

    # Format Bintang untuk Tabel Matriks
    matriks_view = []
    for i in range(n):
        matriks_view.append({
            'kode': f'A{i+1}', 'nama': names[i],
            'vals': [int(x) for x in data[i]]
        })

    # 3. PERHITUNGAN PROMETHEE II
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

    hasil = []
    for i in range(n):
        hasil.append({
            'nama': names[i], 'lf': round(leaving_flow[i], 4),
            'ef': round(entering_flow[i], 4), 'nf': round(net_flow[i], 4)
        })
    hasil.sort(key=lambda x: x['nf'], reverse=True)

    return render_template('index.html', kriteria=criteria_info, matriks=matriks_view, hasil=hasil)

if __name__ == '__main__':
    app.run(debug=True)
