document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages")
    const messageInput = document.getElementById("message-input")
    const sendBtn = document.getElementById("send-btn")
    const resetBtn = document.getElementById("reset-btn")
    const imageUpload = document.getElementById("image-upload")
  
    // Auto-resize textarea
    messageInput.addEventListener("input", function () {
      this.style.height = "auto"
      this.style.height = this.scrollHeight + "px"
    })
  
    // Send message when Enter key is pressed (without Shift)
    messageInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()
        sendMessage()
      }
    })
  
    // Send message when send button is clicked
    sendBtn.addEventListener("click", sendMessage)
  
    // Reset conversation
    resetBtn.addEventListener("click", resetConversation)
  
    // Handle image upload
    imageUpload.addEventListener("change", uploadImage)
  
    // Handle CSV upload
    const csvUpload = document.getElementById('csv-upload');
    csvUpload.addEventListener('change', uploadCSV);
  
    function sendMessage() {
      const message = messageInput.value.trim()
      if (!message) return
  
      // Add user message to chat
      addMessage("user", message)
  
      // Clear input
      messageInput.value = ""
      messageInput.style.height = "auto"
  
      // Show loading indicator
      const loadingMessage = addLoadingMessage()
  
      // Send message to server
      fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Remove loading indicator
          loadingMessage.remove()
  
          // Add assistant response
          addMessage("assistant", data.response)
        })
        .catch((error) => {
          console.error("Error:", error)
          loadingMessage.remove()
          addMessage("assistant", "Sorry, something went wrong. Please try again.")
        })
    }
  
    function uploadImage() {
      const file = imageUpload.files[0]
      if (!file) return
  
      // Create FormData
      const formData = new FormData()
      formData.append("file", file)
  
      // Add uploading message
      addMessage("user", "Uploading image for analysis...")
  
      // Show loading indicator
      const loadingMessage = addLoadingMessage()
  
      // Upload image
      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          // Remove loading indicator
          loadingMessage.remove()
  
          if (data.error) {
            addMessage("assistant", `Error: ${data.error}`)
            return
          }
  
          // Add image preview to user message
          const lastUserMessage = chatMessages.lastElementChild
          const imgElement = document.createElement("img")
          imgElement.src = URL.createObjectURL(file)
          imgElement.alt = "Uploaded image"
          lastUserMessage.querySelector(".message-content").appendChild(imgElement)
  
          // Add assistant response with analysis
          addMessage("assistant", data.analysis)
        })
        .catch((error) => {
          console.error("Error:", error)
          loadingMessage.remove()
          addMessage("assistant", "Sorry, something went wrong with the image upload. Please try again.")
        })
  
      // Reset file input
      imageUpload.value = ""
    }
  
    function uploadCSV() {
      const file = csvUpload.files[0];
      if (!file) return;
      
      // Create FormData
      const formData = new FormData();
      formData.append('file', file);
      
      // Add uploading message
      addMessage('user', `Uploading CSV file: ${file.name}`);
      
      // Show loading indicator
      const loadingMessage = addLoadingMessage();
      
      // Upload CSV
      fetch('/upload-csv', {
          method: 'POST',
          body: formData,
      })
      .then(response => response.json())
      .then(data => {
          // Remove loading indicator
          loadingMessage.remove();
          
          if (data.error) {
              addMessage('assistant', `Error: ${data.error}`);
              return;
          }
          
          // Add assistant response with confirmation
          addMessage('assistant', data.response);
      })
      .catch(error => {
          console.error('Error:', error);
          loadingMessage.remove();
          addMessage('assistant', 'Sorry, something went wrong with the CSV upload. Please try again.');
      });
      
      // Reset file input
      csvUpload.value = '';
  }
  
    function resetConversation() {
      // Clear chat messages except the first welcome message
      while (chatMessages.children.length > 1) {
        chatMessages.removeChild(chatMessages.lastChild)
      }
  
      // Reset conversation on server
      fetch("/reset", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.message)
        })
        .catch((error) => {
          console.error("Error:", error)
        })
    }
  
    function addMessage(role, content) {
      const messageDiv = document.createElement("div")
      messageDiv.className = `message ${role}`
  
      const messageContent = document.createElement("div")
      messageContent.className = "message-content"
      messageContent.textContent = content
  
      messageDiv.appendChild(messageContent)
      chatMessages.appendChild(messageDiv)
  
      // Scroll to bottom
      chatMessages.scrollTop = chatMessages.scrollHeight
  
      return messageDiv
    }
  
    function addLoadingMessage() {
      const loadingDiv = document.createElement("div")
      loadingDiv.className = "message assistant"
  
      const loadingContent = document.createElement("div")
      loadingContent.className = "message-content loading"
      loadingContent.innerHTML =
        'Thinking <div class="loading-dots"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>'
  
      loadingDiv.appendChild(loadingContent)
      chatMessages.appendChild(loadingDiv)
  
      // Scroll to bottom
      chatMessages.scrollTop = chatMessages.scrollHeight
  
      return loadingDiv
    }
  })
  