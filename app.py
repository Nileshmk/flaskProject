# using flask_restful
from flask import Flask, jsonify, request,render_template,make_response, redirect, url_for
from flask_restful import Resource, Api
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import validators,StringField,FileField
import pandas as pd
from plotly.offline import plot
import plotly.express as px
import os
import json
import pandas
# creating the flask app
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
)
csrf = CSRFProtect(app)
api = Api(app)

functionNames = [
    "MAX",
    "MIN",
    "SUM"
]

def handle_uploaded_file(f,fileName):
    # with open('static/' + fileName+'.csv','wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
    fileName = fileName+'.csv'
    f.save(os.path.join(app.root_path,'static',fileName))

class fileForm(FlaskForm):
    name = StringField('FileName',[validators.Length(max=250)])
    file = FileField()

class Dataset(Resource):
  
    def get(self):
  
        return jsonify({'message': 'hello world'})
  
    # Corresponds to POST request
    def post(self):
        form = fileForm()
        if form.validate_on_submit():
            print('true')
            print(form.name.data)
            handle_uploaded_file(form.file.data,form.name.data)
            return redirect(url_for('data'))
        else:
            print('false')
            return make_response(jsonify({'success': False}), 403)


# Create your views here.
def getFilesNames():
    filesNames = []
    for file in os.listdir(".\static"):
        if file.endswith(".csv"):
            filesNames.append(file)
    return filesNames


# another resource to calculate the square of a number
class Compute(Resource):
  
    def post(self, id):
        print(id)
        result = json.loads(request.data.decode('utf-8'))
        id = os.path.join('static',id)
        try:
            dataInCSV =pd.read_csv(id)
            print(result)
            if(result['functionName']=='MAX'):
                return make_response(jsonify({'data': dataInCSV[result['column']].max()}), 200)
            elif(result['functionName']=='MIN'):
                return make_response(jsonify({'data': dataInCSV[result['column']].min()}), 200)
            elif(result['functionName']=='SUM'):
                return make_response(jsonify({'data': dataInCSV[result['column']].sum()}), 200)
            return make_response(jsonify({'success': False}), 403)
        except:
            return make_response(jsonify({'success':False}), 403)
            
class Home(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)
  
class Data(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('upload.html',form=fileForm(),data=getFilesNames()),200,headers)

class Plot(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        df = pd.read_csv('static\california_housing_test.csv')
        fig = px.bar(
            x=df["longitude"], y=df["latitude"]
        )
        gantt_plot = plot(fig,output_type="div")
        return make_response(render_template('display.html',plot_div = gantt_plot,data = getFilesNames(),functionNames=functionNames),200,headers)

class PlotGraph(Resource):

    def post(self,id):
        print(id)
        # result = json.loads(request.data.decode('utf-8'))
        id = os.path.join('static',id)
        result = request.json
        df = pd.read_csv('static\california_housing_test.csv')
        data = {
            'column1':list(df[result['column1']]),
            'column2':list(df[result['column2']])
        }
        return make_response(jsonify(data), 200)

# adding the defined resources along with their corresponding urls
api.add_resource(Home,'/')
api.add_resource(Data,'/data')
api.add_resource(Plot,'/plot')
api.add_resource(Dataset, '/dataset')
api.add_resource(Compute, '/dataset/<id>/compute')
api.add_resource(PlotGraph, '/dataset/<id>/plot')
  
# driver function
if __name__ == '__main__':
  
    app.run()