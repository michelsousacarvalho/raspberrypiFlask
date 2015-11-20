from flask import Flask, render_template
import serial

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
        'statusLapBanheiro': "Apagado"

}

ser = serial.Serial("/dev/ttyACM0", 9600)



@app.route('/')
def index():
    return render_template('test.html', **templateData)


@app.route('/quarto1Alarme/<action>')
def alarmeQuarto1(action):
    global templateData
    global ser

    if action == "off":
        templateData['ativadobuttonquarto1'] = False
        templateData['statusQuarto1'] = "Desativado"
        ser.write("<y10>")
    if action == "on":
        templateData['ativadobuttonquarto1'] = True
        templateData['statusQuarto1'] = "Ativado"
        ser.write("<y1255>")

    ser.close()
    return render_template('test.html', **templateData)


@app.route('/quarto1Lamp/<action>')
def quartolamp(action):
    global  templateData
    if action == "off":
        templateData['lampquarto1'] = False
        templateData['statusLampQuarto1'] = "Apagado"

    if action == "on":
        templateData['lampquarto1'] = True
        templateData['statusLampQuarto1'] = "Aceso"

    return render_template('test.html', **templateData)

@app.route('/cozinhaAlarme/<action>')
def alarmeCozinha(action):
    global  templateData

    if action == "off":
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
        templateData['lampquarto2'] = False
        templateData['statusLampQuarto2'] = "Apagado"

    if action == "on":
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


@app.route('/sel')
def optionSel():
    return 'sel'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


