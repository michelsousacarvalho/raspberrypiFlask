from flask import Flask, render_template
import time
import serial
from flask import request
import RPi.GPIO as GPIO

app = Flask(__name__)

templateData = {
        'ativadobuttonquarto1': False,
        'statusQuarto1' : "Desativado",
        'lampquarto1': False,
        'statusLampQuarto1' : "Apagado",
        'alarmeCozinha': False,
        'statusAlarmeCozinha' : "Desativado",
        'lampCozinha' : False,
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
        'statusDimmerSala':'Desligado',
        'portao': False,
        'portaoStatus':"Fechado",
        'garagemLamp':False,
        'statusGaragemLamp': "Apagado"

}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(2, GPIO.IN)
GPIO.add_event_detect(2, GPIO.RISING)



vel1 = 9600
disp1 = "/dev/ttyACM0"

ser1 = serial.Serial(disp1, vel1)
ser2 = serial.Serial(disp1, vel1)

ser1.close()
ser2.close()


@app.route('/')
def index():
    return render_template('test.html', **templateData)

@app.route('/test',  methods=['POST'])
def test():
    command = request.form.get("a")

    stringcommand = str(command)
    ser1.open()
    ser1.write(stringcommand);
    ser1.close()
    print(stringcommand)
    return render_template('test.html', **templateData)

@app.route('/quarto1Alarme/<action>')
def alarmeQuarto1(action):
    global templateData
    global ser1
    ser1.close()

    if action == "off":
        #ser1.open()

        templateData['ativadobuttonquarto1'] = False
        templateData['statusQuarto1'] = "Desativado"
        #ser1.write("<>")
        #ser1.close()
    if action == "on":
        #ser1.open()
        templateData['ativadobuttonquarto1'] = True
        templateData['statusQuarto1'] = "Ativado"
        #ser1.write("<y2>/n")
        #ser1.close()


    return render_template('test.html', **templateData)


@app.route('/quarto1Lamp/<action>')
def quartolamp(action):
    global  templateData
    global ser1
    # global ser2
    ser1.close()
    # ser2.close()
    # time.sleep(0.2)

    if action == "off":
        ser1.open()
        ser1.write("<y10p3>")
        ser1.close()
        time.sleep(0.5)
        ser1.open()
        ser1.write("<y10p3>")
        ser1.close()
        templateData['lampquarto1'] = False
        templateData['statusLampQuarto1'] = "Apagado"


    if action == "on":
        ser1.open()
        ser1.write("<y1255p3>")
        ser1.close()
        time.sleep(0.5)
        ser1.open()
        ser1.write("<y1255p3>")
        ser1.close()
        templateData['lampquarto1'] = True
        templateData['statusLampQuarto1'] = "Aceso"


    return render_template('test.html', **templateData)
@app.route('/cozinhaAlarme/<action>')
def alarmeCozinha(action):
    global  templateData
    global ser1

    if action == "off":
        ser1.open()

        templateData['alarmeCozinha'] = False
        templateData['statusAlarmeCozinha'] = "Desativado"
    if action == "on":
        templateData['alarmeCozinha'] = True
        templateData['statusAlarmeCozinha'] = "Ativado"

    return render_template('test.html', **templateData)

@app.route('/cozinhaLamp/<action>')
def cozinhalamp(action):
    global  templateData
    if action == "off":
        templateData['lampCozinha'] = False
        templateData['iluminacaoCozinha'] = "Apagado"

    if action == "on":
        templateData['lampCozinha'] = True
        templateData['iluminacaoCozinha'] = "Aceso"

    return render_template('test.html', **templateData)

@app.route('/tempQuarto2')
def tempQuarto2():
    global templateData
    templateData['temperaturaQuarto2'] = 10 #pegar retorno serial

    return render_template('test.html', **templateData)


@app.route('/ventilador/<action>')
def ventilador(action):
    global templateData
    if action == "off":
        templateData['ventilador'] = False
        templateData['ventiladorStatus'] = "Desligado"

    if action == "on":
        templateData['ventilador'] = True
        templateData['ventiladorStatus'] = "Ligado"

    return render_template('test.html', **templateData)


@app.route('/quarto2Lamp/<action>')
def quarto2lamp(action):
    global  templateData

    if action == "off":
        GPIO.output(18, GPIO.LOW)
        templateData['lampquarto2'] = False
        templateData['statusLampQuarto2'] = "Apagado"

    if action == "on":
        GPIO.output(18, GPIO.HIGH)
        templateData['lampquarto2'] = True
        templateData['statusLampQuarto2'] = "Aceso"

    return render_template('test.html', **templateData)

@app.route('/banheiroLamp/<action>')
def banheirolamp(action):
    global templateData
    if action == "off":
        templateData['lampBanheiro'] = False
        templateData['statusLampBanheiro'] = "Apagado"

    if action == "on":
        templateData['lampBanheiro'] = True
        templateData['statusLampBanheiro'] = "Aceso"

    return render_template('test.html', **templateData)


@app.route('/salaLamp/<action>')
def salaLamp(action):
    global templateData
    if action == "off":
        templateData['lampSala'] = False
        templateData['statusLampSala'] = "Apagado"

    if action == "on":
        templateData['lampSala'] = True
        templateData['statusLampSala'] = "Aceso"

    return render_template('test.html', **templateData)


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

    return render_template('test.html', **templateData)

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

    return render_template('test.html', **templateData)


@app.route('/garageLamp/<action>')
def garagemLamp(action):
    global templateData
    if action == "off":
        templateData['garagemLamp'] = False
        templateData['statusGaragemLamp'] = "Apagado"

    if action == "on":
        templateData['garagemLamp'] = True
        templateData['statusGaragemLamp'] = "Aceso"

    return render_template('test.html', **templateData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


while (1):
    print "while"
    if GPIO.event_detected(2) == True:
        print "Detect"
        if GPIO.input(18) == 1:
            GPIO.output(18, GPIO.LOW)
        else:
            GPIO.output(18, GPIO.HIGH)

