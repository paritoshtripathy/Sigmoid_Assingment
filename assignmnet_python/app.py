import time
from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type
from resources import get_bucket, get_buckets_list
import boto3
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client.core import Summary, Counter, Histogram, Gauge
from prometheus_flask_exporter import PrometheusMetrics



app = Flask(__name__)

_INF=float("inf")

graphs={}
graphs['c']= Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h']= Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds', buckets=(1,2,5,6,10,_INF))

metrics = PrometheusMetrics(app)
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")

Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type


@app.route('/', methods=['GET', 'POST'])
def index():
    # start = time.time()
    # graphs['c'].inc()

    # time.sleep(0.600)
    # end=time.time()
    # graphs['h'].observe(end-start)

    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("index.html", buckets=buckets)


# @app.route('/metrics')
# def request_counts():
#     res=[]
#     for k,v in graphs.items():
#         res.append(prometheus_client.generate_latest(v))
#     return Response(res, mimetype="text/plain")    


@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()
    buckets = get_buckets_list()

    return render_template('files.html', my_bucket=my_bucket, files=summaries, buckets=buckets)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)

    flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/create', methods=['POST'])
def create():
    new_bucket=request.form['text']
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=new_bucket)

    flash('New bucket created successfully')
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))

@app.route('/delete_f', methods=['POST'])
def delete_f():
    bucket_name = request.form['bucket']
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    flash('Bucket deleted successfully')
    return redirect(url_for('index'))



@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )
@app.route('/copy', methods=['POST'])
def copy():
    cbucket = request.form['cbucket']
    cfile = request.form['cfile']
    tbucket = request.form['tbucket']
    s3 = boto3.resource('s3')
    copy_source = {
     'Bucket': cbucket,
     'Key': cfile}
    bucket = s3.Bucket(tbucket)
    bucket.copy(copy_source, cfile)
    flash('File copied sucessfully')
    return redirect(url_for('files'))


if __name__ == "__main__":
    app.run()
