const htmlCode = `<!DOCTYPE html>
<html>
    <head>
        <title>Welcome Page</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="welcome-message">
            <h1>Welcome!</h1>
            <p>Please fill out the form below:</p>
        </div>
        <form>
            <div class="buttons">
                <button type="button" class="cancel-button">Cancel</button>
                <button type="submit" class="send-button">Send</button>
            </div>
        </form>
        <script src="script.js"></script>
    </body>
</html>`;

const cssCode = `.welcome-message {
    text-align: center;
    margin-top: 50px;
}
  
form {
    margin: 50px auto;
    width: 80%;
    max-width: 500px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
  
label {
    display: block;
    margin-bottom: 10px;
}
  
input, select {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
  
.buttons {
    display: flex;
    justify-content: space-between;
}
  
.cancel-button {
    background-color: #ccc;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
  
.send-button {
    background-color: #4CAF50;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}`;

const jsCode = `const form = document.querySelector('form');
const cancelButton = document.querySelector('.cancel-button');
        
cancelButton.addEventListener('click', () => {
    form.reset();
});`;

export const writeCodeChat = [
    {
        id: "0",
        title: "HTML",
        language: "html",
        value: htmlCode,
    },
    {
        id: "1",
        title: "CSS",
        language: "css",
        value: cssCode,
    },
    {
        id: "2",
        title: "JS",
        language: "javascript",
        value: jsCode,
    },
];
