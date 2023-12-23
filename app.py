from flask import Flask

app = Flask(__name__)


@app.route('/serviceA')
def service_a():
    # Xử lý logic cho dịch vụ A
    # ...
    return 'Service A'


if __name__ == '__main__':
    app.run()
