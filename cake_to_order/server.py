from waitress import serve

from cake_to_order.wsgi import application

if __name__ == '__main__':
    serve(application, port='8000')
