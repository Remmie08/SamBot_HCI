class App {
    constructor(){
        this.message = document.getElementById("message-body");
        this.aiStatus = document.getElementById("aiStatus");
        this.chatM = document.getElementById("chat-messages");
        this.submitB = document.getElementById("submit-button");

        this.setStatus = this.setStatus.bind(this);
        this.sendMessage = this.sendMessage.bind(this);
        this.showMessage = this.showMessage.bind(this);

        this.submitB.addEventListener("click", this.sendMessage);
    }

    async sendMessage() {

        event.preventDefault();

        this.setStatus("thinking");

        const obj = {
            message: this.message.value
        }

        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(obj)
        });

        this.setStatus("answering");
        await new Promise(r => setTimeout(r, 700));

        const data = await res.json();
        this.showMessage(data.User, data.SamBot);

        this.setStatus("idle");
        this.message.value = "";
    }

    showMessage(userMessage, samBotMessage) {
        const userP = document.createElement("p");
        userP.textContent = `You: ${userMessage}`;
        this.chatM.appendChild(userP);

        const samBotP = document.createElement("p");
        samBotP.textContent = `SamBot: ${samBotMessage}`;
        this.chatM.appendChild(samBotP);

        this.chatM.scrollTop = this.chatM.scrollHeight;
    }

    setStatus(status) {
        if (status === "idle") {
            this.aiStatus.src = "./static/images/idle.png";
        }
        else if (status === "thinking") {
            this.aiStatus.src = "./static/images/think.png";
        }
        else if (status === "answering") {
            this.aiStatus.src = "./static/images/answer.png";
        }
    }

    
}

export default App;