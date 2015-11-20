from flask import Flask, render_template

app = Flask(__name__)

templateData = {
        'ativadobuttonquarto1': False,
        'statusQuarto1' : "Desativado",
        'lampquarto1': False,
        'statusLampQuarto1' : "Apagado",
        'alarmeCozinha': False,
        'statusAlarmeCozinha' : "Desativado",
        'lampCozinha' : False,
        'iluminacaoCozinha': "Apagado"
}

@app.route('/')
def index():

    return render_template('test.html', **templateData)


@app.route('/quarto1Alarme/<action>')
def alarmeQuarto1(action):
    global  templateData
    # print type(templateData)
    if action == "off":
        templateData['ativadobuttonquarto1'] = False
        templateData['statusQuarto1'] = "Desativado"
    if action == "on":
        templateData['ativadobuttonquarto1'] = True
        templateData['statusQuarto1'] = "Ativado"

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
    # print type(templateData)
    if action == "off":
        templateData['alarmeCozinha'] = False
        templateData['statusAlarmeCozinha'] = "Desativado"
    if action == "on":
        templateData['alarmeCozinha'] = True
        templateData['statusAlarmeCozinha'] = "Ativado"

    return render_template('test.html', **templateData)




@app.route('/sel')
def optionSel():
    return 'sel'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


