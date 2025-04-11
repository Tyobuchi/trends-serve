from flask import Flask, request
from pytrends.request import TrendReq
import json
import time
from pytrends.exceptions import TooManyRequestsError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword', 'tecnología')
    pytrends = TrendReq(hl='es', tz=360)
    try:
        time.sleep(2)
        pytrends.build_payload([keyword], timeframe='today 1-m', geo='')
        data = pytrends.interest_over_time()
        if keyword not in data or data[keyword].empty:
            return json.dumps({"error": f"No se encontraron datos para '{keyword}'"})
        result = {str(date): int(value) for date, value in data[keyword].tail(5).items()}
        return json.dumps(result)
    except TooManyRequestsError:
        return json.dumps({"error": "Demasiadas solicitudes a Google Trends. Por favor, intenta de nuevo en unos minutos."})
    except Exception as e:
        return json.dumps({"error": f"Error inesperado: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
