<template>
    <div class="content register-content">
        <div class="register-wrapper">
            <div>
                <router-link to="/">
                    <img class="back" src="@/assets/arrow.png" alt="">
                </router-link>  
                <h1>Регистрация устройства</h1>
            </div>
            <form @submit="register">
                <label>
                    Токен устройства:
                    <br>
                    <input required minlength="4" maxlength="40" @change="inputChange" v-model="tokenModel" type="text" name="" id="" placeholder="Введите токен устройства">
                </label>
                <label>
                    Пароль устройства:
                    <br>
                    <input required minlength="4" maxlength="40" v-model="passwordModel" type="password" name="" id="" placeholder="Введите пароль устройства">
                </label>
                <span class="message"> {{ messageValue }}</span>
                <div class="register-submit-button-wrapper">
                    <button class="register-submit-button" type="submit">Отправить</button>
                </div>

            </form>
        </div>
    </div>

</template>

<script setup>
    import axios from 'axios';
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const router = useRouter()

    const tokenModel = ref("");
    const passwordModel = ref("");
    const messageValue = ref("");

    async function register(event) {
        event.preventDefault();
        messageValue.value = "";

        try {
            const response = await axios.post('/api/devices/register', {
                deviceToken: tokenModel.value,
                password: passwordModel.value
            });

            console.log('Успешный ответ:', response.data);

            let checkTokens = localStorage.getItem("deviceTokens");
            let tokens = [];
            if (checkTokens !== null) {
                tokens = JSON.parse(checkTokens)
            }

            tokens.push(tokenModel.value);
            localStorage.setItem("deviceTokens", JSON.stringify(tokens));
            router.push('/');
            return;

        } catch (error) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 400:
                        console.log('Ресурс уже зарегистрирован:', error.response.data);
                        messageValue.value = "Устройство уже зарегистрировано"
                        break;
                    default:
                        console.log('Данные ошибки:', error.response.data);
                        console.log('Код состояния:', error.response.status);
                        console.log('Заголовки:', error.response.headers);
                }
            } else if (error.request) {
                console.log('Запрос:', error.request);
            } else {
                console.log('Ошибка:', error.message);
            }
        }
    }

    function inputChange() {
        messageValue.value = ""
    }
</script>


<style scoped>
    .register-content {
        display: flex;
        justify-content: center;
    }

    h1 {
        font-family: "Montserrat";
        color: #113259;
        margin-bottom: 48px;
        text-align: center;
        font-size: 25px;
    }


    form {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    input {
        font-family: "Montserrat";
        width: 65%;
        height: 46px;
        background-color: #ffffff;
        border-radius: 10px;
        font-size: 18px;
        border: none;
        padding-left: 12px;
        padding-right: 12px;
        margin-right: 16px;
        
    }

    label {
        margin: 0px;
        color: #113259;
        font-family: "Montserrat";
        font-weight: 600;
        font-size: 18px;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .register-submit-button {
        font-family: "Montserrat";
        background-color: #8AB73F;
        width: 150px;
        height: 45px;
        color: #fff;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        border: none;
    }

    .register-submit-button:hover {
        background-color: #7ea83a;
    }
    
    .register-submit-button-wrapper {
        display: flex;

    }

    .register-wrapper {
        background-color: #EBF5FB;
        padding: 32px;
        margin-top: 24px;
        border-radius: 20px;
        width: 60%;
    }

    .message {
        font-family: "Montserrat";
        font-size: 18px;
        margin-bottom: 16px;
        margin-top: 16px;
        font-weight: 500;
        color: #f04848;
    }

    .back {
        width: 26px;
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .back:hover {
        background-color: #eaeaea;
        box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
    }

    @media (max-width: 576px) {
        .back {
            width: 20px;
            padding: 4px;
            cursor: pointer;
            border-radius: 10px;
            display: none;
        }


        h1 {
            font-family: "Montserrat";
            color: #113259;
            margin-bottom: 32px;
            text-align: center;
            font-size: 18px;
        }


        form {
            display: flex;
            flex-direction: column;
            gap: 32px;
        }

        input {
            font-family: "Montserrat";
            width: 243px;
            height: 43px;
            background-color: #ffffff;
            border-radius: 10px;
            font-size: 16px;
            border: none;
            padding-left: 12px;
            padding-right: 12px;
            margin-right: 16px;
            
        }

        label {
            margin: 0px;
            color: #113259;
            font-family: "Montserrat";
            font-weight: 600;
            font-size: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .register-submit-button {
            font-family: "Montserrat";
            background-color: #8AB73F;
            width: 129px;
            height: 43px;
            color: #fff;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            border: none;
        }

        .register-submit-button:hover {
            background-color: #7ea83a;
        }
        
        .register-submit-button-wrapper {
            display: flex;

        }

        .register-wrapper {
            background-color: #EBF5FB;
            padding: 32px;
            margin-top: 24px;
            border-radius: 20px;
            width: 100%;
        }

        .message {
            font-family: "Montserrat";
            font-size: 16px;
            margin-bottom: 8px;
            margin-top: 8px;
            font-weight: 500;
            color: #f04848;
        }

    }
</style>
