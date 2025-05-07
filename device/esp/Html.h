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
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            form {
                width: 600px;
                display: flex;
                flex-direction: column;
                align-items: center;
                row-gap: 20px;
            }
            form > * { width: 100%; }
            fieldset {
                padding: 20px;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                row-gap: 20px;
                border-radius: 20px;
                border-color: black;
            }
            label {
                display: flex;
                flex-direction: column;
                column-gap: 10px;
                row-gap: 10px;
                justify-content: center;
                align-items: center;
            }
            label.row {
                flex-direction: row;
                justify-content: flex-start;
            }
            label:not(.row) > span {
                width: 100%;
                text-align: left;
            }
            input {
                box-sizing: border-box;
                padding: 5px 10px;
                border: 0;
                outline: 1px solid black;
                border-radius: 5px;
            }
            input:disabled {
                color: #808080;
                outline: 1px solid #808080;
            }
            label > input[type="text"] {
                width: 100%;
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
            @media (width <= 620px) {
                form { width: 100%; }
            }
            @media (width <= 500px) {
                body, input, button { font-size: 14px; }
                h1 { font-size: 24px; }
            }
        </style>
    </head>
    <body>
        <div class="page-content">
            <h1>Welcome to Configuration page of your device!</h1>
            <form action="/config" method="post">
                <fieldset>
                    <legend>Network Configuration</legend>
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
                        <span>Name of device's AP:</span>
                        <input type="text" name="ssidAP" placeholder="MyAP" value="{{ssidAP}}">
                    </label>
                    <label>
                        <span>Password of device's AP:</span>
                        <input type="text" value="{{passwordAP}}" disabled>
                    </label>
                </fieldset>
                <fieldset>
                    <legend>Inner settings</legend>
                    <label>
                        <span>Device token:</span>
                        <input type="text" value="{{token}}" disabled>
                    </label>
                    <label>
                        <span>Device password:</span>
                        <input type="text" name="password" placeholder="not_qwerty" value="{{password}}">
                    </label>
                    <label class="row">
                        <span>Sending data delay (min):</span>
                        <input type="number" name="sendingDelay" placeholder="5" value="{{sendingDelay}}"
                            min="1" max="60">
                    </label>
                </fieldset>
                <div class="buttons">
                    <button type="reset">Reset</button>
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    </body>
</html>
)rawliteral";
