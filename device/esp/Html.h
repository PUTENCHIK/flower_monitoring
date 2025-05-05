// HTML страница для примера
const char* htmlPage = R"rawliteral(
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Device Configuration</title>
        <style>
            body, input, button {
                font-family: Arial, sans-serif;
                font-size: 16px;
            }
            body {
                display: flex;
                justify-content: center;
            }
            h1 {
                text-align: center;
                color: #222222;
            }
            p {
                font-size: 18px;
                color: #444444;
            }
            .page-content {
                width: 1200px;
                display: flex;
                flex-direction: column;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
                row-gap: 20px;
            }
            label {
                display: flex;
                column-gap: 10px;
                row-gap: 10px;
                flex-wrap: wrap;
                justify-content: center;
                align-items: center;
            }
            input[type="text"] {
                padding: 5px 10px;
                border: 0;
                outline: 1px solid black;
                border-radius: 5px;
            }
            .buttons {
                display: flex;
                flex-wrap: wrap;
                column-gap: 20px;
                row-gap: 20px;
                justify-content: center;
            }
            button {
                width: 150px;
                height: 30px;
                border-radius: 5px;
                border: 0;
                cursor: pointer;
            }
            button[type="reset"] {
                background-color: white;
                border: 1px solid black;
            }
            button[type="submit"] {
                background-color: blue;
                color: white;
            }
            @media (width <= 800px) {
                body, input, button { font-size: 15px; }
                h1 { font-size: 28px; }
            }
            @media (width <= 500px) {
                body, input, button { font-size: 14px; }
                h1 { font-size: 24px; }
                body { padding: 0 20px; }
                input { 
                    box-sizing: border-box;
                    width: 100%;
                }
                label {
                    width: 100%;
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="page-content">
            <h1>Welcome to Configuration page of your device!</h1>
            <form action="/config" method="post">
                <label>
                    <span>IP address / domen of server:</span>
                    <input type="text" name="domen" placeholder="http://192.168.0.10:5050" value="{{domen}}">
                </label>
                <label>
                    <span>Name of WiFi / Mobile AP:</span>
                    <input type="text" name="ssidCLI" placeholder="internet" value="{{ssidCLI}}">
                </label>
                <label>
                    <span>Password of WiFi / Mobile AP:</span>
                    <input type="text" name="passwordCLI" placeholder="strong_password" value="{{passwordCLI}}">
                </label>
                <label>
                    <span>Name of AP of this device:</span>
                    <input type="text" name="ssidAP" placeholder="MyAP" value="{{ssidAP}}">
                </label>
                <div class="buttons">
                    <button type="reset">Reset</button>
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    </body>
</html>
)rawliteral";