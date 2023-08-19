from app.main import main


@main.route('/ping')
def ping():
    return {
        'ping': 'pong'
    }

