from flask import session
from flask_socketio import emit, join_room
from datetime import datetime
from database import db, Message, Conversation


def register_events(socketio):

    @socketio.on('join')
    def on_join(data):
        room = f"conv_{data['conversation_id']}"
        join_room(room)

    @socketio.on('send_message')
    def on_send_message(data):
        current_user_id = session.get('user_id')
        if not current_user_id:
            return

        content = data.get('content', '').strip()
        conversation_id = data.get('conversation_id')
        if not content or not conversation_id:
            return

        msg = Message(
            conversation_id=conversation_id,
            sender_id=current_user_id,
            content=content,
            timestamp=datetime.utcnow()
        )
        db.session.add(msg)

        conv = Conversation.query.get(conversation_id)
        conv.last_message_at = datetime.utcnow()
        db.session.commit()

        room = f"conv_{conversation_id}"
        emit('new_message', {
            'sender_id': current_user_id,
            'content': content,
            'timestamp': msg.timestamp.strftime('%H:%M'),
        }, room=room)