from flask import Blueprint, request, jsonify, session
from database import db, Conversation, Message, User

chat_bp = Blueprint('chat', __name__)


def get_or_create_conversation(user1_id, user2_id):
    """Find existing conversation or create a new one."""
    # Always store with smaller id as user1 (avoids duplicates)
    a, b = sorted([user1_id, user2_id])
    
    conv = Conversation.query.filter_by(user1_id=a, user2_id=b).first()
    if not conv:
        conv = Conversation(user1_id=a, user2_id=b)
        db.session.add(conv)
        db.session.commit()
    return conv


@chat_bp.route('/conversation/<int:other_user_id>', methods=['GET'])
def get_conversation(other_user_id):
    """Get or create a conversation, return its history."""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Not logged in'}), 401

    conv = get_or_create_conversation(current_user_id, other_user_id)

    # Mark messages as read
    Message.query.filter_by(
        conversation_id=conv.id,
        is_read=False
    ).filter(Message.sender_id != current_user_id).update({'is_read': True})
    db.session.commit()

    # Return message history
    messages = [
        {
            'id': m.id,
            'sender_id': m.sender_id,
            'content': m.content,
            'timestamp': m.timestamp.strftime('%H:%M'),
            'is_mine': m.sender_id == current_user_id
        }
        for m in conv.messages
    ]

    return jsonify({'conversation_id': conv.id, 'messages': messages})