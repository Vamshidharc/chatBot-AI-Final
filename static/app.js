    class Chatterbox {

        constructor(){
             this.args = {
                    openButton: document.querySelector('.chatterbox__button button'),
                    chatBox: document.querySelector('.chatterbox__support'),
                    sendButton: document.querySelector('.send__button')
             }
                    this.state = false;
                    this.messages=[];

        }

        display() {
            const { openButton, chatBox, sendButton} = this.args;
            openButton.addEventListener('click', () => this.toggleState(chatBox));
            sendButton.addEventListener('click', () => this.onSendButton(chatBox));

            const node = chatBox.querySelector('input');
            node.addEventListener('keyup',({key}) => {
                if (key === "Enter"){
                    this.onSendButton(chatBox);
                }
            });
        }

        toggleState(chatBox) {
             this.state = ! this.state;

             if(this.state) {
                 chatBox.classList.add('chatterbox--active');
             } else {
                  chatBox.classList.remove('chatterbox--active');
             }
        }

        onSendButton(chatBox) {
            var textField = chatBox.querySelector('input');
            let text1 = textField.value
            if (text1 === "") {
               return;
            }
            let msg1 = { name: "User", message: text1}
            //var html = '' ;
            this.messages.push(msg1)

            // Show user input immediately
            this.updateChatText(chatBox)
            textField.value = ''

            // Show "waiting for reply.." message
            let msg2 = { name: "Co-op AI", message: "Waiting for reply..." }
            this.messages.push(msg2)




            //html += '<div class="messages__item messages__item--visitor">' + text1 + '</div>'
            //updateChatText(chatBox, html)

            //textField.value = ''
            //const chatMessage = chatBox.querySelector('.chatterbox__messages');
            //chatMessage.innerHTML = html

            fetch($SCRIPT_ROOT + '/predict', {
                method: 'POST',
                   body: JSON.stringify({message:text1}),
                mode:'cors',
                headers: {
                   'Content-type': 'application/json'
                },
              })
              .then(r => r.json())
              .then(r => {
                // Remove the "waiting for reply.." message
                this.messages.pop();

                // Add the actual reply to the messages
                let msg3 = { name: "Co-op AI", message: r.answer };
                this.messages.push(msg3);
//                let msg2 = { name: "Co-op AI", message: r.answer};
//                this.messages.push(msg2);
                // Update the chat text after the reply is received
                this.updateChatText(chatBox, html)
               // textField.value = ''
            })
            .catch((error) => {
                console.error('Error', error);
                this.updateChatText(chatBox)
                textField.value = '';
              });
        }

        updateChatText(chatBox) {
            var html = '' ;
            this.messages.slice().reverse().forEach((item, index) => {
                 if (item.name === "Co-op AI")
                 {
                    html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
                 }
                 else
                 {
                    html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
                 }
               });

            const chatMessage = chatBox.querySelector('.chatterbox__messages');
            chatMessage.innerHTML = html;

        }

    }
    //document.addEventListener('DOMContentLoaded', () => {
    const chatterbox = new Chatterbox();
    chatterbox.display();
