from flask import Flask, render_template
import time
import serial
from flask import request
import RPi.GPIO as GPIO

taxa = 9600
porta0 = "/dev/ttyACM0"
porta1 = "/dev/ttyACM1"

ser0 = serial.Serial(porta0, taxa)
ser1 = serial.Serial(porta1, taxa)

ser0.close()
ser1.close()

luzQ1 = 8  # Pino fisico 8
luzQ2 = 10  # Pino fisico 10
luzBan = 12  # Pino fisico 12
touch = 16  # Pino fisico 16

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# declara saidas da GPIO
GPIO.setup(luzQ1, GPIO.OUT)
GPIO.setup(luzQ2, GPIO.OUT)
GPIO.setup(luzBan, GPIO.OUT)

# declara entradas da GPIO
GPIO.setup(touch, GPIO.IN)
GPIO.add_event_detect(touch, GPIO.RISING)




app = Flask(__name__)

templateData = {
    'ativadobuttonquarto1': False,
    'statusQuarto1': "Desativado",
    'lampquarto1': False,
    'statusLampQuarto1': "Apagado",
    'alarmeCozinha': False,
    'statusAlarmeCozinha': "Desativado",
    'lampCozinha': False,
    'iluminacaoCozinha': "Apagado",
    'temperaturaQuarto2': 0,
    'ventilador': False,
    'ventiladorStatus': "Desligado",
    'lampquarto2': False,
    'statusLampQuarto2': "Apagado",
    'lampBanheiro': False,
    'statusLapBanheiro': "Apagado",
    'lampSala': False,
    'statusLapSala': "Apagado",
    'dimmerSala': False,
    'statusDimmerSala': 'Desligado',
    'portao': False,
    'portaoStatus': "Fechado",
    'garagemLamp': False,
    'statusGaragemLamp': "Apagado"

}

def rotina():
    global templateData
    if GPIO.event_detected(touch) == True:
        if GPIO.input(luzBan) == 1:
            GPIO.output(luzBan, GPIO.LOW)
        else:
            GPIO.output(luzBan, GPIO.HIGH)
    # return render_template('test.html', **templateData)



@app.route('/')
def index():
    # rotina()
    return render_template('test.html', **templateData)


@app.route('/test', methods=['POST'])
def test():
    command = request.form.get("a")

    stringcommand = str(command)
    ser1.open()
    ser1.write(stringcommand);
    ser1.close()
    print(stringcommand)

    # rotina()
    


@app.route('/quarto1Alarme/<action>')
def alarmeQuarto1(action):
    global templateData
    global ser1
    ser1.close()

    if action == "off":
        # ser1.open()

        templateData['ativadobuttonquarto1'] = False
        templateData['statusQuarto1'] = "Desativado"


        # ser1.write("<>")
        # ser1.close()
    if action == "on":
        # ser1.open()
        templateData['ativadobuttonquarto1'] = True
        templateData['statusQuarto1'] = "Ativado"
        # GPIO.output(8, GPIO.HIGH)
        # ser1.write("<y2>/n")
        # ser1.close()

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/quarto1Lamp/<action>')
def quartolamp(action):
    global templateData

    if action == "off":
        templateData['lampquarto1'] = False
        templateData['statusLampQuarto1'] = "Apagado"
        GPIO.output(luzQ1, GPIO.LOW)

    if action == "on":
        templateData['lampquarto1'] = True
        templateData['statusLampQuarto1'] = "Aceso"
        GPIO.output(luzQ1, GPIO.HIGH)

    rotina()
    return render_template('test.html', **templateData)


@app.route('/cozinhaAlarme/<action>')
def alarmeCozinha(action):
    global templateData
    global ser1

    if action == "off":
        ser1.open()

        templateData['alarmeCozinha'] = False
        templateData['statusAlarmeCozinha'] = "Desativado"
    if action == "on":
        templateData['alarmeCozinha'] = True
        templateData['statusAlarmeCozinha'] = "Ativado"

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/cozinhaLamp/<action>')
def cozinhalamp(action):
    global templateData
    if action == "off":
        templateData['lampCozinha'] = False
        templateData['iluminacaoCozinha'] = "Apagado"

    if action == "on":
        templateData['lampCozinha'] = True
        templateData['iluminacaoCozinha'] = "Aceso"

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/tempQuarto2')
def tempQuarto2():
    global templateData
    templateData['temperaturaQuarto2'] = 10  # pegar retorno serial

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/ventilador/<action>')
def ventilador(action):
    global templateData
    if action == "off":
        templateData['ventilador'] = False
        templateData['ventiladorStatus'] = "Desligado"

    if action == "on":
        templateData['ventilador'] = True
        templateData['ventiladorStatus'] = "Ligado"

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/quarto2Lamp/<action>')
def quarto2lamp(action):
    global templateData

    if action == "off":
        templateData['lampquarto2'] = False
        templateData['statusLampQuarto2'] = "Apagado"
        GPIO.output(luzQ2, GPIO.LOW)

    if action == "on":
        templateData['lampquarto2'] = True
        templateData['statusLampQuarto2'] = "Aceso"
        GPIO.output(luzQ2, GPIO.HIGH)

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/banheiroLamp/<action>')
def banheirolamp(action):
    global templateData
    if action == "off":
        templateData['lampBanheiro'] = False
        templateData['statusLampBanheiro'] = "Apagado"
        GPIO.output(luzBan, GPIO.LOW)

    if action == "on":
        templateData['lampBanheiro'] = True
        templateData['statusLampBanheiro'] = "Aceso"
        GPIO.output(luzBan, GPIO.HIGH)

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/salaLamp/<action>')
def salaLamp(action):
    global templateData
    if action == "off":
        templateData['lampSala'] = False
        templateData['statusLampSala'] = "Apagado"

    if action == "on":
        templateData['lampSala'] = True
        templateData['statusLampSala'] = "Aceso"

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/salaLuminosidaLamp/<action>')
def salaLuminosidadeLamp(action):
    global templateData
    if action == "off":
        templateData['dimmerSala'] = False
        templateData['statusDimmerSala'] = "Desligado"

    if action == "25":
        templateData['dimmerSala'] = True
        templateData['statusDimmerSala'] = "25%"

    if action == "50":
        templateData['dimmerSala'] = True
        templateData['statusDimmerSala'] = "50%"

    if action == "75":
        templateData['dimmerSala'] = True
        templateData['statusDimmerSala'] = "75%"

    if action == "100":
        templateData['dimmerSala'] = True
        templateData['statusDimmerSala'] = "100%"

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/portao/<action>')
def portao(action):
    global templateData
    global ser1
    ser1.close()

    if action == "off":
        ser1.open()
        ser1.write("<y2>/n")
        ser1.close()
        templateData['portao'] = False
        templateData['portaoStatus'] = "Fechado"

    if action == "on":
        templateData['portao'] = True
        templateData['portaoStatus'] = "Aberto"

    rotina()
    # return render_template('test.html', **templateData)


@app.route('/garageLamp/<action>')
def garagemLamp(action):
    global templateData
    if action == "off":
        templateData['garagemLamp'] = False
        templateData['statusGaragemLamp'] = "Apagado"

    if action == "on":
        templateData['garagemLamp'] = True
        templateData['statusGaragemLamp'] = "Aceso"

    rotina()
    # return render_template('test.html', **templateData)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


