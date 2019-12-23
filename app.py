from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64


app = Flask(__name__)

app.config["data"] = "./info"

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/columnas', methods=['POST'])
def columnas():
    if request.method == 'POST':
        da = request.files['file']
        filename = secure_filename(da.filename)
        da.save(os.path.join(app.config["data"], filename))
        df = pd.read_csv('./info/{}'.format(filename))
        columnas = { 
            'columnas': df.columns.tolist(),
            'filename': filename
        }

        
        return render_template('generador.html', columnas=columnas)

@app.route('/grafica', methods=['POST'])
def grafica():
    if request.method == 'POST':
        columna = request.form['columna']
        grafica = request.form['tipo']
        filename = request.form['filename']
        df = pd.read_csv('./info/{}'.format(filename))[columna]
        
        plt.clf() 
        if grafica == 'puntos':
            img = io.BytesIO()
            plt.title("la grafica por: "+columna)
            plt.plot(df.head(10),'--')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })
        elif grafica == 'lineas':
            print('lineas')
            img = io.BytesIO()
            plt.title("la grafica por: "+columna)
            plt.plot(df.head(10))
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })
        elif grafica == 'pastel':
            img = io.BytesIO()
            plt.title("la grafica por: "+columna)
            datos = df.head(10).tolist()
            plt.pie(datos, autopct="%0.1f %%")
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })
        else:
            img = io.BytesIO()
            
            datos = df.head(10).tolist()
            for i in range(len(datos)):
                plt.bar(i, datos[i], align = 'center')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('grafica.html', imagen={ 'imagen': plot_url })

if __name__ == "__main__":
    app.run(port = 80, debug = True)

