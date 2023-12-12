css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img.freepik.com/premium-vector/chat-bot-logo-smiling-virtual-assistant-bot-smiles-icon-logo-robot-head-with-headphones_843540-91.jpg?w=740" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
<div class="avatar">
        <img src="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/57222/question-mark-emoji-clipart-md.png" style="max-height: 73px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>     
    <div class="message">{{MSG}}</div>
</div>
'''