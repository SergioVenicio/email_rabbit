import json
from flask import (
    redirect, url_for, render_template, request,
    jsonify, make_response, current_app as app
)


@app.route('/post_msg', methods=['POST'])
def send_to_queue():

    channel = app.email_queue.publisher_channel

    email = request.form.get('email')
    msg = request.form.get('msg')
    subject = request.form.get('subject')

    if not email:
        return make_response(jsonify({
            'error': 'Email is required!'
        }), 400)

    if not msg:
        return make_response(jsonify({
            'error': 'Message is required!'
        }), 400)

    if not subject:
        return make_response(jsonify({
            'error': 'Suject is required!'
        }), 400)

    json_msg = json.dumps({
        'email': email,
        'subject': subject,
        'msg': msg
    })

    channel.basic_publish(
        exchange='emails', routing_key='emails', body=json_msg
    )

    return make_response(jsonify({
        'success': 'email send!'
    }), 200)


@app.route('/')
def home():
    msg = request.args.get('msg', False)
    return render_template('index.html', msg=msg)
